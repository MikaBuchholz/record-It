from ffmpegWrapper import FfmpegWrapper
from retrieveBuffer import Buffer
from manageVideos import ManageVideos

class RecordIt:
    def __init__(self):
        self.ffmpegWrapperClass = FfmpegWrapper()
        self.bufferClass = Buffer(databasename='rlf-shadowplay-cluster', collectionname='buffers')
        self.manageVideoClass = ManageVideos()
    
    def mainFunction(self):
        ...# Wird auf den Knopfdruck reagieren und dementsprechend die Videos anpassen


    
    