from flask import Flask, render_template
from reports import SolReport
from resources.mappers import ATMO_IMG, ROVER_LOC
from weather_run import request_latest_report
import os

app = Flask(__name__)

# Curiosity Rover
cab_rems_url = 'http://cab.inta-csic.es/rems/rems_weather.xml'  # Info: http://cab.inta-csic.es/rems/#slide-to-main
maas2_apollorion_url = 'https://api.maas2.apollorion.com/'  # Info: https://programmableweb.com/api/maas2-rest-api-v100

rover = 'curiosity'
api_source = 'maas2'
sol, report = request_latest_report(rover, api_source)
sr = SolReport(sol, report, rover)
rep_dict = sr.create_report_dict()
sol_dict = rep_dict.get(sol)
atmo_img = ATMO_IMG.get(sol_dict.get('atmo_opacity').lower())
rov_loc = ROVER_LOC.get(rover)


@app.route("/")
def index():
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=sol_dict.get('min_temp'),
                           max_temp=sol_dict.get('max_temp'), pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), atmo_img=atmo_img,
                           ls=sol_dict.get('ls'), season=sol_dict.get('season').upper(),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), rover_location=rov_loc,
                           last_updated=dir_last_updated('./static'))


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


@app.route("/convert-to-f")
def convert_to_f():
    """Converts temp from rover's API to Fahrenheit"""
    flist = []
    for t in ['min_temp', 'max_temp']:
        c = int(sol_dict.get(t))
        f = int((c * 9 / 5) + 32)
        flist.append(f)
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=flist[0],
                           max_temp=flist[1], pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), atmo_img=atmo_img,
                           ls=sol_dict.get('ls'),
                           season=sol_dict.get('season').upper(),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), rover_location=rov_loc,
                           last_updated=dir_last_updated('./static'))


@app.route("/convert-to-c")
def convert_to_c():
    """Currently Curiosity returns temps in C"""
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=sol_dict.get('min_temp'),
                           max_temp=sol_dict.get('max_temp'), pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity').upper(), atmo_img=atmo_img,
                           ls=sol_dict.get('ls'),
                           season=sol_dict.get('season').upper(),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'), rover_location=rov_loc,
                           last_updated=dir_last_updated('./static'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# index()
