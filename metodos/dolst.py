import os
import math

import numpy as np
from numpy import random
from mutagen.wave import WAVE
from mutagen.mp3 import MP3


def dolst(pausas, programas, fecha):
    texttoreturn=[]
    cortesmadrugada = []
    raiz = 'y/'
    for x in [00, 0o1, 0o2, 0o3, 0o4, 0o5]:  # hace los cortes de madrugada
        for y in [00, 15, 30, 45]:
            cortesmadrugada.append([str((x + (y / 60)) / 24), '0', '0', '0', '0', '0'])
    pausas = np.concatenate((pausas, cortesmadrugada[1:]))
    with open(fecha + '.lst', 'w') as fp:
        fp.write('500\n')
    while len(programas) > 0:
        pausas = printprogrma(fecha, raiz, programas[0:2], pausas, texttoreturn)
        programas = programas[2:]
    return texttoreturn


def printprogrma(fecha, raiz, programa, pausas, texttoreturn):
    dia, mes, ano = getdiamesano(fecha)
    if len(dia) == 1:
        dia = '0' + dia
    nombredeprograma = programa[0, 1]
    horainicial = programa[0, 0]
    horafinal = programa[-1, 0]
    duracionprograma = decimalaminutos(horafinal - horainicial)
    numerodecortes = int((duracionprograma - 2) / 15)
    numbloques = numerodecortes + 1
    bloques = 'a'
    cortesrequeridos = numerodecortes
    dirpath = 'a'
    archivodeprograma = 'a'
    archivodemes = 'a'
    carpeta = 'a'
    print(programa)
    if 'GRABADO' in programa[0, 4]:
        archivodeprogramas = raiz + 'Programas/'
        for x in os.listdir(archivodeprogramas):
            if nombredeprograma in x:
                archivodeprograma = x
        if archivodeprograma == 'a':
            texttoreturn.append('no hay carpeta de ' + programa[0, 1])
        else:
            archivodemeses = archivodeprogramas + archivodeprograma + '/'
            for x in os.listdir(archivodemeses):
                if mes + ' ' + ano in x:
                    archivodemes = x
            if archivodemes == 'a':
                texttoreturn.append('no hay carpeta de ' + programa[0, 1] + ' del mes ' + mes + ' ' + ano)
            else:
                suprapath = archivodemeses + archivodemes + '/'
                suprafiles = os.listdir(suprapath)
                for x in suprafiles:
                    if dia in x:
                        carpeta = x
                if carpeta == 'a':
                    texttoreturn.append('no hay carpeta de ' + programa[0, 1] + ' del dia ' + dia + ' ' + mes)
                else:
                    dirpath = suprapath + carpeta + '/'
                    bloques = os.listdir(dirpath)
                    if len(bloques) == 0:
                        texttoreturn.append('no hay bloques de ' + programa[0, 1] + ' del dia ' + dia + ' ' + mes)
                    else:
                        numbloques = len(bloques)
                        cortesrequeridos = len(bloques) - 1
                        claves = []
                        horas = []
                        newcortes = []
        if cortesrequeridos < numerodecortes:
            for i in range(numerodecortes + 1):
                corte = pausas[0, 1:]
                horas.append(pausas[0, 0])
                for clave in corte:
                    if clave != '0' and clave != 'P0' and clave != 'F0' and clave != '10' and clave != 'PP0' and clave \
                            != 'INE0' and clave != 'FE0' and clave != 'CO0' and clave != 'IN0' and clave != 'PR0':
                        claves.append(clave)
                pausas = pausas[1:]
            numerodecortes = numerodecortes - 1
            if len(claves) % len(pausas[0, 1:]) != 0:
                while len(claves) % len(pausas[0, 1:]) != 0:
                    claves.append('0')
            for x in range(cortesrequeridos+1):
                if 5 != len(claves[5*x:5*(1+x)]):
                    while 5 != len(claves[5*x:5*(1+x)]):
                        claves.append('0')
                newcortes.append([*[float(horas[-cortesrequeridos-1+x])], *claves[5*x:5*(1+x)]])
            b = np.r_[newcortes, pausas]
            pausas = np.array(b)
        if numbloques == 1:
            if bloques != 'a':
                duracion = getlen(dirpath + bloques[0])
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[0]).replace('/', '\\')))
            if not programa[1, 0] == 0.998611111111111:
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]
        else:
            if bloques != 'a':
                bloques.sort()
            for x in range(0, numbloques):
                if bloques != 'a':
                    duracion = getlen(dirpath + bloques[x])
                    with open(fecha + '.lst', 'a') as fp:
                        fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[x]).replace('/', '\\')))
                if not programa[1, 0] == 0.998611111111111:
                    printcorte(fecha, raiz, pausas[0])
                    pausas = pausas[1:]
    elif programa[0, 4] == 'VIVO' and not programa[0, 1] == 'LA MAÑANERA AMLO':
        suprapath = raiz + 'INSTITUCIONAL/VESTIDURAS/'
        suprafolders = os.listdir(suprapath)
        nombredecarpeta = ''
        for x in suprafolders:
            if nombredeprograma in x:
                nombredecarpeta = x
        dirpath = raiz + 'INSTITUCIONAL/VESTIDURAS/' + nombredecarpeta + '/'
        vestiduras = os.listdir(dirpath)
        ENTRADA = ''
        SALIDA = ''
        ROMPE = ''
        IDA = ''
        REGRESO = ''
        for x in vestiduras:
            if 'ENTRADA' in x.upper():
                ENTRADA = x
                break
        for x in vestiduras:
            if 'SALIDA' in x.upper():
                SALIDA = x
                break
        for x in vestiduras:
            if 'REGRESO' in x.upper():
                REGRESO = x
                break
        for x in vestiduras:
            if ('IDA ' in x.upper()) and not ('SALIDA' in x.upper()):
                IDA = x
                break
        if len(IDA) == 0 and len(REGRESO) == 0:
            for x in vestiduras:
                if 'ROMPE' in x.upper():
                    ROMPE = x
                    break
        if IDA == '':
            IDA = ROMPE
        if REGRESO == '':
            REGRESO = ROMPE
        for x in range(numerodecortes + 1):
            if x == 0 and not ENTRADA == '':
                duracion = getlen(dirpath + ENTRADA)
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + ENTRADA).replace('/', '\\')))
            elif not x == 0 and not REGRESO == '':
                duracion = getlen(dirpath + REGRESO)
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + REGRESO).replace('/', '\\')))
            with open(fecha + '.lst', 'a') as fp:
                fp.write("%s\t%s\n" % ('-1', '.stop'))
            if not x == numerodecortes and not IDA == '':
                duracion = getlen(dirpath + IDA)
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + IDA).replace('/', '\\')))
            elif x == numerodecortes and not SALIDA == '':
                duracion = getlen(dirpath + SALIDA)
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + SALIDA).replace('/', '\\')))
            if not programa[1, 0] == 0.998611111111111:
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]
    elif 'HIMNO' in programa[0, 4]:
        printhimno(fecha, raiz)
        printcorte(fecha, raiz, pausas[0])
        pausas = pausas[1:]
    elif programa[0, 1] == 'LA MAÑANERA AMLO':
        pausaespecial1 = np.concatenate((pausas[0], pausas[1, 1:], pausas[2, 1:], pausas[3, 1:]))
        printcorte(fecha, raiz, pausaespecial1)
        with open(fecha + '.lst', 'a') as fp:
            fp.write("%s\t%s\n" % ('-1', '.stop'))
        pausas = pausas[4:]
        pausaespecial2 = np.concatenate(([pausas[3, 0]], pausas[0, 1:], pausas[1, 1:], pausas[2, 1:], pausas[3, 1:]))
        printcorte(fecha, raiz, pausaespecial2)
        pausas = pausas[4:]
    elif programa[0, 4] == 'MUSICA' and programa[0, 5] == 'ARBOL DE MUSICA':
        for x in range(numerodecortes + 1):
            if not programa[1, 0] == 0.998611111111111 and not len(pausas) == 0:
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]
    elif 'CARPETA' in programa[0, 4]:
        for x in range(0, numerodecortes + 1):
            if not (programa[1, 0] == 0.998611111111111 and x == 3):
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]
    elif programa[0, 4] == 'MUSICA SELECCIONADA':
        if programa[0, 1] == 'MUSICA RESISTENCIA':
            dirpath = raiz + 'Programas/' + nombredeprograma + '/' + mes + ' ' + ano + '/' + dia + ' ' + mes + '/'
            rolas = os.listdir(dirpath)
            rolas.sort()
            rompecorte = raiz + 'INSTITUCIONAL/VESTIDURAS/' + nombredeprograma + '/' + \
                         'ROMPE CORTE  LA HISTORIA DE LA RESISTENECIA.mp3'
            duracionrompe = getlen(rompecorte)
            rolasporcorte = int(len(rolas) / 4)
            sobrante = len(rolas) % 3
            n = 0
            for x in range(numerodecortes + 1):
                numrolas = rolasporcorte
                if sobrante > 0:
                    numrolas = numrolas + 1
                    sobrante = sobrante - 1
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracionrompe, rompecorte.replace('/', '\\')))
                for y in range(numrolas):
                    duracion = getlen(dirpath + rolas[n])
                    with open(fecha + '.lst', 'a') as fp:
                        fp.write("%s\t%s\n" % (duracion, (dirpath + rolas[n]).replace('/', '\\')))
                        n = n + 1
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracionrompe, rompecorte.replace('/', '\\')))
                if not (programa[1, 0] == 0.998611111111111 and x == 3):
                    printcorte(fecha, raiz, pausas[0])
                    pausas = pausas[1:]
        if programa[0, 1] == 'Y YO QUE TENGO QUE VER CON':
            suprapath = raiz + 'Programas/' + nombredeprograma + '/' + mes + ' ' + ano + '/'
            suprafiles = os.listdir(suprapath)
            carpeta = ''
            for x in suprafiles:
                if dia in x:
                    carpeta = x
            dirpath = raiz + 'Programas/' + nombredeprograma + '/' + mes + ' ' + ano + '/' + carpeta + '/'
            rolas = os.listdir(dirpath)
            rolas.sort()
            rolasporcorte = int(len(rolas) / (numerodecortes + 1))
            sobrante = len(rolas) % (numerodecortes + 1)
            n = 0
            for x in range(numerodecortes + 1):
                numrolas = rolasporcorte
                if sobrante > 0:
                    numrolas = numrolas + 1
                    sobrante = sobrante - 1
                for y in range(numrolas):
                    duracion = getlen(dirpath + rolas[n])
                    with open(fecha + '.lst', 'a') as fp:
                        fp.write("%s\t%s\n" % (duracion, (dirpath + rolas[n]).replace('/', '\\')))
                        n = n + 1
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]

    return pausas


def getdiamesano(fecha):
    meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMRE', 'OCTUBRE',
             'NOVIEMBRE', 'DICIEMBRE']
    mes = '0'
    ano = fecha[-4:]
    for x in meses:
        if x in fecha:
            mes = x
            break
    dia = fecha[-len(ano) - len(mes) - 2:-len(ano) - len(mes)]
    if not dia.isnumeric():
        dia = dia[-1]
    return dia, mes, ano


def printcorte(fecha, raiz, pausa):
    dirpath = 'y/INSTITUCIONAL/LISTAS/Horas'
    subtring = formatinghora(pausa[0])
    stringtoprint = dirpath.replace('/', '\\') + '\\' + buscararchivo(dirpath, subtring)
    with open(fecha + '.lst', 'a') as fp:
        fp.write("0\t%s\n" % stringtoprint)
    path = raiz + 'INSTITUCIONAL/IMAGEN SONORA 2022/IDENTIFICADORES 2022/'
    x = random.randint(len(os.listdir(path)))
    duracion = getlen(path + os.listdir(path)[x])
    with open(fecha + '.lst', 'a') as fp:
        fp.write("%s\t%s\n" % (duracion, (path + os.listdir(path)[x]).replace('/', '\\')))
        fp.write("-1\t.time\n")
    n = 0
    for clave in pausa[1:]:
        if clave != '0' and clave != 'P0' and clave != 'F0' and clave != '10' and clave != 'PP0' and clave \
                != 'INE0' and clave != 'FE0' and clave != 'CO0' and clave != 'IN0' and clave != 'PR0':
            path = raiz + 'COMERCIALIZACION/'
            if 'PP' in clave:
                n = n + 1
                path = path + 'INE - PP/PP/'
                clave = clave + ' '
                for filename in os.listdir(path):
                    if clave in filename:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
            elif 'IN' in clave:
                n = n + 1
                path = path + 'INE - PP/INE/'
                clave = clave + ' '
                for filename in os.listdir(path):
                    if clave in filename:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
            elif 'FE' in clave:
                n = n + 1
                path = path + 'FEDERALES/'
                if len(clave) < 4:
                    clave = clave[:2] + '0' + clave[2]
                clave = clave + ' '
                for filename in os.listdir(path):
                    if clave in filename:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
            elif 'CO' in clave[0:3]:
                n = n + 1
                path = path + 'COM/'
                clave = clave + ' '
                for filename in os.listdir(path):
                    if clave in filename:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
            elif 'RTC' in clave:
                n = n + 1
                path = path + 'RTC 5MIN/'
                clave = clave[-2:].replace(' ', '')
                clave = '0' + clave + ' '
                for filename in os.listdir(path):
                    if clave in filename[0:4]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
            elif 'PR' in clave:
                n = n + 1
                path = path + 'Promos/'
                for filename in os.listdir(path):
                    if clave + ' ' in filename:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
    if n == 0:
        path = raiz + 'COMERCIALIZACION/Promos/'
        x = random.randint(len(os.listdir(path)))
        if os.listdir(path)[x][0] != 'P':
            while os.listdir(path)[x][0] != 'P':
                x = random.randint(len(os.listdir(path)))
        duracion = getlen(path + os.listdir(path)[x])
        with open(fecha + '.lst', 'a') as fp:
            fp.write("%s\t%s\n" % (duracion, (path + os.listdir(path)[x]).replace('/', '\\')))
    path = raiz + 'INSTITUCIONAL/IMAGEN SONORA 2022/'
    x = random.randint(len(os.listdir(path)))
    filename = os.listdir(path)[x]
    if os.path.isfile(path + filename) != 1:
        while os.path.isfile(path + filename) != 1:
            x = random.randint(len(os.listdir(path)))
            filename = os.listdir(path)[x]
    duracion = getlen(path + os.listdir(path)[x])
    with open(fecha + '.lst', 'a') as fp:
        fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))


def printhimno(fecha, raiz):
    with open(fecha + '.lst', 'a') as fp:
        filepath = raiz + 'HIMNO NACIONAL/'
        filename = 'HIMNO NACIONAL CORTO.mp3'
        duracion = getlen(filepath + filename)
        fp.write("%s\t%s\n" % (duracion, (filepath + filename).replace('/', '\\')))
        return 0


def formatinghora(h):
    parte_decimal, parte_entera = math.modf(float(h) * 24)

    parte_decimal = str(round(parte_decimal * 60))
    parte_entera = str(int(parte_entera))
    if len(parte_decimal) < 2:
        parte_decimal = parte_decimal + '0'
    if len(parte_entera) < 2:
        parte_entera = '0' + parte_entera
    h = parte_entera + '-' + parte_decimal
    return h


def buscararchivo(dirpath, x):
    for filename in os.listdir(dirpath):
        if x in filename:
            return filename
    # print(os.path.isdir(dirpath))
    return 0


def getlen(filename):
    audio = 0
    if filename[-3:] == 'mp3':
        audio = MP3(filename)
    elif filename[-3:] == 'wav':
        audio = WAVE(filename)
    return int(audio.info.length * 1000)


def decimalaminutos(time):
    return round(time * 24 * 60)
