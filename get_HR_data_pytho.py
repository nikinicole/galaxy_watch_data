# -*- coding: utf-8 -*-
"""
main 


"""

import asyncio
import websockets
from funzioni_websockets import *



if __name__ == '__main__':

    print("Starting server on {}...".format(get_ip()))
    loop = asyncio.get_event_loop()

    watch_server = loop.run_until_complete(websockets.serve(watch, '0.0.0.0', 8085))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nBye bye...")

    watch_server.close()
    loop.run_until_complete(watch_server.wait_closed())