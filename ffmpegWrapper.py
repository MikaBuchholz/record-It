from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import remove, system
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

class FfmpegWrapper:
    @staticmethod
    def concatVideos(firstVideo, secondVideo, filename = 'output'):
        FfmpegWrapper.writeVideosToTxt(firstVideo, secondVideo)

        system(f'ffmpeg -i "concat:{firstVideo}.h264|{secondVideo}.h264" -c copy {filename}.h264')
        #system(f'ffmpeg -f concat -i mylist.txt -c copy {filename}.h264')
        remove('mylist.txt')

        return True
    
    @staticmethod
    def concatVideoAndAudio(video, audio, outputName = 'output'):
        system(f'ffmpeg -i {video}.mp4 -i {audio}.mp3 -c:v copy -c:a aac {outputName}.mp4')

        return True
    
    @staticmethod
    def writeVideosToTxt(firstVideo, secondVideo):
        with open('mylist.txt', 'w') as file:
            file.write(f'file {firstVideo}.h264 \nfile {secondVideo}.h264')
            
        return True

    @staticmethod
    def extractVideoClip(file, startTime, endTime, filename = 'subclip'): 
         ffmpeg_extract_subclip(f'{file}.h264', startTime, endTime, targetname= f'{filename}.h264')

         return True

    @staticmethod
    def getVideoLength(filepath):
        video = VideoCapture(filepath)
        fps = video.get(CAP_PROP_FPS)
        frameCount = video.get(CAP_PROP_FRAME_COUNT)
        length = int(frameCount / fps)
        
        return length #Sekunden
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    ...
  