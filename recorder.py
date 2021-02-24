from picamera import PiCamera
from time import time, sleep
from os import system, remove, curdir, path, mkdir, listdir
from retrieveBuffer import Buffer
from shutil import move
from datetime import datetime
from ffmpegWrapper import FfmpegWrapper
from manageVideos import ManageVideos
import keyboard 
from cv2 import waitKey

class Recorder():
    def __init__(self,resWidth = 1280, resHeight = 720, framerate = 30):
        self.buffer = int(Buffer().getBufferValue()) * 60
        self.resWidth = resWidth
        self.resHeight = resHeight
        self.framerate = framerate
        self.camera = PiCamera(resolution=(self.resWidth, self.resHeight), framerate = self.framerate)

        if not path.isdir(f'{curdir}\\rawData'):
            mkdir(f'{curdir}\\rawData')
        
        if not path.isdir(f'{curdir}\\finishedClips'):
            mkdir(f'{curdir}\\finishedClips')

    def startRecording(self):
        outputName = (datetime.now()).strftime('%d%m%Y%H%M%S')
        self.camera.start_recording(f'{outputName}.h264')
        endTime = time() + (2 * self.buffer)
        
        while True:
            currentTime = time()
            
            if currentTime >= endTime:# Muss noch zum Knopfdruck geändert werden
                self.camera.stop_recording()
                self.checkVideoVsBufferLength()
                break
                
            if currentTime > endTime:
                if not ManageVideos().checkRawFolderEmpty():
                    ManageVideos().clearRawFolder()
                    
                self.camera.stop_recording()
                
                latestFile = ManageVideos().getMainFile()
                move(f'{curdir}//{latestFile}.h264', f'{curdir}\\rawData')
                #self.startRecording()
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
        outputName = (datetime.now()).strftime('recordIt-%d-%b-%Y-%H:%M:%S')
        oldestFile = ManageVideos().getRawFile()
        latestFile = ManageVideos().getMainFile()
        print(latestFile)
        curVideoLength = FfmpegWrapper().getVideoLength(latestFile)
        
        if curVideoLength < self.buffer:
            if ManageVideos().checkRawFolderEmpty():
                self.convertToMp4(latestFile, outputName)
                move(f'{curdir}//{outputName}.mp4', f'{curdir}\\finishedClips')
                
            else:
                bufferLength = FfmpegWrapper().getVideoLength(oldestFile)
                startTime = abs(curVideoLength - self.buffer)
                endTime = bufferLength
                
                FfmpegWrapper().extractVideoClip(oldestFile, startTime, endTime, fileName = 'bufferSubClip')
                FfmpegWrapper().concatVideos('bufferSubClip', latestFile, fileName = outputName)
                
                remove('bufferSubClip.h264')
                move(f'{curdir}/{outputName}', f'{curdir}\\finishedClips')
        
        if curVideoLength > self.buffer: #or ManageVideos().checkRawFolderEmpty(self):
            startTime = curVideoLength - self.buffer
            endTime = curVideoLength
            
            FfmpegWrapper().extractVideoClip(latestFile, startTime, endTime, fileName = outputName)

            move(f'{curdir}/{outputName}', f'{curdir}\\finishedClips')
        
    def convertToMp4(self, fileName, outputName):
            system(f'MP4Box -add {fileName}.h264 {outputName}.mp4')
            remove(f'{fileName}.h264')
            print('Done')
            
if __name__ == '__main__':
    Recorder().startRecording()
   



