# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''


import urllib2
import os

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