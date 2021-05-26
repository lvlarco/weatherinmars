from flask import Flask, render_template, request
from reports import SolReport
import weather_run as wr

app = Flask(__name__)

# Curiosity Rover
cab_rems_url = 'http://cab.inta-csic.es/rems/rems_weather.xml'  # Info: http://cab.inta-csic.es/rems/#slide-to-main
maas2_apollorion_url = 'https://api.maas2.apollorion.com/'  # Info: https://www.programmableweb.com/api/maas2-rest-api-v100

source_url = 'curiosity_maas2'

@app.route("/")
def index():
    sol, report = wr.request_latest_report(source=source_url)
    sr = SolReport(sol, report)
    rep_dict = sr.create_report_dict()
    sol_dict = rep_dict.get(sol)
    return render_template('index.html', sol=list(rep_dict.keys())[0], min_temp=sol_dict.get('min_temp'),
                           max_temp=sol_dict.get('max_temp'), pressure=sol_dict.get('pressure'),
                           atmo_opacity=sol_dict.get('atmo_opacity'), ls=sol_dict.get('ls'), month=sol_dict.get('month'),
                           sunrise_time=sol_dict.get('sunrise_time'), sunset_time=sol_dict.get('sunset_time'),
                           terrestrial_date=sol_dict.get('terrestrial_date'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# index()