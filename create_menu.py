from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog as fd
import tkinter as tk
#from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def icon_background(wind,photo):

    wind.iconphoto(True, photo)
    wind.configure(background='AntiqueWhite1')

def _create_check(modulation_window):
    # creating 3 checkbuttons
    check_=0
    tk.Label(modulation_window,text='Select to plot Graph').grid(row=0,column=2,sticky=tk.W)
    mod_sig = tk.IntVar(modulation_window)
    check1 = tk.Checkbutton(modulation_window, text="Modulating Signal", variable=mod_sig)#,state='disabled')
    check1.deselect()
    check1.grid(row=1, column=2,sticky=tk.W)
    car_sig = tk.IntVar(modulation_window)
    check2 = tk.Checkbutton(modulation_window, text="Carrier Signal", variable=car_sig)
    check2.deselect()
    check2.grid(row=2, column=2,sticky=tk.W)
    mes_sig = tk.IntVar(modulation_window)
    check3 = tk.Checkbutton(modulation_window, text='Message Signal', variable=mes_sig)
    check3.select()
    check3.grid(row=3, column=2,sticky=tk.W)
    check_=0
    if (mod_sig.get()):
        check_ += 1
    if (car_sig.get()):
        check_ += 1
    if (mes_sig.get()):
        check_ += 1
    return mod_sig.get(),car_sig.get(),mes_sig.get(),check_

def create_menu_bar(main_window):
    def _quit():
        ans = msg.askyesnocancel('Quit Window', 'Do You Want to Quit ?')
        if (ans):
            # main_window.quit()
            #main_window.destroy()
            main_window.after(2000, main_window.destroy)
    def _saveas():
        ans = msg.askyesno('Patnite Simulator', 'Do You Want to Save ?')
        if (ans):
            msg.showerror('Patnite Simulater','There is Nothing to Save')

    menu_bar = Menu(main_window, bd=3, fg='red', bg='pink')
    filemenu = Menu(menu_bar, tearoff=0)
    filemenu.add_command(label='New', command='')
    filemenu.add_command(label='Open', command='')
    filemenu.add_command(label='Save', command=_saveas)
    filemenu.add_command(label='Save_as', command=_saveas)
    filemenu.add_command(label='Close', command=_quit)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=_quit)
    menu_bar.add_cascade(label='File', menu=filemenu)

    editmenu = Menu(menu_bar, tearoff=0)
    editmenu.add_command(label='Cut', command='')
    editmenu.add_command(label='Copy', command='')
    editmenu.add_command(label='Paste', command='')
    editmenu.add_command(label='Select All', command='')
    menu_bar.add_cascade(label='Edit', menu=editmenu)

    helpmenu = Menu(menu_bar, tearoff=0)
    helpmenu.add_command(label='Help Index', command='')
    helpmenu.add_command(label='About...', command='')
    menu_bar.add_cascade(label='Help', menu=helpmenu)
    main_window.config(menu=menu_bar)

def create_menu_bar1(main_window,canvas):
    def _quit():
        ans = msg.askyesnocancel('Quit Window', 'Do You Want to Quit ?')
        if (ans):
            # main_window.quit()
            #main_window.destroy()
            main_window.after(2000, main_window.destroy)
    def _saveas():
        ans = msg.askyesno('Patnite Simulator', 'Do You Want to Save ?')
        if (ans):
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Images', '*.jpg')]
            file = fd.asksaveasfilename(defaultextension='.png')
            print(file)
            if file:
                try:
                    print(main_window.winfo_children())
                    canvas.print_png(file)
                except:
                    print("nope")
            else:
                msg.showerror('Patnite Simulater','Please Write Valid Name')

    menu_bar = Menu(main_window, bd=3, fg='red', bg='pink')
    filemenu = Menu(menu_bar, tearoff=0)
    filemenu.add_command(label='New', command='')
    filemenu.add_command(label='Open', command='')
    filemenu.add_command(label='Save', command=_saveas)
    filemenu.add_command(label='Save_as', command=_saveas)
    filemenu.add_command(label='Close', command=_quit)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=_quit)
    menu_bar.add_cascade(label='File', menu=filemenu)

    editmenu = Menu(menu_bar, tearoff=0)
    editmenu.add_command(label='Cut', command='')
    editmenu.add_command(label='Copy', command='')
    editmenu.add_command(label='Paste', command='')
    editmenu.add_command(label='Select All', command='')
    menu_bar.add_cascade(label='Edit', menu=editmenu)

    helpmenu = Menu(menu_bar, tearoff=0)
    helpmenu.add_command(label='Help Index', command='')
    helpmenu.add_command(label='About...', command='')
    menu_bar.add_cascade(label='Help', menu=helpmenu)
    main_window.config(menu=menu_bar)
