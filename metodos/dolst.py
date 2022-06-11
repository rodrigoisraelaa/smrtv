import os
import math

import numpy as np
from numpy import random
from mutagen.wave import WAVE
from mutagen.mp3 import MP3


def dolst(pausas, programas, fecha):
    cortesmadrugada = []
    raiz = 'y/'
    for x in [00, 0o1, 0o2, 0o3, 0o4, 0o5]:  # hace los cortes de madrugada
        for y in [00, 15, 30, 45]:
            cortesmadrugada.append([str((x + (y / 60)) / 24), '0', '0', '0', '0', '0'])
    pausas = np.concatenate((pausas, cortesmadrugada[1:]))
    with open(fecha + '.lst', 'w') as fp:
        fp.write('500\n')
    while len(programas) > 0:
        pausas = printprogrma(fecha, raiz, programas[0:2], pausas)
        programas = programas[2:]
    return 0


def printprogrma(fecha, raiz, programa, pausas):
    dia, mes, ano = getdiamesano(fecha)
    nombredeprograma = programa[0, 1]
    horainicial = programa[0, 0]
    horafinal = programa[-1, 0]
    duracionprograma = decimalaminutos(horafinal - horainicial)
    numerodecortes = int((duracionprograma - 2) / 15)
    dirpath = ''
    if programa[0, 4] == 'GRABADO':
        dirpath = raiz + 'Programas/' + nombredeprograma + '/' + mes + ' ' + ano + '/' + dia + ' ' + mes + '/'
        bloques = os.listdir(dirpath)
        cortesrequeridos = len(bloques) - 1
        claves = ['0']
        while cortesrequeridos < numerodecortes:
            for i in range(2):
                for clave in pausas[i, 1:]:
                    if clave != '0' and clave != 'P0' and clave != 'F0' and clave != '10' and clave != 'PP0' and clave \
                            != 'INE0' and clave != 'FE0' and clave != 'CO0' and clave != 'IN0' and clave != 'PR0':
                        claves.append(clave)
            pausas = pausas[1:]
            numerodecortes = numerodecortes - 1
            if len(claves) < len(pausas[0, 1:]):
                while len(claves) < len(pausas[0, 1:]):
                    claves.append('0')
            pausas[0, 1:] = claves
        if len(bloques) == 1:
            duracion = getlen(dirpath + bloques[0])
            with open(fecha + '.lst', 'a') as fp:
                fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[0]).replace('/', '\\')))
            if not programa[1, 0] == 0.998611111111111:
                printcorte(fecha, raiz, pausas[0])
                pausas = pausas[1:]
        elif len(bloques) == 0:
            print('no hay bloques')
        else:
            bloques.sort()
            for x in range(0, numerodecortes + 1):
                duracion = getlen(dirpath + bloques[x])
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[x]).replace('/', '\\')))
                if not programa[1, 0] == 0.998611111111111:
                    printcorte(fecha, raiz, pausas[0])
                    pausas = pausas[1:]
    elif programa[0, 4] == 'VIVO' and not programa[0, 1] == 'LA MAÑANERA AMLO':
        dirpath = raiz + 'INSTITUCIONAL/VESTIDURAS/' + nombredeprograma + '/'
        vestiduras = os.listdir(dirpath)
        ENTRADA = ''
        SALIDA = ''
        ROMPE = ''
        IDA = ''
        REGRESO = ''

        for x in vestiduras:
            if 'ENTRADA' in x:
                ENTRADA = x
                break
        for x in vestiduras:
            if 'SALIDA' in x:
                SALIDA = x
                break
        for x in vestiduras:
            if 'REGRESO' in x:
                REGRESO = x
                break
        for x in vestiduras:
            if 'IDA CORTE' in x:
                IDA = x
                break
        if len(IDA) == 0 and len(REGRESO) == 0:
            for x in vestiduras:
                if 'ROMPE' in x:
                    ROMPE = x
                    break

        for x in range(numerodecortes + 1):
            if IDA == '':
                IDA = ROMPE
            if REGRESO == '':
                REGRESO = ROMPE
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
    elif programa[0, 4] == 'HIMNO':
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
            if not programa[1, 0] == 0.998611111111111:
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
                if programa[1, 0] == 0.998611111111111 and not x == 3:
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
