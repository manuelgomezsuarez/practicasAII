# -*- coding: utf-8 -*-
'''
Created on 20 oct. 2017

@author: admin
'''
import urllib
from bs4 import BeautifulSoup
import sqlite3 as sql
import tkMessageBox
import os
from Tkinter import *

def apartado1():
    try:

        conexion= urllib.urlretrieve("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp","sevillaGuia.txt")
        conexion.close()
    except:
        pass
    
    fichero=open("sevillaGuia.txt")
    texto=fichero.read()
    soup= BeautifulSoup(texto,"html.parser")
    os.remove("database.db")
    conn=sql.connect("database.db")
    try:
        conn.execute('''CREATE TABLE MENU
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             CATEGORIA           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             NOMBRE        TEXT    NOT NULL);''')
        conn.commit
    except:
        pass
        
    
    LinksCategorias=(soup.findAll(class_=["LinkIndice","TituloIndice"]))    
    for n in LinksCategorias:
    #     print(n.get("class")[0])
        
        if(str(n.get("class")[0])=="TituloIndice"):
            nuevaCategoria=unicode(n.string)
            print(nuevaCategoria)
        else:
            nombre=(n.string)
            link=(n.get("href"))
            conn.execute("INSERT INTO MENU (CATEGORIA,LINK,NOMBRE) \
               VALUES (?,?,?)",(nuevaCategoria,link,nombre));
            conn.commit
    
    cursor = conn.execute("SELECT COUNT(*) FROM MENU")
    tkMessageBox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
    print("base creada correctamente")


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


def imprimir_etiquetaArray(array):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in array:
        lb.insert(END,row)
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

def botonBuscarCategoria():
    def listar_busqueda(Event):
        conn = sql.connect('sevillaGuia.db')
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
    
def botonBuscarEventos():
    def listarBusquedaEventos(Event):
        fichero=open("sevillaGuia.txt")
        texto=fichero.read()
        soup= BeautifulSoup(texto,"html.parser")
        eventosFechas=(soup.findAll(class_=["Destacamos","Sala"]))   
        eventosFechasBonito=[]
        eventsResult=[]
        
        for n in eventosFechas:
            if(str(n.get("class")[0])=="Sala"):
                eventosFechasBonito.append(unicode(n.string))
#                 print(n.string)
            else:
#                 print(n.strong.string)
                eventosFechasBonito.append(unicode(n.strong.string))
        for p in range(1,len(eventosFechasBonito)-1):
            if E1.get() in eventosFechasBonito[p]:
                eventsResult.append(eventosFechasBonito[p-1])
                eventsResult.append(eventosFechasBonito[p])

                
                
        imprimir_etiquetaArray(eventsResult)
    v = Toplevel()
    lb = Label(v, text="Introduzca la categoria: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listarBusquedaEventos)
    E1.pack(side = LEFT)
    
        
def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Categorias", command = apartado1)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Buscar Categoria", command = botonBuscarCategoria)
    listar.pack(side = LEFT)
    
    listar = Button(top, text="Buscar Eventos", command = botonBuscarEventos)
    listar.pack(side = LEFT)
    #Buscar = Button(top, text="Buscar", command = buscar_bd)
    #Buscar.pack(side = LEFT)
    top.mainloop()
    
#capturaCodigo("sevillaGuia.txt", "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp");


ventana_principal()