from datetime import datetime
import os
from flasgger import Swagger
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/hello')
def hello():
    """
    A sample endpoint that returns a greeting.
    ---
    responses:
      200:
        description: A string indicating a greeting.
    """
    return 'Hello, world!'


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/about')
def about():
    print('Request for about page received')
    return render_template('about.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route('/hello', methods=['POST'])
# def hello():
#     name = request.form.get('name')

#     if name:
#         print('Request for hello page received with name=%s' % name)
#         return render_template('hello.html', name=name)
#     else:
#         print('Request for hello page received with no name or blank name -- redirecting')
#         return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
