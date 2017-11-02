# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''

import sqlite3
import urllib2
import os
import tkMessageBox

from bs4 import BeautifulSoup
from Tkinter import *

def capturaCodigo(nombreFichero,rss):
    """nombre del txt donde se guardara y rss de la pagina """
    try:
        source = urllib2.urlopen(rss).read()
        f = open(nombreFichero, "w")
        f.write(source)
        f.close()  
        print("txt generado con exito")  
    except miError, e:
        print "Ocurri� un error"
        print e
        
class miError(Exception):
    def __init__(self, valor):
        self.valor = valor
    def __str__(self):
        return "Error " + str(self.valor)
    

def borrarDatabase(nombreDatabase):
    try:
        os.remove(nombreDatabase)
    except:
        pass
    
    
def obtenDatosDePagina(enlace,nombreDatabase):
    datosCategoria = urllib2.urlopen(enlace).read() #buscamos en cada categoria
    soup = BeautifulSoup(datosCategoria, 'html.parser')
    temas=soup.find_all("li",attrs={"class":"threadbit "}) 
    datosArray=[0,0,0,0,0,0]
    for n in range(1,3):
        enlace="https://foros.derecho.com/foro/20-Derecho-Civil-General/page"+str(n)+"?s=64d66ccd12b3ba207cff5a3552db97a9"
        for tema in temas:
            enlace = 'https://foros.derecho.com/' + tema.find('a', {'class':'title'})['href']
            print enlace#enlace
            print tema.find_all("a")[1].text#tema
            print tema.find_all("ul")[0].find_all("li")[0].text#respuestas
            print tema.find_all("ul")[0].find_all("li")[1].text#visitas
            print tema.find_all("a")[2].text#creador
            print tema.find_all("a")[2].get("title").split(",")[1].replace(" el ","")#fecha
            print "*****************"
            print
            datosArray[0]=tema.find_all("a")[1].text
            datosArray[1]=tema.find_all("ul")[0].find_all("li")[0].text
            datosArray[2]=tema.find_all("ul")[0].find_all("li")[1].text
            datosArray[3]=tema.find_all("a")[2].text
            datosArray[4]=tema.find_all("a")[2].get("title").split(",")[1].replace(" el ","")
            datosArray[5]=enlace
        
        
            conn = sqlite3.connect(nombreDatabase)#conecta la base de datos
         
            conn.text_factory = str
            conn.execute("INSERT INTO TEMAS (TEMA,RESPUESTAS,VISITAS,CREADOR,FECHA,ENLACE) \
            VALUES (?,?,?,?,?,?)",(datosArray[0],datosArray[1],datosArray[2],datosArray[3],datosArray[4],datosArray[5]));
            conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM TEMAS")
    tkMessageBox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros") 
    cursor = conn.execute("SELECT ID,TEMA, CREADOR, FECHA from TEMAS")
    
    for row in cursor:
        print "ID = ", row[0]
        print "TEMA = ", row[1]
        print "CREADOR = ", row[2]
        print "FECHA = ", row[3], "\n"             
    conn.close()   
    print "datos extraidos correctamente" 
     

def crearDatabase(nombreDatabase):
    borrarDatabase(nombreDatabase)
    conn = sqlite3.connect(nombreDatabase)    
    print "Opened database successfully"; 
    #creando una tabla
    conn.text_factory = str
    conn.execute('''CREATE TABLE TEMAS
             (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
             TEMA           TEXT    NOT NULL,
             RESPUESTAS            TEXT     NOT NULL,
             VISITAS            TEXT     NOT NULL,
             CREADOR            TEXT     NOT NULL,
             FECHA            TEXT     NOT NULL,
             ENLACE         TEXT    NOT NULL);''')
    print "Table created successfully"; 
    
    conn.close()
    return conn



#enlace="https://foros.derecho.com/foro/20-Derecho-Civil-General"
#nombreDatabase="TEMAS.db"

#crearDatabase(nombreDatabase)    
#obtenDatosDePagina(enlace,nombreDatabase);

    