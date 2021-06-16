import os.path
from flask import Flask, render_template, jsonify, url_for, redirect, session
from flask_autoindex import AutoIndex
from authlib.flask.client import OAuth
import jwt
from functools import wraps

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret'
})
oauth = OAuth(app)
keycloak = oauth.register(name='keycloak',
    client_id='flask-test',
    client_secret='xxx', # modify
    access_token_url='https://id.jackpan-t1.dev.primehub.io/auth/realms/primehub/protocol/openid-connect/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://id.jackpan-t1.dev.primehub.io/auth/realms/primehub/protocol/openid-connect/auth',
    api_base_url='https://id.jackpan-t1.dev.primehub.io/auth',
    client_kwargs=None
)

file_path = "./"
#AutoIndex(app, browse_root=file_path, add_url_rules=False)
files_index = AutoIndex(app, browse_root=file_path, add_url_rules=False)

@app.route('/login')
def login():
    redirect_uri = url_for('autoindex', _external=True)
    return keycloak.authorize_redirect(redirect_uri)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access_token' not in session:
            try:
                token = keycloak.authorize_access_token()
                session['access_token'] = token
                # can decode the token by pyjwt and check does the user have ds:dataset-name
                print(token)
            except Exception as e:
                print(e)
                return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route("/uppy")
def uppy():
    # might need to pass token from here. However, token has expiry time...
    # inside the tusd pre-create hook, can check the token by querying /userinfo
    return render_template("uppy.html", value="dataset-mount-test")

@app.route('/')
@app.route('/<path:path>')
@requires_auth
def autoindex(path='.'):
    return files_index.render_autoindex(path)

if __name__ == '__main__':
    app.run()
