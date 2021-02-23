from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg
from os import remove, system
import cv2

class FfmpegWrapper:
    def __init__(self):
        pass

    def concatVideos(self, firstVideo, secondVideo, filename = 'output'):
        self.writeVideosToTxt(firstVideo, secondVideo)

        system(f'ffmpeg -f concat -i mylist.txt -c copy {filename}.mp4')
        remove('mylist.txt')

        return True
    
    def concatVideoAndAudio(self, video, audio, outputName = 'output'):
        system(f'ffmpeg -i {video}.mp4 -i {audio}.mp3 -c:v copy -c:a aac {outputName}.mp4')

        return True
        
    def writeVideosToTxt(self, firstVideo, secondVideo):
        with open('mylist.txt', 'w') as file:
            file.write(f'file {firstVideo}.mp4\nfile {secondVideo}.mp4')
            
        return True

    def extractVideoClip(self, file, startTime, endTime, filename = 'subclip'): 
         ffmpeg_extract_subclip(f'{file}.mp4', startTime, endTime, targetname= f'{filename}.mp4')

         return True

    def getVideoLength(self, file):
        video = cv2.VideoCapture(f'./{file}.mp4')
        fps = video.get(cv2.CAP_PROP_FPS)
        frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = int(frameCount / fps)
        
        return length #Sekunden
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    print(FfmpegWrapper().getVideoLength('SexAv'))