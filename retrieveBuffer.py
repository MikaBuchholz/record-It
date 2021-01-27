import pymongo

class RetrieveBuffer():
    def __init__(self, databaseName = 'Buffer', collectionName = 'BufferSaves'):
        self.databaseName = databaseName
        self.collectionName = collectionName
        self.data = open('creds.txt', 'r').read().split()
        self.name, self.password = self.data[0], self.data[1]
        self.client = pymongo.MongoClient(f'mongodb+srv://{self.name}:{self.password}@rlf-shadowplay-cluster.6budz.mongodb.net/rlf-shadowplay-cluster?retryWrites=true&w=majority')
        self.database= self.client[self.databaseName]
        self.collection = self.database[self.collectionName]
    
    def returnBufferValue(self):
        result = self.collection.find({})
        for result in result:
            return result['buffer']
    
    def saveBufferValue(self):
        with open('bufferValue.txt', 'w') as file:
            bufferValue = self.returnBufferValue()
            file.write(bufferValue)
        
        return True

if __name__ == '__main__':
    print(RetrieveBuffer(databaseName="rlf-shadowplay-cluster", collectionName= "buffers").saveBufferValue())