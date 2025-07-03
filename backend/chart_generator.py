import pandas as pd
import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ChartGenerator:
    """Advanced chart generation for data visualization"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = self._get_numeric_columns()
        self.categorical_columns = self._get_categorical_columns()
    
    def _get_numeric_columns(self) -> List[str]:
        """Get numeric columns from dataframe"""
        numeric_cols = []
        for col in self.df.columns:
            try:
                pd.to_numeric(self.df[col], errors='coerce')
                numeric_count = pd.to_numeric(self.df[col], errors='coerce').notna().sum()
                if numeric_count > len(self.df) * 0.5:
                    numeric_cols.append(col)
            except:
                continue
        return numeric_cols
    
    def _get_categorical_columns(self) -> List[str]:
        """Get categorical columns from dataframe"""
        return [col for col in self.df.columns if col not in self.numeric_columns]
    
    def generate_chart_config(self, chart_type: str, x_column: str, y_column: str, 
                            title: str = None, theme: str = "default") -> Dict[str, Any]:
        """Generate chart configuration for React/Recharts"""
        
        try:
            # Prepare data
            chart_data = []
            for index, row in self.df.iterrows():
                data_point = {}
                data_point[x_column] = row[x_column]
                
                if y_column in self.numeric_columns:
                    try:
                        data_point[y_column] = float(pd.to_numeric(row[y_column], errors='coerce'))
                    except:
                        data_point[y_column] = 0
                else:
                    data_point[y_column] = row[y_column]
                
                chart_data.append(data_point)
            
            # Color schemes
            color_schemes = {
                "default": ["#8884d8", "#82ca9d", "#ffc658", "#ff7c7c", "#8dd1e1"],
                "business": ["#2563eb", "#16a34a", "#dc2626", "#ca8a04", "#9333ea"],
                "modern": ["#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"],
                "professional": ["#1f2937", "#374151", "#6b7280", "#9ca3af", "#d1d5db"]
            }
            
            colors = color_schemes.get(theme, color_schemes["default"])
            
            if title is None:
                title = f"{y_column} by {x_column}"
            
            # Generate configuration based on chart type
            if chart_type.lower() == "bar":
                return self._create_bar_chart_config(chart_data, x_column, y_column, title, colors)
            elif chart_type.lower() == "line":
                return self._create_line_chart_config(chart_data, x_column, y_column, title, colors)
            elif chart_type.lower() == "pie":
                return self._create_pie_chart_config(chart_data, x_column, y_column, title, colors)
            elif chart_type.lower() == "area":
                return self._create_area_chart_config(chart_data, x_column, y_column, title, colors)
            elif chart_type.lower() == "scatter":
                return self._create_scatter_chart_config(chart_data, x_column, y_column, title, colors)
            else:
                return self._create_bar_chart_config(chart_data, x_column, y_column, title, colors)
                
        except Exception as e:
            logger.error(f"Error generating chart config: {str(e)}")
            return {"error": f"Chart generation failed: {str(e)}"}
    
    def _create_bar_chart_config(self, data: List[Dict], x_col: str, y_col: str, 
                                title: str, colors: List[str]) -> Dict[str, Any]:
        """Create bar chart configuration"""
        return {
            "type": "bar",
            "data": data,
            "title": title,
            "config": {
                "xAxisKey": x_col,
                "yAxisKey": y_col,
                "barColor": colors[0],
                "showGrid": True,
                "showTooltip": True,
                "showLegend": False,
                "responsive": True
            },
            "layout": {
                "width": "100%",
                "height": 300,
                "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5}
            }
        }
    
    def _create_line_chart_config(self, data: List[Dict], x_col: str, y_col: str, 
                                 title: str, colors: List[str]) -> Dict[str, Any]:
        """Create line chart configuration"""
        return {
            "type": "line",
            "data": data,
            "title": title,
            "config": {
                "xAxisKey": x_col,
                "yAxisKey": y_col,
                "lineColor": colors[0],
                "strokeWidth": 2,
                "showGrid": True,
                "showTooltip": True,
                "showLegend": False,
                "showDots": True,
                "responsive": True
            },
            "layout": {
                "width": "100%",
                "height": 300,
                "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5}
            }
        }
    
    def _create_pie_chart_config(self, data: List[Dict], x_col: str, y_col: str, 
                                title: str, colors: List[str]) -> Dict[str, Any]:
        """Create pie chart configuration"""
        return {
            "type": "pie",
            "data": data,
            "title": title,
            "config": {
                "nameKey": x_col,
                "valueKey": y_col,
                "colors": colors,
                "showTooltip": True,
                "showLegend": True,
                "responsive": True,
                "innerRadius": 0,
                "outerRadius": 120
            },
            "layout": {
                "width": "100%",
                "height": 300,
                "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5}
            }
        }
    
    def _create_area_chart_config(self, data: List[Dict], x_col: str, y_col: str, 
                                 title: str, colors: List[str]) -> Dict[str, Any]:
        """Create area chart configuration"""
        return {
            "type": "area",
            "data": data,
            "title": title,
            "config": {
                "xAxisKey": x_col,
                "yAxisKey": y_col,
                "areaColor": colors[0],
                "strokeColor": colors[1],
                "showGrid": True,
                "showTooltip": True,
                "showLegend": False,
                "responsive": True
            },
            "layout": {
                "width": "100%",
                "height": 300,
                "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5}
            }
        }
    
    def _create_scatter_chart_config(self, data: List[Dict], x_col: str, y_col: str, 
                                    title: str, colors: List[str]) -> Dict[str, Any]:
        """Create scatter plot configuration"""
        return {
            "type": "scatter",
            "data": data,
            "title": title,
            "config": {
                "xAxisKey": x_col,
                "yAxisKey": y_col,
                "dotColor": colors[0],
                "dotSize": 6,
                "showGrid": True,
                "showTooltip": True,
                "showLegend": False,
                "responsive": True
            },
            "layout": {
                "width": "100%",
                "height": 300,
                "margin": {"top": 20, "right": 30, "left": 20, "bottom": 5}
            }
        }
    
    def suggest_best_chart_type(self, x_column: str, y_column: str) -> Dict[str, Any]:
        """Suggest the best chart type based on data types"""
        
        x_is_categorical = x_column in self.categorical_columns
        y_is_categorical = y_column in self.categorical_columns
        
        # Count unique values
        x_unique_count = self.df[x_column].nunique()
        y_unique_count = self.df[y_column].nunique()
        
        suggestions = []
        
        if x_is_categorical and not y_is_categorical:
            if x_unique_count <= 10:
                suggestions.append({
                    "chart_type": "bar",
                    "reason": "Best for comparing numeric values across categories",
                    "confidence": "high"
                })
                suggestions.append({
                    "chart_type": "pie",
                    "reason": "Good for showing proportions when categories < 10",
                    "confidence": "medium"
                })
            else:
                suggestions.append({
                    "chart_type": "bar",
                    "reason": "Bar chart handles many categories well",
                    "confidence": "medium"
                })
        
        elif not x_is_categorical and not y_is_categorical:
            suggestions.append({
                "chart_type": "scatter",
                "reason": "Perfect for showing correlation between two numeric variables",
                "confidence": "high"
            })
            suggestions.append({
                "chart_type": "line",
                "reason": "Good if x-axis represents time or sequential data",
                "confidence": "medium"
            })
        
        elif not x_is_categorical and y_is_categorical:
            suggestions.append({
                "chart_type": "bar",
                "reason": "Switch axes - categories work better on x-axis",
                "confidence": "medium"
            })
        
        else:  # Both categorical
            suggestions.append({
                "chart_type": "bar",
                "reason": "Consider aggregating data first",
                "confidence": "low"
            })
        
        # Time series detection
        if any(keyword in x_column.lower() for keyword in ['date', 'time', 'month', 'quarter', 'year']):
            suggestions.insert(0, {
                "chart_type": "line",
                "reason": "Time series data is best visualized with line charts",
                "confidence": "very_high"
            })
        
        return {
            "recommended_charts": suggestions,
            "data_analysis": {
                "x_column_type": "categorical" if x_is_categorical else "numeric",
                "y_column_type": "categorical" if y_is_categorical else "numeric",
                "x_unique_values": x_unique_count,
                "y_unique_values": y_unique_count
            }
        }
    
    def create_dashboard_config(self) -> Dict[str, Any]:
        """Create a dashboard with multiple chart suggestions"""
        
        dashboard_charts = []
        
        # Try to create meaningful combinations
        for i, y_col in enumerate(self.numeric_columns[:3]):  # Max 3 charts
            for x_col in self.categorical_columns[:2]:  # Try up to 2 categorical columns
                suggestion = self.suggest_best_chart_type(x_col, y_col)
                if suggestion["recommended_charts"]:
                    best_chart = suggestion["recommended_charts"][0]
                    chart_config = self.generate_chart_config(
                        best_chart["chart_type"], 
                        x_col, 
                        y_col,
                        f"{y_col} Analysis"
                    )
                    dashboard_charts.append({
                        "id": f"chart_{i}",
                        "title": f"{y_col} by {x_col}",
                        "chart_type": best_chart["chart_type"],
                        "config": chart_config,
                        "position": {"x": (i % 2) * 6, "y": (i // 2) * 4, "w": 6, "h": 4}
                    })
                    break
        
        return {
            "dashboard_id": "auto_generated",
            "title": "Data Analysis Dashboard",
            "charts": dashboard_charts,
            "layout": "grid",
            "theme": "professional"
        }