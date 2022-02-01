import json
import time
import asyncio

import __aws_props as ap
import __iot
import simpleaudio as sa

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from pirc522 import RFID

ACKFlag = False
LedFlag = False
Alert = sa.WaveObject.from_wave_file("/home/pi/Desktop/__sys47.wav")

def pub_callback(mid):
    global ACKFlag
    
    ACKFlag=True
    print("AckReceive")

async def pubAsync(topic, user_id):
    global ACKFlag
    print(topic)
    send_message ={
                "message":{
                    "user_ID": user_id,
                    "client_ID": ap.CLIENT_ID,
                    "price": ap.PRICE,
                }
    }
    payload = json.dumps(send_message)
            
    ap.MYCLIENT.publishAsync(topic, payload, 1, pub_callback)
    while not ACKFlag: pass

async def main():
    global ACKFlag
    global LedFlag
    global Alert
    
    
    print("startUp")
    
    render = __iot.Render(RFID())
    ap.setup()
    isalert = object()
    
    print("now Start")
    while True:
        
        user_ID = render.recognit()
        if render.state=="touched":
            
            if not ACKFlag and not LedFlag:
                print("ACKweit@"+user_ID)
                await pubAsync(f"buyer/purchase/{user_ID}",user_ID)
            elif not LedFlag:
                #led.on()
                LedFlag=True
                isalert = Alert.play()
                print("Led//")
            if ACKFlag and LedFlag:
                print("Led ...//")
                if not isalert.is_playing(): isalert = Alert.play()
        elif render.state=="undefind":
            print("undefind@"+user_ID)
#             led.off()
            ACKFlag=False
            LedFlag=False
            isalert.stop()
            print("Led//")
            render.suspend()
        else:
            render.suspend()
            
    rdr.cleanup()

if __name__=='__main__':
    asyncio.run(main())
