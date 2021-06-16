from flask import Flask, render_template, request
from reports import SolReport
import weather_run as wr
import os

app = Flask(__name__)

# Curiosity Rover
cab_rems_url = 'http://cab.inta-csic.es/rems/rems_weather.xml'  # Info: http://cab.inta-csic.es/rems/#slide-to-main
maas2_apollorion_url = 'https://api.maas2.apollorion.com/'  # Info: https://programmableweb.com/api/maas2-rest-api-v100

source_url = 'curiosity_maas2'
sol, report = wr.request_latest_report(source=source_url)
sr = SolReport(sol, report)
rep_dict = sr.create_report_dict()
sol_dict = rep_dict.get(sol)

@app.route("/")
def index():
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=sol_dict.get('min_temp'),
                           max_temp=sol_dict.get('max_temp'), pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), ls=sol_dict.get('ls'), month=sol_dict.get('month'),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), last_updated=dir_last_updated('./static'))

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

@app.route("/convert-to-c")
def convert_to_c():
    f_max = int(sol_dict.get('max_temp'))
    c_max = int((f_max - 32) * (5 / 9))
    f_min = int(sol_dict.get('min_temp'))
    c_min = int((f_min - 32) * (5 / 9))
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=c_min,
                           max_temp=c_max, pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), ls=sol_dict.get('ls'), month=sol_dict.get('month'),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), last_updated=dir_last_updated('./static'))

@app.route("/convert-to-f")
def convert_to_f():
    """Currently Curiosity returns in F"""
    # self.max_temp_f = self.max_temp
    # c = (self.max_temp.get() - 32) * (5 / 9)
    # self.max_temp_c = tk.IntVar()
    # self.max_temp_c.set(c)
    # self.min_temp_f = self.min_temp
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=sol_dict.get('min_temp'),
                           max_temp=sol_dict.get('max_temp'), pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), ls=sol_dict.get('ls'), month=sol_dict.get('month'),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), last_updated=dir_last_updated('./static'))


if __name__ == '__main__':

    app.run(debug=True)
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# index()