import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Advanced analytics and AI-powered insights for spreadsheet data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = self._identify_numeric_columns()
        self.date_columns = self._identify_date_columns()
        self.categorical_columns = self._identify_categorical_columns()
    
    def _identify_numeric_columns(self) -> List[str]:
        """Identify numeric columns in the dataframe"""
        numeric_cols = []
        for col in self.df.columns:
            try:
                pd.to_numeric(self.df[col], errors='coerce')
                # Check if conversion was successful for most values
                numeric_count = pd.to_numeric(self.df[col], errors='coerce').notna().sum()
                if numeric_count > len(self.df) * 0.5:  # More than 50% are numeric
                    numeric_cols.append(col)
            except:
                continue
        return numeric_cols
    
    def _identify_date_columns(self) -> List[str]:
        """Identify date columns in the dataframe"""
        date_cols = []
        for col in self.df.columns:
            try:
                pd.to_datetime(self.df[col], errors='coerce')
                date_count = pd.to_datetime(self.df[col], errors='coerce').notna().sum()
                if date_count > len(self.df) * 0.5:
                    date_cols.append(col)
            except:
                continue
        return date_cols
    
    def _identify_categorical_columns(self) -> List[str]:
        """Identify categorical columns"""
        categorical_cols = []
        for col in self.df.columns:
            if col not in self.numeric_columns and col not in self.date_columns:
                categorical_cols.append(col)
        return categorical_cols
    
    def generate_insights(self) -> Dict[str, Any]:
        """Generate comprehensive insights about the data"""
        insights = {
            "data_summary": self._get_data_summary(),
            "statistical_insights": self._get_statistical_insights(),
            "trend_analysis": self._get_trend_analysis(),
            "correlation_analysis": self._get_correlation_analysis(),
            "outlier_detection": self._detect_outliers(),
            "recommendations": self._generate_recommendations()
        }
        return insights
    
    def _get_data_summary(self) -> Dict[str, Any]:
        """Get basic data summary"""
        return {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "numeric_columns": len(self.numeric_columns),
            "categorical_columns": len(self.categorical_columns),
            "date_columns": len(self.date_columns),
            "missing_values": self.df.isnull().sum().to_dict(),
            "data_types": self.df.dtypes.astype(str).to_dict()
        }
    
    def _get_statistical_insights(self) -> Dict[str, Any]:
        """Generate statistical insights for numeric columns"""
        insights = {}
        
        for col in self.numeric_columns:
            try:
                series = pd.to_numeric(self.df[col], errors='coerce').dropna()
                if len(series) > 0:
                    insights[col] = {
                        "mean": float(series.mean()),
                        "median": float(series.median()),
                        "std": float(series.std()),
                        "min": float(series.min()),
                        "max": float(series.max()),
                        "range": float(series.max() - series.min()),
                        "coefficient_variation": float(series.std() / series.mean()) if series.mean() != 0 else 0,
                        "quartiles": {
                            "q1": float(series.quantile(0.25)),
                            "q2": float(series.quantile(0.5)),
                            "q3": float(series.quantile(0.75))
                        }
                    }
            except Exception as e:
                logger.error(f"Error calculating statistics for {col}: {str(e)}")
                
        return insights
    
    def _get_trend_analysis(self) -> Dict[str, Any]:
        """Analyze trends in the data"""
        trends = {}
        
        # If we have sequential data (like quarters, months), analyze trends
        for col in self.numeric_columns:
            try:
                series = pd.to_numeric(self.df[col], errors='coerce').dropna()
                if len(series) > 2:
                    # Calculate trend direction
                    trend_slope = np.polyfit(range(len(series)), series, 1)[0]
                    
                    # Calculate growth rate
                    if len(series) > 1:
                        growth_rate = ((series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100) if series.iloc[0] != 0 else 0
                    else:
                        growth_rate = 0
                    
                    trends[col] = {
                        "trend_direction": "increasing" if trend_slope > 0 else "decreasing" if trend_slope < 0 else "stable",
                        "trend_strength": abs(trend_slope),
                        "growth_rate_percent": float(growth_rate),
                        "volatility": float(series.std() / series.mean()) if series.mean() != 0 else 0
                    }
            except Exception as e:
                logger.error(f"Error calculating trends for {col}: {str(e)}")
                
        return trends
    
    def _get_correlation_analysis(self) -> Dict[str, Any]:
        """Analyze correlations between numeric columns"""
        correlations = {}
        
        if len(self.numeric_columns) > 1:
            try:
                # Create correlation matrix for numeric columns only
                numeric_df = self.df[self.numeric_columns].apply(pd.to_numeric, errors='coerce')
                corr_matrix = numeric_df.corr()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_value = corr_matrix.iloc[i, j]
                        if abs(corr_value) > 0.7:  # Strong correlation threshold
                            strong_correlations.append({
                                "column1": corr_matrix.columns[i],
                                "column2": corr_matrix.columns[j],
                                "correlation": float(corr_value),
                                "strength": "strong positive" if corr_value > 0.7 else "strong negative"
                            })
                
                correlations = {
                    "correlation_matrix": corr_matrix.round(3).to_dict(),
                    "strong_correlations": strong_correlations
                }
            except Exception as e:
                logger.error(f"Error calculating correlations: {str(e)}")
                
        return correlations
    
    def _detect_outliers(self) -> Dict[str, Any]:
        """Detect outliers in numeric columns using IQR method"""
        outliers = {}
        
        for col in self.numeric_columns:
            try:
                series = pd.to_numeric(self.df[col], errors='coerce').dropna()
                if len(series) > 4:  # Need at least 5 points for meaningful outlier detection
                    Q1 = series.quantile(0.25)
                    Q3 = series.quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outlier_indices = series[(series < lower_bound) | (series > upper_bound)].index.tolist()
                    outlier_values = series[(series < lower_bound) | (series > upper_bound)].tolist()
                    
                    if outlier_indices:
                        outliers[col] = {
                            "outlier_count": len(outlier_indices),
                            "outlier_percentage": len(outlier_indices) / len(series) * 100,
                            "outlier_values": [float(x) for x in outlier_values],
                            "lower_bound": float(lower_bound),
                            "upper_bound": float(upper_bound)
                        }
            except Exception as e:
                logger.error(f"Error detecting outliers for {col}: {str(e)}")
                
        return outliers
    
    def _generate_recommendations(self) -> List[str]:
        """Generate AI-powered recommendations based on the analysis"""
        recommendations = []
        
        try:
            # Check data quality
            missing_percentage = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
            if missing_percentage > 10:
                recommendations.append(f"• Consider addressing missing data ({missing_percentage:.1f}% of total data)")
            
            # Check for trends
            trends = self._get_trend_analysis()
            for col, trend_data in trends.items():
                if trend_data["growth_rate_percent"] > 20:
                    recommendations.append(f"• {col} shows strong growth ({trend_data['growth_rate_percent']:.1f}%) - consider scaling strategies")
                elif trend_data["growth_rate_percent"] < -10:
                    recommendations.append(f"• {col} shows decline ({trend_data['growth_rate_percent']:.1f}%) - investigate causes")
            
            # Check for outliers
            outliers = self._detect_outliers()
            for col, outlier_data in outliers.items():
                if outlier_data["outlier_percentage"] > 15:
                    recommendations.append(f"• {col} has many outliers ({outlier_data['outlier_percentage']:.1f}%) - review data quality")
            
            # Check correlations
            correlations = self._get_correlation_analysis()
            if "strong_correlations" in correlations:
                for corr in correlations["strong_correlations"]:
                    recommendations.append(f"• Strong correlation between {corr['column1']} and {corr['column2']} ({corr['correlation']:.2f})")
            
            if not recommendations:
                recommendations.append("• Data appears well-structured with no major issues detected")
                recommendations.append("• Consider creating visualizations to better understand patterns")
        
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            recommendations.append("• Unable to generate specific recommendations - data analysis completed")
        
        return recommendations
    
    def create_summary_report(self) -> str:
        """Create a comprehensive summary report"""
        insights = self.generate_insights()
        
        report = "📊 **DATA ANALYSIS REPORT**\n\n"
        
        # Data Summary
        summary = insights["data_summary"]
        report += "**📋 Data Overview:**\n"
        report += f"• Dataset: {summary['total_rows']} rows × {summary['total_columns']} columns\n"
        report += f"• Numeric columns: {summary['numeric_columns']}\n"
        report += f"• Categorical columns: {summary['categorical_columns']}\n\n"
        
        # Key Statistics
        if insights["statistical_insights"]:
            report += "**📈 Key Statistics:**\n"
            for col, stats in list(insights["statistical_insights"].items())[:3]:  # Top 3 columns
                report += f"• {col}: Mean = {stats['mean']:.2f}, Range = {stats['range']:.2f}\n"
            report += "\n"
        
        # Trends
        if insights["trend_analysis"]:
            report += "**📊 Trend Analysis:**\n"
            for col, trend in insights["trend_analysis"].items():
                direction = trend["trend_direction"]
                growth = trend["growth_rate_percent"]
                report += f"• {col}: {direction} trend ({growth:+.1f}% growth)\n"
            report += "\n"
        
        # Recommendations
        if insights["recommendations"]:
            report += "**💡 Recommendations:**\n"
            for rec in insights["recommendations"][:5]:  # Top 5 recommendations
                report += f"{rec}\n"
        
        return report
    
    def forecast_next_period(self, column: str, periods: int = 1) -> Dict[str, Any]:
        """Simple forecasting for numeric columns"""
        try:
            series = pd.to_numeric(self.df[column], errors='coerce').dropna()
            if len(series) < 3:
                return {"error": "Need at least 3 data points for forecasting"}
            
            # Simple linear trend forecasting
            x = np.arange(len(series))
            coeffs = np.polyfit(x, series, 1)
            
            forecasts = []
            for i in range(1, periods + 1):
                forecast_value = coeffs[0] * (len(series) + i - 1) + coeffs[1]
                forecasts.append(float(forecast_value))
            
            return {
                "column": column,
                "forecasts": forecasts,
                "trend_slope": float(coeffs[0]),
                "confidence": "medium",  # Simple model, medium confidence
                "method": "linear_trend"
            }
        except Exception as e:
            logger.error(f"Error forecasting {column}: {str(e)}")
            return {"error": f"Forecasting failed: {str(e)}"}