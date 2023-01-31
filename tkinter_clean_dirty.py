from itertools import count
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from os.path import exists
import pandas as pd
import numpy as np
import time, serial
from sklearn.ensemble import RandomForestClassifier

ser = serial.Serial('COM3', 38400)
ser.close()
ser.open()


train = pd.read_csv("datasets/Final.csv")
train['LABEL'].replace(to_replace=["Clean", "Dirty"], value=[0,1], inplace=True)
temp = train
X = temp.drop('LABEL', axis=1)
y = train['LABEL']

rf_clf = RandomForestClassifier(n_estimators=30)
rf_clf.fit(X,y)

path = 'datasets/'


def take_readings_turbulance():
    def start_counter(label):
        counter = count(0)
        def update_func():
            label.config(text=str(next(counter)))
            label.after(1000, update_func)  # 1000ms
        update_func()
    
    root = tk.Tk()
    root.wm_title("Turbulance Window Readings")

    close_time = time.time()+60

    data = ser.readline()
    data_point = data.decode()

    turbulance = []

    if data_point != '':
        print(data_point)
        turbulance.append(data_point.strip())

    finalDict = {'Turbulance':turbulance}
    def _quit():
        print(finalDict)
        df = pd.DataFrame(finalDict)
        df.to_csv(path + 'turbulance.csv', index=False, mode='w')
        root.quit()     # stops mainloop
        root.destroy()
    
    label = tk.Label(root, fg="red")
    label.pack()
    start_counter(label)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    tk.mainloop()


def take_readings_pH():
    
    def start_counter(label):
        counter = count(0)
        def update_func():
            label.config(text=str(next(counter)))
            label.after(1000, update_func)  # 1000ms
        update_func()
    
    root = tk.Tk()
    root.wm_title("pH Window Readings")

    close_time = time.time()+60

    data = ser.readline()
    data_point = data.decode()

    pH = []

    if data_point != '':
        print(data_point)
        pH.append(data_point.strip())

    finalDict = {'pH':pH}

    def _quit():
        print(finalDict)
        df = pd.DataFrame(finalDict)
        df.to_csv(path + 'pH.csv', index=False)
        root.quit()     # stops mainloop
        root.destroy()
    
    label = tk.Label(root, fg="red")
    label.pack()
    start_counter(label)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)
    tk.mainloop()


class Switch(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, pH, Turbulance, Analysis, Results):
            frame = F(self.container, self)
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")  
        self.show_frame(StartPage)

    def refresh_frame(self):
        for F in (StartPage, pH, Turbulance, Analysis, Results):
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

        b1 = tk.Button(self, text="pH", command= lambda: controller.show_frame(pH))
        b1.pack()
        b2 = tk.Button(self, text="Turbulance", command= lambda: controller.show_frame(Turbulance))
        b2.pack()
        b3 = tk.Button(self, text="Send For Analysis", command = lambda: controller.show_frame(Analysis))
        b3.pack()

class pH(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="pH")
        label.pack(pady=10,padx=10)
        b1 = tk.Button(self, text="Start", command=take_readings_pH)
        b1.pack()
        b3 = tk.Button(self, text="Back to Home", command= lambda: controller.show_frame(StartPage))
        b3.pack()

class Turbulance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Turbulance")
        label.pack(pady=10,padx=10)
        b1 = tk.Button(self, text="Start", command=take_readings_turbulance)
        b1.pack()
        b2 = tk.Button(self, text="Back to Home", command= lambda: controller.show_frame(StartPage))
        b2.pack()

class Analysis():
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        if exists(path+'pH.csv') == True and exists(path+'turbulance.csv') == True:
            pH_data = pd.read_csv(path+'pH.csv')
            turb_data = pd.read_csv(path+'turbulance.csv')

            pH_data = pH_data['pH']
            pH = pH_data.to_list()
            turb_data = turb_data['Turbulance']
            turb = turb_data.to_list()
            final_dict = {'pH':pH, 'Turbulance':turb}
            df = pd.DataFrame(final_dict)
            df.to_csv(path+"ph_turb_data.csv", index=False)

        if exists(path+"ph_turb_data.csv"):
            b3 = tk.Button(self, text="Analyse", command = lambda: controller.show_frame(Results))
            b3.pack()

class Results():
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        data = pd.read_csv(path+"ph_turb_data.csv")
        pred = rf_clf.predict(data)
        print(pred)
        ans = np.bincount(pred).argmax()
        if ans == 0:
            label = tk.Label(self, text = "Clean")
            label.pack(padx=10, pady=10)
        elif ans == 1:
            label = tk.Label(self, text = "Dirty")
            label.pack(padx=10, pady=10)