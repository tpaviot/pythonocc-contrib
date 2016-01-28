##Copyright 2016 Thomas Paviot (tpaviot@gmail.com)
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
from OCC.Display.SimpleGui import init_display
from OCC.Bnd import Bnd_Box
from OCC.BRepBndLib import brepbndlib_Add

import ifc_metadata

# viewer settings
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Open the IFC file using IfcOpenShell
filepath = "models/HelloHouse_IFC4.ifc"
print("Opening IFC file %s ..." % filepath, end="")
ifc_file = ifcopenshell.open(filepath)
print("file opened.")
# The geometric elements in an IFC file are the IfcProduct elements.
# So these are opened and displayed.
products = ifc_file.by_type("IfcProduct")
metadata = ifc_metadata.metadata_dictionary(ifc_file)

# First filter products to display
# just keep the ones with a 3d representation
products_to_display = []
for product in products:
    if (product.is_a("IfcOpeningElement") or
         product.is_a("IfcSite") or product.is_a("IfcAnnotation")):
            continue
    if product.Representation is not None:
        products_to_display.append(product)
print("Products to display: %i" % len(products_to_display))
# For every product a shape is created if the shape has a Representation.
print("Traverse data with associated 3d geometry")
idx = 0
product_shapes = {}
for product in products_to_display:
        # display current product
        shape = ifcopenshell.geom.create_shape(settings, product).geometry
        product_shapes[shape] = product
        idx += 1
        print("\r[%i%%]Product: %s" % (int(idx*100/len(products_to_display)), product))
        #print(metadata[product])


def print_shape_properties(shp, *kwargs):
    """ a callback that prints properties of the selected shape
    Pretty printing properties
    """
    for shape in shp:
        print(shape.ShapeType())
        print("#################\nProduct properties:")
        print("#IFC definition :")
        print("%s" % product_shapes[shape])
        print("#################")
        print("#IFC Properties")
        properties = metadata[product_shapes[shape]]
        for prop in properties:
            print(prop)
            subproperties = properties[prop]
            for subprop in subproperties:
                print("\t%s:%s" % (subprop, subproperties[subprop]))


def compute_bbox(shp, *kwargs):
    print("#Computed bounding box")
    for shape in shp:
        bbox = Bnd_Box()
        brepbndlib_Add(shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        dx = xmax - xmin
        dy = ymax - ymin
        dz = zmax - zmin
        print("\tdimensions: dx=%f, dy=%f, dz=%f." % (dx, dy, dz))
        print("\tcenter: x=%f, y=%f, z=%f" % (xmin + dx/2.,
                                              ymin + dy/2.,
                                              zmin + dz/2.))

# Initialize a graphical display window
print("Initializing pythonocc display ...", end="")
display, start_display, add_menu, add_function_to_menu = init_display()
print("initialization ok.")
# register callback
display.register_select_callback(print_shape_properties)
display.register_select_callback(compute_bbox)
# then pass each shape to the display
nbr_shapes = len(product_shapes)
idx = 0
for ps in product_shapes:
    display.DisplayShape(ps)
    idx += 1
    # progress bar
    print("[%i%%] Sending shapes to pythonocc display." % int(idx*100/nbr_shapes))
display.FitAll()
display.display_graduated_trihedron()
start_display()
