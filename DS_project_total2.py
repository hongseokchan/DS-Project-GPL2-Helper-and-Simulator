from __future__ import division, print_function
from visual import *
from visual.graph import *
import wx
import math
from Tkinter import *
from PIL import Image
from PIL import ImageTk

root = Tk()

root.title("General Physics 2 Simulator and Helper")
root.geometry("418x495+100+100")
root.resizable(False,False)

def gpl6(evt):
    execfile("gpe6_microwave.py")

def gpl4(evt):
    execfile("gpe4_helmholtz_coil2.py")

def gpl3(evt):
    execfile("gpe3_light_bulb.py")

def gpl1(evt):
    execfile("gpe1_coulombs_balance.py")


Label1 = Label(root, width = 29, height = 2 ,text = "General Physics 2 Lab helper")
Label1.grid(row = 0,column = 0,rowspan = 2)

Label1 = Label(root, width = 29, height = 2 ,text = "18-119 seokchan 18-080 hangyeol")
Label1.grid(row = 0,column = 1,rowspan = 2)

frame1=Frame(root, relief="solid", bd=2)
frame1.grid(row = 2,column = 0)

image_micro = ImageTk.PhotoImage(Image.open("microwave_exp.PNG").resize((200,200)))
label_micro_image=Label(frame1, image=image_micro)
label_micro_image.pack()
label_micro_image.bind("<Button-1>", gpl6)
label_micro_text = Label(frame1,text = "Microwave, gpl6")
label_micro_text.pack()


frame2=Frame(root, relief="solid", bd=2)
frame2.grid(row = 2,column = 1)

image_helm = ImageTk.PhotoImage(Image.open("helmholtz_coil.PNG").resize((200,200)))
label_helm_image=Label(frame2, image=image_helm)
label_helm_image.bind("<Button-1>", gpl4)
label_helm_image.pack()
label_helm_text = Label(frame2,text = "Helmholtz coil, gpl4")
label_helm_text.pack()

frame3=Frame(root, relief="solid", bd=2)
frame3.grid(row = 3,column = 0)

image_light = ImageTk.PhotoImage(Image.open("light_bulb.PNG").resize((200,200)))
label_light_image=Label(frame3, image=image_light)
label_light_image.bind("<Button-1>", gpl3)
label_light_image.pack()
label_light_text = Label(frame3,text = "Light Bulb, gpl3")
label_light_text.pack()

frame4=Frame(root, relief="solid", bd=2)
frame4.grid(row = 3,column = 1)

image_balance = ImageTk.PhotoImage(Image.open("coulombs_balance.PNG").resize((200,200)))
label_balance_image=Label(frame4, image=image_balance)
label_balance_image.bind("<Button-1>", gpl1)
label_balance_image.pack()
label_balance_text = Label(frame4,text = "coulombs_balance, gpl1")
label_balance_text.pack()

root.mainloop()
