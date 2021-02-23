#from picamera import PiCamera
from time import time
from os import system, remove, curdir, path, mkdir, listdir
from retrieveBuffer import Buffer
from shutil import move
from datetime import datetime
from ffmpegWrapper import FfmpegWrapper
from keyboard import keyboard

class Recorder():
    def __init__(self,resWidth = 1280, resHeight = 720, framerate = 30):
        self.buffer = int(Buffer().getBufferValue()) * 60
        self.resWidth = resWidth
        self.resHeight = resHeight
        self.framerate = framerate
        #self.camera = picamera.PiCamera(resolution=(self.resWidth, self.resHeight), framerate = self.framerate)

        if not path.isdir(f'{curdir}\\rawData'):
            mkdir(f'{curdir}\\rawData')
        
        if not path.isdir(f'{curdir}\\finishedClips'):
            mkdir(f'{curdir}\\finishedClips')

    def startRecording(self):
        outputName = (datetime.now()).strftime('%d%m%Y%H%M%S')
        self.camera.start_recording(f'main.h264')
        endTime = time() + (2 * self.buffer)
        
        while True:
            time = time()
            
            if keyboard.is_pressed('q'):
                self.camera.stop_recording()
                self.checkVideoVsBufferLength()
                
            if time > endTime:
                self.camera.stop_recording()
                latestFile = self.getLatestFile()
                path = f'{curdir}\\rawData'
                
                move(f'{curdir}\\{latestFile}', path)

        '''
            [/////]
            [////////]

            Max Video Laenge = 2 * Buffer
            1: Neue Video Laenge kuerzer als Buffer => Cutting, Stitching, Render
            2: Neues Video Laenge groesser als Buffer => Cutting, Render
            => raw Ordner clear & fertiger clip
            
            3: raw Ordner ist leer => Cutting, Render
            3.1: Video Laenge kuerzer oder groeßer check => no cutting or cutting
            
        '''
        #self.convertToMp4(fileName, f'{fileName}{random.randint(1, 100)}')

    def checkVideoVsBufferLength(self):
        outputName = (datetime.now()).strftime('recordIt %d-%b-%Y %H:%M:%S')
        oldestFile = self.getRawFile()
        latestFile = self.getMainFile()
        curVideoLength = FfmpegWrapper().getVideoLength(latestFile)
        bufferLength = FfmpegWrapper().getVideoLength(oldestFile)
        
        if curVideoLength < self.buffer:
            startTime = abs(curVideoLength - self.buffer)
            endTime = bufferLength
            
            FfmpegWrapper().extractVideoClip(oldestFile, startTime, endTime, fileName = 'bufferSubClip')
            FfmpegWrapper().concatVideos('bufferSubClip', latestFile, fileName = outputName)
            
            remove('bufferSubClip.h264')
            move(f'{curdir}\\{outputName}', f'{curdir}\\finishedClips')
        
        if curVideoLength > self.buffer or self.checkRawFolder(self):
            startTime = curVideoLength - self.buffer
            endTime = curVideoLength
            
            FfmpegWrapper().extractVideoClip(latestFile, startTime, endTime, fileName = outputName)

            move(f'{curdir}\\{outputName}', f'{curdir}\\finishedClips')
        
    def checkRawFolder(self):
        return len((listdir(f'{curdir}\\rawData'))) > 0

    def getRawFile(self):
        for file in listdir(f'{curdir}\\rawData'):
            if file[-4:] == 'h264':
                return file[-4:]

    def getMainFile(self):
        for file in listdir(f'{curdir}'):
            if file[-4:] == 'h264':
                return file[-4:]
    
    def convertToMp4(self, fileName, outputName):
        try:
            system(f'MP4Box -add ./{fileName}.h264 ./{outputName}.mp4')
            remove(f'{fileName}.h264')
            #self.startRecording(random.randit(1, 100))
            print('Done')
            
        except:
            return False
        

if __name__ == '__main__':
    Recorder().startRecording()
    #Recorder().startRecording('TestFile2')
    #Recorder().convertToMp4('TestFile2', 'SexAv')




