from tkinter import *
from tkinter import colorchooser

def color_choose():
    global colore
    colore = colorchooser.askcolor(title="Choose")
    print(colore)

def draw_pencil(event):
    x1, y1 = (event.x - pad_size),(event.y - pad_size) 
    x2, y2 = (event.x + pad_size),(event.y + pad_size)
    canvas.create_oval(x1,y1,x2,y2, outline= colore[1], fill= colore[1])

def size_of_line(size):
    global pad_size
    pad_size = int(size)

def clear():
    canvas.delete('all')

def eraser_color():
    global colore
    colore = [0,'white']


colore = [0,"black"]
pad_size = 10

root = Tk()
root.geometry('1280x720')
root.columnconfigure(6, weight=1)
root.rowconfigure(2,weight=1)

button_1 = Button(root, text="Select", command=color_choose)
button_1.grid(row=0,column=0)
button_2 = Button(root, text="Clear",command=clear)
button_2.grid(row=0,column=6)
button_3 = Button(root, text="Eraser",command=eraser_color)
button_3.grid(row=0,column=4)

canvas = Canvas(root, cursor='pencil',bg='white')
canvas.grid(row=2,column=0, columnspan=7,padx=5, pady=5,sticky=E + W + S + N)

canvas.bind('<B1-Motion>', draw_pencil)
canvas.bind('<Button-1>', draw_pencil)


v = IntVar(value=10)
Scale(root, variable=v,from_= 1, to=100, orient=HORIZONTAL, command=size_of_line).grid(row=0, column=1, padx=100)

root.mainloop()