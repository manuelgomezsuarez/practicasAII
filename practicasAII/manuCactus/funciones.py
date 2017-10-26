# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import os
import sqlite3
import tkMessageBox
'''
Created on 26 oct. 2017

@author: admin
'''

def obtenUrlCategorias():
    url="http://latiendadelcactus.es/la-tienda/manufacturer/?categorylayout=0&showcategory=1&showproducts=1&productsublayout=0&latest=0&topten=0&recent=0"
    source = urllib2.urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')
    categorias=soup.find_all(class_=["cat-title"])
    urlCategorias=[]
    nombreCategorias=[]
    for n in categorias:
        urlCategorias.append(url+"/"+n.string.replace(" ","-").encode("utf-8"))
        nombreCategorias.append(n.string.encode("utf8"))
    return urlCategorias,nombreCategorias

def obtenProductosCategoria(urlCategoria):
    url=urlCategoria
    source = urllib2.urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')
    linksProductos=soup.find_all(class_=["spacer-handler"])
    soupPrecios=soup.find_all(class_=["PricesalesPrice"])
    precios=[]
    urlProductos=[]
    for n in linksProductos:
        urlProductos.append(n.a.get("href"))
    for n in range(len(soupPrecios)):
        if  (n%2):
            precios.append(soupPrecios[n].string)
    return urlProductos,precios

def obtenPaginasCategoria(urlCategoria):
    url=urlCategoria
    source = urllib2.urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')
    paginas=soup.findAll("a",attrs={"class":"pagenav"})
    urlPaginas=[]
    for n in paginas:
        if (urlCategoria+"/"+n.get("href").encode("utf-8") not in urlPaginas):
            urlPaginas.append(urlCategoria+"/"+n.get("href").encode("utf-8"))
    return urlPaginas    



def borrarDatabase(nombreDatabase):
    try:
        os.remove(nombreDatabase)
    except:
        pass


