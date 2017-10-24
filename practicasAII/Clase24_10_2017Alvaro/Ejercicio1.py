# -*- coding: utf-8 -*-
'''
Created on 24 oct. 2017

@author: Garbancito
'''
import urllib2
import Funciones
from bs4 import BeautifulSoup


nombreFichero="delicatessin.txt"

#Funciones.capturaCodigo(nombreFichero, "http://www.delicatessin.com/es/Delicatessin")

def obtenDatosDeFichero(nombreFichero):
    source= open(nombreFichero,"r").read()
    soup = BeautifulSoup(source, 'html.parser')
    linkApartados=soup.find_all(class_=["tree dhtml"])
    
#     for apartado in linkApartados[0]:
#         datosCategoria = urllib2.urlopen(apartado.a.get("href")).read()
#         articulos=soup.find_all(class_=["item"])
#         for articulo in articulos:
#             print articulo
        #print apartado.a.get("href")
        #print apartado.a.string
    
    articulo=[]
    articulos=[]
    #nos metemos en las categoria
    for apartado in linkApartados[0]:
        datosCategoria = urllib2.urlopen(apartado.a.get("href")).read() #buscamos en cada categoria
        soup1 = BeautifulSoup(datosCategoria, 'html.parser')
        articulos=soup1.find_all(class_=["prod_wrap"]) #buscamos los objetos de la pagina
        
        for articulo in articulos: #por cada articulo
            linkNombrePrecio=articulo.find_all(class_=["prod_snimka","prod_name","product_preu","product_preu preu_reduit"])
            
            #categoria,link,nombre,precioFinal,descuento
            print apartado.a.string
            print linkNombrePrecio[0].get("href")
            print linkNombrePrecio[1].a.string
            precios=linkNombrePrecio[2].text.encode("utf-8").replace("€","").replace(",",".").split()
            if len(precios)==2:
                print precios[1]
                print("Descuento:")
                print int(100-((float(precios[1])*100)/float(precios[0])))
                print 
            else:
                print precios[0]
            print 
          
           
          
        
obtenDatosDeFichero(nombreFichero)