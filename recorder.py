import picamera
import time
from os import system, remove
from retrieveBuffer import Buffer
import random
from datetime import datetime
from ffmpegWrapper import getVideoLength, extractVideoClip, concatVideos

class Recorder():
    def __init__(self,resWidth = 1280, resHeight = 720, framerate = 30):
        self.buffer = int(Buffer().getBufferValue()) * 60
        self.resWidth = resWidth
        self.resHeight = resHeight
        self.framerate = framerate
        self.camera = picamera.PiCamera(resolution=(self.resWidth, self.resHeight), framerate = self.framerate)
    
    def startRecording(self):
        self.camera.start_recording(f'main.h264')
        endTime = time.time() + (2 * self.buffer)
        
        while True:
            time = time.time()
            
            if keyboard.is_pressed('q'):
                self.camera.stop_recording()
                self.checkVideoVsBufferLength()
                
            if time > endTime:
                self.camera.stop_recording()
                
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
    
    def recordItLogic(self):
        videoLength = self.ffmpegWrapperClass().getVideoLength('main.h264')
        start = videoLength - self.buffer
        stop = videoLength
        outputName = (datetime.now()).strftime('recordIt %d-%b-%Y %H:%M:%S')
        self.ffmpegWrapperClass.extractVideoClip('main.h264', start, stop, outputName)
        remove('main.h264')
    
    def checkVideoVsBufferLength(self):
        curVideoLength = getVideoLength(video) # Muss noch zu echtem Video werden
        outputName = (datetime.now()).strftime('recordIt %d-%b-%Y %H:%M:%S')
        
        if videoLength < bufferLength:
            startTime = abs(curVideoLength - self.buffer)
            endTime = self.buffer
            
            extractVideoClip(buffer, startTime, endTime, fileName = 'bufferSubClip')
            concatVideos('bufferSubClip', video, fileName = outputName)
            #Files müssen noch deleted werden
        
        if videoLength > bufferLength or self.checkBufferFolder(self):
            startTime = curVideoLength - self.buffer
            endTime = curVideoLength
            
            extractVideoClip(video, startTime, endTime, fileName = outputName)
            #Files müssen noch deleted werden
        
    def checkBufferFolder(self):
        ... #Zu lazy jetzt den Folder zu checken, dass machst du zukunfts Mika / Aryeh
            #Return: True / False
        
    def convertToMp4(self, fileName, outputName):
        try:
            system(f'MP4Box -add ./{fileName}.h264 ./{outputName}.mp4')
            remove(f'{fileName}.h264')
            #self.startRecording(random.randit(1, 100))
            print('Done')
            
        
        except:
            return False
        

if __name__ == '__main__':
    Recorder().startRecording('TestFile2')
    #Recorder().convertToMp4('TestFile2', 'SexAv')




