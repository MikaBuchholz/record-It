from os import curdir, listdir, remove

class ManageVideos:
    @staticmethod #@staticmethod wird in dieser Datei verwendet, weil die Klasse hier nicht zum Initialisieren eines Objektes verwendet wird, sondern nur als eine Gruppierung von Methoden dient
    def getRawFile():
        for file in listdir(f'{curdir}/rawData'): #Listet alle Dateien im Ordner rawData auf
            if file[-4:] == 'h264': #Fillter nur nach Dateien mit Typ .h264
                return file[:-5] #Gibt nur den Namen der Datei aus, ohne .h264

    @staticmethod
    def getMainFile(): 
        for file in listdir(f'{curdir}'): #Listet alle Dateien im Ordner des Ausführenden Programms auf
            if file[-4:] == 'h264': #Fillter nur nach Dateien mit Typ .h264
                return file[:-5] #Gibt nur den Namen der Datei aus, ohne .h264
    
    @staticmethod
    def checkRawFolderEmpty():
        folderLength = len((listdir(f'{curdir}/rawData'))) #Gibt mir die Menge an Dateien die im rawData Ordner enthalten sind
        
        if folderLength == 0: # Ist diese Menge 0, gibt es also keine Dateien im Ordner wird der Wert True zurückgegeben
            return True
        
        return False # Ist diese Menge nicht gleich 0, gibt es also Dateien im Ordner, wird False zurückgegeben
    
    @staticmethod
    def clearRawFolder():
        for file in listdir(f'{curdir}/rawData'): #Listet alle Dateien im Ordner rawData auf
            remove(f'{curdir}/rawData/{file}') # Löscht jede Datei aus diesem Ordner für Platzschaffung
    
    @staticmethod
    def clearMainFolder():
        for file in listdir(curdir): #Listet alle Dateien im Ordner des Ausführenden Programms auf
            if file[-4:] == 'h264' or file[-3:] == 'mp4' or file[-3:] == 'wav': #Weil dieser Ordner die Scripts und configs enthält wollen wir nur 3 bestimmte Dateitypen Löschen
                remove(f'{curdir}/{file}') #Löscht Datei sollte sie im if-statement vorkommen