import pandas as pd
import json
import os

from datetime import datetime, date


class SolReport(object):
    def __init__(self, sol, report, rover):
        self.sol = sol
        self.report = report
        self.rover = rover
        self.json_file = r'./resources/{}_historical_reports.json'.format(self.rover)
        self.uom_temp = self.define_uom_temp()
        self.min_temp = None
        self.max_temp = None
        self.pressure = None
        self.atm_opacity = None
        self.ls = None
        self.season = None
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
        self.season = self.define_mars_season()
        self.sunrise_time, self.sunset_time = self.format_suntime()
        self.terretrial_date = self.format_terrestrial_date()

    def define_uom_temp(self):
        """Currently MAAS2 and Percy's NASA API return temp in Celsius"""
        return 'celsius'

    def define_mars_season(self):
        """Defines the season in Mars. If API returns a value for a season, returns that value. Else it will calculate
        the season based on the solar longitude 'ls'
        """
        if self.rover == 'curiosity':
            if self.ls is not None:
                if 0 <= int(self.ls) < 90:
                    return 'Spring'
                elif 90 <= int(self.ls) < 180:
                    return 'Summer'
                elif 180 <= int(self.ls) < 270:
                    return 'Autum'
                else:
                    return 'Winter'
            else:
                return self.report.get('season').title()
        else:
            return self.report.get('season').title()

    def format_suntime(self):
        """Formats sunrise and sunset time to format %H:%M"""
        slist = []
        if self.rover == 'perseverance':
            try:
                for s in ['sunrise', 'sunset']:
                    stime = datetime.strptime(self.report.get(s), '%H:%M:%S')
                    slist.append(datetime.strftime(stime, '%H:%M'))
                return slist[0], slist[1]
            except ValueError as e:
                print(type(e), e)
        else:
            return self.report.get('sunrise'), self.report.get('sunset')

    def format_terrestrial_date(self):
        """Extracts terrestrial date from source or leaves it blank"""
        self.terretrial_date = self.report.get('terrestrial_date')
        if self.terretrial_date is None:
            return ''
        else:
            if self.rover == 'curiosity':
                d = datetime.strptime(self.terretrial_date, '%Y-%m-%dT%H:%M:%S.000Z')
                return datetime.strftime(d, '%d %b %y')
            else:
                d = datetime.strptime(self.terretrial_date, '%Y-%m-%d')
                return datetime.strftime(d, '%d %b %y')

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
        """Creates a dictionary with key-value pair to be saved into json"""
        report_dict = {self.sol: {'min_temp': self.min_temp,
                                  'max_temp': self.max_temp,
                                  'pressure': self.pressure,
                                  'atmo_opacity': self.atm_opacity,
                                  'ls': self.ls,
                                  'season': self.season,
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
                print('Created new json for {}. Entry for Sol {}'.format(self.rover.capitalize(), self.sol))
        else:
            with open(self.json_file) as feedsjson:
                feeds = json.load(feedsjson)
            if self.check_existing_sol() is not True:
                print("New entry in json for {} Sol {}".format(self.rover.capitalize(), self.sol))
                if isinstance(feeds, dict):
                    feeds = [feeds]
                feeds.append(data)
                with open(self.json_file, mode='w') as f:
                    f.write(json.dumps(feeds, indent=2))
            else:
                print("{} record for Sol {} already exists in json".format(self.rover.capitalize(), self.sol))
