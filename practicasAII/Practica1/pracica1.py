# -*- coding: utf-8 -*-
'''
Created on 13 oct. 2017

@author: admin
'''
import Tkinter as tk
from Tkinter import  *
import sqlite3
import feedparser
from ScrolledText import *


url="http://www.us.es/rss/feed/portada"
rss=feedparser.parse(url)
entradas=rss.entries

def pueblaBaseDatos(conn):
    for noticia in entradas:
        titulo=str(noticia.title.encode('utf-8'))
        link=str(noticia.link.encode('utf-8'))
        fecha=str(noticia.published_parsed[2])+"/" +str(noticia.published_parsed[1])+"/" +str(noticia.published_parsed[0])
        conn.execute("INSERT INTO NOTICIAS (TITULO,LINK,FECHA) VALUES ('"+titulo+"','"+link+"' ,'"+fecha+"')");
    conn.commit()
def almacenaNoticias():
    
    conn=sqlite3.connect("noticias.sqlite3")
    
    try:
        conn.execute('''CREATE TABLE NOTICIAS
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             TITULO           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             FECHA        TEXT    NOT NULL);''')
        conn.commit()
        print "Table created successfully";
    except:
        print("Ya estaba creada la tabla")
        pass
    pueblaBaseDatos(conn)
    texto="BD creada correctamente"
    v=tk.Tk()
    mensaje=tk.Message(v,text=texto,width=150)
    mensaje.pack()
    v.mainloop()

def listaNoticias():
    conn=sqlite3.connect("noticias.sqlite3")
    c=conn.cursor()
    noticias=""
    for n in c.execute("SELECT * FROM NOTICIAS"):
        noticias+=n[1]+" \n"+n[2]+"\n"+n[3]+"\n\n"
    
    v=tk.Tk()
    mensaje = ScrolledText(v, width=150, height=40)
    mensaje.insert(INSERT, noticias)
    mensaje.insert(END,"Fin")
    mensaje.pack()
    v.mainloop()
    
    
    
ventana = tk.Tk()

button_frame = tk.Frame(ventana)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

b1 = tk.Button(button_frame, text='Almacenar',command=almacenaNoticias)

b2 = tk.Button(button_frame, text='Listar',command=listaNoticias)
b3 = tk.Button(button_frame, text='Buscar')

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

b1.grid(row=0, column=0, sticky=tk.W+tk.E)
b2.grid(row=0, column=1, sticky=tk.W+tk.E)
b3.grid(row=0,column=2,sticky=tk.W+tk.E)
ventana.mainloop()




