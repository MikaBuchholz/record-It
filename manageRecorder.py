from ffmpegWrapper import FfmpegWrapper
from retrieveBuffer import RetrieveBuffer
from manageVideos import ManageVideos

class RecordIt():
    def __init__(self):
        self.ffmpegWrapperClass = FfmpegWrapper()
        self.bufferClass = RetrieveBuffer(databaseName="rlf-shadowplay-cluster", collectionName= "buffers")
        self.manageVideoClass = ManageVideos()
        
    
    def mainFunction(self):
        ...#Wird auf den Knopfdruck reagieren und dementsprechend die Videos passend zu


    
    