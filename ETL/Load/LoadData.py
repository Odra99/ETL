from sys import path
from os.path import dirname as dir
from numpy import append
path.append(dir(path[0]))
import pandas as pd
from sqlalchemy import create_engine

from Extract.ExtractDB import ExtractDB
from Connector.DataBase import cur

class Loader:
    
    def __init__(self):
        self.extractDB = ExtractDB()
        self.engine = create_engine('postgresql://postgres:Odra20$@localhost:5432/ProjectIA')
    
    def updateEmployee(self,Dpi,Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,Apellido_Casada,Cedula_Orden,Cedula_Registro,Direccion,Nit,Genero,Telefono,Correo_Electronico,Fecha_Nacimiento):
        query =  ('UPDATE "Persona"	SET "Primer_Nombre"= %s, "Segundo_Nombre"= %s, "Primer_Apellido"=%s, "Segundo_Apellido"=%s, "Apellido_Casada"=%s, "Cedula_Orden"=%s, "Cedula_Registro"=%s, "Direccion"=%s, "Nit"=%s, "Genero"=%s, "Telefono"=%s, "Correo_Electronico"=%s, "Fecha_Nacimiento"=%s WHERE "Dpi"=%s;    ')
        var_update = (Primer_Nombre,Segundo_Nombre,Primer_Apellido,Segundo_Apellido,Apellido_Casada,Cedula_Orden,Cedula_Registro,Direccion,Nit,Genero,Telefono,Correo_Electronico,Fecha_Nacimiento,Dpi)
        cur.execute(query,var_update)
    
    def updateDBEmployee(self,employees):
        tmp_people =  pd.DataFrame(columns=['Dpi','Primer_Nombre','Segundo_Nombre','Primer_Apellido','Segundo_Apellido','Apellido_Casada','Cedula_Orden','Cedula_Registro','Direccion','Nit','Genero','Telefono','Correo_Electronico','Fecha_Nacimiento'])
        employees = employees.astype(object).where(pd.notnull(employees), None)
        for i,row in employees.iterrows():
            if self.extractDB.existsEmployee(row['Dpi']):
                self.updateEmployee(row['Dpi'],row['Primer_Nombre'],row['Segundo_Nombre'],row['Primer_Apellido'],row['Segundo_Apellido'],row['Apellido_Casada'],row['Cedula_Orden'],row['Cedula_Registro'],row['Direccion'],row['Nit'],row['Genero'],row['Telefono'],row['Correo_Electronico'],row['Fecha_Nacimiento'])
            else:
                tmp_people = tmp_people.append(row)
        return tmp_people

    def updateEnterprise(self,Codigo,Nombre,Nit,Direccion,Telefono):
        query = ('UPDATE public."Empresa" SET  "Nombre"=%s, "Nit"=%s, "Direccion"=%s, "Telefono"=%s WHERE "Codigo"=%s;')
        var_update = (Nombre,Nit,Direccion,Telefono,Codigo)
        cur.execute(query,var_update)
    
    def updateDBEnterprise(self,enterprise):
        tmp_enterprise = pd.DataFrame(columns=['Codigo','Nombre','Nit','Direccion','Telefono'])
        enterprise = enterprise.astype(object).where(pd.notnull(enterprise), None)
        for i,row in enterprise.iterrows():
            if self.extractDB.existsEnterprise(row['Codigo']):
                self.updateEnterprise(row['Codigo'],row['Nombre'],row['Nit'],row['Direccion'],row['Telefono'])
            else:
                tmp_enterprise = tmp_enterprise.append(row)
        return tmp_enterprise
    
    def loadData(self,enterprises,employees, works):
        insert_employees = self.updateDBEmployee(employees)
        insert_employees.to_sql('Persona',con=self.engine,if_exists='append',index=False)
        insert_enterprises = self.updateDBEnterprise(enterprises)
        insert_enterprises.to_sql('Empresa',con=self.engine,if_exists='append',index=False)
        works.to_sql('Trabajo',con=self.engine,if_exists='append',index=False)
        
        