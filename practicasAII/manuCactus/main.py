# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2017

@author: admin
'''
import funciones
from Tkinter import *
import sqlite3
import tkMessageBox



nombreDatabase="database.db"

funciones.borrarDatabase(nombreDatabase)
conn = sqlite3.connect(nombreDatabase) 
conn.text_factory = str
conn.execute('''CREATE TABLE CACTUS
             (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
             CATEGORIA           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             PRECIO            TEXT    );''')
print "Table created successfully"; 

categorias,nombresCategorias=funciones.obtenUrlCategorias()
print(len(categorias))
print(len(nombresCategorias))
for n in range(0,len(categorias)):
    paginas=funciones.obtenPaginasCategoria(categorias[n])
    for p in paginas:
        url,precio=funciones.obtenProductosCategoria(p)
        for b in range(0,len(url)):
            print(nombresCategorias[n])
            print(url[b])
            print(precio[b])
            conn.execute("INSERT INTO CACTUS (CATEGORIA,LINK,PRECIO) \
            VALUES (?,?,?)",(nombresCategorias[n],url[b],precio[b]));
    conn.commit()
cursor = conn.execute("SELECT COUNT(*) FROM CACTUS")
tkMessageBox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros") 


