# -*- coding: utf-8 -*-
'''
Created on 13 oct. 2017

@author: admin
'''
import Tkinter as tk
import sqlite3
import feedparser
from pattern.web import Link


url="http://www.us.es/rss/feed/portada"
rss=feedparser.parse(url)
entradas=rss.entries

def almacenaNoticias():
    conn=sqlite3.connect("noticias")
    
    try:
        conn.execute('''CREATE TABLE NOTICIAS
             (ID INT PRIMARY KEY     NOT NULL,
             TITULO           TEXT    NOT NULL,
             LINK            TEXT     NOT NULL,
             FECHA        TEXT    NOT NULL);''')
        conn.commit()
        print "Table created successfully";
    except:
        print("Ya estaba creada la tabla")
        pass
    idNoticia=0
    for noticia in entradas:
        titulo=str(noticia.title.encode('utf-8'))
        link=str(noticia.link.encode('utf-8'))
        fecha=str(noticia.published_parsed[2])+"/" +str(noticia.published_parsed[1])+"/" +str(noticia.published_parsed[0])
        conn.execute("INSERT INTO NOTICIAS (ID,TITULO,LINK,FECHA) \
           VALUES ("+str(idNoticia)+",'"+titulo+"','"+link+"' ,'"+fecha+"')");
        conn.commit  
        

#         print(titulo)
#         print(link)
#         print(fecha)
#         print(idNoticia)
        idNoticia+=1
    print("Noticias guardadas correctamente")


ventana = tk.Tk()

button_frame = tk.Frame(ventana)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

b1 = tk.Button(button_frame, text='Almacenar',command=almacenaNoticias)
b2 = tk.Button(button_frame, text='Listar')
b3 = tk.Button(button_frame, text='Buscar')

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

b1.grid(row=0, column=0, sticky=tk.W+tk.E)
b2.grid(row=0, column=1, sticky=tk.W+tk.E)
b3.grid(row=0,column=2,sticky=tk.W+tk.E)
ventana.mainloop()