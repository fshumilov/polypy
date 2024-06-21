from dash import html, dcc


def create_layout(df):
    layout = html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Fertility rate, total (births per woman)',
                    id='crossfilter-xaxis-column',
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='crossfilter-xaxis-type',
                    labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                )
            ],
                style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    df['Indicator Name'].unique(),
                    'Life expectancy at birth, total (years)',
                    id='crossfilter-yaxis-column'
                ),
                dcc.RadioItems(
                    ['Linear', 'Log'],
                    'Linear',
                    id='crossfilter-yaxis-type',
                    labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={'padding': '10px 5px'}
        ),

        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                hoverData={'points': [{'customdata': 'Japan'}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ], style={'display': 'inline-block', 'width': '49%'}),

        html.Div(dcc.Slider(
            df['Year'].min(),
            df['Year'].max(),
            step=None,
            id='crossfilter-year--slider',
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()}
        ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
    ])
    return layout
