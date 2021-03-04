from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import remove, system, remove
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT

class FfmpegWrapper:
    @staticmethod #@staticmethod wird in dieser Datei verwendet, da die Klasse hier nicht zum Initialisieren eines Objektes verwendet wird, sondern nur als eine Gruppierung von Methoden dient
    def concatVideos(firstVideo, secondVideo, filename = 'output'): #Schneidet 2 Videos zusammen und nimmt einen Ausgabenamen 
        system(f'ffmpeg -i "concat:{firstVideo}.h264|{secondVideo}.h264" -c copy {filename}.h264') #Nimmt beide Videos und Schneidet sie zusammen und gibt das Produkt aus, mit dem Angegebenen Namen
       
        return True
    
    @staticmethod
    def concatVideoAndAudio(video, audio, outputName = 'output', fileEx = 'mp4'): #Schneidet Video und Audio zusammen, nimmt aber einen Optionalen Parameter, da nicht immer der selbe Dateityp gegeben ist
        system(f'ffmpeg -i {video}.{fileEx}-i audio.wav -c copy -map 0:v:0 -map 1:a:0 {outputName}.mp4') #Nimmt Audio und legt diese über das Video, gibt dann die Datei mit beidem Aus
        
        #Alternativen, alle diese Befehle Arbeiten wie der Obere, haben aber kleinere Unterschiede:
        #system(f'ffmpeg -i {video}.{fileEx} -i audio.wav -c:v copy -c:a aac {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i {audio}.wav -c copy {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i {audio}.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {outputName}.mp4')
        #system(f'ffmpeg -i {video}.{fileEx} -i audio.wav -shortest {outputName}.mp4')
        
        return True

    @staticmethod
    def extractVideoClip(file, startTime, endTime, filename = 'subclip'): #Nimmt ein Video, die Sekunde aber der Gestartet und Geendet werden soll, und schneidet einen Clip aus diesem heraus
         ffmpeg_extract_subclip(f'{file}.h264', startTime, endTime, targetname= f'{filename}.h264') #Schneidet ein Untervideo aus dem Hauptvideo aus
                                                                                                    #Dabei bleibt das Originalle Video erhalten, der Entstandene Clip ist ein weiteres Video
         return True

    @staticmethod
    def getVideoLength(filepath): #Gibt die Lenge von Videos zurück, nimmt einen Weg zu Video, weil diese nicht immer im selben Ordner sind
        video = VideoCapture(filepath) #Lädt das Video
        fps = video.get(CAP_PROP_FPS) #Bestimmt die FPS des Videos
        frameCount = video.get(CAP_PROP_FRAME_COUNT) #Berechnet wie viele Bilder im Video sind
        length = int(frameCount / fps) #Teil die Bilderanzahl durch die FPS un ermittelt dadurch die Länge des Videos in Sekunden 
        
        return length #Sekunden
    
    @staticmethod
    def convertToMp4(fileName, output): #Nimmt eine Video un wandelt es in eine mp4 um und gibt dies unter angegebenem Namen aus
        system(f'MP4Box -add {fileName}.h264 {output}.mp4') #Umwandlung von h264 --> mp4
        remove(f'{fileName}.h264') #Löscht das alte Video um Speicherplatz frei zu halten
    
if __name__ == '__main__':
    #FfmpegWrapper().concatVideos('TestFile157', 'TestFile278')
    ...
  