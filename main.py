import sys, os
from metodos.formating import formatingpausas, formatingprogram
from metodos.checaArchivos import checaarchivos
from metodos.dolst import dolst, getdiamesano
import pandas as pd
from tkinter import *
from tkinter import filedialog

roottxt = 'roottxt.txt'
global root
if os.path.exists(roottxt):
    with open(roottxt, 'r') as fp:
        root = fp.readlines()[0]
        if not root[-1] == '/':
            root = root + '/'
else:
    root = ''


def openFile():
    filepath = filedialog.askopenfilename()
    T.insert(END, filepath)


def hacerLista(root=root):
    df = pd.read_csv(T.get(first=0, last=1)[0])
    df2 = pd.read_csv(T.get(first=0, last=1)[1])
    programas, pausas, fecha = checaarchivos(df, df2)
    pausas = formatingpausas(pausas)
    programas = formatingprogram(programas)
    toprin = dolst(pausas, programas, fecha, root)
    if len(toprin) == 0:
        T.insert(END, 'exito')
    else:
        for x in toprin:
            T.insert(END, x)


def seleccionarCarpeta():
    dir = filedialog.askdirectory()
    global root
    root = dir
    with open(roottxt, 'w') as fp:
        fp.write(root)


window = Tk()
window.geometry("1000x500")
button = Button(text='Seleccionar archivo', command=openFile)
button.pack()
button2 = Button(text='Hacer lista', command=hacerLista)
button2.pack()
button3 = Button(text='Selecciona Directorio de Zara', command=seleccionarCarpeta)
button3.pack()
T = Listbox(window, height=500, width=150)
T.pack()

window.mainloop()

