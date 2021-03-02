import os
import pymongo
from dotenv import load_dotenv, find_dotenv

class Buffer:
    def __init__(self, databasename = 'rlf-shadowplay-cluster', collectionname = 'buffers', secondcollectionname = 'captures'):
        self.databasename = databasename
        self.collectionname = collectionname
        self.secondcollectionname = secondcollectionname
        
        self.updateValues() # connect to database and set class vars
    
    def updateValues(self):
        # load .env file
        load_dotenv(find_dotenv())
        MONGO_URI = os.environ.get('MONGO_URI')

        # connect to database
        client = pymongo.MongoClient(MONGO_URI)
        database = client[self.databasename]
        self.collection = database[self.collectionname]
        self.secondcollection = database[self.secondcollectionname]
        
        # get database data and get buffer value
        primaryData = self.collection.find({})
        for item in primaryData:
            if item['date']: # check if data came from website (needs/can to be reworked)
                self.__bufferValue = item['buffer']
                self.__recording = item['recording']
                break
        
        secondaryData = self.secondcollection.find({})
        for item in secondaryData:
            if item['date']: # check if data came from website (needs/can to be reworked)
                self.__btnPress = item['btnPressed']
                break
            
    def getBufferValue(self):
        return self.__bufferValue
    
    def getRecordingValue(self):
        return self.__recording
    
    def getBtnPress(self):  
        for item in self.secondcollection.find({}):
            if item['model'] == 'Capture':
                return item['btnPressed']
    
    def toggleBtnPress(self, state = False):
        if type(state) == bool:
            filter = { 'model': 'Capture'}
            update = { '$set': { 'btnPressed': state } }
            
            self.secondcollection.update_one(filter, update)
        
if __name__ == '__main__':
    Buffer().updateConfig()
    print(Buffer().getBufferValue())
    print(Buffer().getRecordingValue())
    if (Buffer().getRecordingValue()):
        print('Recording ON')
    else:
        print('Recording OFF')