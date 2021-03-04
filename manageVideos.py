from os import curdir, listdir, remove

class ManageVideos:
    @staticmethod
    def getRawFile():
        for file in listdir(f'{curdir}/rawData'):
            if file[-4:] == 'h264':
                return file[:-5]

    @staticmethod
    def getMainFile():
        for file in listdir(f'{curdir}'):
            if file[-4:] == 'h264':
                return file[:-5]
    
    @staticmethod
    def checkRawFolderEmpty():
        folderLength = len((listdir(f'{curdir}/rawData'))) 
        
        if folderLength == 0:
            return True
        
        return False
    
    @staticmethod
    def clearRawFolder():
        for file in listdir(f'{curdir}/rawData'):
            remove(f'{curdir}/rawData/{file}')
    
    @staticmethod
    def clearMainFolder():
        for file in listdir(curdir):
            if file[-4:] == 'h264' or file[-3:] == 'mp4' or file[-3:] == 'wav':
                remove(f'{curdir}/{file}')