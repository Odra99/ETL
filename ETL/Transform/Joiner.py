from sys import path
from os.path import dirname as dir
import time
from tkinter import END
import numpy as np
path.append(dir(path[0]))
import pandas as pd


class Joiner:
    
    relabelEnterprise = {
        'Codigo_Unico_Empresa':'Codigo',
        'Nombre_Empresa':'Nombre',
        'Nit_Empresa':'Nit',
        'Direccion_Empresa':'Direccion',
        'Telefono_Empresa':'Telefono'
    }
    
    relabelEmployee = {
        'Correo_Electronico_Trabajo':'Correo_Electronico'
    }
    
    relabelWork = {
        'Dpi':'ID_Persona',
        'Codigo_Unico_Empresa': 'ID_Empresa'
        
    }
    
    optionalColumnsEmployee = {
        'Cedula_Orden',
        'Cedula_Registro',
        'Direccion',
        'Genero',
        'Telefono',
        'Correo_Electronico_Trabajo',
        'Fecha_Nacimiento'
    }
    
    optionalColumnsWork = {
        'Nombre_Puesto',
        'Mes_Planilla',
        'Salario'
    }

    def __init__(self,consoleText):
        self.files = []
        self.consoleText = consoleText
        self.enterprises = pd.DataFrame(columns=['Codigo','Nombre','Nit','Direccion','Telefono'])
        self.people =  pd.DataFrame(columns=['Dpi','Primer_Nombre','Segundo_Nombre','Primer_Apellido','Segundo_Apellido','Apellido_Casada','Cedula_Orden','Cedula_Registro','Direccion','Nit','Genero','Telefono','Correo_Electronico','Fecha_Nacimiento'])
        self.payroll = pd.DataFrame(columns=['Fecha_Inicial','Fecha_Final','Nombre_Puesto','Mes_Planilla','Salario'])
        
    def setFiles(self,files):
        self.files = files
    
    def getEnterprises(self,file):
        enterprise = file[['Codigo_Unico_Empresa','Nombre_Empresa','Nit_Empresa']]
        if 'Direccion_Empresa' in file:
            direccion = file['Direccion_Empresa']
            enterprise = enterprise.join(direccion)
        if 'Telefono_Empresa' in file:
            telefono = file['Telefono_Empresa']
            enterprise = enterprise.join(telefono)
        for label in enterprise:
            if label in self.relabelEnterprise:
                enterprise = enterprise.rename(columns = {label: self.relabelEnterprise[label]})
        self.enterprises = pd.concat([self.enterprises,enterprise])
        self.enterprises = self.enterprises.drop_duplicates()
    
    def getEmployee(self,file):
        employee = file[['Dpi','Nit','Primer_Nombre','Segundo_Nombre','Primer_Apellido','Segundo_Apellido','Apellido_Casada']]
        for label in file:
            if label in self.optionalColumnsEmployee:
                column = file[label]
                employee = employee.join(column)
        for label in employee:
            if label in self.relabelEmployee:
                employee = employee.rename(columns = {label: self.relabelEmployee[label]})
        self.people = pd.concat([self.people,employee])
        self.people = self.people.drop_duplicates()
    
    def getWorks(self,file):
        works = file[['Fecha_Inicial','Fecha_Final','Codigo_Unico_Empresa','Dpi',]]
        for label in file:
            if label in self.optionalColumnsWork:
                column = file[label]
                works = works.join(column)
        for label in works:
            if label in self.relabelWork:
                works = works.rename(columns = {label: self.relabelWork[label]})
        self.payroll = pd.concat([self.payroll,works])
        self.payroll = self.payroll.drop_duplicates()
    
    def join(self):
        #time.sleep(5) 
        self.consoleText.insert(END,"Preparando tablas: "+'\n')
        for file in self.files:
           self.getEnterprises(file)
           self.getEmployee(file)
           self.getWorks(file)
    