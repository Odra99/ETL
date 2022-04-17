import re
from sys import path
from os.path import dirname as dir
import numpy as np

path.append(dir(path[0]))
import pandas as pd
from validate_email import validate_email


class Transformer:
    def __init__(self):
        self.files = []

    def verifyCodesDpi(self, txt):
        if txt in self.dpiStructure:
            return txt
        else:
            return False

    def verifyCedulaOrder(self, txt):
        if txt in self.cedulaOrden:
            return txt
        else:
            return None

    def verifyGender(self, txt):
        if txt == "F" or txt == "M":
            return txt
        else:
            return None

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

    def cleanDigits(self, file):
        # Clean DPI
        file["Dpi"] = file["Dpi"].map(self.justDigits)
        # Clean Codigo Empresa
        file["Codigo_Unico_Empresa"] = file["Codigo_Unico_Empresa"].map(self.justDigits)
        # Clean celphone
        file["Telefono"] = file["Telefono"].map(self.justDigits)
        if "Telefono_Empresa" in file:
            file["Telefono_Empresa"] = file["Telefono_Empresa"].map(self.justDigits)
        return file

    def cleanAlfN(self, file):
        # Clean Nit
        file["Nit"] = file["Nit"].map(self.justAlfNumber)
        # Clean Nit_Empresa
        file["Nit_Empresa"] = file["Nit_Empresa"].map(self.justAlfNumber)

    def cleanCedula(self, file):
        if "Cedula_Orden" in file:
            # Clean Cedula Orden
            file["Cedula_Orden"] = file["Cedula_Orden"].map(self.justAlfNumber)
            # Clean Cedula Registro
            file["Cedula_Registro"] = file["Cedula_Registro"].map(self.justDigits)

    def cleanGender(self, file):
        file["Genero"] = file["Genero"].str.title().str.strip()
        file["Genero"] = file["Genero"].replace({"Masculino": "M", "Femenino": "F"})
        file["Genero"] = file["Genero"].map(self.verifyGender)

    def cleanStatus(self, file):
        file["Condicion_Laboral"] = file["Condicion_Laboral"].str.title().str.strip()
        file["Condicion_Laboral"] = file["Condicion_Laboral"].replace(
            {"Activo": "A", "Inactivo": "I"}
        )

    def formatDates(self, file):
        file["Fecha_Inicial"] = file["Fecha_Inicial"].apply(
            lambda x: pd.to_datetime(x, infer_datetime_format=True).strftime("%d/%m/%Y")
        )
        file["Fecha_Final"] = file["Fecha_Final"].apply(
            lambda x: pd.to_datetime(x, infer_datetime_format=True).strftime("%d/%m/%Y")
        )
        if "Fecha_Nacimiento" in file:
            file["Fecha_Nacimiento"] = file["Fecha_Nacimiento"].apply(
                lambda x: pd.to_datetime(x, infer_datetime_format=True).strftime(
                    "%d/%m/%Y"
                )
            )

    def verifyDPI(self, file):
        file["Count_DPI"] = file["Dpi"].str.len()
        rejectdata = file[file["Count_DPI"] != 13]
        file.drop(file[file["Count_DPI"] != 13].index, inplace=True)
        file["Codes_DPI"] = file["Dpi"].str[-4:]
        file["Codes_DPI"] = file["Codes_DPI"].map(self.verifyCodesDpi)
        rejectdata2 = file[file["Codes_DPI"] == False]
        file.drop(file[file["Codes_DPI"] == False].index, inplace=True)
        del file["Codes_DPI"]
        del file["Count_DPI"]        
        del rejectdata["Count_DPI"]
        del rejectdata2["Count_DPI"]
        del rejectdata2["Codes_DPI"]
        return pd.concat([rejectdata, rejectdata2])
    
    def getRejectData(self,file):
        rejectdata = pd.DataFrame()
        for label in self.requiredColumns:
            rejectdataAux = file[file[label].astype(str).str.len() == 0]
            file.drop(file[file[label].astype(str).str.len() == 0].index, inplace=True)
            rejectdata = pd.concat([rejectdata,rejectdataAux])
        return rejectdata

    def verifyCedula(self, file):
        if "Cedula_Orden" in file:
            file["Cedula_Orden"] = file["Cedula_Orden"].map(self.verifyCedulaOrder)
            file["Cedula_Registro"].mask(
                file["Cedula_Registro"].str.len() == 0, None, inplace=True
            )
            file["Cedula_Registro"].mask(
                file["Cedula_Orden"].str.len() == 0, None, inplace=True
            )

    def verifyEmail(self, file):
        file["valid_email"] = file["Correo_Electronico_Trabajo"].apply(validate_email)
        file["Correo_Electronico_Trabajo"].mask(
            file["valid_email"] == False, None, inplace=True
        )
        del file["valid_email"]

    def verifyNames(self, file):
        file["is_married"] = file["Apellido_Casada"].str.len() > 0
        file["is_women"] = np.where(file["Genero"] == "F", True, False)
        file["verify_married_last_name"] = file["is_married"] & file["is_women"]
        del file["is_married"]
        del file["is_women"]
        file["Apellido_Casada"].mask(
            file["verify_married_last_name"] == False, None, inplace=True
        )
        del file["verify_married_last_name"]

    def deleteDuplicatedData(self, file, i):
        duplicatedData = pd.DataFrame()
        mask = file.duplicated(keep="first")
        duplicatedData = pd.concat([duplicatedData,file.loc[mask]])
        name = "WrongData/Duplicated/duplicatedData" + str(i) + ".csv"
        duplicatedData.to_csv(name,index=False)
        
    def deleteRejectedData(self,i,rejectData):
        name = "WrongData/ErrorData/rejectedData" + str(i) + ".csv"
        rejectData.to_csv(name,index=False)
        
    def setFiles(self, files):
        self.files = files

    def transform(self):
        print("Transformando Datos")
        i = 1
        for file in self.files:
            self.cleanGender(file)
            self.cleanStatus(file)
            self.cleanDigits(file)
            self.formatDates(file)
            self.verifyEmail(file)
            rejectData1 = self.verifyDPI(file)
            self.cleanCedula(file)
            self.verifyCedula(file)
            self.verifyNames(file)
            self.cleanAlfN(file)
            print('Eliminando Datos incorrectos')
            rejectData2 = self.getRejectData(file)
            rejectData = pd.concat([rejectData1,rejectData2])
            self.deleteDuplicatedData(file, i)
            self.deleteRejectedData(i,rejectData)
            i = i + 1
    
    requiredColumns = [
        'Dpi',
        'Nit',
        'Fecha_Inicial',
        'Fecha_Final',
        'Nombre_Empresa',
        'Nit_Empresa',
        'Codigo_Unico_Empresa',
        'Primer_Nombre',
        'Segundo_Nombre',
        'Primer_Apellido',
        'Segundo_Apellido',
        'Apellido_Casada',
        
    ]

    dpiStructure = [
        "0101","0102","0103","0104","0105","0106","0107","0108","0109","0110","0111","0112","0113","0114","0115","0116","0117",
        "0201","0202","0203","0204","0205","0206","0207","0208",
        "0301","0302","0303","0304","0305","0306","0307","0308","0309","0310","0311","0312","0313","0314","0315","0316",
        "0401","0402","0403","0404","0405","0406","0407","0408","0409","0410","0411","0412","0413","0414","0415","0416",
        "0501","0502","0503","0504","0505","0506","0507","0508","0509","0510","0511","0512","0513",
        "0601","0602","0603","0604","0605","0606","0607","0608","0609","0610","0611","0612","0613","0614",
        "0701","0702","0703","0704","0705","0706","0707","0708","0709","0710","0711","0712","0713","0714","0715","0716","0717","0718","0719",
        "0801","0802","0803","0804","0805","0806","0807","0808",
        "0901","0902","0903","0904","0905","0906","0907","0908","0909","0910","0911","0912","0913","0914","0915","0916","0917","0918","0919","0920","0921","0922","0923","0924",
        "1001","1002","1003","1004","1005","1006","1007","1008","1009","1010","1011","1012","1013","1014","1015","1016","1017","1018","1019","1020",
        "1101","1102","1103","1104","1105","1106","1107","1108","1109",
        "1201","1202","1203","1204","1205","1206","1207","1208","1209","1210","1211","1212","1213","1214","1215","1216","1217","1218","1219","1220","1221","1222","1223","1224","1225","1226","1227","1228","1229",
        "1301","1302","1303","1304","1305","1306","1307","1308","1309","1310","1311","1312","1313","1314","1315","1316","1317","1318","1319","1320","1321","1322","1323","1324","1325","1326","1327","1328","1329","1330","1331","1332",
        "1401","1402","1403","1404","1405","1406","1407","1408","1409","1410","1411","1412","1413","1414","1415","1416","1417","1418","1419","1420","1421","1422",
        "1501","1502","1503","1504","1505","1506","1507","1508",
        "1601","1602","1603","1604","1605","1606","1607","1608","1609","1610","1611","1612","1613","1614","1615","1616","1617",
        "1701","1702","1703","1704","1705","1706","1707","1708","1709","1710","1711","1712",
        "1801","1802","1803","1804","1805",
        "1901","1902","1903","1904","1905","1906","1907","1908","1909","1910",
        "2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011",
        "2101","2102","2103","2104","2105","2106","2107",
        "2201","2202","2203","2204","2205","2206","2207","2208","2209","2210","2211","2212","2213","2214","2215","2216","2217",
    ]

    cedulaOrden = [
        "A1","B2","C3","D4","E5",
        "F6","G7","H8","I9","J10",
        "K11","L12","M13","N14","Ñ15",
        "O16","P17","Q18","R19","S20",
        "T21","U22"
    ]