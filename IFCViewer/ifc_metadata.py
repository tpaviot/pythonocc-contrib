##Copyright 2016 Thomas Krijnen
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

try:
    import ifcopenshell
    import ifcopenshell.geom.occ_utils
except ImportError:
    print("This example requires ifcopenshell for python. Please go to  http://ifcopenshell.org/python.html")

class metadata_dictionary(object):
    
    def __init__(self, file):
        self.file = file
        self.cache = {}
        
        
    def process(self, i):
        if i.is_a("IfcRelDefinesByProperties"):
            return self[i.RelatingPropertyDefinition]
        elif i.is_a("IfcPropertySingleValue"):
            # wrappedValue is an IfcOpenShell specific-attribute
            # to obtain the value SELECT-based simple type
            return i.Name, i.NominalValue.wrappedValue
        elif i.is_a("IfcPropertyEnumeratedValue"):
            return i.Name, tuple(map(operator.attrgetter('wrappedValue'), i.EnumerationValues))
        elif i.is_a("IfcPhysicalSimpleQuantity"):
            # IfcPhysicalSimpleQuantity has many subtypes, with each
            # a different attribute name, but the same index (3).
            return i.Name, i[3]
        # TODO: Not all subtypes of IfcProperty currently implemented
        
        
    def __getitem__(self, i):
        id = i.id()
        if id in self.cache:
            return self.cache[id]

        # Dynamically resolve the relevant attribute based on entity type
        attrs = {
            "IfcObject": "IsDefinedBy",
            "IfcPropertySet": "HasProperties",
            "IfcElementQuantity": "Quantities"
        }
        
        for entity_type, attribute_name in attrs.items():
            if i.is_a(entity_type):
                # Process the aggregate of properties, quantities
                # or sets and convert into a dictionary
                props = dict(filter(None, map(self.process, getattr(i, attribute_name))))
                if not i.is_a("IfcObject"):
                    props = i.Name, props
                self.cache[id] = props
                return props
                
    def __iter__(self):
        for object in self.file.by_type("IfcObject"):
            yield object.GlobalId, self[object]
                
if __name__ == "__main__":
    import sys
    import pprint

    filepath = "models/Office_A_20110811.ifc"
    print("Opening IFC file %s" % filepath, file=sys.stderr)
    ifc_file = ifcopenshell.open(filepath)
    print("file opened.", file=sys.stderr)

    metadata = metadata_dictionary(ifc_file)
    
    for product in ifc_file.by_type("IfcProduct"):
        print(product)
        print("=" * 20)
        pprint.pprint(metadata[product])
        print()
        
    # Alternatively, convert to a dict directly
    d = dict(metadata)
    pprint.pprint(d)
