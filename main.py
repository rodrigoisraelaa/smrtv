import sys, os
from metodos.formating import formatingpausas, formatingprogram
from metodos.checaArchivos import checaarchivos
from metodos.dolst import dolst, getdiamesano
import pandas as pd
from tkinter import *
from tkinter import filedialog

root = ''


def openFile():
    filepath = filedialog.askopenfilename()
    T.insert(END, filepath)


def hacerLista():
    df = pd.read_csv(T.get(first=0, last=1)[0])
    df2 = pd.read_csv(T.get(first=0, last=1)[1])
    programas, pausas, fecha = checaarchivos(df, df2)
    pausas = formatingpausas(pausas)
    programas = formatingprogram(programas)
    print(dolst(pausas, programas, fecha, root+'/'))


def seleccionarCarpeta():
    dir = filedialog.askdirectory()
    global root
    root = dir


window = Tk()
window.geometry("500x500")
button = Button(text='Seleccionar archivo', command=openFile)
button.pack()
button2 = Button(text='Hacer lista', command=hacerLista)
button2.pack()
button3 = Button(text='Selecciona Directorio de Zara', command=seleccionarCarpeta)
button3.pack()
T = Listbox(window, height=500, width=150)
T.pack()

window.mainloop()

# df = pd.read_csv('01 DEL 06 AL 13 JUNIO 2022 PARA RODRIGO.xlsx - MIERCOLES.csv')
# df2 = pd.read_csv('02 DEL 07 AL 13 JUNIO 2022 PROGRAMACION XHEREL 106-9 FM PARA RODRIGO.xlsx - Miercoles.csv')
# df = pd.read_csv('01 DEL 06 AL 13 JUNIO 2022 PARA RODRIGO.xlsx - VIERNES.csv')
# df2 = pd.read_csv('02 DEL 07 AL 13 JUNIO 2022 PROGRAMACION XHEREL 106-9 FM PARA RODRIGO.xlsx - Viernes.csv')
# # df = pd.read_csv('01 DEL 06 AL 13 JUNIO 2022 PARA RODRIGO.xlsx - LUNES FM.csv')
# # df2 = pd.read_csv('programaslunes13junio2022 - Hoja 1.csv')
# # df = pd.read_csv('01 DEL 06 AL 13 JUNIO 2022 PARA RODRIGO.xlsx - MARTES FM.csv')
# # df2 = pd.read_csv('programasmartes14junio2022 - Hoja 1.csv')
# df2 = pd.read_csv('01 DEL 06 AL 13 JUNIO 2022 PARA RODRIGO.xlsx - DOMINGO FM.csv')
# df = pd.read_csv('02 DEL 07 AL 13 JUNIO 2022 PROGRAMACION XHEREL 106-9 FM PARA RODRIGO.xlsx - Domingo.csv')
# programas, pausas, fecha = checaarchivos(df, df2)
# pausas = formatingpausas(pausas)
# programas = formatingprogram(programas)
# dia, mes, ano = getdiamesano(fecha)
# fecha = dia+mes+ano
# a = dolst(pausas, programas, fecha, root)
# print(a)
