import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
from tkinter.constants import *
from tkinter import font

HEIGHT = 320
WIDTH = 480
pil_image = Image.open(r'resources/mars_background.jpg').resize((WIDTH, HEIGHT), Image.ANTIALIAS)
thermometer = Image.open(r"resources/Thermometer.png").resize((40, 40), Image.ANTIALIAS)
forecast_img = r'resources/sun.png'
FONT = 'Corbel'
BACKGROUND_COLOR = 'gray15'
FOREGROUND_COLOR = 'snow'


class WeatherDashboard(tk.Frame):
    def __init__(self, master, report):
        tk.Frame.__init__(self, master)
        self.master = master
        self.report = report
        self.sol = self.report.name
        self.left_frame = tk.Frame(self.master, height=HEIGHT, width=WIDTH / 2, bg=BACKGROUND_COLOR)
        self.left_frame.pack(side=LEFT)
        self.left_frame.pack_propagate(False)
        self.right_frame = tk.Frame(self.master, height=HEIGHT, width=WIDTH / 2, bg=BACKGROUND_COLOR)
        self.right_frame.pack(side=RIGHT)
        self.right_frame.pack_propagate(False)
        self.left_frame_widget(self.left_frame)
        self.right_frame_widgets(self.right_frame)

    def left_frame_widget(self, frame):
        sol_label = tk.Label(frame, text='Sol\n{}'.format(self.report.name),
                             font=(FONT, 22), bg=BACKGROUND_COLOR,
                             fg=FOREGROUND_COLOR)
        sol_label.pack(padx=0, pady=20)
        date_label = tk.Label(frame, text='{}'.format(self.report.terrestrial_date),
                              font=(FONT, 14), bg=BACKGROUND_COLOR,
                              fg=FOREGROUND_COLOR)
        date_label.pack(padx=0, pady=0)
        ls_label = tk.Label(frame, text='{}° Ls'.format(self.report.solar_longitude), font=(FONT, 16),
                            bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        ls_label.pack(padx=0, pady=20)
        tk.Label(frame, text='{}'.format(self.report.month), font=(FONT, 16), bg=BACKGROUND_COLOR,
                 fg=FOREGROUND_COLOR).pack(padx=0, pady=20)

    def right_frame_widgets(self, frame):
        """Defines details of properties of Sol from report"""
        fframe = tk.Frame(frame, height=150, width=750, bg=BACKGROUND_COLOR)
        fframe.pack()
        self.forecast_frame(fframe)
        tframe = tk.Frame(frame, height=150, width=750, bg=BACKGROUND_COLOR)
        tframe.pack()
        self.temperature_frame(tframe)
        # tk.Label(frame,
        #          text='Max Temperature {}°F\nMin Temperature {}°F'.format(self.report.max_temp,
        #                                                                   self.report.min_temp),
        #          font=(FONT, 13),
        #          bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(padx=0, pady=15)
        tk.Label(frame,
                 text='Sunset {}\nSunrise {}'.format(self.report.sunset, self.report.sunrise),
                 font=(FONT, 13),
                 bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(padx=0, pady=15)

    def forecast_frame(self, frame):
        fimg = ImageTk.PhotoImage(Image.open(forecast_img).resize((40, 40), Image.ANTIALIAS))
        image_label = tk.Label(frame, image=fimg, bg=BACKGROUND_COLOR)
        image_label.image = fimg
        image_label.pack(side=LEFT, padx=5, pady=45)
        atm_label = tk.Label(frame,
                             text='{}'.format(self.report.atm_opacity),
                             font=(FONT, 17),
                             bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        atm_label.pack(side=RIGHT, padx=5, pady=45)

    def temperature_frame(self, frame):
        timg = ImageTk.PhotoImage(thermometer)
        image_label = tk.Label(frame, image=timg, bg=BACKGROUND_COLOR)
        image_label.image = timg
        image_label.pack(side=LEFT, padx=0, pady=15)
        tk.Label(frame,
                 text='Max Temperature {}°F\nMin Temperature {}°F'.format(self.report.max_temp,
                                                                          self.report.min_temp),
                 font=(FONT, 13),
                 bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(side=RIGHT, padx=0, pady=15)

    def insert_background_canvas(self):
        canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        canvas.pack()
        background_img = ImageTk.PhotoImage(pil_image)
        canvas.create_image(0, 0, image=background_img, anchor=NW)
        canvas.image = background_img

    def insert_background_pillow(self):
        background_img = ImageTk.PhotoImage(pil_image)
        image_label = tk.Label(image=background_img)
        image_label.image = background_img
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        image_label.pack()


class WeatherWebApp(object):
    def __init__(self, report):
        self.report = report
        self.sol = self.report.name




# def display_font(self):
#     frame = tk.Frame()
#     frame.pack()
#     print(len(font.families()))
#     for f in font.families()[:50]:
#         tk.Label(frame, text='THIS IS {}'.format(f), font=(f, 12)).pack()
