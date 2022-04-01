#!/usr/bin/env python3

import threading, time
import websocket_server_threaded as WS


# This class will hold a websocket server that runs asynchronously
# from the rest of the program

class WebSockServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.server_port = port

    def run(self):
        # Create server class
        ws_server = WS.WebsocketServer(self.server_port)

        # Bind callbacks to server
        ws_server.set_fn_new_client(self.new_client)
        ws_server.set_fn_client_left(self.client_left)
        ws_server.set_fn_message_received(self.message_received)

        # Start server
        ws_server.run_thread()

        print("Server now available on localhost:{}".format(self.server_port))

        # Nothing else to do
        while(1):
            time.sleep(1)
            
        print("Exiting server thread")


    # Called for every client connecting (after handshake)
    def new_client(self, client, server):
        print("New client connected to server and was given ID {}".format(client['id']))


    # Called for every client disconnecting
    def client_left(self, client, server):
        print("Client {} disconnected from server".format(client['id']))


    # Called when a client sends a message
    def message_received(self, client, server, message):

        debug_message = "Msg received from client {}:\n\t{}".format(client['id'], message)

        print(debug_message)

        reply = "Python got your message, it was: <b>{}</b>".format(message)

        server.send_message(client, reply)
        

# =============================================================
# Entry of program        
if __name__ == "__main__": 

    print("Hello, starting server now...")

    # Create thread to listen on 9000
    server_thread_handle = WebSockServer(9000)
    server_thread_handle.start()

    # Nothing else to do
    while(1):
        time.sleep(1)
        
    print("Exit program")