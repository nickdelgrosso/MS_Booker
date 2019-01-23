__version__ = '0.1.0'

from flask import Flask
from . import config

app = Flask(__name__)

app.config.from_object(config.BaseConfig)

from . import views