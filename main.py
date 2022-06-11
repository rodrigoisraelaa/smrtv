import sys, os
from metodos.formating import formatingpausas, formatingprogram
from metodos.checaArchivos import checaarchivos
from metodos.dolst import dolst
import pandas as pd
from tkinter import *
from tkinter import filedialog


# def openFile():
#     filepath = filedialog.askopenfilename()
#     T.insert(END, filepath)
#
#
# def hacerLista():
#     df = pd.read_excel(T.get(first=0, last=1)[0])
#     df2 = pd.read_excel(T.get(first=0, last=1)[1])
#     programas, pausas, fecha = checaarchivos(df, df2)
#     print(fecha)
#     pausas = formatingpausas(pausas)
#     programas = formatingprogram(programas)
#     #dolst(pausas, fecha)
# window = Tk()
# window.geometry("500x500")
# button = Button(text='Seleccionar archivo', command=openFile)
# button.pack()
# button2 = Button(text='Hacer lista', command=hacerLista)
# button2.pack()
# T = Listbox(window, height=500, width=150)
# T.pack()
#
# window.mainloop()

df = pd.read_excel('comercialeslunes13dejunio2022.xlsx')
df2 = pd.read_excel('programaslunes13junio2022.xlsx')
programas, pausas, fecha = checaarchivos(df, df2)
pausas = formatingpausas(pausas)
programas = formatingprogram(programas)
dolst(pausas, programas, fecha)


