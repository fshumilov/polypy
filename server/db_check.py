"""
This app consists of 2 parts: parsing and database requests
"""

import db_requests

# Database requests part:
x = db_requests.get_polymer_catalog()
# print(type(x))
print(x.head())

y = db_requests.get_property_type()
print(y.head())

z = db_requests.get_property_value()
print(z.head())