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
        Generate a chart from the data for Recharts
        
        Args:
            chart_type: Type of chart ('bar', 'line', 'pie', 'scatter')
            x_column: Column name for x-axis
            y_column: Column name for y-axis (can be comma-separated for multiple series)
            title: Chart title
        
        Returns:
            Dict with chart data and configuration for Recharts
        """
        try:
            # Handle multiple y-columns for comparisons
            y_columns = [col.strip() for col in y_column.split(',')]
            
            # Prepare data for Recharts format
            chart_data = []
            for index, row in self.df.iterrows():
                data_point = {}
                
                # Handle x-axis data
                x_value = row[x_column]
                if pd.isna(x_value):
                    continue
                data_point[x_column] = str(x_value)
                
                # Handle y-axis data (potentially multiple columns)
                for y_col in y_columns:
                    if y_col in self.df.columns:
                        y_value = row[y_col]
                        if pd.isna(y_value):
                            y_value = 0
                        else:
                            try:
                                # Try to convert to number
                                y_value = float(pd.to_numeric(y_value, errors='coerce'))
                                if pd.isna(y_value):
                                    y_value = 0
                            except:
                                y_value = 0
                        data_point[y_col] = y_value
                
                chart_data.append(data_point)
            
            if title is None:
                if len(y_columns) > 1:
                    title = f"{' vs '.join(y_columns)} by {x_column}"
                else:
                    title = f"{y_columns[0]} by {x_column}"
            
            # Create Recharts-compatible configuration
            config = {
                "xAxisKey": x_column,
                "yAxisKey": y_columns[0],  # Primary y-axis
                "yAxisKeys": y_columns,    # All y-axis keys for multi-series
                "showGrid": True,
                "showTooltip": True,
                "showLegend": len(y_columns) > 1,
                "responsive": True
            }
            
            # Add type-specific configurations
            if chart_type.lower() == 'bar':
                config.update({
                    "barColors": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"][:len(y_columns)],
                })
            elif chart_type.lower() == 'line':
                config.update({
                    "lineColors": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"][:len(y_columns)],
                    "strokeWidth": 2,
                    "showDots": True
                })
            elif chart_type.lower() == 'pie':
                # For pie charts, use the first y-column
                config.update({
                    "nameKey": x_column,
                    "valueKey": y_columns[0],
                    "colors": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"],
                    "innerRadius": 0,
                    "outerRadius": 120
                })
            elif chart_type.lower() == 'area':
                config.update({
                    "areaColors": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"][:len(y_columns)],
                    "strokeColors": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"][:len(y_columns)]
                })
            elif chart_type.lower() == 'scatter':
                config.update({
                    "dotColor": "#8884d8",
                    "dotSize": 6
                })
            
            return {
                "success": True,
                "type": chart_type.lower(),
                "data": chart_data,
                "config": config,
                "title": title,
                "x_column": x_column,
                "y_column": y_column,
                "y_columns": y_columns,
                "message": f"Generated {chart_type} chart with {len(chart_data)} data points comparing {len(y_columns)} series"
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
    
    def query_data(self, question: str, filter_column: str = None, filter_value: str = None, count_column: str = None) -> Dict[str, Any]:
        """
        Query and analyze data to answer specific questions
        
        Args:
            question: The specific question being asked
            filter_column: Column to filter by
            filter_value: Value to filter for
            count_column: Column to count or analyze
        
        Returns:
            Dict with direct answer to the question
        """
        try:
            question_lower = question.lower()
            
            # Determine what type of question this is
            if any(word in question_lower for word in ['how many', 'count', 'number of']):
                return self._handle_count_question(question, filter_column, filter_value, count_column)
            elif any(word in question_lower for word in ['which', 'what', 'list', 'show']):
                return self._handle_list_question(question, filter_column, filter_value, count_column)
            elif any(word in question_lower for word in ['total', 'sum']):
                return self._handle_sum_question(question, filter_column, filter_value, count_column)
            elif any(word in question_lower for word in ['average', 'mean']):
                return self._handle_average_question(question, filter_column, filter_value, count_column)
            else:
                return self._handle_general_question(question, filter_column, filter_value, count_column)
                
        except Exception as e:
            logger.error(f"Error in query_data: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Could not answer the question: {question}"
            }
    
    def _handle_count_question(self, question: str, filter_column: str, filter_value: str, count_column: str) -> Dict[str, Any]:
        """Handle counting questions"""
        try:
            df_filtered = self.df.copy()
            
            # Auto-detect filter from question if not provided
            if not filter_column or not filter_value:
                filter_column, filter_value = self._extract_filter_from_question(question)
            
            # Apply filter if specified
            if filter_column and filter_value and filter_column in self.df.columns:
                # Case-insensitive filtering
                df_filtered = df_filtered[df_filtered[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
            
            # Count the results
            count = len(df_filtered)
            
            # Create a descriptive message
            if filter_column and filter_value:
                message = f"Found {count} items where {filter_column} contains '{filter_value}'"
            else:
                message = f"Total count: {count} items"
            
            return {
                "success": True,
                "result": count,
                "question": question,
                "filter_applied": f"{filter_column} = {filter_value}" if filter_column and filter_value else "None",
                "message": message,
                "data_sample": df_filtered.head(5).to_dict('records') if len(df_filtered) > 0 else []
            }
            
        except Exception as e:
            logger.error(f"Error in count question: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _handle_list_question(self, question: str, filter_column: str, filter_value: str, count_column: str) -> Dict[str, Any]:
        """Handle listing/showing questions"""
        try:
            df_filtered = self.df.copy()
            
            # Auto-detect filter from question if not provided
            if not filter_column or not filter_value:
                filter_column, filter_value = self._extract_filter_from_question(question)
            
            # Apply filter if specified
            if filter_column and filter_value and filter_column in self.df.columns:
                df_filtered = df_filtered[df_filtered[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
            
            # Limit results to prevent overwhelming response
            results = df_filtered.head(10).to_dict('records')
            total_count = len(df_filtered)
            
            message = f"Found {total_count} matching items"
            if total_count > 10:
                message += " (showing first 10)"
            
            return {
                "success": True,
                "result": results,
                "total_count": total_count,
                "question": question,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error in list question: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _handle_sum_question(self, question: str, filter_column: str, filter_value: str, count_column: str) -> Dict[str, Any]:
        """Handle sum/total questions"""
        try:
            df_filtered = self.df.copy()
            
            # Auto-detect filter and numeric column
            if not filter_column or not filter_value:
                filter_column, filter_value = self._extract_filter_from_question(question)
            
            if not count_column:
                count_column = self._detect_numeric_column_from_question(question)
            
            # Apply filter if specified
            if filter_column and filter_value and filter_column in self.df.columns:
                df_filtered = df_filtered[df_filtered[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
            
            # Calculate sum
            if count_column and count_column in df_filtered.columns:
                total = pd.to_numeric(df_filtered[count_column], errors='coerce').sum()
                message = f"Total {count_column}: {total}"
            else:
                total = len(df_filtered)
                message = f"Total count: {total}"
            
            return {
                "success": True,
                "result": float(total),
                "question": question,
                "column_summed": count_column,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error in sum question: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _handle_average_question(self, question: str, filter_column: str, filter_value: str, count_column: str) -> Dict[str, Any]:
        """Handle average questions"""
        try:
            df_filtered = self.df.copy()
            
            # Auto-detect filter and numeric column
            if not filter_column or not filter_value:
                filter_column, filter_value = self._extract_filter_from_question(question)
            
            if not count_column:
                count_column = self._detect_numeric_column_from_question(question)
            
            # Apply filter if specified
            if filter_column and filter_value and filter_column in self.df.columns:
                df_filtered = df_filtered[df_filtered[filter_column].astype(str).str.contains(filter_value, case=False, na=False)]
            
            # Calculate average
            if count_column and count_column in df_filtered.columns:
                avg = pd.to_numeric(df_filtered[count_column], errors='coerce').mean()
                message = f"Average {count_column}: {avg:.2f}"
            else:
                avg = len(df_filtered)
                message = f"Count: {avg}"
            
            return {
                "success": True,
                "result": float(avg),
                "question": question,
                "column_averaged": count_column,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error in average question: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _handle_general_question(self, question: str, filter_column: str, filter_value: str, count_column: str) -> Dict[str, Any]:
        """Handle general questions about the data"""
        try:
            # Provide data overview
            total_rows = len(self.df)
            columns = list(self.df.columns)
            
            # Try to find relevant information based on question keywords
            question_lower = question.lower()
            relevant_info = []
            
            for col in columns:
                if any(word in col.lower() for word in question_lower.split()):
                    unique_values = self.df[col].value_counts().head(5)
                    relevant_info.append(f"{col}: {dict(unique_values)}")
            
            message = f"Data overview: {total_rows} rows, {len(columns)} columns"
            if relevant_info:
                message += f"\nRelevant data: {'; '.join(relevant_info)}"
            
            return {
                "success": True,
                "result": {
                    "total_rows": total_rows,
                    "columns": columns,
                    "relevant_info": relevant_info
                },
                "question": question,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Error in general question: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _extract_filter_from_question(self, question: str) -> tuple:
        """Extract filter column and value from natural language question"""
        question_lower = question.lower()
        
        # Look for patterns like "sukin has finished", "products are pending", etc.
        for col in self.df.columns:
            col_lower = col.lower()
            if col_lower in question_lower:
                # Found a column name in the question
                # Now look for values in that column that appear in the question
                unique_values = self.df[col].astype(str).str.lower().unique()
                for value in unique_values:
                    if value in question_lower and len(value) > 2:  # Avoid short meaningless matches
                        return col, value
        
        # Try to find common patterns
        if 'sukin' in question_lower:
            # Look for columns that might contain 'sukin'
            for col in self.df.columns:
                if self.df[col].astype(str).str.contains('sukin', case=False).any():
                    return col, 'sukin'
        
        if 'pending' in question_lower:
            for col in self.df.columns:
                if self.df[col].astype(str).str.contains('pending', case=False).any():
                    return col, 'pending'
        
        if 'finished' in question_lower or 'complete' in question_lower:
            for col in self.df.columns:
                if any(self.df[col].astype(str).str.contains(word, case=False).any() for word in ['finished', 'complete', 'done']):
                    return col, 'finished'
        
        return None, None
    
    def _detect_numeric_column_from_question(self, question: str) -> str:
        """Detect which numeric column the question is asking about"""
        question_lower = question.lower()
        
        # Check if question mentions specific column names
        for col in self.df.columns:
            if col.lower() in question_lower:
                # Check if it's numeric
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    return col
        
        # Default to first numeric column
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                return col
        
        return None
    
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