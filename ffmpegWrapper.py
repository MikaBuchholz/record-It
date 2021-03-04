from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import remove, system, remove
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

class FfmpegWrapper:
    @staticmethod
    def concatVideos(firstVideo, secondVideo, filename = 'output'):
        system(f'ffmpeg -i "concat:{firstVideo}.h264|{secondVideo}.h264" -c copy {filename}.h264')
       
        return True
    
    @staticmethod
    def concatVideoAndAudio(video, audio, outputName = 'output', fileEx = 'mp4'):
        system(f'ffmpeg -i {video}.{fileEx}-i audio.wav -c copy -map 0:v:0 -map 1:a:0 {outputName}.mp4')
        
        #Alternativen:
        #system(f'ffmpeg -i {video}.{fileEx} -i audio.wav -c:v copy -c:a aac {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i {audio}.wav -c copy {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i {audio}.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i audio.wav -shortest {outputName}.mp4')
        
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
    
    @staticmethod
    def convertToMp4(fileName, output):
        system(f'MP4Box -add {fileName}.h264 {output}.mp4')
        remove(f'{fileName}.h264')
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    ...
  