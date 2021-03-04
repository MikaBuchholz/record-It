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
        self.buffer = float(Buffer().getBufferValue()) * 60 # Holt den neusten buffer-Wert aus der Datenbank und speichert diesen in einer Variable
        self.resWidth = resWidth # Speichert die Bildbreite
        self.resHeight = resHeight # Speichert die Bildhöhe
        self.framerate = framerate # Speichert die Bildrate
        self.camera = PiCamera(resolution=(self.resWidth, self.resHeight), framerate = self.framerate) # Initialisiert die PiCamera (Kamera) mit gegebenen Werten
        
        # Erstellt Ordner in denen Videos gespeichert werden:
        if not path.isdir(f'{curdir}/rawData'):
            mkdir(f'{curdir}/rawData') # rawData Ordner enthält temporäre Dateien
        
        if not path.isdir(f'{curdir}/finishedClips'):
            mkdir(f'{curdir}/finishedClips') # finishedClips Ordner enthält durch Knopfdruck gespeichert endgültige Dateien
        
        # Falls die Ordner schon existieren werden diese geleert, damit die Logik der Programmes funktioniert & für Speicherplatz natürlich ;)
        ManageVideos().clearMainFolder()
        ManageVideos().clearRawFolder()

    def startRecording(self, session): # Startet die Aufnahme; 'session' ist die bestehende Verbindung zur Datenbank
        outputName = (datetime.now()).strftime('%Y%m%d%H%M%S') # Temporärer Dateiname im folgenden Formatbeispiel: 20200320010203 (JahrMonatTagStundeMinuteSekunde)
        
        self.camera.start_recording(f'{outputName}.h264') # Startet die Bildaufnahme der PiCamera
        audio = AudioRecorder() # Initialisiert die Tonaufnahme
        
        endTime = time() + (2 * self.buffer) # Die Endzeit für das Zwischenspeichern einer temporären Datei ist die 'jetzige' Zeit addiert mit dem doppelten buffer-Wert 
        
        print('Recording...') # Debug/feedback
        
        while True: # while loop entspricht einer konstanten Aufnahme mit einem vorgesehenen Ende
            currentTime = time()
            audio.record() # Startet die Tonaufnahme
            
            if session.getBtnPress(): # Überprüft Datenbank ob Knopf auf Internetseite gedrückt wurde
                self.camera.stop_recording() # Stoppt die Bildaufnahme der PiCamera und speichert eine Videodatei ab
                audio.stop() # Stoppt die Tonaufnahme und speichert eine Tondatei ab
                
                self.checkVideoVsBufferLength() # Startet edge-case Logik für 'Shadowplay-artige' Funktion/Endergebnis
                break
                
            if currentTime > endTime: # Überprüft ob die doppelte Buffer-Zeit vergangen ist
                # Leert den rawData Ordner, da nur eine Datei in diesem vorhanden sein darf:
                if not ManageVideos().checkRawFolderEmpty(): 
                    ManageVideos().clearRawFolder()
                    
                self.camera.stop_recording() # Stoppt die Bildaufnahme der PiCamera und speichert eine Videodatei ab
                audio.stop() # Stoppt die Tonaufnahme und speichert eine Tondatei ab
                
                latestFile = ManageVideos().getMainFile() # Speichert den Namen der temporären Videodatei in einer Variable ab für den Ffmpeg-wrapper
                
                FfmpegWrapper().concatVideoAndAudio(latestFile, 'audio', latestFile, fileEx = 'h264') # Verbindet Ton und Video
                
                move(f'{curdir}/{latestFile}.h264', f'{curdir}/rawData') # Verschiebt das fertige Video in den temporären Ordner
                break

    def checkVideoVsBufferLength(self): # Edge-case Überprüfungslogik
        outputName = (datetime.now()).strftime('%Y%m%d%H%M%S') # Temporärer Dateiname im folgenden Formatbeispiel: 20200320010203 (JahrMonatTagStundeMinuteSekunde)
        fullOutputName = (datetime.now()).strftime('recordIt-%d-%b-%Y-%H-%M-%S') # Endgültiger Dateiname (lesbar), Format: recordIt-20-03-21-11-03-45
        
        oldestFile = ManageVideos().getRawFile() # Holt sich die temporäre Datei
        latestFile = ManageVideos().getMainFile() # Holt sich die aktuelle Datei
        
        oldestFilePath = f'{curdir}/rawData/{oldestFile}' # Holt sich den Dateipfad der temporären Datei
        latestFilePath = f'{curdir}/{latestFile}' # Holt sich den Dateipfad der aktuellen Datei
        
        curVideoLength = FfmpegWrapper().getVideoLength(f'{latestFilePath}.h264') # Beschafft sich die Länge des aktuellen Videos (wichtig für folgende Logik)
        
        if curVideoLength < self.buffer: # Wenn die Länge des Videos kleiner als der Buffer ist, muss überprüft werden ob es möglich ist die Restzeit zu füllen
            if ManageVideos().checkRawFolderEmpty(): # Wenn keine temporären Dateien existieren, kann das aktuellste Video ohne Schneiden etc. abgespeichert werden
                FfmpegWrapper().convertToMp4(latestFile, fullOutputName) # Konvertiert Video zu .mp4
                
                FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName) # Verbindet Ton und Video (buggy)
                
                move(f'{curdir}/{fullOutputName}.mp4', f'{curdir}/finishedClips') # Verschiebt fertiges Video in den finishedClips Ordner
                
            else: # Gibt es temporäre Dateien muss die Restzeit gefüllt werden
                bufferLength = FfmpegWrapper().getVideoLength(f'{oldestFilePath}.h264') # Holt sich die Länge der temporären Datei
                startTime = abs(curVideoLength - self.buffer) # Berechnet den Anfang des notwendigen Schnitts
                endTime = abs(bufferLength) # Berechnet das Ende des notwendigen Schnitts (natürlich das 'maximale' Ende des Videos)
              
                FfmpegWrapper().extractVideoClip(oldestFilePath, startTime, endTime, filename = 'bufferSubClip') # Extrahiert den gewünschten Ausschnitt aus dem temporären Video um diesen mit dem aktuellesten Video zu verbinden
                FfmpegWrapper().concatVideos('bufferSubClip', latestFilePath, filename = outputName) # Verbindet gewünschten Ausschnitt und aktuellstes Video
                remove('bufferSubClip.h264') # Löscht den nun nutzlosen gewünschten Ausschnitt, da dieser beim Verbinden nicht automatisch entfernt wird
                FfmpegWrapper().convertToMp4(outputName, fullOutputName) # Konvertiert Video zu .mp4
                
                FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName) # Verbindet Ton und Video (buggy)
                
                move(f'{curdir}/{fullOutputName}.mp4', f'{curdir}/finishedClips') # Verschiebt fertiges Video in den finishedClips Ordner
        
        if curVideoLength > self.buffer: # Wenn die Videolänge größer als die Bufferzeit ist, ist eine temporäre Datei nicht nötig
            startTime = curVideoLength - self.buffer # Berechnet den Anfang des notwendigen Schnitts
            endTime = curVideoLength # Berechnet das Ende des notwendigen Schnitts (natürlich das 'maximale' Ende des Videos)
            
            FfmpegWrapper().extractVideoClip(latestFilePath, startTime, endTime, fileName = outputName) # Extrahiert den gewünschten Ausschnit aus aktuellster Datei
            FfmpegWrapper().convertToMp4(outputName, fullOutputName) # Konvertiert Video zu .mp4
            
            FfmpegWrapper().concatVideoAndAudio(fullOutputName, 'audio', fullOutputName) # Verbindet Ton und Video (buggy)
            
            move(f'{curdir}/{fullOutputName}', f'{curdir}/finishedClips') # Verschiebt fertiges Video in den finishedClips Ordner
        
# Debug code:   
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
