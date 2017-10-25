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
    
def obtenDatosDeFichero(nombreFichero):
    source= open(nombreFichero,"r").read()
    soup = BeautifulSoup(source, 'html.parser')
    linkApartados=soup.find_all(class_=["tree dhtml"])

    
    
    productos=[]
    #nos metemos en las categoria
    for apartado in linkApartados[0]:
        paginacionArray=[]
        paginacionArray.append(apartado.a.get("href"))
        
        datosCategoria = urllib2.urlopen(apartado.a.get("href")).read() #buscamos en cada categoria
        soup1 = BeautifulSoup(datosCategoria, 'html.parser')
        
        
        #iniciamos un bucle para la paginacion
        paginacion=soup1.find_all("ul",{"class":"pagination"}) 
        
        for pagina in paginacion: #metemos en un array todos las paginas de cada categoria

            for enlace in pagina.find_all('a'):
                if enlace.get("href") not in paginacionArray: #hacemos esto para que no meta varias veces la misma pagina
                    paginacionArray.append(enlace.get("href"))
               
        
        
        for pagina in paginacionArray: #para cada pagina de la categoria
            datosCategoria = urllib2.urlopen(pagina).read() #leemos el html porque cambia al pasar la pagina
            soup1 = BeautifulSoup(datosCategoria, 'html.parser')
            articulos=soup1.find_all(class_=["prod_wrap"]) #buscamos los objetos de la pagina
            print pagina
            for articulo in articulos: #por cada articulo
                
                producto=[0,0,0,0,0]
                linkNombrePrecio=articulo.find_all(class_=["prod_snimka","prod_name","product_preu","product_preu preu_reduit"])
                 
                producto[0]=apartado.a.string #categoria
                producto[1]=linkNombrePrecio[0].get("href") #link al producto
                producto[2]=linkNombrePrecio[1].a.string #nombre producto
                 
                precios=linkNombrePrecio[2].text.encode("utf-8").replace("€","").replace(",",".").split()
                if len(precios)==2:
                    producto[3]=precios[1]#precio final
                    producto[4]=int(100-((float(precios[1])*100)/float(precios[0]))) #descuento
                      
                else:
                    producto[3]=precios[0] #precio final
                    producto[4]=0 #descuento
                #print 
                productos.append(producto)
           
    print "datos extraidos correctamente" 
    return productos 

def crearDatabase(nombreDatabase,arrayDatos):
    borrarDatabase(nombreDatabase)
    conn = sqlite3.connect(nombreDatabase)    
    print "Opened database successfully"; 
    #creando una tabla
    conn.execute('''CREATE TABLE DELICATESSIN
             (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
             CATEGORIA           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             NOMBRE            TEXT     NOT NULL,
             PRECIO            REAL     NOT NULL,
             DESCUENTO         INTEGER    NOT NULL);''')
    print "Table created successfully"; 
    
    #introduciendo valores
    for i in arrayDatos:
        conn.execute("INSERT INTO DELICATESSIN (CATEGORIA,LINK,NOMBRE,PRECIO,DESCUENTO) \
        VALUES (?,?,?,?,?)",(i[0],i[1],i[2],i[3],i[4]));
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM DELICATESSIN")
    tkMessageBox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros") 
    conn.close()
    return conn





    


    