import logging
from dash import Dash
import dash_bootstrap_components as dbc

from dash_app.layouts import layout
from dash_app.callbacks import register_callbacks
from config.settings import config


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Set the layout
app.layout = layout
logging.info("Layout loading ...")

# Register all callbacks
register_callbacks(app)
logging.info("Callbacks registering ...")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=config['DEBUG'])
