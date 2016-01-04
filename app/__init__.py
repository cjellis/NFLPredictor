# Import flask and template operators
from flask import Flask, render_template

# Import a module / component using its blueprint handler variable
from app.basicWeek import basic
from app.basicFullSeason import fullSeason
from app.midlevel import mid
from app.custom import custom
# Define the WSGI application object
app = Flask(__name__)
app.debug = True

# Register blueprint(s)
app.register_blueprint(basic)
app.register_blueprint(fullSeason)
app.register_blueprint(mid)
app.register_blueprint(custom)


@app.route('/', methods=['GET'])
def run():
    return render_template('index.html')

