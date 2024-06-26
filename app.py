from dash import Dash
import dash_bootstrap_components as dbc

from dash_app.layouts import layout
from dash_app.callbacks import register_callbacks
from config.settings import config


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Set the layout
app.layout = layout

# Register all callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=config['DEBUG'])
