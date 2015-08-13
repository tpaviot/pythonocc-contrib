import sys
sys.path.append('../..')

import WebServer.TornadoWeb
import tornado.ioloop

import ifcopenshell
import ifcopenshell.geom

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

f = ifcopenshell.open("IfcOpenHouse.ifc")


def generate_shapes():
    for product in f.by_type("IfcProduct"):
        if product.is_a("IfcOpeningElement"):
            continue
        if product.Representation:
            try:
                shape = ifcopenshell.geom.create_shape(settings, product).geometry
                yield product.is_a(), shape
            except:
                pass

colors = {'IfcRoof': (0.6, 0.2, 0.1),
          'IfcPlate': (0.4, 0.7, 0.8),
          'IfcMember': (0.5, 0.3, 0.1),
          'IfcSite': (0.2, 0.4, 0.1)}

renderer = WebServer.TornadoWeb.TornadoWebRenderer()
for entity_type, shape in generate_shapes():
    renderer.display(shape, color=colors.get(entity_type))

print(renderer)
if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()
