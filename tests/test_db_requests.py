import unittest
from models.db_requests import _get_data, _convert_to_df


class TestDbRequests(unittest.TestCase):

    def setUp(self):
        # setup code, if necessary
        pass

    def tearDown(self):
        # teardown code, if necessary
        pass

    def test_get_data(self):
        result = _get_data(
            sql_query="SELECT * FROM campusplastics.polymer_catalog",
            column_names=["id", "polymer_name"]
        )
        self.assertIsInstance(result, list)  # check if the result is a list

        # Optionally, add more specific checks if possible:
        if result:
            self.assertTrue(all(isinstance(row, list) for row in result))  # check if all items in the list are tuples
            self.assertTrue(all(len(row) == 2 for row in result))  # check if all tuples have 2 elements

    def test_convert_to_df(self):
        data = [(1, 'Polymer A'), (2, 'Polymer B')]
        df = _convert_to_df(data, column_names=["id", "polymer_name"])
        self.assertEqual(df.shape, (2, 2))  # check if the dataframe has the correct shape
        self.assertListEqual(list(df.columns), ["id", "polymer_name"])  # check if the dataframe has the correct columns

if __name__ == '__main__':
    unittest.main()
