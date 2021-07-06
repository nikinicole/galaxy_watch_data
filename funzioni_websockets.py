# -*- coding: utf-8 -*-
"""
script per la connessione fra lo smartwach e il websocket 

inoltre i dati vengono salvati in un csv nella cartella "dati"
"""
#import time
import json
import socket
import logging
#import sqlite3
import asyncio
#import websockets
#import matplotlib.pyplot as plt
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation







hr = []
hrv = []
HR = []
HRV = []
timestamp = []

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")



STATE = {"value": -127, "name": ""}

USERS = set()
WATCHES = set()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 53))
    ip = s.getsockname()[0]
    s.close()
    return ip


figure, ax = plt.subplots(figsize=(4,3))
line, = ax.plot(x, y)
plt.axis([0, 4*np.pi, -1, 1])


def state_event():
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    logging.info("New User...")
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    logging.info("User gone...")
    await notify_users()



async def w_register(websocket):
    WATCHES.add(websocket)
    logging.info("New watch connected...")

async def w_unregister(websocket):
    WATCHES.remove(websocket)
    logging.info("Watch gone...")
    
    



async def watch(websocket, path):
   
   
   
    await w_register(websocket)

    try:
                

        async for message in websocket:

            if message == "quit":
                break

            var = ''
            try:
               
                var = json.loads(message) #Messaggio ricevuto dal galaxy
                print(var)
               
            except ValueError:
                print("Decoding JSON has failed")

            if "type" in var:

                if var["type"] == "quit":
                    break

                if var["type"] == "hrm":

                    hr = int(var["hr"])
                    hrv = int(var["hrv"])
                    time = float(var["timestamp"])
                    

            
                   
            HR.append(hr)
            HRV.append(hrv)
            timestamp.append(time)
           
                   

                   
    finally:
        await w_unregister(websocket)
       
       
   
       
       
        #SALVO I DATI IN UN CSV
        header = [['HR','HRV']]
        physio_data = (HR,HRV)
        import pandas as pd
        
        my_df = pd.DataFrame()
        my_df['HRV'] =HRV
        my_df['HR'] =  HR
        my_df['timestamp'] = timestamp
        
        filename = '_' + dt_string + '.csv'
        
        my_df.to_csv(filename, sep = ';', header = True)


        