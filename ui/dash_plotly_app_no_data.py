from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


# Sample data for the dropdown options
dropdown_data_1 = ['Polyurethane']
dropdown_data_2 = ['Option 1', 'Option 2', 'Option 3']
dropdown_data_3 = ['Option 1', 'Option 2', 'Option 3']
dropdown_data_4 = ['Option 1', 'Option 2', 'Option 3']
dropdown_data_5 = ['Option 1', 'Option 2', 'Option 3']

# MainPanel data
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

#  Styles
sidebar_style = {
    'width': '30%',
    'display': 'inline-block',
    'verticalAlign': 'top',
    'padding': '20px',
    'boxShadow': '2px 2px 2px lightgrey'
}

main_panel_style = {
    'width': '70%',
    'display': 'inline-block',
    'padding': '20px'
}


def app_title():
    return html.Div([
        html.H1(children='Polymer Reviewer'),
        html.Div(children='''
                find your polymer place among others
            '''),
        html.Hr()
    ])


def dropdown_sidebar(data, header=""):
    return html.Div([
        html.Br(),
        html.Div(children=header),
        dcc.Dropdown(
            #  PAY ATTENTION: the ids are the same for all created dropdowns
            id='dropdown',
            options=[
                {'label': item, 'value': item} for item in data
            ],
            value=data[0] if data else None
        )
    ])


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([

    dbc.Row([
        app_title()
    ]),
    dbc.Row([
        # SidebarPanel
        html.Div([
            # SidebarPanel Title:
            html.H3("Set the characteristics of search*:"),
            # SideBarPanel dropdowns
            dropdown_sidebar(dropdown_data_1, "1. Select the polymer type:"),
            dropdown_sidebar(dropdown_data_2, "2. Set the first property:"),
            dropdown_sidebar(dropdown_data_3),
            dropdown_sidebar(dropdown_data_4, "3. Set the second property:"),
            dropdown_sidebar(dropdown_data_5),
        ], style=sidebar_style),

        # MainPanel
        html.Div([
            html.H3("Output:"),
            html.Div(children='''
                Search results:
            '''),
            dcc.Graph(
                id='life-exp-vs-gdp',
                figure=fig
            )
        ], style=main_panel_style)
    ])

], fluid=True)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
