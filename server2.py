#!/usr/bin/python
# -*- coding: utf-8 -*-
from websocket_server import WebsocketServer
import json
import time
import io


nicks = {}
vehicles = {}
capture = {}


def new_client(client, server):
    print('Client connected')



def client_left(client, server):
    print('Client(%d) disconnected' % client['id'])
    global nicks
    nicks = {}




def message_received(client, server, message):
    info = json.loads(message)
    if 'auth' in info:
        with io.open('whitelist.txt') as file:
            for line in file:
                if info['auth'] in line:
                    server.send_message(client, 'Granted!')
                    return
        server.send_message(client, 'Go away!')
    else:
        if 'sender' in info:
            if info['sender']['sender'] not in nicks:
                nicks.update({info['sender']['sender']: {
                    'timestamp': time.time(),
                    'heading': info['sender']['heading'],
                    'health': info['sender']['health'],
                    'x': info['sender']['pos']['x'],
                    'y': info['sender']['pos']['y'],
                    }})
            else:
                if nicks[info['sender']['sender']]['timestamp'] \
                    < time.time():
                    nicks.update({info['sender']['sender']: {
                        'timestamp': time.time(),
                        'heading': info['sender']['heading'],
                        'health': info['sender']['health'],
                        'x': info['sender']['pos']['x'],
                        'y': info['sender']['pos']['y'],
                        }})
        if 'vehicles' in info:
            inf = info['vehicles']
            for a in inf:
                if a and a['id'] not in vehicles:
                    if 'health' in a:
                        vehicles.update({a['id']: {
                            'timestamp': time.time(),
                            'heading': a['heading'],
                            'engine': a['engine'],
                            'health': a['health'],
                            'healthstamp': time.time(),
                            'x': a['pos']['x'],
                            'y': a['pos']['y'],
                            }})
                    else:
                        vehicles.update({a['id']: {
                            'timestamp': time.time(),
                            'heading': a['heading'],
                            'engine': a['engine'],
                            'x': a['pos']['x'],
                            'health': 'xz',
                            'healthstamp': time.time(),
                            'y': a['pos']['y'],
                            }})
                else:
                    if vehicles[a['id']]['timestamp'] < time.time():
                        if 'health' in a:
                            vehicles.update({a['id']: {
                                'timestamp': time.time(),
                                'heading': a['heading'],
                                'engine': a['engine'],
                                'health': a['health'],
                                'healthstamp': time.time(),
                                'x': a['pos']['x'],
                                'y': a['pos']['y'],
                                }})
                        else:
                            vehicles.update({a['id']: {
                                'timestamp': time.time(),
                                'heading': a['heading'],
                                'engine': a['engine'],
                                'health': vehicles[a['id']]['health'],
                                'healthstamp': vehicles[a['id'
                                        ]]['healthstamp'],
                                'x': a['pos']['x'],
                                'y': a['pos']['y'],
                                }})
        answer = {}
        answer['nicks'] = nicks
        answer['vehicles'] = vehicles
        answer['timestamp'] = time.time()
        server.send_message(client, str.encode(json.dumps(answer)))
        print ('Client(%d) said: %s' % (client['id'], message))


PORT = 8993
server = WebsocketServer(PORT, '185.238.0.84')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
