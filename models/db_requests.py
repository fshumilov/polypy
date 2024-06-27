import pandas as pd
import psycopg2.extras


from config.db_config import DB_SETTINGS, SQL_QUERIES, COLUMN_NAMES

"""
- the code made based on https://www.youtube.com/watch?v=M2NzvnfS-hI&ab_channel=techTFQ
- the database schema: https://lucid.app/lucidchart/8f8007f6-802e-440c-8822-46c49292bcf1/edit?beaconFlowId=EB3BE07D9A97FFAE&invitationId=inv_7341cdab-f138-47bf-842b-205d6ce31584&page=0_0#
- the UI draft layout: https://www.figma.com/design/LhOBONmYC35csJrW40NxVu/Untitled?node-id=1-1347&t=0arozdUpv8eGptKM-0

3 tables: schema.table_name: (column_names)
    campusplastics.polymer_catalog: ("id", "polymer_name")
    campusplastics.property_type: ("id", "polymer_catalog_id", "property_type")
    campusplastics.property_value: ("id", "property_type_id", "property_name", "value", "unit", "test_standard")
"""


def _get_data(sql_query, column_names):
    """
    Maintain the connection to database and collecting data
    :param sql_query: string, query of SQL request to a database
    :param column_names: list of column names
    :return: list of lists
    """
    try:
        with psycopg2.connect(
                host=DB_SETTINGS['host'],
                database=DB_SETTINGS['database'],
                user=DB_SETTINGS['user'],
                password=DB_SETTINGS['password'],
                port=DB_SETTINGS['port_id']
        ) as conn:

            # value in brackets is required for getting info in the dict form
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                # fetching the polymer catalog value
                cur.execute(sql_query)
                table_data = []
                for record in cur.fetchall():
                    one_data_line = []
                    for column in column_names:
                        one_data_line.append(record[column])

                    table_data.append(one_data_line)  # list of lists

        return table_data

    except psycopg2.Error as error:
        print(f"Database error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


def _convert_to_df(data, column_names):
    """
    To convert the list of lists into a dataframe
    :param data: list of lists
    :param column_names: list of column names
    :return: a dataframe
    """
    df = pd.DataFrame(data, columns=column_names)
    return df


def get_polymer_catalog():
    """
    Get the data from a database
    :return: a dataframe
    """
    sql_query_polymer_catalog = SQL_QUERIES['polymer_catalog']
    column_names_polymer_catalog = COLUMN_NAMES['polymer_catalog']
    data = _get_data(sql_query_polymer_catalog, column_names_polymer_catalog)
    df = _convert_to_df(data, column_names_polymer_catalog)
    return df


def get_property_type():
    """
    Get the data from a database
    :return: a dataframe
    """
    sql_query_property_type = SQL_QUERIES['property_type']
    column_names_property_type = COLUMN_NAMES['property_type']
    data = _get_data(sql_query_property_type, column_names_property_type)
    df = _convert_to_df(data, column_names_property_type)
    return df


def get_property_value():
    """
    Get the data from a database
    :return: a dataframe
    """
    sql_query_property_name = SQL_QUERIES['property_value']
    column_names_property_name = COLUMN_NAMES['property_value']
    data = _get_data(sql_query_property_name, column_names_property_name)
    df = _convert_to_df(data, column_names_property_name)
    return df
