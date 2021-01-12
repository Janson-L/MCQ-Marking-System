import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
from main import omrmarking
import cv2

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 700, height = 700, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

#frame=tk,Frame(root,bg="white")
#frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

#Read CSv
def getCSV ():

    #import_file_path = filedialog.askopenfilename()
    #path = pd.read_csv (import_file_path)
    #print (path)

    import_file_path = filedialog.askopenfilename()
    global path
    path = import_file_path
    print (path)
    return import_file_path

#def openfile():
#    filename = filedialog.askopenfilename(title='open')
#    global imgpath
#    imgpath = filename
#    return filename

#def openImg():
#    x = openfile()
#    show(x)

def getResult():

    resultlabel = Label(root, bg="white", text="Result:")
    resultlabel.place(x=80, y=480)

    result=omrmarking(path)
    noresult = Label(root, bg="white", text=result, fg='green')
    noresult.place(x=80, y=520)


#button_explore = Button(root, text="Browse Files", command=openImg)
#button_explore.place(x=80, y=80, width=140, height=40)

browseButton_CSV = tk.Button(root,text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_CSV)

btnRead = tk.Button(root, height=1, width=10, text="Scan", command=getResult)
btnRead.place(x=80, y=400, width=140, height=40)

root.mainloop()
