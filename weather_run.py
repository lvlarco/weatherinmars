# -*- coding: utf-8 -*-

# from weather_gui import WeatherDashboard
from reports import SolReport
from requests.exceptions import RequestException
# import tkinter as tk
import requests
import xmltodict

# Input
rover = 'curiosity'
api = 'maas2'

# Curiosity Rover
cab_rems_url = 'http://cab.inta-csic.es/rems/rems_weather.xml'  # Info: http://cab.inta-csic.es/rems/#slide-to-main
maas2_apollorion_url = 'https://api.maas2.apollorion.com/'  # Info: https://programmableweb.com/api/maas2-rest-api-v100

# Perseverance Rover
m2020_nasa_url = 'https://mars.nasa.gov/rss/api/?feed=weather&category=mars2020&feedtype=json'  # From Percy's weather site

source_dict = {'curiosity_maas2': maas2_apollorion_url,
               'curiosity_cab': cab_rems_url,
               'perseverance_nasa': m2020_nasa_url}


def request_latest_report(rover='curiosity', api='maas2'):
    """Returns the Sol and dictionary data from the specified source url. Defaults to curiosity_maas2

    :param rover: name of rover/lander. Supports 'curiosity' or 'perseverance'
    :type rover: str
    :param api: API source. Supports 'cab', 'maas2' for Curiosity, and 'nasa' for Perseverance
    :type api: str
    """
    source = '{}_{}'.format(rover, api)
    try:
        if source == 'curiosity_cab':
            resp = requests.get(source_dict.get(source))
            data = xmltodict.parse(resp.content).get('weather_report')
            return data.get('sol'), data.get('magnitudes')
        elif source == 'curiosity_maas2':
            data = requests.get(source_dict.get(source)).json()
            return data.get('sol'), data
        elif source == 'perseverance_nasa':
            data = requests.get(source_dict.get(source)).json().get('sols')
            sdata = sorted(data, key=lambda d: d.get('sol'), reverse=True)
            return sdata[0].get('sol'), sdata[0]
        else:
            raise Exception('Please select a valid source for data extraction')
    except RequestException as e:
        print(type(e), e)


def request_sol_report(sol):
    """Returns a report for a specific Sol. Only works for MAAS2 API

    :param sol: Sol value to be extracted
    :type sol: str
    """
    try:
        return requests.get(maas2_apollorion_url + str(sol)).json()
    except RequestException as e:
        print(type(e), e)


if __name__ == '__main__':
    sol, report = request_latest_report(rover=rover, api=api)
    sr = SolReport(sol, report, rover)
    metadata_df = sr.create_report_table()
    print(metadata_df)
    # sr.save_report(sr.create_report_dict(), file_type='json')
    # root = tk.Tk()
#     WeatherDashboard(root, metadata_df)
#     root.mainloop()
