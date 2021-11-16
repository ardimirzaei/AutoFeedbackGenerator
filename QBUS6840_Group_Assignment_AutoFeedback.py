# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 12:38:25 2021

@author: ArdiMirzaei
"""


import tkinter as tk
import pyperclip
import pandas as pd 


#%%
window = tk.Tk()
window.title('My Window')
window.geometry('300x1280')

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
    if not label_names[df.Category[df.ShortName == k].values[0]]:
        tk.Label(window, bg='white', width=40, text=df.CatLongName[df.ShortName == k].values[0]).pack()
        label_names[df.Category[df.ShortName == k].values[0]] = True
    c1 = tk.Checkbutton(window, text=k,
                                variable=v, onvalue=1, offvalue=0, 
                                command=generate_feedback)
    c1.pack(anchor = "w")



# l = tk.Label(window, bg='white', width=50, text='feedback copied to clipboard')

# l.pack()

B1 = tk.Button(window, text = "Clear Outputs",activebackground="red", bd=3,bg="yellow",width=10, command = clear_options) #Button

B2= tk.Button(window, text = "Copy",activebackground="red", bd=3,bg="lightgreen",width=10, command = generate_feedback) #Button

B1.pack()
B2.pack()


window.mainloop()

#%%
