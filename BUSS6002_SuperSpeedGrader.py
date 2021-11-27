# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:55:50 2021

@author: -
"""

import tkinter as tk
import re

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



#%%
import warnings
warnings.filterwarnings('ignore')

#%%
browser = webdriver.Chrome()
browser.get('https://canvas.sydney.edu.au/courses/37425/gradebook/speed_grader?assignment_id=335732')


#%%
question = "question_score_1838756_visible"
# start_time = datetime.now()
def send_00():
    send_marks_to_browser(0,question)
    update_scores()
    print(0)
    # start_time = datetime.now()
    
def send_05():
    send_marks_to_browser(5,question )
    update_scores()
    print(f'5')
    # start_time = datetime.now()
    
def send_10():
    send_marks_to_browser(10,question)
    update_scores()
    print(f'10')
    # start_time = datetime.now()

def send_00n():
    send_marks_to_browser(0,question)
    update_scores()
    next_student()
    print(f'0')
    # start_time = datetime.now()
    
def send_05n():
    send_marks_to_browser(5,question )
    update_scores()
    next_student()
    print(f'5')
    # start_time = datetime.now()

def send_10n():
    send_marks_to_browser(10,question)
    update_scores()
    next_student()
    print(f'10')
    # print(f'10 - ({(datetime.now() - start_time).total_seconds():.2f}s)')
    # start_time = datetime.now()
#%%
def send_marks_to_browser(mark, question):
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_element_by_id("speedgrader_iframe"))
    qid = int(re.findall("\d{7}",question)[0])
    browser.find_element_by_xpath(f'//*[@id="quiz_nav_{qid}"]/a').click()
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.ID, question)))
    browser.find_element_by_id(question).click()
    browser.find_element_by_id(question).clear()
    browser.find_element_by_id(question).send_keys(mark)
    browser.switch_to.default_content()

def update_scores():
    browser.switch_to.frame(browser.find_element_by_id("speedgrader_iframe"))
    browser.find_element_by_class_name("button-container").click()

def next_student():
    browser.switch_to.default_content()
    browser.find_element_by_id("next-student-button").click()
    
def prev_student():
    browser.switch_to.default_content()
    browser.find_element_by_id("prev-student-button").click()


#%%
root = tk.Tk()
root.title('BUSS6002 - SuperSpeedGrader')
root.geometry('300x100')

root.columnconfigure(0, pad=3)
root.columnconfigure(1, pad=3)
root.columnconfigure(2, pad=3)


root.rowconfigure(0, pad=3)
root.rowconfigure(1, pad=3)
root.rowconfigure(2, pad=3)


B1 = tk.Button(root, text = "0 Marks",activebackground="lightyellow", bd=3,bg="#F52E2E",width=12, command = send_00) #Button

B2 = tk.Button(root, text = "5 Marks",activebackground="lightyellow", bd=3,bg="lightgreen",width=12, command = send_05) #Button

B3 = tk.Button(root, text = "10 Marks",activebackground="lightyellow", bd=3,bg="#32CD32",width=12, command = send_10) #Button

B_n = tk.Button(root, text = "Next Student",activebackground="lightyellow", bd=3,bg="#AEC6CF",width=12, command = next_student) #Button

B_p = tk.Button(root, text = "Prev Student",activebackground="lightyellow", bd=3,bg="#AEC6CF",width=12, command = prev_student) #Button

B_u = tk.Button(root, text = "Update Scores",activebackground="lightyellow", bd=3,bg="#AEC6CF",width=12, command = update_scores) #Button

B1n = tk.Button(root, text = "0 M + Next",activebackground="lightyellow", bd=3,bg="#F52E2E",width=12, command = send_00n) #Button

B2n = tk.Button(root, text = "5 M + Next",activebackground="lightyellow", bd=3,bg="lightgreen",width=12, command = send_05n) #Button

B3n = tk.Button(root, text = "10 M + Next",activebackground="lightyellow", bd=3,bg="#32CD32",width=12, command = send_10n) #Button

B1.grid(row = 0, column = 0)
B2.grid(row = 0, column = 1)
B3.grid(row = 0, column = 2)
B_n.grid(row = 1, column = 1)
B_p.grid(row = 1, column = 0)
B_u.grid(row = 1, column = 2)
B1n.grid(row = 2, column = 0)
B2n.grid(row = 2, column = 1)
B3n.grid(row = 2, column = 2)
# B1.pack()
# B2.pack()
# B3.pack()
# B_n.pack()
# B_p.pack()


root.mainloop()



    
