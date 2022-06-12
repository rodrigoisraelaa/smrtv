import pandas as pd


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


def checaarchivos(x1, x2):
    if type(x2.iloc[1, 0]) == str:
        program = x1
        continuidad = x2
    else:
        program = x2
        continuidad = x1

    dia1, mes1, ano1 = getdiamesano(continuidad.iloc[2, 0].replace(' ', '').replace('DE', '').upper())
    dia2, mes2, ano2 = getdiamesano(program.iloc[1, 1].replace(' ', '').replace('FECHA:', '').upper())
    Fecha1 = dia1 + mes1 + ano1
    Fecha2 = dia2 + mes2 + ano2

    if Fecha1 != Fecha2:
        quit('No tienen la misma fecha perri')

    return program, continuidad, continuidad.iloc[2, 0].replace(' ', '').replace('DE', '')
