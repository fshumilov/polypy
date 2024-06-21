from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


from server.db_requests import get_property_type, get_property_value


# Sample data for the dropdown options
df_dropdown_polymer_type = ['Polyurethane']
# Get a dataframe from the data base
df_property_type = get_property_type()
df_property_value = get_property_value()

# List data for property dropdowns
dropdown_1_property = df_property_type['property_type'].tolist()
dropdown_2_property = df_property_type['property_type'].tolist()


# MainPanel data
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
print(df.head())

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
        html.Div(children="- find your polymer place among others",
                 style={'padding-left': '10px'}
                 ),
        html.Hr()
    ])


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
            dropdown_sidebar(df_dropdown_polymer_type, "dd_polymer_type", "1. Select the polymer type:"),

            dropdown_sidebar(dropdown_1_property, "dd_first_property",
                             "2. Set the first property:", placeholder="Select a property type..."),
            dropdown_sidebar([], "dd_first_property_name", placeholder="Select a property name..."),

            dropdown_sidebar(dropdown_2_property, "dd_second_property",
                             "3. Set the second property:", placeholder="Select a property type..."),
            dropdown_sidebar([], "dd_second_property_name", placeholder="Select a property name..."),

            html.Br(),
            html.Div(children='* all columns are mandatory')
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


# Callbacks to update the second dropdown based on the first dropdown selection
@app.callback(
    Output('dd_first_property_name', 'options'),
    Input('dd_first_property', 'value')
)
def update_first_property(selected_value):
    if selected_value:  # e.g. selected_value == "Reological"
        return filter_property_names(selected_value)
    else:
        return ["Please, select the property type first"]


@app.callback(
    Output('dd_second_property_name', 'options'),
    Input('dd_second_property', 'value')
)
def update_second_property(selected_value):
    if selected_value:  # e.g. selected_value == "Reological"
        return filter_property_names(selected_value)
    else:
        return ["Please, select the property type first"]


def filter_property_names(selected_value):
    """
    Filters property names based on the selected property type value
    and returns them in a format suitable for a dropdown.

    :param selected_value: The selected value from the first dropdown, representing the property type.
    :type selected_value: str
    :return: A list of dictionaries, each containing 'label' and 'value' keys for the filtered property names.
    :rtype: list of dict
    """
    # Filter the property type DataFrame based on the selected value from the first dropdown
    df_filtered_property_type = df_property_type[df_property_type['property_type'] == selected_value]

    # Get the 'id' values from the filtered property type DataFrame
    id_values_property_type = df_filtered_property_type['id'].tolist()

    # Filter the property value DataFrame to include only rows with matching 'property_type_id' values
    df_filtered_property_value = df_property_value[
        df_property_value['property_type_id'].isin(id_values_property_type)
    ]

    # Create a list of dictionaries for the dropdown options using the filtered property names
    filtered_property_names = [{'label': name, 'value': name} for name in
                               df_filtered_property_value['property_name'].tolist()]
    return filtered_property_names


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
