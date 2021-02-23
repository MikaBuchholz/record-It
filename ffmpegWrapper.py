from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import remove, system
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

class FfmpegWrapper:
    @staticmethod
    def concatVideos(firstVideo, secondVideo, filename = 'output'):
        FfmpegWrapper.writeVideosToTxt(firstVideo, secondVideo)

        system(f'ffmpeg -f concat -i mylist.txt -c copy {filename}.mp4')
        remove('mylist.txt')

        return True
    
    @staticmethod
    def concatVideoAndAudio(video, audio, outputName = 'output'):
        system(f'ffmpeg -i {video}.mp4 -i {audio}.mp3 -c:v copy -c:a aac {outputName}.mp4')

        return True
    
    @staticmethod
    def writeVideosToTxt(firstVideo, secondVideo):
        with open('mylist.txt', 'w') as file:
            file.write(f'file {firstVideo}.mp4\nfile {secondVideo}.mp4')
            
        return True

    @staticmethod
    def extractVideoClip(file, startTime, endTime, filename = 'subclip'): 
         ffmpeg_extract_subclip(f'{file}.mp4', startTime, endTime, targetname= f'{filename}.mp4')

         return True

    @staticmethod
    def getVideoLength(file):
        video = cv2.VideoCapture(f'./{file}.mp4')
        fps = video.get(cv2.CAP_PROP_FPS)
        frameCount = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = int(frameCount / fps)
        
        return length #Sekunden
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    print(FfmpegWrapper().getVideoLength('Test'))