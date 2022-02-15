import json
import asyncio
import boto3

import __aws_props as ap
import __iot
import simpleaudio as sa
from pirc522 import RFID



BUCKET_NAME = '####'

ACKFlag = False
LedFlag = False
SetFlag = False
SetSound = sa.WaveObject.from_wave_file("./data/###.wav")
Alert = sa.WaveObject.from_wave_file("./data/#?#.wav")

S3_RESOURCE = boto3.resource('s3')


s3_data = StringIO(s3_object.get()['Body'].read().decode('utf-8'))

async def pubAsync(topic, user_id):
    global ACKFlag
    send_message = {
                "message":{
                    "user_ID": user_id,
                    "client_ID": ap.CLIENT_ID,
                }
    }
    payload = json.dumps(send_message)
            
    ap.MYCLIENT.publishAsync(topic, payload, 1, pub_callback)
    while not ACKFlag: pass

async def subAsync(_user_id):
    global ACKFlag
    global LedFlag
    global SetFlag
    global SetSound
    global BUCKET_NAME
    global S3_RESOURCE

    s3_object = S3_RESOURCE.Object(bucket_name=BUCKET_NAME, Prefix=f'buyer/purchase/{_user_id}.json')
    SetFlag = True
    ACKFlag = False
    s3_data = s3_object.get()['Body'].read().decode('utf-8').replace('\n', '')
    data = json.loads(s3_data)
    print("Received a settlement message: ")
    print(data["message"]["user_ID"])
    print("from you should pay: ")
    print(data["message"]["price"])
    print("--------------\n\n")
    input("prease Enter to complete payment.")
    await pubAsync("buyer/compleate",_user_id)
    SetSound.play()
    print("Led//")
    SetFlag = False
    LedFlag = False

def pub_callback(mid):
    global ACKFlag
    ACKFlag=True
    print("AckReceive")

async def main():
    global ACKFlag
    global LedFlag
    global SetFlag
    global Alert
    
    print("startUp")
    
    render = __iot.Render(RFID())
    ap.setup()
  
    print("now Start")
    while True:
        
        user_ID = render.recognit()
        if render.state=="touched":
            
            if not ACKFlag and not LedFlag and not SetFlag:
                print("ACKweit@"+user_ID)
                await pubAsync("buyer/settlement",user_ID)

            elif not LedFlag and not SetFlag:
                #led.on()
                LedFlag=True
                Alert.play()
                print("Led//")
                
            if ACKFlag and LedFlag and not SetFlag:
                print("Subweit@"+user_ID)
                await subAsync(user_ID)  
        
        elif render.state=="undefind":
            print("undefind@"+user_ID)
            ACKFlag=False
            LedFlag=False
            render.suspend()
        else :
            render.suspend()
 
    render.cleanup()

if __name__=='__main__':
    asyncio.run(main())