from app import app

@app.route('/health')
def health():
    """
    A sample endpoint that returns info about health.
    ---
    responses:
      200:
        description: A string indicating that health is ok.
    """
    return "OK"

@app.route('/hello') #/apidocs
def hello():
    """
    A sample endpoint that returns a greeting.
    ---
    responses:
      200:
        description: A string indicating a greeting.
    """
    app.logger.info('Hello, World!')
    return 'Hello, world!'