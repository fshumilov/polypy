from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from config.settings import df_property_type, df_property_value, df_polymer_name
from .layout_elements import create_initial_figure


def register_callbacks(app):
    # Callbacks to update the second dropdown based on the first dropdown selection
    @app.callback(
        Output('dd_first_property_name', 'options'),
        Input('dd_first_property', 'value')
    )
    def update_first_property(selected_value):
        if selected_value:  # e.g. selected_value == "Rheological"
            return filter_property_names(selected_value)
        else:
            return ["Please, select the property type first"]

    @app.callback(
        Output('dd_second_property_name', 'options'),
        Input('dd_second_property', 'value')
    )
    def update_second_property(selected_value):
        if selected_value:  # e.g. selected_value == "Rheological"
            return filter_property_names(selected_value)
        else:
            return ["Please, select the property type first"]

    def filter_property_names(selected_value):
        """
        Filters property names based on the selected property type value
        and returns them in a format suitable for a dropdown
        :param selected_value: The selected value from the first dropdown, representing the property type
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

            # Retrieve value units for selected parameter
            unit1 = df_property_value[df_property_value['property_name'] == param1]['unit'].values
            unit2 = df_property_value[df_property_value['property_name'] == param2]['unit'].values
            # unit1 and unit2 are np.arrays

            # Retrieve the polymer name
            polymer_name = df_polymer_name['polymer_name'].values

            # Determine the type of values and generate the appropriate plot
            if not pd.isna(values1_double).all() and not pd.isna(values2_double).all():
                # Both parameters are double: Scatter plot
                fig = px.scatter(
                    x=values1_double, y=values2_double,
                    labels={'x': f"{param1}, {unit1[0]} ", 'y': f"{param2}, {unit2[0]} "}
                ).update_traces(
                    hovertemplate=(
                        f'Polymer: %{{hovertext}}<br><br>'
                        f'{param1}: %{{x}} {unit1[0]}<br>'
                        f'{param2}: %{{y}} {unit2[0]}'
                    ),
                    hovertext=polymer_name
                )
            elif values1_text != "NaN" and values2_text != "NaN":
                # Both parameters are text: Heatmap
                fig = px.density_heatmap(
                    x=values1_text, y=values2_text,
                    labels={'x': param1, 'y': param2}
                )
                # Update traces to include custom data for hover
                fig.update_traces(
                    hovertemplate=(
                        f'Polymer: {polymer_name}<br><br>'
                        f'{param1}: %{{x}}<br>'
                        f'{param2}: %{{y}}'
                    )
                )
            elif not pd.isna(values1_double).all() and values2_text != "NaN":
                # Parameter 1 is double and Parameter 2 is text: Histogram
                fig = px.histogram(
                    x=values1_double, color=values2_text,
                    labels={'x': f"{param1}, {unit1[0]} ", 'color': param2}
                )
                fig.update_traces(
                    hovertemplate=(
                        f'Polymer: {polymer_name}<br><br>'
                        f'{param1}: %{{x}} {unit1[0]}<br>'
                        f'{param2}: {values2_text}'
                    )
                )
            elif not pd.isna(values2_double).all() and values1_text != "NaN":
                # Parameter 2 is double and Parameter 1 is text: Histogram
                fig = px.histogram(
                    x=values2_double, color=values1_text,
                    labels={'x': f"{param2}, {unit2[0]} ", 'color': param1}
                )
                fig.update_traces(
                    hovertemplate=(
                        f'Polymer: {polymer_name}<br><br>'
                        f'{param2}: %{{x}} {unit2[0]}<br>'
                        f'{param1}: {values1_text}'
                    )
                )
            else:
                # Handle the case where data types are mismatched or no data is available
                fig = create_initial_figure()

            return fig
        else:
            return create_initial_figure()
