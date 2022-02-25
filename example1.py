print("Xin chào ThingsBoard")
from random import random
import paho.mqtt.client as mqttclient
import time
import json
import pandas as pd
import random
BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "9Mfr9yQ9wePUdOBkgJDq"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 20
humi = 50
light_intensity = 0.5
counter = 0
longitude = 106.7
latitude = 10.6
name='Quang Ngai'
path='./vn.csv'
def update_coord(path): 
    #read file csv
    data= pd.read_csv(path)
    k=random.randint(0,len(data)-1)
    #trả về ngẫu nhiên tên và tọa độ của một địa điểm trong file  csv
    return data['city'][k],data['lat'][k],data['lng'][k]

while True:
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intensity,'longitude': longitude ,'latitude' : latitude,'name':name}
    temp += 1
    humi += 1
    light_intensity += 1
    name,latitude ,longitude =update_coord(path)
    print(name,latitude ,longitude)
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)
    
