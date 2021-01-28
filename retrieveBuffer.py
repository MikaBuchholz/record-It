import os
import json
import pymongo
from dotenv import load_dotenv, find_dotenv

class Buffer:
    def __init__(self, databasename = 'rlf-shadowplay-cluster', collectionname = 'buffers'):
        # Check if config.json does exist
        if os.path.isfile('config.json'):
            # load config.json and get buffer value
            with open('config.json', 'r') as fin:
                data = json.load(fin)
                self.__bufferValue = data['buffer']['value']
        else:
            # load .env file
            load_dotenv(find_dotenv())
            MONGO_URI = os.environ.get('MONGO_URI')

            # connect to database
            client = pymongo.MongoClient(MONGO_URI)
            database = client[databasename]
            collection = database[collectionname]
            
            # get database data and get buffer value
            data = collection.find({})
            for item in data:
                if item['date']: # check if data came from website (needs to be reworked)
                    self.__bufferValue = item['buffer']
                    break
                
            # write buffer value to config.json (simultaneously creating config.json)
            with open('config.json', 'w') as fout:
                config = {}
                config['buffer'] = { 'value': self.__bufferValue }
                json.dump(config, fout)
            
    def getBufferValue(self):
        return self.__bufferValue
            
if __name__ == '__main__':
    print(Buffer().getBufferValue())