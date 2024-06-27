from dash import html, dcc
import plotly.graph_objects as go


# The app title
def app_title():
    return html.Div([
        html.H1(children='Polymer Reviewer'),
        html.Div(children="- find your polymer place among others",
                 style={'padding-left': '10px'}
                 ),
        html.Hr()
    ])


# Sidebar
def dropdown_sidebar(data, dropdown_id, header="", placeholder="Select an option..."):
    return html.Div([
        html.Br(),
        html.Div(children=header),
        dcc.Dropdown(
            id=dropdown_id,
            options=[
                {'label': item, 'value': item} for item in data
            ],
            # To select the first one from list
            # value=data[0] if data else None
            value=None,
            placeholder=placeholder
        )
    ])


# MainPanel data
# Define the initial figure with a message
def create_initial_figure():
    fig = go.Figure()
    fig.add_annotation(
        x=0.5, y=0.5, text="Not all parameters are selected",
        showarrow=False, font=dict(size=20), xref="paper", yref="paper"
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig
