from models.db_requests import get_property_type, get_property_value


# The dash app config
config = {
    'DEBUG': True
}

# ___________________________________________
# Sample data for the dropdown options
df_dropdown_polymer_type = ['Polyurethane']
df_property_type = get_property_type()
df_property_value = get_property_value()

# List data for property dropdowns
dropdown_1_property = df_property_type['property_type'].tolist()
dropdown_2_property = df_property_type['property_type'].tolist()


# ___________________________________________
#  Dash UI Styles
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
