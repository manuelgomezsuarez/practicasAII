# -*- coding: utf-8 -*-
'''
Created on 20 oct. 2017

@author: Garbancito
'''
import urllib2
from bs4 import BeautifulSoup

import sqlite3
import os
import tkMessageBox
from Tkinter import *

def capturaCodigo(nombreFichero,rss):
    """nombre del txt donde se guardara y rss de la pagina """
    try:
        source = urllib2.urlopen(rss).read()
        f = open(nombreFichero, "w")
        f.write(source)
        f.close()    
    except miError, e:
        print "Ocurrió un error"
        print e
        
class miError(Exception):
    def __init__(self, valor):
        self.valor = valor
    def __str__(self):
        return "Error " + str(self.valor)
    
def obtenDatosDeFichero(nombreFichero):
    source= open(nombreFichero,"r").read()
    soup = BeautifulSoup(source, 'html.parser')
    linkApartados=soup.find_all(class_=["LinkIndice","TituloIndice"])
    subArrayInformacion=[]
    arrayInformacion=[]
    for a in linkApartados:

        if(a.get("class")[0]=="TituloIndice"):     
            subArrayInformacion=[]
            categoria=unicode(a.string)
            
        else:
            subArrayInformacion.append(categoria)
            subArrayInformacion.append(unicode(a.string))
            subArrayInformacion.append(a.get("href"))
            arrayInformacion.append(subArrayInformacion)
    
    return arrayInformacion

def crearDatabase(nombreDatabase,arrayDatos):
    conn = sqlite3.connect(nombreDatabase)    
    print "Opened database successfully"; 
    #creando una tabla
    conn.execute('''CREATE TABLE SEVILLAGUIA
             (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
             CATEGORIA           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             NOMBRE         TEXT    NOT NULL);''')
    print "Table created successfully"; 
    
    #introduciendo valores
    for i in arrayDatos:
        conn.execute("INSERT INTO SEVILLAGUIA (CATEGORIA,NOMBRE,LINK) \
        VALUES (?,?,?)",(i[0],i[1],i[2]));
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM SEVILLAGUIA")
    tkMessageBox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros") 
    conn.close()
    return conn


    
def borrarDatabase(nombreDatabase):
    try:
        os.remove(nombreDatabase)
    except:
        pass

def bottonAlmacenarBd():
    borrarDatabase("sevillaGuia.db")
    crearDatabase("sevillaGuia.db", obtenDatosDeFichero("sevillaGuia.txt"))
    print "DB creada correctamente"


def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)


def buttonBuscarCategoria():
    def listar_busqueda(Event):
        conn = sqlite3.connect('sevillaGuia.db')
        conn.text_factory = str
        s = "%"+E1.get()+"%" 
        print s
        cursor = conn.execute("""SELECT CATEGORIA,NOMBRE,LINK FROM SEVILLAGUIA WHERE CATEGORIA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca la categoria: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listar_busqueda)
    E1.pack(side = LEFT)
    
def buttonBuscarEvento():
    def listar_busqueda(Event):
       
        s = E1.get()
        print s
        source= open("sevillaGuia.txt","r").read()
        soup = BeautifulSoup(source, 'html.parser')
        eventos=[]
        subEventos=[]
        for i in soup.find_all(class_=["Destacamos","Sala"]):
            if (i.get("class")[0]=="Sala"):
                
                subEventos.append(unicode(i.string))   
                
               
            elif(i.get("class")[0]=="Destacamos"):
                
                if(i.strong.string!=None):
                    subEventos.append(unicode(i.strong.string))
                    subEventos.append(unicode(i.text))
                    
                if len(subEventos)==3:
                    eventos.append(subEventos)
                subEventos=[]
               
                    
                
        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        
        for i in eventos:
            if s in i[2]:
        
                lb.insert(END,i[0])
                lb.insert(END,i[1])
                lb.insert(END,'')
        lb.pack(side = LEFT, fill = BOTH)
        sc.config(command = lb.yview)
        #print(linkApartados[0].strong.string)
        
           

           
            
    
    v = Toplevel()
    lb = Label(v, text="Introduzca el evento: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listar_busqueda)
    E1.pack(side = LEFT)
    
    
def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Categorias", command = bottonAlmacenarBd)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Buscar Categoria", command = buttonBuscarCategoria)
    listar.pack(side = LEFT)
    Buscar = Button(top, text="BuscarEvento", command = buttonBuscarEvento)
    Buscar.pack(side = LEFT)
    top.mainloop()
    
#capturaCodigo("sevillaGuia.txt", "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp");


ventana_principal()



