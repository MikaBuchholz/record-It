import os
import json
import pymongo
from dotenv import load_dotenv, find_dotenv

class Buffer:
    def __init__(self, databasename = 'rlf-shadowplay-cluster', collectionname = 'buffers'):
        self.databasename = databasename
        self.collectionname = collectionname
        
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
        collection = database[self.collectionname]
        
        # get database data and get buffer value
        data = collection.find({})
        for item in data:
            if item['date']: # check if data came from website (needs/can to be reworked)
                self.__bufferValue = item['buffer']
                self.__recording = item['recording']
                break
            
        # write buffer value to config.json (simultaneously creating config.json)
        with open('config.json', 'w') as fout:
            config = {}
            config['buffer'] = { 'value': self.__bufferValue}
            config['recording'] = self.__recording
            json.dump(config, fout)
            
    def getBufferValue(self):
        return self.__bufferValue
    
    def getRecordingValue(self):
        return self.__recording
    
if __name__ == '__main__':
    Buffer().updateConfig()
    print(Buffer().getBufferValue())
    print(Buffer().getRecordingValue())
    if (Buffer().getRecordingValue()):
        print('Recording ON')
    else:
        print('Recording OFF')