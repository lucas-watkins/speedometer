from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from speedtest import SpeedTest, Previous
import plotting as plting
from datetime import timedelta
from threading import Thread

app = Flask('Speedometer')


def get_last_speed_test() -> str:
    if len(Previous.tests) <= 0:
        return 'No Tests Yet'
    test = Previous.tests[len(Previous.tests) - 1]
    return f'Latest Test: | Download {test.download_speed} mbps | Upload {test.upload_speed} mbps |'


@app.route('/')
def main_route() -> str:
    return render_template('index.html',
                           hourly_plot=plting.gen_plot(timedelta(hours=1), 'Hourly Bandwidth'),
                           daily_plot=plting.gen_plot(timedelta(days=1), 'Daily Bandwidth'),
                           weekly_plot=plting.gen_plot(timedelta(days=7), 'Average 7-Day Bandwith'), 
                           monthly_plot=plting.gen_plot(timedelta(days=30), 'Average 30-Day Bandwidth'),
                           last_speed_test=get_last_speed_test()
                           )


@app.route('/speedtest')
async def speedtest_on_demand() -> str:
    Thread(target=SpeedTest().run).start()
    return render_template('speedtest.html')


if __name__ == '__main__':
    try:
        WSGIServer(('0.0.0.0', 80), app).serve_forever()
        Previous.pickle_tests()
    except KeyboardInterrupt:
        Previous.pickle_tests()
