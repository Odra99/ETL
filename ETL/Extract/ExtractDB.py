from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))
from ETL.Connector.DataBase import cur


class ExtractDB:
    
    selectEmployee = """SELECT "Dpi" from "Persona" where "Dpi" ={0};"""
    selectEnterprise = """SELECT "Codigo" from "Empresa" where "Codigo" ={0};"""
    
    def existsEnterprise(self,code):
        query = self.selectEnterprise.format(code)
        cur.execute(query)
        return cur.fetchone() is not None
    
    def existsEmployee(self,code):
        query = self.selectEmployee.format(code)
        cur.execute(query)
        return cur.fetchone() is not None