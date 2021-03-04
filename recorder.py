#!/usr/bin/python3
from picamera import PiCamera
from time import time, sleep
from os import system, remove, curdir, path, mkdir, listdir
from retrieveBuffer import Buffer
from shutil import move
from datetime import datetime
from ffmpegWrapper import FfmpegWrapper
from manageVideos import ManageVideos
from Audio import AudioRecorder

class Recorder:
    def __init__(self, resWidth = 1280, resHeight = 720, framerate = 30):
        self.buffer = float(Buffer().getBufferValue()) * 60
        self.resWidth = resWidth
        self.resHeight = resHeight
        self.framerate = framerate
        self.camera = PiCamera(resolution=(self.resWidth, self.resHeight), framerate = self.framerate)
        
        if not path.isdir(f'{curdir}/rawData'):
            mkdir(f'{curdir}/rawData')
        
        if not path.isdir(f'{curdir}/finishedClips'):
            mkdir(f'{curdir}/finishedClips')
        
        ManageVideos().clearMainFolder()
        ManageVideos().clearRawFolder()

    def startRecording(self, session):
        outputName = (datetime.now()).strftime('%Y%m%d%H%M%S')
        
        self.camera.start_recording(f'{outputName}.h264')
        audio = AudioRecorder()
        
        endTime = time() + (2 * self.buffer)
        
        print('Recording...')
        
        while True:
            currentTime = time()
            audio.record()
            
            if session.getBtnPress():
                self.camera.stop_recording()
                audio.stop()
                
                self.checkVideoVsBufferLength()
                break
                
            if currentTime > endTime:
                if not ManageVideos().checkRawFolderEmpty():
                    ManageVideos().clearRawFolder()
                    
                self.camera.stop_recording()
                audio.stop()
                
                latestFile = ManageVideos().getMainFile()
                
                FfmpegWrapper().concatVideoAndAudio(latestFile, 'audio', latestFile, fileEx = 'h264')
                
                move(f'{curdir}/{latestFile}.h264', f'{curdir}/rawData')
                break

    def checkVideoVsBufferLength(self):
        outputName = (datetime.now()).strftime('%Y%m%d%H%M%S')
        fullOutputName = (datetime.now()).strftime('recordIt-%d-%b-%Y-%H-%M-%S')
        
        oldestFile = ManageVideos().getRawFile()
        latestFile = ManageVideos().getMainFile()
        
        oldestFilePath = f'{curdir}/rawData/{oldestFile}'
        latestFilePath = f'{curdir}/{latestFile}'
        
        curVideoLength = FfmpegWrapper().getVideoLength(f'{latestFilePath}.h264')
        
        if curVideoLength < self.buffer:
            if ManageVideos().checkRawFolderEmpty():
                FfmpegWrapper().convertToMp4(latestFile, fullOutputName)
                
                FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName)
                
                move(f'{curdir}/{fullOutputName}.mp4', f'{curdir}/finishedClips')
                
            else:
                bufferLength = FfmpegWrapper().getVideoLength(f'{oldestFilePath}.h264')
                startTime = abs(curVideoLength - self.buffer)
                endTime = abs(bufferLength)
              
                FfmpegWrapper().extractVideoClip(oldestFilePath, startTime, endTime, filename = 'bufferSubClip')
                FfmpegWrapper().concatVideos('bufferSubClip', latestFilePath, filename = outputName)
                remove('bufferSubClip.h264')
                FfmpegWrapper().convertToMp4(outputName, fullOutputName)
                
                FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName)
                
                move(f'{curdir}/{fullOutputName}.mp4', f'{curdir}/finishedClips')
        
        if curVideoLength > self.buffer:
            startTime = curVideoLength - self.buffer
            endTime = curVideoLength
            
            FfmpegWrapper().extractVideoClip(latestFilePath, startTime, endTime, fileName = outputName)
            FfmpegWrapper().convertToMp4(outputName, fullOutputName)
            
            FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName)
            
            move(f'{curdir}/{fullOutputName}', f'{curdir}/finishedClips')
        
    
if __name__ == '__main__':
    session = Buffer()
    rec = Recorder()
    session.toggleBtnPress(False)
    
    while session.getRecordingValue():
        rec.startRecording(session)
        session.updateValues()
        session.toggleBtnPress(False)
        ManageVideos().clearMainFolder()
        
'''
            Dev. Konzept:
            [/////]
            [////////]

            Max Video Laenge = 2 * Buffer
            1: Neue Video Laenge kuerzer als Buffer => Cutting, Stitching, Render
            2: Neues Video Laenge groesser als Buffer => Cutting, Render
            => raw Ordner clear & fertiger clip
            
            3: raw Ordner ist leer => Cutting, Render
            3.1: Video Laenge kuerzer oder groeßer check => no cutting or cutting
            
'''
