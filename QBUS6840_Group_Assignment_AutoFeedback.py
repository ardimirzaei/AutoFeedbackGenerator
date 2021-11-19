# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:38:25 2021

@author: ArdiMirzaei
"""
import tkinter as tk
import pyperclip
import pandas as pd 
from tkinter.tix import *

#%%

root = tk.Tk()
root.title('QBUS6840 - AutoFeedback')
root.geometry('300x680')

class ScrolledFrame(tk.Frame):

    def __init__(self, parent, vertical=True, horizontal=False):
        super().__init__(parent)

        # canvas for inner frame
        self._canvas = tk.Canvas(self)
        self._canvas.grid(row=0, column=0, sticky='news') # changed

        # create right scrollbar and connect to canvas Y
        self._vertical_bar = tk.Scrollbar(self, orient='vertical', command=self._canvas.yview)
        if vertical:
            self._vertical_bar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._vertical_bar.set)

        # create bottom scrollbar and connect to canvas X
        self._horizontal_bar = tk.Scrollbar(self, orient='horizontal', command=self._canvas.xview)
        if horizontal:
            self._horizontal_bar.grid(row=1, column=0, sticky='we')
        self._canvas.configure(xscrollcommand=self._horizontal_bar.set)

        # inner frame for widgets
        self.inner = tk.Frame(self._canvas, bg='red')
        self._window = self._canvas.create_window((0, 0), window=self.inner, anchor='nw')

        # autoresize inner frame
        self.columnconfigure(0, weight=1) # changed
        self.rowconfigure(0, weight=1) # changed

        # resize when configure changed
        self.inner.bind('<Configure>', self.resize)
        self._canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        # resize inner frame to canvas size
        canvas_width = event.width
        self._canvas.itemconfig(self._window, width = canvas_width)

    def resize(self, event=None): 
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))



window = ScrolledFrame(root)
window.pack(expand=True, fill='both')


df = pd.read_csv("https://raw.githubusercontent.com/ardimirzaei/AutoFeedbackGenerator/main/QBUS6840_2021S2_Comments.csv")

paste_data = {k : '"' for k in pd.unique(df.Category) }
marks_data = {k : df.MaxCatMarks[df.Category==k].values[0] for k in pd.unique(df.Category) }
comment_options = {k: v for k, v in zip(df.ShortName.values, df.Comment.values)}
label_names = {k : False for k in pd.unique(df.Category)}
values_data = {k : v for k, v in zip(df.ShortName.values , df.Value.values) }
ck_box_variables = {k: tk.IntVar() for k in comment_options.keys()}
# bad_variables = {k: tk.IntVar() for k in comment_options.keys()}

def generate_feedback():
    # feedback = '"'
    marks_data = {k : df.MaxCatMarks[df.Category==k].values[0] for k in pd.unique(df.Category) }
    paste_data = {k : '"' for k in pd.unique(df.Category) }

    for k in comment_options.keys():
        if ck_box_variables[k].get() == 1:
            _task = df.Category[df.ShortName == k].values[0]
            # feedback += "" + comment_options[k] + "\n"
            paste_data[_task] += comment_options[k] + "\n"
            marks_data[_task] += values_data[k]
    
    for k in paste_data.keys():
        paste_data[k] += '"'
        
    # for k in comment_options.keys():
    #     if bad_variables[k].get() == 1:
    #         feedback += "\n\n" + comment_options[k]
    # feedback = feedback.strip()
    # feedback += '"'
    feedback = "\t".join([f'{m}\t{c}' for c,m in zip(  paste_data.values(), marks_data.values())])
    # copy feedback to the clipboard
    pyperclip.copy(feedback)
    pyperclip.paste()

def clear_options():
    for k, v in ck_box_variables.items():
        v.set(0)

for k, v in ck_box_variables.items():
    labelframe = tk.LabelFrame(window.inner)
    labelframe.pack(fill="both", expand=True)
    if not label_names[df.Category[df.ShortName == k].values[0]]:
        tk.Label(labelframe, bg='white', width=40, text=df.CatLongName[df.ShortName == k].values[0]).pack()
        label_names[df.Category[df.ShortName == k].values[0]] = True
    c1 = tk.Checkbutton(labelframe, text=k,
                                variable=v, onvalue=1, offvalue=0, 
                                command=generate_feedback)
    c1.pack(anchor = "w")



# l = tk.Label(window, bg='white', width=50, text='feedback copied to clipboard')

# l.pack()

B1 = tk.Button(labelframe, text = "Clear Outputs",activebackground="red", bd=3,bg="yellow",width=10, command = clear_options) #Button

B2= tk.Button(labelframe, text = "Copy",activebackground="red", bd=3,bg="lightgreen",width=10, command = generate_feedback) #Button

B1.pack()
B2.pack()


root.mainloop()

#%%
