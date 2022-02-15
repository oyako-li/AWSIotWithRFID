from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
CLIENT_ID = '###'
MYCLIENT = AWSIoTMQTTClient('myClientID')
PRICE = 360

def setup():
    MYCLIENT.configureEndpoint('###.amazonaws.com', 443)
    MYCLIENT.configureCredentials('rootCA.pem', '###-private.pem.key', '###-certificate.pem.ctr')
    MYCLIENT.congigureOfflinePublishQueueing(-1)
    MYCLIENT.congigureDrainingFrequency(2)
    MYCLIENT.congigureConnectDisconnectTimeout(10)
    MYCLIENT.congigureMQTTOperationTimeout(5)
    MYCLIENT.connect()
