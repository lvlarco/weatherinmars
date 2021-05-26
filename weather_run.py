# from weather_gui import WeatherDashboard
from reports import SolReport
from requests.exceptions import RequestException
import tkinter as tk
import requests
import xmltodict

# Curiosity Rover
cab_rems_url = 'http://cab.inta-csic.es/rems/rems_weather.xml'  # Info: http://cab.inta-csic.es/rems/#slide-to-main
maas2_apollorion_url = 'https://api.maas2.apollorion.com/'  # Info: https://www.programmableweb.com/api/maas2-rest-api-v100

source_url = 'curiosity_maas2'


def request_latest_report(source):
    try:
        if source == 'curiosity_cab':
            resp = requests.get(cab_rems_url)
            data = xmltodict.parse(resp.content).get('weather_report')
            return data.get('sol'), data.get('magnitudes')
        elif source == 'curiosity_maas2':
            data = requests.get(maas2_apollorion_url).json()
            return data.get('sol'), data
        else:
            raise Exception('Please select a valid source for data extraction')
    except RequestException as e:
        print(e)


def request_sol_report(sol):
    """Returns a report for a specific Sol. Only works for MAAS2 API

    :param sol: str. Sol value to be extracted
    """
    try:
        return requests.get(maas2_apollorion_url + str(sol)).json()
    except RequestException as e:
        print(e)


# sol, report = request_latest_report(source=source_url)
# sr = SolReport(sol, report)
# metadata_df = sr.create_report_table()
# sr.save_report(sr.create_report_dict(), file_type='json')
# root = tk.Tk()
# WeatherDashboard(root, metadata_df)
# root.mainloop()
