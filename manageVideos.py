from os import curdir, listdir, remove

class ManageVideos:
    def __init__(self):
        pass
 
    def getRawFile(self):
        for file in listdir(f'{curdir}\\rawData'):
            if file[-4:] == 'h264':
                return file[:-5]

    def getMainFile(self):
        for file in listdir(f'{curdir}'):
            if file[-4:] == 'h264':
                return file[:-5]
    
    def checkRawFolderEmpty(self):
        folderLength = len((listdir(f'{curdir}\\rawData'))) 
        
        if folderLength == 0:
            return True
        
        if folderLength != 0:
            return False
    
    def clearRawFolder(self):
        for file in listdir(f'{curdir}\\rawData'):
            remove(f'{curdir}\\rawData//{file}')