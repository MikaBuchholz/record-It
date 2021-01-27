from os import curdir, listdir, 

class ManageVideos():
    def __init__(self):
        self.videoList = []

    def getVideosInDirectory(self):
            for file in listdir(curdir):
                if file.split('.')[-1] == 'mp4':
                    self.videoList.append(file.split('.')[0])
            
            return self.videoList
    