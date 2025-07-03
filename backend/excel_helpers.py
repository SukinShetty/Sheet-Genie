import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import io
import base64
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment
import xlsxwriter
from typing import Dict, List, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class ExcelHelper:
    """Helper class for Excel operations using AI function calling"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.original_df = df.copy()
    
    def sum_range(self, range_spec: str) -> Dict[str, Any]:
        """
        Calculate sum of a range of cells
        
        Args:
            range_spec: Range specification like "A1:A10", "B2:D5", etc.
        
        Returns:
            Dict with result and formula
        """
        try:
            # Parse range specification
            start_cell, end_cell = self._parse_range(range_spec)
            
            # Get the data slice
            data_slice = self._get_data_slice(start_cell, end_cell)
            
            # Calculate sum
            total = np.sum(data_slice.values)
            
            # Update dataframe with formula if needed
            formula = f"=SUM({range_spec})"
            
            return {
                "success": True,
                "result": float(total),
                "formula": formula,
                "range": range_spec,
                "message": f"Sum of {range_spec} is {total}"
            }
            
        except Exception as e:
            logger.error(f"Error in sum_range: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not calculate sum for range {range_spec}"
            }
    
    def average_range(self, range_spec: str) -> Dict[str, Any]:
        """
        Calculate average of a range of cells
        
        Args:
            range_spec: Range specification like "A1:A10", "B2:D5", etc.
        
        Returns:
            Dict with result and formula
        """
        try:
            # Parse range specification
            start_cell, end_cell = self._parse_range(range_spec)
            
            # Get the data slice
            data_slice = self._get_data_slice(start_cell, end_cell)
            
            # Calculate average
            avg = np.mean(data_slice.values)
            
            # Update dataframe with formula if needed
            formula = f"=AVERAGE({range_spec})"
            
            return {
                "success": True,
                "result": float(avg),
                "formula": formula,
                "range": range_spec,
                "message": f"Average of {range_spec} is {avg:.2f}"
            }
            
        except Exception as e:
            logger.error(f"Error in average_range: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not calculate average for range {range_spec}"
            }
    
    def create_pivot(self, rows: List[str], values: List[str], aggfunc: str = 'sum') -> Dict[str, Any]:
        """
        Create a pivot table from the data
        
        Args:
            rows: List of column names to use as rows
            values: List of column names to aggregate
            aggfunc: Aggregation function ('sum', 'mean', 'count', etc.)
        
        Returns:
            Dict with pivot table data
        """
        try:
            # Create pivot table
            pivot_table = pd.pivot_table(
                self.df, 
                index=rows, 
                values=values, 
                aggfunc=aggfunc,
                fill_value=0
            )
            
            # Convert to dict for JSON serialization
            pivot_dict = pivot_table.to_dict(orient='index')
            
            return {
                "success": True,
                "pivot_table": pivot_dict,
                "rows": rows,
                "values": values,
                "aggfunc": aggfunc,
                "message": f"Created pivot table with {len(pivot_dict)} rows"
            }
            
        except Exception as e:
            logger.error(f"Error in create_pivot: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not create pivot table"
            }
    
    def generate_chart(self, chart_type: str, x_column: str, y_column: str, title: str = None) -> Dict[str, Any]:
        """
        Generate a chart from the data
        
        Args:
            chart_type: Type of chart ('bar', 'line', 'pie', 'scatter')
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            title: Chart title
        
        Returns:
            Dict with chart data and configuration
        """
        try:
            # Prepare data
            x_data = self.df[x_column].tolist()
            y_data = self.df[y_column].tolist()
            
            if title is None:
                title = f"{y_column} by {x_column}"
            
            # Create chart based on type
            if chart_type.lower() == 'bar':
                fig = px.bar(
                    x=x_data, 
                    y=y_data,
                    labels={'x': x_column, 'y': y_column},
                    title=title
                )
            elif chart_type.lower() == 'line':
                fig = px.line(
                    x=x_data, 
                    y=y_data,
                    labels={'x': x_column, 'y': y_column},
                    title=title
                )
            elif chart_type.lower() == 'pie':
                fig = px.pie(
                    values=y_data, 
                    names=x_data,
                    title=title
                )
            elif chart_type.lower() == 'scatter':
                fig = px.scatter(
                    x=x_data, 
                    y=y_data,
                    labels={'x': x_column, 'y': y_column},
                    title=title
                )
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            # Convert to JSON
            chart_json = fig.to_json()
            
            return {
                "success": True,
                "chart_data": json.loads(chart_json),
                "chart_type": chart_type,
                "x_column": x_column,
                "y_column": y_column,
                "title": title,
                "message": f"Generated {chart_type} chart"
            }
            
        except Exception as e:
            logger.error(f"Error in generate_chart: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not generate {chart_type} chart"
            }
    
    def format_cells(self, range_spec: str, format_type: str, format_value: str = None) -> Dict[str, Any]:
        """
        Format cells in the specified range
        
        Args:
            range_spec: Range specification like "A1:A10", "B2:D5", etc.
            format_type: Type of formatting ('currency', 'percentage', 'date', 'bold', 'color')
            format_value: Additional format value (e.g., color code)
        
        Returns:
            Dict with formatting result
        """
        try:
            # Parse range specification
            start_cell, end_cell = self._parse_range(range_spec)
            
            # Apply formatting based on type
            formatting_info = {
                "range": range_spec,
                "format_type": format_type,
                "format_value": format_value
            }
            
            if format_type == 'currency':
                formatting_info['number_format'] = '$#,##0.00'
            elif format_type == 'percentage':
                formatting_info['number_format'] = '0.00%'
            elif format_type == 'date':
                formatting_info['number_format'] = 'mm/dd/yyyy'
            elif format_type == 'bold':
                formatting_info['font'] = {'bold': True}
            elif format_type == 'color':
                formatting_info['fill'] = {'color': format_value or 'FFFF00'}
            
            return {
                "success": True,
                "formatting": formatting_info,
                "range": range_spec,
                "message": f"Applied {format_type} formatting to {range_spec}"
            }
            
        except Exception as e:
            logger.error(f"Error in format_cells: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not format cells in range {range_spec}"
            }
    
    def _parse_range(self, range_spec: str) -> tuple:
        """Parse range specification like A1:B10 into start and end coordinates"""
        try:
            start_cell, end_cell = range_spec.split(':')
            return start_cell.strip(), end_cell.strip()
        except ValueError:
            # Single cell reference
            return range_spec.strip(), range_spec.strip()
    
    def _get_data_slice(self, start_cell: str, end_cell: str) -> pd.DataFrame:
        """Get data slice from DataFrame based on cell references"""
        # Convert Excel cell references to pandas iloc indices
        start_row, start_col = self._cell_to_indices(start_cell)
        end_row, end_col = self._cell_to_indices(end_cell)
        
        # Get the slice
        return self.df.iloc[start_row:end_row+1, start_col:end_col+1]
    
    def _cell_to_indices(self, cell: str) -> tuple:
        """Convert Excel cell reference like A1 to (row, col) indices"""
        # Extract column letters and row number
        col_letters = ''.join(filter(str.isalpha, cell))
        row_num = int(''.join(filter(str.isdigit, cell)))
        
        # Convert column letters to number (A=0, B=1, ..., Z=25, AA=26, etc.)
        col_num = 0
        for i, char in enumerate(reversed(col_letters)):
            col_num += (ord(char) - ord('A') + 1) * (26 ** i)
        col_num -= 1  # Convert to 0-based indexing
        
        # Convert to 0-based row indexing
        row_num -= 1
        
        return row_num, col_num
    
    def get_updated_data(self) -> List[List[Any]]:
        """Get the updated dataframe as a list of lists for the frontend"""
        try:
            # Include headers as first row
            headers = self.df.columns.tolist()
            data_rows = self.df.values.tolist()
            return [headers] + data_rows
        except Exception as e:
            logger.error(f"Error getting updated data: {str(e)}")
            return []
    
    def export_to_excel(self, filename: str = None) -> bytes:
        """Export the dataframe to Excel format"""
        if filename is None:
            filename = "updated_spreadsheet.xlsx"
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        output.seek(0)
        return output.getvalue()


def create_sample_data() -> pd.DataFrame:
    """Create sample data for demonstration"""
    data = {
        'Product': ['Laptop Pro', 'Tablet Air', 'Phone Max', 'Watch Series', 'Earbuds Pro'],
        'Q1 Sales': [15000, 8000, 25000, 5000, 12000],
        'Q2 Sales': [18000, 9500, 28000, 6200, 14500],
        'Q3 Sales': [22000, 11000, 32000, 7500, 16000],
        'Q4 Sales': [25000, 13500, 35000, 9000, 18500],
        'Total': [80000, 42000, 120000, 27700, 61000],
        'Growth %': [12.5, 15.2, 8.7, 18.3, 13.1]
    }
    return pd.DataFrame(data)