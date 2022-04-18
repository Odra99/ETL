from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))
from tkinter import END

from ETL.Extract.ExtractFile import Extract
from ETL.Transform.Transformer import Transformer
from ETL.Transform.Joiner import Joiner
from ETL.Load.LoadData import Loader

class ETLController:
    
    def __init__(self,console,files):
        self.files = files
        self.consoleText = console
        
    
    def etlProcess(self):
        #time.sleep(0.1) 
        self.consoleText.insert(END,"Leyendo Archivos \n")
        extract = Extract(self.consoleText)
        for file in self.files:
            extract.storageFiles(file)
        extract.verifyFiles()
        transform = Transformer(self.consoleText)
        transform.setFiles(extract.files,extract.filesNames)
        transform.transform()
        joiner = Joiner(self.consoleText)
        joiner.setFiles(transform.files)
        joiner.join()
        loader = Loader(self.consoleText)
        loader.loadData(joiner.enterprises,joiner.people,joiner.payroll)