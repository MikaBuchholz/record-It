import os
import pymongo
from dotenv import load_dotenv, find_dotenv

class Buffer:
    def __init__(self, databasename = 'rlf-shadowplay-cluster', collectionname = 'buffers', secondcollectionname = 'captures'):
        self.databasename = databasename
        # Bei MongoDB ist eine collection das gleiche wie ein Table in SQL
        self.collectionname = collectionname # collection in dem der buffer-Wert und der Aufnahme-Status gespeichert ist
        self.secondcollectionname = secondcollectionname # collection in dem der gespeichert ist ob der Knopf auf der Internetseite gedrückt wurde oder nicht
        
        self.updateValues() # mit der Datenbank verbinden und weiter Klassen-Variablen deklarieren
    
    def updateValues(self):
        # .env datei laden und daraus den connection-string zur Datenbanken holen/finden, da wir dies nicht auf github publishen wollen
        load_dotenv(find_dotenv())
        MONGO_URI = os.environ.get('MONGO_URI') # connection-string in MONGO_URI Konstante speichern

        # Zur Datenbank verbinden:
        client = pymongo.MongoClient(MONGO_URI) # Einen client kreieren um eine Verbindung zu initialisieren
        database = client[self.databasename] # Die Datenbank aus der client-Verbindung erhalten
        self.collection = database[self.collectionname] # Die buffer-Wert & Aufnahme-Status collection aus der datenbank erhalten
        self.secondcollection = database[self.secondcollectionname] # Die Knopf collection aus der Datenbank erhalten
        
        # Den buffer-Wert und Aufnahme-Status erhalten:
        primaryData = self.collection.find({}) # Speichert die ganze information der buffer-Wert & Aufnahme-Status collection in der primaryData Variable
        for item in primaryData: # Über die 'Blöcke' von Information iterieren
            if item['date']: # Wenn der Informations-Block einen 'date' Datenfeld besitzt ist diese Information von der offiziellen Internetseite gekommen und somit valide
                self.__bufferValue = item['buffer'] # buffer-Wert in Objekt speichern
                self.__recording = item['recording'] # Aufnahme-Status in Objekt speichern
                break
        
        # Den Knopfdruck-Status erhalten:
        secondaryData = self.secondcollection.find({}) # Speichert die ganze information der Knopf collection in der primaryData Variable
        for item in secondaryData: # Über die 'Blöcke' von Information iterieren
            if item['date']: # Wenn der Informations-Block einen 'date' Datenfeld besitzt ist diese Information von der offiziellen Internetseite gekommen und somit valide
                self.__btnPress = item['btnPressed'] # Knopfdruck-Status in Objekt speichern
                break
    
    def getBufferValue(self): # Gibt den (privaten) buffer-Wert zurück
        return self.__bufferValue
    
    def getRecordingValue(self): # Gibt den (privaten) Aufnahme-Status zurück
        return self.__recording
    
    def getBtnPress(self): # Gibt den Knopfdruck-Status zurück
        # Folgender Code iteriert über die Knopf collection und gibt die neusten Änderungen zurück
        # Dies ist wichtig, da in der Hauptdatei (recorder.py) konstant gechecked werden muss, ob der Knopf gedrückt wird
        for item in self.secondcollection.find({}): # Über die 'Blöcke' von Information iterieren
            if item['model'] == 'Capture': # Wenn das Datenfeld 'model' den Wert 'Capture' hat, dann ist dieser valide für den Knopfdruck (Wichtig, damit nicht zwischendurch Datenmanipulation betrieben werden kann)
                return item['btnPressed'] # Knopfdruck-Status zurückgeben
    
    def toggleBtnPress(self, state = False):
        if type(state) == bool: # 'state' darf auf keinen Fall etwas anderes als ein boolean sein, da dies das Hauptprogramm (recorder.py) direkt crashen würde 
            filter = { 'model': 'Capture'} # Der Filter für die Änderung von Daten in der Datenbank. So soll also Information geändert werden welche zum Knopfdruck feature gehören
            update = { '$set': { 'btnPressed': state } } # Der Wert des 'btnPressed' Datenfeld soll zum Wert der state Variable geändert werden
            
            self.secondcollection.update_one(filter, update) # Nun wird die Information der Knopfdruck collection, gemäß dem Filter und der update-Information, geändert

# Debug code:
if __name__ == '__main__':
    import time
    
    session = Buffer()
    
    while True:
        print(session.getBtnPress())
        time.sleep(3)
        print(session.getBtnPress())
        time.sleep(3)
        session.toggleBtnPress(False)
        print('Changed Btn Press to False')
        time.sleep(3)