# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''

import Funciones

from Tkinter import *
import sqlite3





def botonAlmacenarProductos():
    nombreDatabase="TEMAS.db"
    
    enlace="https://foros.derecho.com/foro/20-Derecho-Civil-General"
    Funciones.crearDatabase(nombreDatabase)
    Funciones.obtenDatosDePagina(enlace,nombreDatabase);
    
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
        cursor = conn.execute("""SELECT NOMBRE,PRECIO FROM CACTUS WHERE CATEGORIA LIKE ?""",(w.get(),)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        #conn.close()
    conn = sqlite3.connect('TEMAS.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT DISTINCT CATEGORIA FROM TEMAS """) # el distinct es para que coja un ejemplo de cada categoria
    categorias=[]
    for i in cursor:
        print i
        categorias.append(i[0])

    master = Toplevel()
    w = Spinbox(master,values=(categorias))
    w.pack(side = LEFT)
    w.bind("<Return>", botonIntroducirCategoria)
    
def listar_bd():
    conn = sqlite3.connect('TEMAS.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TEMA,CREADOR, FECHA FROM TEMAS")
    imprimir_etiqueta2(cursor)
    conn.close()
        
def imprimir_etiqueta2(cursor):
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
    
def listar_bdStats():
    conn = sqlite3.connect('TEMAS.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TEMA, CREADOR, FECHA, VISITAS FROM TEMAS ORDER BY VISITAS DESC")
    imprimir_etiquetaStats(cursor)
    conn.close()
        
def imprimir_etiquetaStats(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,row[3])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

def listar_bdRespuestas():
    conn = sqlite3.connect('TEMAS.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TEMA, CREADOR, FECHA, RESPUESTAS FROM TEMAS ORDER BY RESPUESTAS DESC")
    imprimir_etiquetaStats(cursor)
    conn.close()
        
def imprimir_etiquetaRespuestas(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,row[3])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)



def imprimir_etiquetaCreador(cursor):
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

    

    
def botonBuscarCreador():
    def listar_busqueda(Event):
       
        s = "%"+E1.get()+"%" 
        print s
        conn = sqlite3.connect('TEMAS.db')
        cursor = conn.execute("""SELECT DISTINCT TEMA,CREADOR,FECHA FROM TEMAS WHERE CREADOR LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiquetaCreador(cursor)

    v = Toplevel()
    lb = Label(v, text="Introduzca el evento: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listar_busqueda)
    E1.pack(side = LEFT)
    
def botonBuscarTema():
    def listar_busqueda(Event):
       
        s = "%"+E1.get()+"%" 
        print s
        conn = sqlite3.connect('TEMAS.db')
        cursor = conn.execute("""SELECT DISTINCT TEMA,CREADOR,FECHA FROM TEMAS WHERE TEMA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiquetaCreador(cursor)

    v = Toplevel()
    lb = Label(v, text="Introduzca el evento: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listar_busqueda)
    E1.pack(side = LEFT)
    
def botonBuscarFecha():
    def listar_busqueda(Event):
       
        s = "%"+E1.get()+"%" 
        print s
        conn = sqlite3.connect('TEMAS.db')
        cursor = conn.execute("""SELECT DISTINCT TEMA,CREADOR,FECHA FROM TEMAS WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiquetaCreador(cursor)

    v = Toplevel()
    lb = Label(v, text="Introduzca el evento: ")
    lb.pack(side = LEFT)
    E1 = Entry(v)
    E1.bind("<Return>", listar_busqueda)
    E1.pack(side = LEFT)
    
def salir():
    quit()
        
def ventanaPrincipal():
        
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    
    datosmenu = Menu(menu)
    menu.add_cascade(label="Datos", menu=datosmenu)
    datosmenu.add_command(label="Almacenar Temas", command=botonAlmacenarProductos)
    datosmenu.add_command(label="Mostrar", command=listar_bd)
    datosmenu.add_command(label="Salir Programa", command=root.quit)
    
    buscarmenu = Menu(menu)
    menu.add_cascade(label="Buscar", menu=buscarmenu)
    buscarmenu.add_command(label="Buscar Tema", command=botonBuscarTema)
    buscarmenu.add_command(label="Buscar Creador", command=botonBuscarCreador)
    buscarmenu.add_command(label="Buscar Fecha", command=botonBuscarFecha)
    
    estadisticasmenu = Menu(menu)
    menu.add_cascade(label="Buscar", menu=estadisticasmenu)
    estadisticasmenu.add_command(label="temas populares", command=listar_bdStats)
    estadisticasmenu.add_command(label="temas Activos", command=listar_bdRespuestas)
    
    
    mainloop()
    
#     top = Tk()
# 
# 
#     almacenar = Button(top, text="Almacenar Temas", command = botonAlmacenarProductos)
#     almacenar.pack(side = LEFT)
#    
#     buscarCategorias = Button(top, text="Mostrar Temas", command = listar_bd)
#     buscarCategorias.pack(side = LEFT)
#     
#     salida = Button(top, text="Salir Programa", command = salir)
#     salida.pack(side = LEFT)
# 
#     popular = Button(top, text="temas populares", command = listar_bdStats)
#     popular.pack(side = LEFT)
# 
#     
#     respuestas = Button(top, text="temas Activos", command = listar_bdRespuestas)
#     respuestas.pack(side = LEFT)
# 
#     
#     creador = Button(top, text="Buscar Creador", command = botonBuscarCreador)
#     creador.pack(side = LEFT)
#     
#     creador = Button(top, text="Buscar Fecha", command = botonBuscarFecha)
#     creador.pack(side = LEFT)
#     top.mainloop()

    


ventanaPrincipal()