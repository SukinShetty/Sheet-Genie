import unittest
import requests
import json
import pandas as pd
import io
import os
from backend.excel_helpers import ExcelHelper, create_sample_data

# Get the backend URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    for line in f:
        if line.startswith('REACT_APP_BACKEND_URL='):
            BACKEND_URL = line.strip().split('=')[1].strip('"\'')
            break

API_URL = f"{BACKEND_URL}/api"

class TestColumnManipulation(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create sample data
        self.sample_df = create_sample_data()
        self.excel_helper = ExcelHelper(self.sample_df)
        
        # Get sample data from API to ensure we're working with the same data
        response = requests.get(f"{API_URL}/sample-data")
        self.assertEqual(response.status_code, 200)
        self.api_data = response.json()
        self.assertTrue(self.api_data["success"])
        
        print(f"Setup complete. Using API URL: {API_URL}")
    
    def test_add_column_direct(self):
        """Test add_column function directly"""
        print("\n=== Testing add_column function directly ===")
        
        # Test adding a column with 10% higher values than Q2 Sales
        result = self.excel_helper.add_column(
            column_name="Q2 Sales +10%",
            formula_description="10% higher than Q2 Sales",
            base_column="Q2 Sales",
            operation="percentage_increase",
            value=0.1
        )
        
        # Check if operation was successful
        self.assertTrue(result["success"])
        self.assertEqual(result["column_name"], "Q2 Sales +10%")
        self.assertEqual(result["base_column"], "Q2 Sales")
        
        # Check if the column was actually added to the dataframe
        self.assertIn("Q2 Sales +10%", self.excel_helper.df.columns)
        
        # Check if the values are correctly calculated (10% higher than Q2 Sales)
        for i, row in self.excel_helper.df.iterrows():
            self.assertAlmostEqual(
                row["Q2 Sales +10%"], 
                row["Q2 Sales"] * 1.1,
                places=1
            )
        
        # Check the data type of the new column values
        for value in self.excel_helper.df["Q2 Sales +10%"]:
            self.assertIsInstance(value, (int, float))
        
        # Check the format of the returned data
        updated_data = self.excel_helper.get_updated_data()
        self.assertIsInstance(updated_data, list)
        self.assertIsInstance(updated_data[0], list)  # Headers
        self.assertIsInstance(updated_data[1], list)  # First data row
        
        # Check that the values in the updated data are not objects
        for row in updated_data[1:]:  # Skip header row
            self.assertIsInstance(row[-1], (int, float))  # Last column should be our new column
        
        print(f"Added column: {result['column_name']}")
        print(f"Sample values: {result['sample_values']}")
    
    def test_delete_column_direct(self):
        """Test delete_column function directly"""
        print("\n=== Testing delete_column function directly ===")
        
        # First add a column to delete
        self.excel_helper.add_column(
            column_name="Test Column to Delete",
            formula_description="Test column",
            base_column="Q1 Sales",
            operation="copy"
        )
        
        # Verify the column was added
        self.assertIn("Test Column to Delete", self.excel_helper.df.columns)
        
        # Now delete the column
        result = self.excel_helper.delete_column(column_name="Test Column to Delete")
        
        # Check if operation was successful
        self.assertTrue(result["success"])
        self.assertEqual(result["column_name"], "Test Column to Delete")
        
        # Check if the column was actually removed from the dataframe
        self.assertNotIn("Test Column to Delete", self.excel_helper.df.columns)
        
        # Check the format of the returned data
        updated_data = self.excel_helper.get_updated_data()
        self.assertIsInstance(updated_data, list)
        self.assertIsInstance(updated_data[0], list)  # Headers
        
        print(f"Deleted column: {result['column_name']}")
        print(f"Remaining columns: {result['remaining_columns']}")
    
    def test_add_column_via_api(self):
        """Test adding a column via the chat API"""
        print("\n=== Testing add_column via chat API ===")
        
        # Send a chat message to add a column
        chat_message = "Add a column with values 10% higher than Q2 sales"
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": chat_message}
        )
        
        # Check if request was successful
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])
        
        # Check if function results are present
        self.assertIn("function_results", result)
        self.assertIsInstance(result["function_results"], list)
        self.assertTrue(len(result["function_results"]) > 0)
        
        # Check if the first function result is successful
        function_result = result["function_results"][0]
        self.assertTrue(function_result["success"])
        
        # Check if updated data is present and properly formatted
        self.assertIn("updated_data", result)
        self.assertIsInstance(result["updated_data"], list)
        self.assertTrue(len(result["updated_data"]) > 0)
        
        # Check the data types in the updated data
        headers = result["updated_data"][0]
        self.assertIn("Q2 Sales", headers)  # Original column should be present
        
        # Find the new column (should contain "Q2" and either "10%" or "+10%")
        new_column_index = None
        for i, header in enumerate(headers):
            if "Q2" in header and ("10%" in header or "+10" in header):
                new_column_index = i
                break
        
        self.assertIsNotNone(new_column_index, "New column not found in headers")
        
        # Check that the values in the new column are not objects
        for row in result["updated_data"][1:]:  # Skip header row
            self.assertIsInstance(row[new_column_index], (int, float, str))
            # If it's a string, it should be convertible to a number
            if isinstance(row[new_column_index], str):
                try:
                    float(row[new_column_index])
                except ValueError:
                    self.fail(f"Value '{row[new_column_index]}' is not a valid number")
        
        print(f"API response: {result['response']}")
        if new_column_index is not None:
            print(f"New column found at index {new_column_index}: {headers[new_column_index]}")
    
    def test_delete_column_via_api(self):
        """Test deleting a column via the chat API"""
        print("\n=== Testing delete_column via chat API ===")
        
        # First add a column to delete
        add_response = requests.post(
            f"{API_URL}/chat",
            json={"message": "Add a column called 'Test Delete' that copies the Q1 Sales values"}
        )
        self.assertEqual(add_response.status_code, 200)
        add_result = add_response.json()
        self.assertTrue(add_result["success"])
        
        # Now delete the column
        delete_message = "Delete the 'Test Delete' column"
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": delete_message}
        )
        
        # Check if request was successful
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result["success"])
        
        # Check if function results are present
        self.assertIn("function_results", result)
        self.assertIsInstance(result["function_results"], list)
        self.assertTrue(len(result["function_results"]) > 0)
        
        # Check if the first function result is successful
        function_result = result["function_results"][0]
        self.assertTrue(function_result["success"])
        
        # Check if updated data is present and properly formatted
        self.assertIn("updated_data", result)
        self.assertIsInstance(result["updated_data"], list)
        self.assertTrue(len(result["updated_data"]) > 0)
        
        # Check that the deleted column is not in the headers
        headers = result["updated_data"][0]
        self.assertNotIn("Test Delete", headers)
        
        print(f"API response: {result['response']}")
    
    def test_export_to_excel(self):
        """Test exporting modified data to Excel"""
        print("\n=== Testing export to Excel functionality ===")
        
        # First add a column to ensure we have modified data
        self.excel_helper.add_column(
            column_name="Export Test Column",
            formula_description="Test column for export",
            base_column="Q3 Sales",
            operation="percentage_increase",
            value=0.2
        )
        
        # Test the export_to_excel function directly
        excel_bytes = self.excel_helper.export_to_excel()
        self.assertIsInstance(excel_bytes, bytes)
        
        # Try to read the Excel file to verify it's valid
        df = pd.read_excel(io.BytesIO(excel_bytes))
        self.assertIn("Export Test Column", df.columns)
        
        # Test the export API endpoint
        response = requests.get(f"{API_URL}/export-excel", stream=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                     response.headers["Content-Type"])
        
        # Save the file temporarily to verify it
        with open("/tmp/export_test.xlsx", "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        
        # Verify the exported file
        self.assertTrue(os.path.exists("/tmp/export_test.xlsx"))
        
        print("Export to Excel functionality works correctly")


if __name__ == "__main__":
    unittest.main()