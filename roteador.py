import socket 
import argparse
from _thread import *
import json
import time

parser = argparse.ArgumentParser(description='Router program.')
parser.add_argument("addr", help="IP address that router will bind.")
parser.add_argument("period", help="Period between sending messages.")
parser.add_argument("-s", "--startup_commands", help="Start the router with a default virtual topoly.")

args = parser.parse_args()

UDP_IP = args.addr
UDP_PORT = 55151

database = [{"ip": '', "weight": '', "source": ''}]
routing_table = [{"ip": '', "weight": '', "source": ''}]

addr = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
sock.bind(addr)

def sendmsg(sock, dest, cont, tipo):
    msg = {
        "type": tipo,
        "source": args.addr,
        "destination": dest,
        "payload": cont
    }
    msgjson = json.dumps(msg).encode()
    sock.sendto(msgjson, (str(dest), UDP_PORT))

def rcv_update(sock):
    while True:
        try:
            data, addr1 = sock.recvfrom(1024)
            print("Dados: ", data)
        except:
            continue

def update_routing_table():
    aux = {}
    for i in database:
        aux['ip'] = i['ip']
        aux['weight'] = i['weight']
        aux['source'] = i['source']
        for io in database:
            if io['ip'] == i['ip']:
                if int(io['weight']) < int(i['weight']):
                    aux['weight'] = io['weight']
                    aux['sourie'] = io['source']
        
        att2 = 0
        for j in routing_table:
            if j['ip'] == aux['ip']:
                j['source'] = aux['source']
                j['weight'] = aux['weight']
                # subs_json(routing_table, ROUTE_TABLE_FILE)
                saveondb(j['ip'], j['weight'], j['source'], routing_table)
                att2 += 1
        if att2 == 0:
            routing_table.append({"ip": aux['ip'], "weight": aux['weight'], "source": aux['source']})
        try:
            database.remove({"ip": '', "weight": '', "source": ''})
        except:
            'print()'
        
    print('routing table:', routing_table)
        

def updatemsg(sock, period):
    while True:
        time.sleep(10)
        update_routing_table()
        try:
            sendmsg(sock, '127.0.1.2', 'oi', 'update')
        except:
            continue

def saveondb(ip, weight, source, file):
    found = 0
    for info in file:
        print('entrei')
        if info["ip"] == ip and info["source"] == source:
            info["weight"] = weight
            print('alterei o peso')
            found += 1
    if found == 0:
        print('adicionando um novo.')
        file.append({"ip": ip, "weight": weight, "source": source})
    try:
        file.remove({"ip": '', "weight": '', "source": ''})
    except:
        'print()'

            
            

start_new_thread(rcv_update,(sock, ))

start_new_thread(updatemsg,(sock, args.period))

while True:
    inp = input()
    config = inp.split(' ')
    if "add" in inp:
        saveondb(config[1], config[2], args.addr, database)
        print('teste do saveondb:', database)
    if "send" in inp:
        sendmsg(sock, config[1], config[2], 'data')
    
   