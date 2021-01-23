import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
from main import omrmarking
import cv2

root= tk.Tk()
root.title("MCQ Marking System")

canvas1 = tk.Canvas(root, width = 700, height = 700, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

#frame=tk,Frame(root,bg="white")
#frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

#Read CSv
def getCSV ():
    import_file_path = filedialog.askopenfilename()
    global path
    path = import_file_path
    print (path)
    return import_file_path

#Open Image of Student's OMR
def openfile():
    filename = filedialog.askopenfilename(title='open')
    global imgpath
    imgpath = filename
    print(imgpath)
    return filename

#Output Image Uploaded
def show(p):
    img = Image.open(p)
    img = img.resize((250, 400))
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.place(x=350, y=150)

def openImg():
    x = openfile()
    show(x)

#Get result
def getResult():
    resultlabel = Label(root, bg="white", text="Result:")
    resultlabel.place(x=80, y=480)

    result=omrmarking(path,imgpath)
    noresult = Label(root, bg="white", text=result, fg='green')
    noresult.place(x=80, y=520)
    show("Marked/1.jpg")


#button_explore = Button(root, text="Browse Files", command=openImg)
#button_explore.place(x=80, y=80, width=140, height=40)

canvas1.create_text(250,80, text="INSTRUCTION:\n1) Insert the Answer Sheet in Excel file format by clicking 'Import CSV File'\n2) Insert Student's Answer Sheet in Image file format by clicking 'Import Image File'\n3) Press 'Scan Result' to get final result\n4) Press 'End Program' to leave")
#Import CSV Button
browseButton_CSV = tk.Button(root,text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=browseButton_CSV)

#Import Image Button
browseButton_IMG= tk.Button(root,text="      Import Image File     ", command=openImg, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 200, window=browseButton_IMG)

#Scan button
btnRead = tk.Button(root, height=1, width=10, text="Scan Result", command=getResult, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
btnRead.place(x=80, y=400, width=140, height=40)

button_quit=Button(root,text="Exit Program",command=root.quit, bg='red', fg='white', font=('helvetica', 12, 'bold'))
button_quit.place(x=240,y=600,width=200, height=60)

root.mainloop()
