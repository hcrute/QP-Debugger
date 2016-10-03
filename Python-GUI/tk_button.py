#!/user/bin/python

import Tkinter
import tkMessageBox

top = Tkinter.Tk()

def helloCallBack():
    tkMessageBox.showinfo("Hello Python", "Hello World")

B = Tkinter.Button(top, text = "Hello", command = helloCallBack)

B.pack()

#code to add widgets

top.mainloop()
