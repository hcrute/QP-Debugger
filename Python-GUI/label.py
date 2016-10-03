from Tkinter import *

root = Tk()

var = StringVar()
label = Label(root, textvariable=var, relief=RAISED)

var.set("Hey?! How's it going?")
label.pack()
root.mainloop()
