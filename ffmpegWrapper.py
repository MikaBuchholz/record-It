from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import remove, system
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

class FfmpegWrapper:
    def __init__(self):
        self.videoType = 'h264'

    def concatVideos(self, firstVideo, secondVideo, filename = 'output'):
        self.writeVideosToTxt(firstVideo, secondVideo)

        system(f'ffmpeg -f concat -i mylist.txt -c copy {filename}.{self.videoType}')
        remove('mylist.txt')

        return True
    
    def concatVideoAndAudio(self, video, audio, outputName = 'output'):
        system(f'ffmpeg -i {video}.{self.videoType} -i {audio}.mp3 -c:v copy -c:a aac {outputName}.{self.videoType}')

        return True
        
    def writeVideosToTxt(self, firstVideo, secondVideo):
        with open('mylist.txt', 'w') as file:
            file.write(f'file {firstVideo}.{self.videoType}\nfile {secondVideo}.{self.videoType}')
            
        return True

    def extractVideoClip(self, file, startTime, endTime, filename = 'subclip'): 
         ffmpeg_extract_subclip(f'{file}.{self.videoType}', startTime, endTime, targetname= f'{filename}.{self.videoType}')

         return True

    def getVideoLength(self, file):
        video = VideoCapture(f'./{file}.{self.videoType}')
        fps = video.get(CAP_PROP_FPS)
        frameCount = video.get(CAP_PROP_FRAME_COUNT)
        length = int(frameCount / fps)
        
        return length #Sekunden
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    print(FfmpegWrapper().getVideoLength('SexAv'))