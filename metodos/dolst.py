import os
import math

import numpy as np
from numpy import random
from mutagen.wave import WAVE
from mutagen.mp3 import MP3


def dolst(pausas, programas, fecha, root):
    texttoreturn = []
    cortesmadrugada = []
    raiz = root
    for x in [00, 0o1, 0o2, 0o3, 0o4, 0o5]:  # hace los cortes de madrugada
        for y in [00, 15, 30, 45]:
            cortesmadrugada.append([str((x + (y / 60)) / 24), '0', '0', '0', '0', '0'])
    pausas = np.concatenate((pausas, cortesmadrugada[1:]))
    with open(fecha + '.lst', 'w') as fp:
        fp.write('2000\n')
    while len(programas) > 0:
        pausas, texttoreturn = printprogrma(fecha, raiz, programas[0:2], pausas, texttoreturn)
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
    if 'GRABADO' in programa[0, 4] and not programa[0, 1] == 'RESUMEN LA MAÑANERA':
        archivodeprogramas = raiz + 'Programas/'
        for x in os.listdir(archivodeprogramas):
            if nombredeprograma in x:
                archivodeprograma = x
                break
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
            for x in range(cortesrequeridos + 1):
                if 5 != len(claves[5 * x:5 * (1 + x)]):
                    while 5 != len(claves[5 * x:5 * (1 + x)]):
                        claves.append('0')
                newcortes.append([*[float(horas[-cortesrequeridos - 1 + x])], *claves[5 * x:5 * (1 + x)]])
            b = np.r_[newcortes, pausas]
            pausas = np.array(b)
        if numbloques == 1:
            if bloques != 'a':
                duracion = getlen(dirpath + bloques[0])
                with open(fecha + '.lst', 'a') as fp:
                    fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[0]).replace('/', '\\')))
            if not programa[1, 0] == 0.998611111111111 or x != numerodecortes:
                texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                pausas = pausas[1:]
        elif numbloques != 0:
            if bloques != 'a':
                bloques.sort()
            for x in range(0, numbloques):
                if bloques != 'a':
                    duracion = getlen(dirpath + bloques[x])
                    with open(fecha + '.lst', 'a') as fp:
                        fp.write("%s\t%s\n" % (duracion, (dirpath + bloques[x]).replace('/', '\\')))
                if not programa[1, 0] == 0.998611111111111 or x != numerodecortes:
                    texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                    pausas = pausas[1:]
        else:
            texttoreturn.append('No hay bloques en la carpeta de ' + programa[0, 1] + ' en la carpeta de ' + dia + mes)
    elif programa[0, 4] == 'VIVO' and not programa[0, 1] == 'LA MAÑANERA AMLO':
        suprapath = raiz + 'Institucional/VESTIDURAS/'
        suprafolders = os.listdir(suprapath)
        nombredecarpeta = ''
        for x in suprafolders:
            if nombredeprograma in x:
                nombredecarpeta = x
        if nombredecarpeta == '':
            texttoreturn.append('no hay carpeta de vestiduras de' + programa[0, 1])
        dirpath = suprapath + nombredecarpeta + '/'
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
            if not programa[1, 0] == 0.998611111111111 or x != numerodecortes:
                texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                pausas = pausas[1:]
    elif 'HIMNO' in programa[0, 4]:
        printhimno(fecha, raiz)
        texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn, morelia='M')
        pausas = pausas[1:]
    elif programa[0, 1] == 'LA MAÑANERA AMLO':
        pausaespecial1 = np.concatenate((pausas[0], pausas[1, 1:], pausas[2, 1:], pausas[3, 1:]))
        texttoreturn = printcorte(fecha, raiz, pausaespecial1, texttoreturn)
        with open(fecha + '.lst', 'a') as fp:
            fp.write("%s\t%s\n" % ('-1', '.stop'))
        pausas = pausas[4:]
        pausaespecial2 = np.concatenate(([pausas[3, 0]], pausas[0, 1:], pausas[1, 1:], pausas[2, 1:], pausas[3, 1:]))
        texttoreturn = printcorte(fecha, raiz, pausaespecial2, texttoreturn)
        pausas = pausas[4:]
    elif programa[0, 4] == 'MUSICA' and programa[0, 5] == 'ARBOL DE MUSICA':
        for x in range(numerodecortes + 1):
            if (not programa[1, 0] == 0.998611111111111 or x != numerodecortes) and len(pausas) != 0:
                texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                pausas = pausas[1:]
    elif 'CARPETA' in programa[0, 4]:
        for x in range(0, numerodecortes + 1):
            if not programa[1, 0] == 0.998611111111111 or x != numerodecortes:
                texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                pausas = pausas[1:]
    elif programa[0, 4] == 'MUSICA SELECCIONADA':
        if programa[0, 1] == 'MUSICA RESISTENCIA':
            dirpath = raiz + 'Programas/' + nombredeprograma + '/' + mes + ' ' + ano + '/' + dia + ' ' + mes + '/'
            rolas = os.listdir(dirpath)
            rolas.sort()
            rompecorte = raiz + 'Institucional/VESTIDURAS/' + nombredeprograma + '/' + \
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
                if not programa[1, 0] == 0.998611111111111 or x != numerodecortes:
                    texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
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
                texttoreturn = printcorte(fecha, raiz, pausas[0], texttoreturn)
                pausas = pausas[1:]

    return pausas, texttoreturn


def getdiamesano(fecha):
    meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE',
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


def print_titulo_de_corte(raiz, pausa, fecha):
    dirpath = raiz + 'Institucional/LISTAS/Horas'
    subtring = formatinghora(pausa[0])
    print(buscararchivo(dirpath, subtring))
    stringtoprint = dirpath.replace('/', '\\') + '\\' + buscararchivo(dirpath, subtring)
    with open(fecha + '.lst', 'a') as fp:
        fp.write("0\t%s\n" % stringtoprint)


def print_identificador_de_corte(fecha, raiz, morelia):
    path = raiz + 'Institucional/IMAGEN SONORA 2022/IDENTIFICADORES 2022/'
    if morelia == 'M':
        for d in os.listdir(path):
            if 'MORELIA' in d.upper():
                x = path + d
    else:
        y = random.randint(len(os.listdir(path)))
        x = path + os.listdir(path)[y]
    duracion = getlen(x)
    with open(fecha + '.lst', 'a') as fp:
        fp.write("%s\t%s\n" % (duracion, x.replace('/', '\\')))


def print_locucion_por_hora(fecha):
    with open(fecha + '.lst', 'a') as fp:
        fp.write("-1\t.time\n")


def print_comercializacion(fecha, raiz, pausa, texttoprint):
    n = 0
    for clave in pausa[1:]:
        if clave != '0' and clave != 'P0' and clave != 'F0' and clave != '10' and clave != 'PP0' and clave != 'INE0' and \
                clave != 'FE0' and clave != 'CO0' and clave != 'IN0' and clave != 'PR0' and clave == clave:
            path = raiz + 'COMERCIALIZACION/'
            print(clave)
            if 'PP' == clave[:2]:
                n = n + 1
                path = path + 'INE - PP/PP/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
            elif 'IN' == clave[:2]:
                n = n + 1
                path = path + 'INE - PP/INE/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
            elif 'FE' == clave[:2]:
                n = n + 1
                path = path + 'FEDERALES/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
            elif 'CO' == clave[:2]:
                n = n + 1
                path = path + 'COM/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
            elif 'RT' == clave[:2]:
                n = n + 1
                path = path + 'RTC 5MIN/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
            elif 'PR' == clave[:2]:
                n = n + 1
                path = path + 'Promos/'
                duracion = 0
                for filename in os.listdir(path):
                    if clave in filename[:5]:
                        duracion = getlen(path + filename)
                        with open(fecha + '.lst', 'a') as fp:
                            fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))
                        break
                if duracion == 0:
                    texttoprint.append('no existe ' + clave)
    if n == 0:
        path = raiz + 'COMERCIALIZACION/Promos/'
        x = random.randint(len(os.listdir(path)))
        if os.listdir(path)[x][:2] != 'PR':
            while os.listdir(path)[x][:2] != 'PR':
                x = random.randint(len(os.listdir(path)))
        duracion = getlen(path + os.listdir(path)[x])
        with open(fecha + '.lst', 'a') as fp:
            print(os.listdir(path)[x][:4])
            fp.write("%s\t%s\n" % (duracion, (path + os.listdir(path)[x]).replace('/', '\\')))
    return texttoprint


def print_promo_estacion(raiz, fecha):
    path = raiz + 'Institucional/IMAGEN SONORA 2022/'
    x = random.randint(len(os.listdir(path)))
    filename = os.listdir(path)[x]
    if os.path.isfile(path + filename) != 1:
        while os.path.isfile(path + filename) != 1:
            x = random.randint(len(os.listdir(path)))
            filename = os.listdir(path)[x]
    duracion = getlen(path + os.listdir(path)[x])
    with open(fecha + '.lst', 'a') as fp:
        fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))


def print_patrocinador_de_hora(raiz, fecha):
    path = raiz + 'COMERCIALIZACION/PERSONAJES HORAS/'
    x = random.randint(len(os.listdir(path)))
    filename = os.listdir(path)[x]
    duracion = getlen(path + os.listdir(path)[x])
    with open(fecha + '.lst', 'a') as fp:
        fp.write("%s\t%s\n" % (duracion, (path + filename).replace('/', '\\')))


def printcorte(fecha, raiz, pausa, texttoprint, morelia=None):
    print_titulo_de_corte(raiz, pausa, fecha)
    print_identificador_de_corte(fecha, raiz, morelia)
    print_patrocinador_de_hora(raiz, fecha)
    print_locucion_por_hora(fecha)
    texttoprint = print_comercializacion(fecha, raiz, pausa, texttoprint)
    print_promo_estacion(raiz, fecha)
    return texttoprint


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
