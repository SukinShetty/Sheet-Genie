import os
import json
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
from openai import OpenAI
from backend.excel_helpers import ExcelHelper, create_sample_data
from backend.advanced_analytics import AdvancedAnalytics
from backend.chart_generator import ChartGenerator

logger = logging.getLogger(__name__)

class AIService:
    """Service for handling AI interactions with OpenAI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.current_data = None
        self.excel_helper = None
        self.analytics = None
        self.chart_generator = None
    
    def set_spreadsheet_data(self, data: List[List[Any]]) -> None:
        """Set the current spreadsheet data"""
        try:
            # Convert to DataFrame, ensuring all data is properly formatted
            if not data or len(data) < 2:
                # Fallback to sample data
                self.current_data = create_sample_data()
                self.excel_helper = ExcelHelper(self.current_data)
                return
            
            # Convert all data to strings first to handle mixed types
            headers = [str(item) for item in data[0]]
            rows = []
            for row in data[1:]:
                formatted_row = []
                for item in row:
                    if isinstance(item, (int, float)):
                        formatted_row.append(item)
                    else:
                        formatted_row.append(str(item))
                rows.append(formatted_row)
            
            # Create DataFrame
            self.current_data = pd.DataFrame(rows, columns=headers)
            self.excel_helper = ExcelHelper(self.current_data)
            logger.info(f"Set spreadsheet data with {len(self.current_data)} rows")
        except Exception as e:
            logger.error(f"Error setting spreadsheet data: {str(e)}")
            # Fallback to sample data
            self.current_data = create_sample_data()
            self.excel_helper = ExcelHelper(self.current_data)
    
    def get_default_data(self) -> List[List[Any]]:
        """Get default sample data"""
        df = create_sample_data()
        # Convert to list format with headers
        data = [df.columns.tolist()] + df.values.tolist()
        return data
    
    async def process_chat_message(self, message: str) -> Dict[str, Any]:
        """Process a chat message using OpenAI function calling"""
        try:
            # If no data is set, use sample data
            if self.current_data is None:
                self.current_data = create_sample_data()
                self.excel_helper = ExcelHelper(self.current_data)
            
            # Define available functions
            functions = [
                {
                    "type": "function",
                    "function": {
                        "name": "sum_range",
                        "description": "Calculate the sum of a range of cells",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "range_spec": {
                                    "type": "string",
                                    "description": "Range specification like 'A1:A10' or 'B2:D5'"
                                }
                            },
                            "required": ["range_spec"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "average_range",
                        "description": "Calculate the average of a range of cells",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "range_spec": {
                                    "type": "string",
                                    "description": "Range specification like 'A1:A10' or 'B2:D5'"
                                }
                            },
                            "required": ["range_spec"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "create_pivot",
                        "description": "Create a pivot table from the data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "rows": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of column names to use as rows"
                                },
                                "values": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of column names to aggregate"
                                },
                                "aggfunc": {
                                    "type": "string",
                                    "enum": ["sum", "mean", "count", "max", "min"],
                                    "description": "Aggregation function to use"
                                }
                            },
                            "required": ["rows", "values"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "generate_chart",
                        "description": "Generate a chart from the data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "chart_type": {
                                    "type": "string",
                                    "enum": ["bar", "line", "pie", "scatter"],
                                    "description": "Type of chart to generate"
                                },
                                "x_column": {
                                    "type": "string",
                                    "description": "Column name for x-axis"
                                },
                                "y_column": {
                                    "type": "string",
                                    "description": "Column name for y-axis"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Chart title"
                                }
                            },
                            "required": ["chart_type", "x_column", "y_column"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "format_cells",
                        "description": "Format cells in the specified range",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "range_spec": {
                                    "type": "string",
                                    "description": "Range specification like 'A1:A10' or 'B2:D5'"
                                },
                                "format_type": {
                                    "type": "string",
                                    "enum": ["currency", "percentage", "date", "bold", "color"],
                                    "description": "Type of formatting to apply"
                                },
                                "format_value": {
                                    "type": "string",
                                    "description": "Additional format value (e.g., color code)"
                                }
                            },
                            "required": ["range_spec", "format_type"]
                        }
                    }
                }
            ]
            
            # Create context about the current data
            data_context = f"Current spreadsheet data has {len(self.current_data)} rows and {len(self.current_data.columns)} columns. "
            data_context += f"Columns: {', '.join(self.current_data.columns.tolist())}. "
            data_context += f"Sample data: {self.current_data.head(3).to_string()}"
            
            # Create the chat completion request
            messages = [
                {
                    "role": "system",
                    "content": f"""You are SheetGenie, an AI assistant that helps users with Excel spreadsheet tasks. 
                    You can perform calculations, create charts, format cells, and provide insights about spreadsheet data.
                    
                    {data_context}
                    
                    IMPORTANT FORMATTING RULES:
                    - Always format your responses in clear bullet points
                    - Use short, concise sentences
                    - Break down complex information into digestible points
                    - Use • for main points and ◦ for sub-points
                    - Keep each bullet point to 1-2 lines maximum
                    - Use numbers (1., 2., 3.) for sequential steps or rankings
                    
                    When users ask for help, analyze their request and use the appropriate function if needed.
                    Always provide clear, helpful responses in bullet point format and explain what you're doing."""
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
            
            # Call OpenAI API
            response = await self._call_openai_api(messages, functions)
            
            # Process the response
            result = await self._process_openai_response(response)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Sorry, I encountered an error processing your request.",
                "response": "I'm having trouble processing your request right now. Please try again."
            }
    
    async def _call_openai_api(self, messages: List[Dict], functions: List[Dict]) -> Any:
        """Call OpenAI API with function calling"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=functions,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1000
            )
            return response
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    async def _process_openai_response(self, response: Any) -> Dict[str, Any]:
        """Process OpenAI response and execute any function calls"""
        try:
            message = response.choices[0].message
            
            # Check if there are tool calls
            if message.tool_calls:
                # Process each tool call
                function_results = []
                
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the function
                    result = await self._execute_function(function_name, function_args)
                    function_results.append(result)
                
                # Get the updated data
                updated_data = self.excel_helper.get_updated_data()
                
                return {
                    "success": True,
                    "message": message.content or "Function executed successfully",
                    "function_results": function_results,
                    "updated_data": updated_data,
                    "response": self._format_ai_response(self._format_function_response(function_results))
                }
            else:
                # No function calls, just return the message with formatting
                formatted_response = self._format_ai_response(message.content)
                return {
                    "success": True,
                    "message": message.content,
                    "response": formatted_response,
                    "updated_data": self.excel_helper.get_updated_data() if self.excel_helper else None
                }
                
        except Exception as e:
            logger.error(f"Error processing OpenAI response: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Error processing AI response",
                "response": "I encountered an error while processing the response."
            }
    
    async def _execute_function(self, function_name: str, function_args: Dict) -> Dict[str, Any]:
        """Execute a function call"""
        try:
            if function_name == "sum_range":
                return self.excel_helper.sum_range(function_args["range_spec"])
            elif function_name == "average_range":
                return self.excel_helper.average_range(function_args["range_spec"])
            elif function_name == "create_pivot":
                return self.excel_helper.create_pivot(
                    function_args["rows"],
                    function_args["values"],
                    function_args.get("aggfunc", "sum")
                )
            elif function_name == "generate_chart":
                return self.excel_helper.generate_chart(
                    function_args["chart_type"],
                    function_args["x_column"],
                    function_args["y_column"],
                    function_args.get("title")
                )
            elif function_name == "format_cells":
                return self.excel_helper.format_cells(
                    function_args["range_spec"],
                    function_args["format_type"],
                    function_args.get("format_value")
                )
            else:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}",
                    "message": f"Function {function_name} is not supported"
                }
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing {function_name}"
            }
    
    def _format_function_response(self, function_results: List[Dict]) -> str:
        """Format function results into a readable response with bullet points"""
        if not function_results:
            return "No functions were executed."
        
        responses = []
        for result in function_results:
            if result.get("success"):
                message = result.get("message", "Function executed successfully")
                # Format as bullet point
                responses.append(f"• {message}")
            else:
                error_msg = result.get('error', 'Unknown error')
                responses.append(f"• Error: {error_msg}")
        
        return "\n".join(responses)
    
    def _format_ai_response(self, text: str) -> str:
        """Format AI response text into better bullet points"""
        if not text:
            return text
            
        # Split into sentences and convert to bullet points if it's a long paragraph
        sentences = text.split('. ')
        
        # If it's already formatted or short, return as is
        if '•' in text or '◦' in text or len(sentences) <= 2:
            return text
            
        # If it's a long paragraph, convert to bullet points
        if len(sentences) > 3:
            formatted_points = []
            for i, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if sentence and not sentence.endswith('.'):
                    sentence += '.'
                if sentence:
                    formatted_points.append(f"• {sentence}")
            return "\n".join(formatted_points)
        
        return text
    
    def export_excel(self) -> bytes:
        """Export current data to Excel format"""
        if self.excel_helper:
            return self.excel_helper.export_to_excel()
        else:
            # Create sample data and export
            df = create_sample_data()
            helper = ExcelHelper(df)
            return helper.export_to_excel()