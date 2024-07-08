from dash import html, dcc
import dash_bootstrap_components as dbc


from .layout_elements import app_title, dropdown_sidebar, create_initial_figure
from config.settings import df_dropdown_polymer_type, dropdown_1_property, dropdown_2_property
from config.settings import sidebar_style, main_panel_style


layout = dbc.Container([

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
