import os
import json
import pymongo
from dotenv import load_dotenv, find_dotenv

class Buffer:
    def __init__(self, databasename = 'rlf-shadowplay-cluster', collectionname = 'buffers', secondcollectionname = 'captures'):
        self.databasename = databasename
        self.collectionname = collectionname
        self.secondcollectionname = secondcollectionname
        
        # Check if config.json does exist
        if os.path.isfile('config.json'):
            # load config.json and get buffer value
            with open('config.json', 'r') as fin:
                data = json.load(fin)
                self.__bufferValue = data['buffer']['value']
                self.__recording = data['recording']
        else:
            self.updateConfig() # connect to database and retrieve buffer value
    
    def updateConfig(self):
        # load .env file
        load_dotenv(find_dotenv())
        MONGO_URI = os.environ.get('MONGO_URI')

        # connect to database
        client = pymongo.MongoClient(MONGO_URI)
        database = client[self.databasename]
        self.collection = database[self.collectionname]
        self.secondCollection = database[self.secondcollectionname]
        
        # get database data and get buffer value
        primaryData = self.collection.find({})
        for item in primaryData:
            if item['date']: # check if data came from website (needs/can to be reworked)
                self.__bufferValue = item['buffer']
                self.__recording = item['recording']
                break
        
        secondaryData = self.secondCollection.find({})
        for item in secondaryData:
            if item['date']:
                self.__btnPress = item['btnPressed']
                break

        # write buffer value to config.json (simultaneously creating config.json)
        with open('config.json', 'w') as fout:
            config = {}
            config['buffer'] = { 'value': self.__bufferValue}
            config['recording'] = self.__recording
            config['btnPressed'] = self.__btnPress
            json.dump(config, fout)
            
    def getBufferValue(self):
        return self.__bufferValue
    
    def getRecordingValue(self):
        return self.__recording
    
    def getBtnPress(self):  
        for item in self.secondCollection.find({}):
            if item['model']:
                return item['btnPressed']
    
    def modifyPressedValue(self, configInput = False):
        buffer = self.getBufferValue()
        recordVal = self.getRecordingValue()

        with open('config.json', 'w') as fout:
            config = {}
            config['buffer'] = { 'value': buffer}
            config['recording'] = recordVal
            config['btnPressed'] = configInput
            json.dump(config, fout)

if __name__ == '__main__':
    Buffer().updateConfig()
    print(Buffer().getBufferValue())
    print(Buffer().getRecordingValue())
    if (Buffer().getRecordingValue()):
        print('Recording ON')
    else:
        print('Recording OFF')