from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from server.db_requests import get_property_type, get_property_value

# Sample data for the dropdown options
df_dropdown_polymer_type = ['Polyurethane']
# Get a dataframe from the data base
df_property_type = get_property_type()
df_property_value = get_property_value()
print(df_property_value.columns)

# List data for property dropdowns
dropdown_1_property = df_property_type['property_type'].tolist()
dropdown_2_property = df_property_type['property_type'].tolist()


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
                id='graph',
                figure=create_initial_figure()
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


# Callback to update the graph based on selected parameters
@app.callback(
    Output('graph', 'figure'),
    Input('dd_first_property_name', 'value'),
    Input('dd_second_property_name', 'value')
)
def update_graph(param1, param2):
    if param1 and param2:  # e.g. "Load" and "Density"
        # Retrieve values for the selected parameters
        print("___________________________________")
        values1_double = df_property_value[
            df_property_value['property_name'] == param1
            ]['value_double'].values
        print(values1_double)
        values2_double = df_property_value[
            df_property_value['property_name'] == param2
            ]['value_double'].values
        print(values2_double)

        values1_text = df_property_value[
            df_property_value['property_name'] == param1
            ]['value_text'].values
        print(values1_text)
        values2_text = df_property_value[
            df_property_value['property_name'] == param2
            ]['value_text'].values
        print(values2_text)

        # Determine the type of values and generate the appropriate plot
        if not pd.isna(values1_double).all() and not pd.isna(values2_double).all():
            # Both parameters are double: Scatter plot
            fig = px.scatter(x=values1_double, y=values2_double, labels={'x': param1, 'y': param2})
        elif values1_text != "NaN" and values2_text != "NaN":
            # Both parameters are text: Heatmap
            fig = px.density_heatmap(
                x=values1_text, y=values2_text, labels={'x': param1, 'y': param2}
            )
        elif not pd.isna(values1_double).all() and values2_text != "NaN":
            # Parameter 1 is double and Parameter 2 is text: Histogram
            fig = px.histogram(x=values1_double, color=values2_text, labels={'x': param1, 'color': param2})
        elif not pd.isna(values2_double).all() and values1_text != "NaN":
            # Parameter 2 is double and Parameter 1 is text: Histogram
            fig = px.histogram(x=values2_double, color=values1_text, labels={'x': param1, 'color': param2})
        else:
            # Handle the case where data types are mismatched or no data is available
            fig = create_initial_figure()

        return fig
    else:
        return create_initial_figure()


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
