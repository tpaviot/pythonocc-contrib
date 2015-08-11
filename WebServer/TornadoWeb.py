###############################################################################
#                                                                             #
# Copyright 2015 Thomas Krijnen                                               #
#                                                                             #
# This module is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Lesser General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This module is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Lesser General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public License    #
# along with this module.  If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################

import os
import uuid
import json
import socket
import tempfile
import threading
from collections import namedtuple, defaultdict

import tornado.web
import tornado.ioloop
import tornado.httpserver

import OCC.Visualization


VIEWER_IFRAME_TEMPLATE = """
<div id='placeholder_%(id)s'></div>
<script type='text/javascript'>
    var iframe = document.createElement('iframe');
    iframe.style.border = 'none';
    iframe.style.width = '100%%';
    iframe.style.height = '600px';
    iframe.src = window.location.protocol + '//' + window.location.hostname + ':%(port)d/get/%(id)s/';
    document.getElementById('placeholder_%(id)s').appendChild(iframe);
</script>
"""

VIEWER_TEMPLATE = """
<!DOCTYPE HTML>
<html lang="en">
<head>
    <title>pythonOCC TornadoWeb renderer</title>
    <meta charset="utf-8">
    <style type="text/css">
        body {
            background-color: #fff;
            margin: 0px;
            padding: 0px;
        }
        canvas {
            display: block;
        }
    </style>
    <script type="text/javascript" src="https://cdn.rawgit.com/mrdoob/three.js/eee231960882f6f3b6113405f524956145148146/build/three.min.js"></script>
    <script type="text/javascript" src="https://cdn.rawgit.com/mrdoob/three.js/bde2a91316041e39a198d92255c701d4020bf4d4/examples/js/controls/OrbitControls.js"></script>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
    <script type="text/javascript">
        $(function() {
            var create_material = function(r, g, b) {
                return new THREE.MeshPhongMaterial({ambient: 0x101010, color: new THREE.Color(r, g, b), specular: 0x222222, shininess: 30, side: THREE.DoubleSide});
            };

            var container = document.body;

            var camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 200);
            camera.position.z = 100;
            var controls = new THREE.OrbitControls(camera);

            var scene = new THREE.Scene();
            scene.add(new THREE.AmbientLight(0xcccccc));
            directionalLight = new THREE.DirectionalLight(0xffffff);
            directionalLight.position.x = 1;
            directionalLight.position.y = -1;
            directionalLight.position.z = 2;
            directionalLight.position.normalize();
            scene.add(directionalLight);

            renderer = new THREE.WebGLRenderer({antialias:true});
            renderer.setClearColor("#fff");
            renderer.setSize(window.innerWidth, window.innerHeight);

            document.body.appendChild(renderer.domElement);

            renderer.shadowMapEnabled = true;
            renderer.shadowMapType = THREE.PCFShadowMap;

            var render = function() {
               renderer.render(scene, camera);
            }

            var animate = function() {
                requestAnimationFrame(animate);
                controls.update();
                render();
            }

            window.addEventListener('resize', function() {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }, false);

            var old_hash = null;

            var poll_for_changes = function() {
                $.ajax({url:"/shape_list/%(viewer_id)s/", dataType:'json'}).then(function(shape_list) {
                    if (shape_list.hash == old_hash) return;

                    var clear_scene = function() {
                        var children = scene.children;
                        for (var i = children.length - 1; i >= 0; i--) {
                            var child = children[i];
                            child.clear();
                            this.removeChild(child);
                        }
                    };

                    if (old_hash) clear_scene();
                    old_hash = shape_list.hash;

                    var requests = shape_list.keys.map(function(shape_id) {
                        return function() {
                            var d = $.Deferred();
                            $.ajax({url:"/shape/%(viewer_id)s/"+shape_id, dataType:"script"}).then(function() {
                                var mesh = new THREE.Mesh(new Shape(), create_material.apply(null, shape_list.colors[shape_id]));
                                d.resolve(mesh);
                            });
                            return d;
                        }
                    });

                    var make_requests = function() {
                        var r = requests.splice(0,1)[0];
                        if (r) {
                            r().then(function(mesh) {
                                scene.add(mesh);
                                make_requests();
                            });
                        } else {
                            $("#loading").css('display', 'none');
                            return animate();
                        }
                    }

                    make_requests();
                });
            };

            poll_for_changes();
            setInterval(poll_for_changes, 10000);
        });
    </script>
</head>
<body><div id='loading'>Loading...</div></body>
</html>
"""

STATIC_DATA = namedtuple("_DATA", ("SHAPES_PER_VIEWER", "COLORS_PER_VIEWER", "VIEWER_BY_ID"))(defaultdict(list), defaultdict(list), {})


class ViewerHandler(tornado.web.RequestHandler):
    # Return the main viewer HTML code. The id is written to
    # the subsequent request URLs performed by the viewer
    def get(self, viewer_id):
        self.write(VIEWER_TEMPLATE % locals())


class ShapeHandler(tornado.web.RequestHandler):
    # Return the tesselated shape geometry
    def get(self, viewer_id, shape_id):
        self.write(STATIC_DATA.SHAPES_PER_VIEWER[viewer_id][int(shape_id)])


class ShapeListHandler(tornado.web.RequestHandler):
    # Return a list of shapes and colors associated with this viewer.
    # The list contains a hash value that the client can use to
    # redraw the scene when polling for changes.
    def get(self, viewer_id):
        STATIC_DATA.VIEWER_BY_ID[viewer_id].stop_server(delay=60)
        shape_list = tuple(range(len(STATIC_DATA.SHAPES_PER_VIEWER[viewer_id])))
        color_list = tuple(map(tuple, STATIC_DATA.COLORS_PER_VIEWER[viewer_id]))
        self.write(json.dumps({'hash': hash(shape_list + color_list), 'keys': shape_list, 'colors': color_list}))


application = tornado.web.Application([
    (r"/get/(\w+)/?", ViewerHandler),
    (r"/shape/(\w+)/(\d+)/?", ShapeHandler),
    (r"/shape_list/(\w+)/?", ShapeListHandler)
  # Static files are no longer necessary due dependencies being served from CDNs.
#   (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.getcwd(), "static")})
])

DEFAULT_COLOR = (0.6, 0.6, 0.6)


class TornadoWebRenderer(object):
    port = None
    timer = None

    def __init__(self):
        self.id = uuid.uuid4().hex
        # Register the viewer so that subsequent requests will postpone the
        # viewer from being terminated
        STATIC_DATA.VIEWER_BY_ID[self.id] = self

    def start_server(self):
        if self.port:
            # Server already started, do nothing
            return

        # Create a new server, let the OS pick a port number for us
        self.server = tornado.httpserver.HTTPServer(application)
        self.server.listen(0)
        self.server.start()

        # Find the port number so that the HTML client can connect
        self.socket = next(iter(self.server._sockets.values()))
        self.port = self.socket.getsockname()[1]

        # Stop the server if a request has not been made after 60 seconds
        # self.stop_server(60.)

    def stop_server(self, delay=0):
        if self.timer is not None:
            self.timer.cancel()
        if delay == 0:
            self.server.stop()
            self.server = None
        else:
            self.timer = threading.Timer(delay, self.stop_server)

    def _repr_html_(self):
        self.start_server()
        return VIEWER_IFRAME_TEMPLATE % self.__dict__

    def __repr__(self):
        self.start_server()
        return "<%s at http://%s:%d/get/%s>" % (self.__class__.__name__,
                                                socket.getfqdn(), self.port,
                                                self.id)

    def tesselate(self, shape):
        fn = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        tess = OCC.Visualization.Tesselator(shape)
        # TODO: The fact that this has to be emitted to
        #       the file system is somewhat inconvenient.
        tess.ExportShapeToThreejs(fn)
        with open(fn) as f:
            data = f.read()
        os.unlink(fn)
        return data

    def Display(self, shape, idx=None, color=None):
        if color is None:
            color = DEFAULT_COLOR
        shape_list = STATIC_DATA.SHAPES_PER_VIEWER[self.id]
        colors = STATIC_DATA.COLORS_PER_VIEWER[self.id]
        if idx is not None:
            shape_list[idx] = self.tesselate(shape)
            colors[idx] = color
        else:
            idx = len(shape_list)
            shape_list.append(self.tesselate(shape))
            colors.append(color)
        return idx
