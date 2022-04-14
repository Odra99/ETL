from sys import path
from os.path import dirname as dir
from tkinter import N

path.append(dir(path[0]))
import pandas as pd
from validate_email import validate_email


class Transformer:

    dpiStructure = [
        "0101",
        "0102",
        "0103",
        "0104",
        "0105",
        "0106",
        "0107",
        "0108",
        "0109",
        "0110",
        "0111",
        "0112",
        "0113",
        "0114",
        "0115",
        "0116",
        "0117",
    ]

    def __init__(self):
        self.files = []
        self.rejectedData = []

    def cleanDigits(self, file):
        # Clean DPI
        file["Dpi"] = file.Dpi.map(self.justDigits)
        # Clean Nit
        file["Nit"] = file.Nit.map(self.justAlfNumber)
        # Clean Nit_Empresa
        file["Nit_Empresa"] = file.Nit_Empresa.map(self.justAlfNumber)
        # Clean celphone
        file["Telefono"] = file["Telefono"].map(self.justDigits)
        if "Telefono_Empresa" in file:
            file["Telefono_Empresa"] = file["Telefono_Empresa"].map(self.justDigits)
        return file

    def justDigits(self, txt):
        try:
            int(txt)
            return txt
        except:
            return "".join(c for c in txt if c.isdigit())

    def justAlfNumber(self, txt):
        try:
            int(txt)
            return txt
        except:
            return "".join(c for c in txt if c.isdigit() or c.isalpha())

    def cleanGender(self, file):
        file["Genero"] = file["Genero"].str.title().str.strip()
        file["Genero"] = file["Genero"].replace({"Masculino": "M", "Femenino": "F"})

    def cleanStatus(self, file):
        file["Condicion_Laboral"] = file["Condicion_Laboral"].str.title().str.strip()
        file["Condicion_Laboral"] = file["Condicion_Laboral"].replace(
            {"Activo": "A", "Inactivo": "I"}
        )

    def formatDates(self, file):
        file["Fecha_Inicial"] = file["Fecha_Inicial"].apply(
            lambda x: pd.to_datetime(x).strftime("%d/%m/%Y")
        )
        file["Fecha_Final"] = file["Fecha_Final"].apply(
            lambda x: pd.to_datetime(x).strftime("%d/%m/%Y")
        )

    def verifyDPI(self, file):
        file['Count_DPI'] = file['Dpi'].str.len()
        file.drop(file[file['Count_DPI'] != 13].index, inplace = True)
        file['Codes_DPI'] = file['Dpi'].str[-4:]
        file["Codes_DPI"] = file["Codes_DPI"].map(self.verifyCodesDpi)
        file.drop(file[file['Codes_DPI']==False].index,inplace=True)
        del file['Codes_DPI']
        del file['Count_DPI'] 

    def verifyCodesDpi(self,txt):
        if txt in self.dpiStructure:
            return txt
        else:
            return False

    def verifyEmail(self, file):
        file["valid_email"] = file["Correo_Electronico_Trabajo"].apply(validate_email)
        file.drop(file[file['valid_email']==False].index,inplace=True)
        del file['valid_email']

    def setFiles(self, files):
        self.files = files

    def transform(self):
        for file in self.files:
            self.cleanStatus(file)
            self.cleanDigits(file)
            self.formatDates(file)
            self.verifyEmail(file)
            self.verifyDPI(file)
            file.to_csv("prueba.csv")
            print(file)
