# myapp/util/assets.py

from flask.ext.assets import Bundle, Environment
from .. import app

bundles = {

    'js': Bundle(
        'js/swearjar.js',
        output='gen/script.js'),

    'css': Bundle(
        'css/bootstrap.min.css',
        'css/bootstrap-theme.min.css',
        'css/stylesheet.css',
        'css/home.css',
        'css/stylish-portfolio.css',
        output='gen/style.css'),

    'giphy': Bundle(
        'js/giphy.js',
        output='gen/giphy.js')
}

assets = Environment(app)

assets.register(bundles)
