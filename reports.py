import pandas as pd
import json
import os

from datetime import datetime, date


class SolReport(object):
    def __init__(self, sol, report):
        self.sol = sol
        self.report = report
        self.json_file = r'./resources/historical_reports.json'
        self.min_temp = None
        self.max_temp = None
        self.pressure = None
        self.atm_opacity = None
        self.ls = None
        self.month = None
        self.sunrise_time = None
        self.sunset_time = None
        self.terretrial_date = None
        self.define_parameters()

    def define_parameters(self):
        self.min_temp = self.report.get('min_temp')
        self.max_temp = self.report.get('max_temp')
        self.pressure = self.report.get('pressure')
        self.atm_opacity = self.report.get('atmo_opacity')
        self.ls = self.report.get('ls')
        self.month = self.report.get('season')
        self.sunrise_time = self.report.get('sunrise')
        self.sunset_time = self.report.get('sunset')
        self.terretrial_date = self.define_terrestrial_date()

    def define_terrestrial_date(self):
        """Extracts terrestrial date from source or leaves it blank"""
        self.terretrial_date = self.report.get('terrestrial_date')
        if self.terretrial_date is None:
            return ''
        else:
            d = datetime.strptime(self.terretrial_date, '%Y-%m-%dT%H:%M:%S.000Z')
            return datetime.strftime(d, '%d %b %Y')

    def create_report_table(self):
        """Creates a dataframe table of all parameters of the report"""
        report_index = ['min_temp', 'max_temp', 'pressure', 'atm_opacity', 'solar_longitude', 'month', 'sunrise',
                        'sunset', 'terrestrial_date']
        report_data = [self.min_temp, self.max_temp, self.pressure,
                       self.atm_opacity, self.ls, self.month, self.sunrise_time, self.sunset_time,
                       self.terretrial_date]
        report_data = ['' if elem is None else elem for elem in report_data]
        report_df = pd.Series(data=report_data, index=report_index)
        report_df.name = self.sol
        return report_df

    def create_report_dict(self):
        report_dict = {self.sol: {'min_temp': self.min_temp,
                                  'max_temp': self.max_temp,
                                  'pressure': self.pressure,
                                  'atmo_opacity': self.atm_opacity,
                                  'ls': self.ls,
                                  'month': self.month,
                                  'sunrise_time': self.sunrise_time,
                                  'sunset_time': self.sunset_time,
                                  'terrestrial_date': self.terretrial_date}}
        return report_dict

    def return_earth_date(self, mission='curiosity'):
        """Converts the Sol to a corresponding Earth date.
        The Sol number is the amount of sol days the rover/lander has spent in Mars. Default assuments is Curiosity
        August 5, 2012, PDT
        """
        pass

    def check_existing_sol(self):
        """Returns True if Sol number exists in json file"""
        with open(self.json_file, mode='r') as f:
            j_report = json.load(f)
        for j in j_report:
            if str(self.sol) in list(j.keys())[0]:
                return True

    def save_report(self, data, file_type='json'):
        a = []
        if not os.path.isfile(self.json_file):
            a.append(data)
            with open(self.json_file, mode='w') as f:
                f.write(json.dumps(a, indent=2))
        else:
            with open(self.json_file) as feedsjson:
                feeds = json.load(feedsjson)
            if self.check_existing_sol() is not True:
                print("New entry in json for Sol {}".format(self.sol))
                if isinstance(feeds, dict):
                    feeds = [feeds]
                feeds.append(data)
                with open(self.json_file, mode='w') as f:
                    f.write(json.dumps(feeds, indent=2))
            else:
                print("Sol {} already exists in json".format(self.sol))
