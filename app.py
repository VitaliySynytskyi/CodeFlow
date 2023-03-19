from datetime import datetime
from applicationinsights import TelemetryClient
from applicationinsights.flask.ext import AppInsights
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = 'e3f5ef91-2bac-4e31-b7bd-cea717f7aaad'
telemetry_client = TelemetryClient('e3f5ef91-2bac-4e31-b7bd-cea717f7aaad')
AppInsights(app)


@app.errorhandler(Exception)
def log_exception(exc):
    telemetry_client.track_exception()
    return 'Error', 500


@app.route('/')
def index():
    telemetry_client.track_event('CustomEvent', {'value': 1})
    telemetry_client.track_trace('CustomTrace', severity=3)
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    telemetry_client.track_event('CustomEvent', {'value': 1})
    telemetry_client.track_trace('CustomTrace', severity=3)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    telemetry_client.track_event('CustomEvent', {'value': 1})
    telemetry_client.track_trace('CustomTrace', severity=3)
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
