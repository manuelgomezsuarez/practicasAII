# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''

import Funciones
from Tkinter import *

nombreFichero="delicatessin.txt"
nombreDatabase="DELICATESSIN.db"


def ventanaPrincipal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Productos", command = Funciones.botonAlmacenarProductos)
    almacenar.pack(side = LEFT)
   
    buscarCategorias = Button(top, text="Mostrar Categoria", command = Funciones.botonMostrarListaCategoria)
    buscarCategorias.pack(side = LEFT)

    top.mainloop()
    

        

ventanaPrincipal()
