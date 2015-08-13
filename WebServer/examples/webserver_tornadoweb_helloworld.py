import sys
sys.path.append('../..')

import WebServer.TornadoWeb
import tornado.ioloop

from OCC.BRepPrimAPI import BRepPrimAPI_MakeTorus

renderer = WebServer.TornadoWeb.TornadoWebRenderer()

torus = BRepPrimAPI_MakeTorus(40, 10).Shape()

renderer.DisplayShape(torus)

print(renderer)
if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()
