import os
from flask import Flask, render_template
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix

class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

app = Flask(__name__)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=os.environ['FRONT_END_PATH'])

AutoIndex(app, browse_root="/srv/data")

@app.route("/uppy")
def uppy():
    return render_template("uppy.html", primehub_scheme=os.environ['PRIMEHUB_SCHEME'], primehub_domain=os.environ['PRIMEHUB_DOMAIN'], tusd_path=os.environ['TUSD_PATH'])

if __name__ == '__main__':
    app.run()
