# -*- coding: utf-8 -*-

import tkinter as tk
import pandas as pd
import numpy as np
from reports import SolReport
import weather_run as wr
from PIL import Image, ImageTk
from tkinter.constants import CENTER, RIGHT, LEFT, TOP, BOTTOM, NW, NE, SW, SE
from datetime import datetime

HEIGHT = 320
WIDTH = 480
pil_image = Image.open(r'static/curiosity.jpg').resize((WIDTH, HEIGHT), Image.ANTIALIAS)
thermometer = Image.open(r"resources/Thermometer.png").resize((40, 40), Image.ANTIALIAS)
forecast_img = r'static/sun.png'
FONT = 'Roboto'
BACKGROUND_COLOR = 'gray15'
FOREGROUND_COLOR = 'snow'
COLOR1 = '#ECF0F1'
COLOR2 = '#E8D3D3'
PADDING = WIDTH * 0.08

source_url = 'curiosity_maas2'


class WeatherDashboard(tk.Frame):
    def __init__(self, master, report):
        tk.Frame.__init__(self, master)
        self.master = master
        self.report = report
        self.sol = self.report.name
        self.max_temp = tk.IntVar()
        self.max_temp.set(int(self.report.max_temp))
        self.min_temp = tk.IntVar()
        self.min_temp.set(int(self.report.min_temp))
        self.calculate_temps()
        self.counter_btn = 1
        self.p1, self.p2, self.p3, self.p4 = [np.nan] * 4
        self.calc_canvas_points(PADDING)

        # self.left_frame = tk.Frame(self.master, height=HEIGHT, width=WIDTH / 2, bg=BACKGROUND_COLOR)
        # self.left_frame.pack(side=LEFT)
        # self.left_frame.pack_propagate(False)
        # self.right_frame = tk.Frame(self.master, height=HEIGHT, width=WIDTH / 2, bg=BACKGROUND_COLOR)
        # self.right_frame.pack(side=RIGHT)
        # self.right_frame.pack_propagate(False)
        # self.left_frame_widget(self.left_frame)
        # self.right_frame_widgets(self.right_frame)
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.insert_background_canvas()
        self.init_temps_canvas()
        self.init_suntime_canvas()
        self.init_location_canvas()
        self.init_sol_canvas()
        self.init_uom_button()
        self.update_report()

        # self.insert_background_pillow()

    # def left_frame_widget(self, frame):
    #     ls_label = tk.Label(frame, text='{}° Ls'.format(self.report.solar_longitude), font=(FONT, 16),
    #                         bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    #     ls_label.pack(padx=0, pady=20)
    #     tk.Label(frame, text='{}'.format(self.report.month), font=(FONT, 16), bg=BACKGROUND_COLOR,
    #              fg=FOREGROUND_COLOR).pack(padx=0, pady=20)
    #
    # def date_frame(self, frame):
    #     sol_label = tk.Label(frame, text='Sol'.format(self.report.name),
    #                          font=(FONT, 22), bg=BACKGROUND_COLOR,
    #                          fg=FOREGROUND_COLOR)
    #     sol_label.pack(padx=0, pady=20)
    #     sol_value_label = tk.Label(frame, text='{}'.format(self.report.name),
    #                                font=(FONT, 22), bg=BACKGROUND_COLOR,
    #                                fg=FOREGROUND_COLOR)
    #     sol_value_label.pack(padx=0, pady=20)
    #     date_label = tk.Label(frame, text='{}'.format(self.report.terrestrial_date),
    #                           font=(FONT, 14), bg=BACKGROUND_COLOR,
    #                           fg=FOREGROUND_COLOR)
    #     date_label.pack(padx=0, pady=0)
    #
    # def right_frame_widgets(self, frame):
    #     """Defines details of properties of Sol from report"""
    #     fframe = tk.Frame(frame, height=150, width=750, bg=BACKGROUND_COLOR)
    #     fframe.pack()
    #     self.forecast_frame(fframe)
    #     tframe = tk.Frame(frame, height=150, width=750, bg=BACKGROUND_COLOR)
    #     tframe.pack()
    #     self.temperature_frame(tframe)
    #     # tk.Label(frame,
    #     #          text='Max Temperature {}°F\nMin Temperature {}°F'.format(self.report.max_temp,
    #     #                                                                   self.report.min_temp),
    #     #          font=(FONT, 13),
    #     #          bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(padx=0, pady=15)
    #     tk.Label(frame,
    #              text='Sunset {}\nSunrise {}'.format(self.report.sunset, self.report.sunrise),
    #              font=(FONT, 13),
    #              bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(padx=0, pady=15)
    #
    # def forecast_frame(self, frame):
    #     fimg = ImageTk.PhotoImage(Image.open(forecast_img).resize((40, 40), Image.ANTIALIAS))
    #     image_label = tk.Label(frame, image=fimg, bg=BACKGROUND_COLOR)
    #     image_label.image = fimg
    #     image_label.pack(side=LEFT, padx=5, pady=45)
    #     atm_label = tk.Label(frame,
    #                          text='{}'.format(self.report.atm_opacity),
    #                          font=(FONT, 17),
    #                          bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
    #     atm_label.pack(side=RIGHT, padx=5, pady=45)
    #
    # def temperature_frame(self, frame):
    #     timg = ImageTk.PhotoImage(thermometer)
    #     image_label = tk.Label(frame, image=timg, bg=BACKGROUND_COLOR)
    #     image_label.image = timg
    #     image_label.pack(side=LEFT, padx=0, pady=15)
    #     tk.Label(frame,
    #              text='Max Temperature {}°F\nMin Temperature {}°'.format(self.max_temp.get(),
    #                                                                      self.min_temp.get()),
    #              font=(FONT, 13),
    #              bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR).pack(side=RIGHT, padx=0, pady=15)

    def insert_background_canvas(self):
        background_img = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, image=background_img, anchor=NW)
        self.canvas.image = background_img

    def init_temps_canvas(self):
        """Canvas to display Max and Min temps, atmo opacity"""
        x_off, y_off = (-95, 50)
        off_center = 1
        anchor_p = self.p2
        # Temps
        self.max_temp_canvas = self.canvas.create_text(anchor_p[0] + x_off, anchor_p[1] + y_off,
                                                       anchor=CENTER,
                                                       text='{}°'.format(self.max_temp.get()),
                                                       font=(FONT, 50, 'bold'),
                                                       fill=COLOR1)
        self.canvas.create_text(anchor_p[0] + x_off + 15, anchor_p[1] + y_off + 72 + 12,
                                anchor=SW,
                                text='LOW',
                                font=(FONT, 6, 'bold'),
                                fill=COLOR2)
        self.min_temp_canvas = self.canvas.create_text(anchor_p[0] + x_off, anchor_p[1] + y_off + 72,
                                                       anchor=CENTER,
                                                       text='{}°'.format(self.min_temp.get()),
                                                       font=(FONT, 18, 'bold'),
                                                       fill=COLOR1)

    def init_suntime_canvas(self):
        """Creates canvas text for Sunset and Sunrise times"""
        x_off, y_off = (-95, -12)
        off_center = 6
        anchor_p = self.p4
        # Sunrise/Sunset

        self.canvas.create_text(anchor_p[0] - 100, anchor_p[1] + y_off - 29,
                                anchor=SE,
                                text='SUNRISE',
                                font=(FONT, 8, 'bold'),
                                fill=COLOR2)

        self.canvas.create_text(anchor_p[0] - 100, anchor_p[1] + y_off,
                                anchor=SE,
                                text=self.report.sunrise,
                                font=(FONT, 22, 'bold'),
                                fill=COLOR1)

        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off - 29,
                                anchor=SE,
                                text='SUNSET',
                                font=(FONT, 8, 'bold'),
                                fill=COLOR2)
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off,
                                anchor=SE,
                                text=self.report.sunset,
                                font=(FONT, 22, 'bold'),
                                fill=COLOR1)

    def init_location_canvas(self):
        """Creates canvas text for Sunset and Sunrise times"""
        x_off, y_off = (22, 5)
        anchor_p = self.p1
        # Location
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off,
                                anchor=NW,
                                text='Gale Crater,',
                                font=(FONT, 14),
                                fill=COLOR2)
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off + 16,
                                anchor=NW,
                                text='MARS',
                                font=(FONT, 40, 'bold'),
                                fill=COLOR1)
        # Date
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off + 110,
                                anchor=SW,
                                text=self.report.terrestrial_date,
                                font=(FONT, 14, 'bold'),
                                fill=COLOR1)

    def init_sol_canvas(self):
        """Creates canvas for Sol and Terrestrial date"""
        x_off, y_off = (22, -12)
        anchor_p = self.p3
        # Location
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off - 34,
                                anchor=SW,
                                text='SOL',
                                font=(FONT, 11, 'bold'),
                                fill=COLOR2)
        self.canvas.create_text(anchor_p[0], anchor_p[1] + y_off + 5,
                                anchor=SW,
                                text=self.report.name,
                                font=(FONT, 30, 'bold'),
                                fill=COLOR1)

    def insert_background_pillow(self):
        background_img = ImageTk.PhotoImage(pil_image)
        image_label = tk.Label(image=background_img)
        image_label.image = background_img
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        image_label.pack()

    def calc_canvas_points(self, padding):
        """Calculates the four points of the canvas depending on height and width of screen. Measured
        from 0, 0 at the top left corner

        p1 ---------------- p2
        |                   |
        |                   |
        |                   |
        p3 ---------------- p4

        :param padding: value to create an offset from screen edges
        :type padding: int (in pixels)
        """
        p1 = [0, 0]
        p2 = [WIDTH, 0]
        p3 = [0, HEIGHT]
        p4 = [WIDTH, HEIGHT]

        self.p1 = [p + padding for p in p1]
        self.p2 = [p2[0] - padding, p2[1] + padding]
        self.p3 = [p3[0] + padding, p3[1] - padding]
        self.p4 = [p - padding for p in p4]

    def init_uom_button(self):
        """Creates a widget button that converts Units of Measure when clicked"""
        self.uom_btn = tk.Button(self.master, text='°F',
                                 font=(FONT, 12, 'bold'),
                                 # fg=COLOR2,
                                 # bg='#DE7D7D',
                                 command=self.update_temps)
        # button_img = Image.open('resources/ftoc.JPG').resize((40, 40))
        img_size = 35
        self.master.ftoc_img = ImageTk.PhotoImage(Image.open('resources/ftoc.JPG').resize((img_size, img_size)))
        self.master.ctof_img = ImageTk.PhotoImage(Image.open('resources/ctof.JPG').resize((img_size, img_size)))
        self.uom_btn.configure(activebackground="#33B5E5", relief='flat', image=self.master.ftoc_img)
        self.canvas.create_window(self.p2[0] - 25, self.p2[1] + 82, anchor=SW, window=self.uom_btn)

    def update_temps(self):
        """Updates the corresponding UoM temperature in UI"""
        self.counter_btn += 1
        # Odd - F, Even - C
        if (self.counter_btn % 2) == 0:  # if even (C)
            max_temp_val = self.max_temp_c.get()
            min_temp_val = self.min_temp_c.get()
            # btn_text = '°C'
            btn_img = self.master.ctof_img
        else:  # if odd (F)
            max_temp_val = self.max_temp_f.get()
            min_temp_val = self.min_temp_f.get()
            # btn_text = '°F'
            btn_img = self.master.ftoc_img
        try:
            self.canvas.itemconfigure(self.max_temp_canvas, text='{}°'.format(max_temp_val))
            self.canvas.itemconfigure(self.min_temp_canvas, text='{}°'.format(min_temp_val))
            self.uom_btn.configure(image=btn_img)
            # self.master.itemconfigure(self.uom_btn, text='°C')
            # self.master.after(10, self.update_temps)
        except StopIteration as e:
            print(e)

    def update_report(self):
        """Updates the report once a day"""
        s, r = wr.request_latest_report(source=source_url)
        sr = SolReport(s, r)
        self.report = sr.create_report_table()
        self.master.after(86400000, self.update_report)
        print('Report updated on {}'.format(datetime.now().strftime('%Y-%m-%d at %H:%M')))

    def calculate_temps(self):
        """Calculates the min and max temperatures in F and C.
        Assumes source data is originally in F."""
        # F to C
        self.max_temp_f = self.max_temp
        c = (self.max_temp.get() - 32) * (5 / 9)
        self.max_temp_c = tk.IntVar()
        self.max_temp_c.set(c)
        self.min_temp_f = self.min_temp
        c = (self.min_temp.get() - 32) * (5 / 9)
        self.min_temp_c = tk.IntVar()
        self.min_temp_c.set(c)

        # #C to F - not implemented yet
        # f = (self.max_temp.get() * 1.8) + 32
        # self.max_temp_f.set(f)

    # def display_font(self):
    #     frame = tk.Frame()
    #     frame.pack()
    #     print(len(font.families()))
    #     for f in font.families()[:50]:
    #         tk.Label(frame, text='THIS IS {}'.format(f), font=(f, 12)).pack()


if __name__ == '__main__':
    sol, report = wr.request_latest_report(source=source_url)
    sr = SolReport(sol, report)
    metadata_df = sr.create_report_table()
    # sr.save_report(sr.create_report_dict(), file_type='json')
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    WeatherDashboard(root, metadata_df)
    root.mainloop()
