# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''

import Funciones
from Tkinter import *
import sqlite3

nombreFichero="delicatessin.txt"
nombreDatabase="DELICATESSIN.db"


def botonAlmacenarProductos():
    Funciones.crearDatabase("DELICATESSIN.db", Funciones.obtenDatosDeFichero("delicatessin.txt"))
    print "DB creada correctamente"
    

def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        
        
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)



    
def botonMostrarListaCategoria():
    def botonIntroducirCategoria(Event):
        print w.get()
        cursor = conn.execute("""SELECT NOMBRE,PRECIO FROM DELICATESSIN WHERE CATEGORIA LIKE ?""",(w.get(),)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        #conn.close()
    conn = sqlite3.connect('DELICATESSIN.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT DISTINCT CATEGORIA FROM DELICATESSIN """) # el distinct es para que coja un ejemplo de cada categoria
    categorias=[]
    for i in cursor:
        categorias.append(i[0])
    master = Toplevel()
    w = Spinbox(master,values=(categorias))
    w.pack(side = LEFT)
    w.bind("<Return>", botonIntroducirCategoria)

def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Productos", command = botonAlmacenarProductos)
    almacenar.pack(side = LEFT)
   
    buscarCategorias = Button(top, text="Mostrar Categoria", command = botonMostrarListaCategoria)
    buscarCategorias.pack(side = LEFT)

    top.mainloop()
    

        

ventanaPrincipal()
