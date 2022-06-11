import pandas as pd


def checaarchivos(x1, x2):
    if type(x2.iloc[1, 0]) == str:
        program = x1
        continuidad = x2
    else:
        program = x2
        continuidad = x1

    if continuidad.iloc[2, 0].replace(' ', '').replace('DE', '')[-10:] != program.iloc[1, 1].replace(' ', '').replace(
            'FECHA:', '')[-10:]:
        quit('No tienen la misma fecha perri')

    return program, continuidad, continuidad.iloc[2, 0].replace(' ', '').replace('DE', '')
