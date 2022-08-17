#!/usr/bin/env python
import re
from itertools import zip_longest
from xml.sax.saxutils import prepare_input_source
#patron = r"ticky: ERROR: ([\w ]* (\w) *)"
patronE = r"ticky: ERROR ([\w ]*)"
patronI = r"ticky: INFO ([\w [#\]]*)"
nombre = r"\(([\w.]*)\)"
error = []
userE = []
userI = []
user = []
info = []

countE = 0
countI = 0

per_user = {'name': 'Username', 'info': 'INFO', 'error': 'ERRO'}

with open("/Users/jesus/SCRIPTS/PYTHON/LEARN_2022/syslog.log", "r") as f:
    for i in f:
        linea = i.strip()
        #print("Esta es una linea {}".format(linea))
        respuestaE = re.search(patronE     , linea)
        if(respuestaE is not None):
            error.append(respuestaE[1])
            countE =+ 1
            respuestaN = re.search(nombre, linea)
            if(respuestaN is not None):
                userE.append(respuestaN[1])

        respuestaI = re.search(patronI, linea)
        if(respuestaI is not None):
            #print(respuestaI[0])
            info.append(respuestaI[1])
            countI =+ 1
            respuestaN = re.search(nombre, linea)
            if(respuestaN is not None):
                userI.append(respuestaN[1])
        respuesta = re.search(nombre, linea) 
        if(respuesta is not None):
                user.append(respuesta[1])    
        countE = 0
        countI = 0 

        #per_user = {'Username' : paths, 'usage: ' : usage}

ERRORES =  (dict( (l, error.count(l) ) for l in set(error)))
dicE = (dict( (l, userE.count(l) ) for l in set(userE)))
dicI = (dict( (l, userI.count(l) ) for l in set(userI)))


with open('error_message.csv', 'w+') as f:
    f.write("Error, Count\n")
    for i in ERRORES:
        f.write("{}, {} \n".format(i,ERRORES[i]))

USUARIOS = set(user)
USUARIOS2 = sorted(USUARIOS)
print(dicE)

with open('user_statistics.csv', 'w+') as f:
    f.write("Username, INFO, ERROR \n")
    for i in USUARIOS2:
        try:
            errores = dicE[i]
        except:
            errores = 0
        try:
            info = dicI[i]
        except:
            info = 0
        f.write("{}, {}, {} \n".format(i, errores, info))