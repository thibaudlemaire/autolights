#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from django.core.wsgi import get_wsgi_application
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from websockets import WebSocketRoot, ConsoleWebSocketHandler
import logging


class DjangoThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Disable cherryPy log propagation
        logging.getLogger('cherrypy').propagate = False
        logging.getLogger('ws4py').propagate = False

        # Setup server
        cherrypy.config.update("user_interface/server.conf")

        # Mount Django app
        application = get_wsgi_application()
        cherrypy.tree.graft(application, "/")

        # Mount the static folder
        cherrypy.tree.mount(None, '/static', "user_interface/static.conf")

        # Mount websocket server
        WebSocketPlugin(cherrypy.engine).subscribe()
        cherrypy.tools.websocket = WebSocketTool()
        cherrypy.tree.mount(WebSocketRoot(), '/ws', config={
            '/console': {
                'tools.websocket.on': True,
                'tools.websocket.handler_cls': ConsoleWebSocketHandler,
                'tools.websocket.protocols': ['console']
            }
        }
                            )

        # Launch a second server to listen on port 9000
        server2 = cherrypy._cpserver.Server()
        server2.socket_port = 9000
        server2._socket_host = "0.0.0.0"
        server2.thread_pool = 30
        server2.subscribe()

        # Start engine
        cherrypy.engine.signals.subscribe()
        cherrypy.engine.start()
        logging.info("Web server listening on port 80")
        logging.info("Waiting for distant shell on port 9000")
        #cherrypy.engine.block()

    def stop_server(self):
        cherrypy.engine.exit()




