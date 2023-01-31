import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from os.path import exists
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import numpy as np
import time, serial
import math
# import mediapipe as mp
# import joblib
# import cv2
from itertools import count
from sklearn.ensemble import RandomForestClassifier

plt.style.use('seaborn')
ser = serial.Serial('COM7', 38400)
ser.close()
ser.open()
train = pd.read_csv("datasets/Training-Final.csv")
train['LABEL'].replace(to_replace=["HEALTHY", "FALSE"], value=[0,1], inplace=True)
temp = train
X = temp.drop('LABEL', axis=1)
y = train['LABEL']

rf_clf = RandomForestClassifier(n_estimators=30)
rf_clf.fit(X,y)

path = 'datasets/'


def graph_window_IR():
    root = tk.Tk()
    root.wm_title("IR Graph Window")
    b = plt.figure(figsize=(7, 3.5), dpi=100)
    ax2 = b.add_subplot(1, 1, 1)
    xI = []
    y0I = []
    finalDict = {'x': []}
    pos = 'upper left'
    def animateIR(i, xI, y0I):
        ser.reset_input_buffer()
        data = ser.readline()
        data_point = data.strip()
        if data_point != '':
            ax2.clear()
            xI.append(i)
            y0I.append(int(data_point))
            finalDict["x"].append(int(data_point))
            xI = xI[-50:]
            y0I = y0I[-50:]
            print(len(xI))
            ax2.plot(xI, y0I, label = 'y')
            ax2.legend(loc=pos)
    canvas = FigureCanvasTkAgg(b, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(side= tk.TOP, fill = tk.BOTH, expand = True)

    def _quit():
        print(finalDict)
        df = pd.DataFrame(finalDict)
        df.to_csv(path + 'IR.csv', index=False, mode='w')
        root.quit()     # stops mainloop
        root.destroy()
    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    root.ani = animation.FuncAnimation(b, animateIR, fargs=(xI, y0I), interval=200)
    tk.mainloop()

def graph_window_MYO():
    root = tk.Tk()
    root.wm_title("Tremor Graph Window")
    a = plt.figure(figsize=(7, 3.5), dpi=100)
    ax1 = a.add_subplot(1, 1, 1)
    xM = []
    yM = []
    finalDict = {'x': []}
    pos = 'upper left'

    def animateMYO(i, xI, y0I):
        ser.reset_input_buffer()
        data = ser.readline()
        data_point = data.strip()
        if data_point != '':
            ax1.clear()
            xI.append(i)
            y0I.append(int(data_point))
            finalDict["x"].append(int(data_point))
            xI = xI[-50:]
            y0I = y0I[-50:]
            ax1.plot(xI, y0I, label = 'y')
            ax1.legend(loc=pos)

    canvas = FigureCanvasTkAgg(a, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(side= tk.TOP, fill = tk.BOTH, expand = True)

    def _quit():
        print(finalDict)
        df = pd.DataFrame(finalDict)
        df.to_csv(path + 'MYO.csv', index=False, mode='w')
        root.quit()     # stops mainloop
        root.destroy()
    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    root.ani = animation.FuncAnimation(a, animateMYO, fargs=(xM, yM), interval=100)
    tk.mainloop()

def graph_window_tremor():
    
    def start_counter(label):
        counter = count(0)
        def update_func():
            label.config(text=str(next(counter)))
            label.after(1000, update_func)  # 1000ms
        update_func()
    
    root = tk.Tk()
    root.wm_title("Tremor Graph Window")
    a = plt.figure(figsize=(7, 3.5), dpi=100)
    ax1 = a.add_subplot(1, 1, 1)
    xT = []
    y0T = []
    y1T = []
    y2T = [] 
    y3T = [] 
    y4T = [] 
    y5T = []
    pos = 'upper center'

    finalDict = {'a1': [], 'a2': [], 'a3': [], 'g1': [], 'g2': [], 'g3': []}

    close_time = time.time()+60

    def animateTremor(i, xT, y0T, y1T, y2T, y3T, y4T, y5T):
        ser.reset_input_buffer()
        data = ser.readline()
        data_point = data.decode()

        if data_point != '':
            data_point = data_point.strip().split(", ")
            ax1.clear()

            if len(data_point) > 1:
                xT.append(i)
                xT = xT[-20:]
                print(data_point)
                if data_point[0]:
                    y0T.append(int(data_point[0]))
                    finalDict["a1"].append(int(data_point[0]))
                    y0T = y0T[-20:]
                    ax1.plot(xT, y0T, label="accelX")
                    ax1.legend(loc=pos)

                if data_point[1]:
                    y1T.append(int(data_point[1]))
                    finalDict["a2"].append(int(data_point[1]))
                    y1T = y1T[-20:]
                    ax1.plot(xT, y1T, label="accelY")
                    ax1.legend(loc=pos)
                
                if data_point[2]:
                    y2T.append(int(data_point[2]))
                    finalDict["a3"].append(int(data_point[2]))
                    y2T = y2T[-20:]
                    ax1.plot(xT, y2T, label="accelZ")
                    ax1.legend(loc=pos)

                if data_point[3]:
                    y3T.append(int(data_point[3]))
                    finalDict["g1"].append(int(data_point[3]))
                    y3T = y3T[-20:]
                    ax1.plot(xT, y3T, label="gyroX")
                    ax1.legend(loc=pos)

                if data_point[4]:
                    y4T.append(int(data_point[4]))
                    finalDict["g2"].append(int(data_point[4]))
                    y4T = y4T[-20:]
                    ax1.plot(xT, y4T, label="gyroY")
                    ax1.legend(loc=pos)
                
                if data_point[5]:
                    y5T.append(int(data_point[5]))
                    finalDict["g3"].append(int(data_point[5]))
                    y5T = y5T[-20:]
                    ax1.plot(xT, y5T, label="gyroZ")
                    ax1.legend(loc=pos, bbox_to_anchor=(0.5, 1.05), fancybox=True, shadow=True, ncol=6, columnspacing=0.8)
    
    canvas = FigureCanvasTkAgg(a, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(side= tk.TOP, fill = tk.BOTH, expand = True)

    def _quit():
        print(finalDict)
        df = pd.DataFrame(finalDict)
        df.to_csv(path + 'tremor.csv', index=False, mode='w')
        root.quit()     # stops mainloop
        root.destroy()
    
    label = tk.Label(root, fg="red")
    label.pack()
    start_counter(label)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    root.ani = animation.FuncAnimation(a, animateTremor, fargs=(xT, y0T, y1T, y2T, y3T, y4T, y5T), interval=200)
    tk.mainloop()

class Switch(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, Tremor, ObjectD, MYO, Analysis):
            frame = F(self.container, self)
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")  
        self.show_frame(StartPage)

    def refresh_frame(self):
        for F in (StartPage, Tremor, ObjectD, MYO, Analysis):
            frame = F(self.container, self)
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

    def show_frame(self, cont):
        self.refresh_frame()
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page")
        label.pack(pady=10, padx=10)

        b1 = tk.Button(self, text="Tremor", command= lambda: controller.show_frame(Tremor))
        b1.pack()
        b2 = tk.Button(self, text="IR", command= lambda: controller.show_frame(ObjectD))
        b2.pack()
        b3 = tk.Button(self, text="MYO", command= lambda: controller.show_frame(MYO))
        b3.pack()


class Tremor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Tremor")
        label.pack(pady=10,padx=10)
        b1 = tk.Button(self, text="Start", command=graph_window_tremor)
        b1.pack()
        b2 = tk.Button(self, text="Send For Analysis", command = lambda: controller.show_frame(Analysis))
        b2.pack()
        if exists(path+'tremor.csv') == False:
            b2['state'] = DISABLED
        else:
            b2['state'] = NORMAL
        b3 = tk.Button(self, text="Back to Home", command= lambda: controller.show_frame(StartPage))
        b3.pack()    

class ObjectD(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="IR")
        label.pack(padx=10, pady=10)
        b1 = tk.Button(self, text="Start", command= graph_window_IR)
        b1.pack()
        b2 = tk.Button(self, text="Back to home", command= lambda: controller.show_frame(StartPage))
        b2.pack()

class MYO(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="MYO")
        label.pack(padx=10, pady=10)
        b1 = tk.Button(self, text="Start", command = graph_window_MYO)
        b1.pack()
        b2 = tk.Button(self, text="Back to Home", command= lambda:controller.show_frame(StartPage))
        b2.pack()

class Analysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        if exists(path+'tremor.csv'):
            data = pd.read_csv(path+'tremor.csv')
            y_pred = rf_clf.predict(data)
            ans = np.bincount(y_pred).argmax()
            label = tk.Label(self, text = ans)
            label.pack(padx=10, pady=10)
            b2 = tk.Button(self, text="Back to Tremor Page", command= lambda: controller.show_frame(Tremor))
            b2.pack()

app = Switch()
app.mainloop()

