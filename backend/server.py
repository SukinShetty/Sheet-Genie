from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import pandas as pd
import io
from backend.ai_service import AIService
from backend.excel_helpers import create_sample_data
from backend.google_sheets_service import GoogleSheetsService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
ai_service = AIService()
google_sheets_service = GoogleSheetsService()

# Create the main app without a prefix
app = FastAPI(title="SheetGenie API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    updated_data: Optional[List[List[Any]]] = None
    function_results: Optional[List[Dict]] = None
    session_id: Optional[str] = None
    error: Optional[str] = None

class SpreadsheetData(BaseModel):
    data: List[List[Any]]
    session_id: Optional[str] = None

class GoogleSheetRequest(BaseModel):
    url: str
    session_id: Optional[str] = None

# Routes
@api_router.get("/")
async def root():
    return {"message": "SheetGenie API is running!"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.get("/sample-data")
async def get_sample_data():
    """Get sample spreadsheet data"""
    try:
        data = ai_service.get_default_data()
        return {
            "success": True,
            "data": data,
            "message": "Sample data retrieved successfully"
        }
    except Exception as e:
        logging.error(f"Error getting sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    """Upload and process Excel file"""
    try:
        # Check file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
        
        # Read the file
        contents = await file.read()
        
        # Process Excel file
        df = pd.read_excel(io.BytesIO(contents))
        
        # Convert to list format
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Set the data in AI service
        ai_service.set_spreadsheet_data(data)
        
        return {
            "success": True,
            "data": data,
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "message": f"Excel file '{file.filename}' uploaded successfully"
        }
        
    except Exception as e:
        logging.error(f"Error uploading Excel file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/load-google-sheet")
async def load_google_sheet(request: GoogleSheetRequest):
    """Load data from Google Sheets URL"""
    try:
        # Validate URL first
        validation = google_sheets_service.validate_sheet_url(request.url)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        # Fetch data from Google Sheets
        result = google_sheets_service.fetch_sheet_data(request.url)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Set the data in AI service
        ai_service.set_spreadsheet_data(result["data"])
        
        return {
            "success": True,
            "data": result["data"],
            "sheet_id": result.get("sheet_id"),
            "method": result.get("method"),
            "rows": result.get("rows", 0),
            "columns": result.get("columns", 0),
            "message": result["message"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error loading Google Sheet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/validate-google-sheet")
async def validate_google_sheet_url(request: GoogleSheetRequest):
    """Validate Google Sheets URL"""
    try:
        validation = google_sheets_service.validate_sheet_url(request.url)
        return validation
    except Exception as e:
        logging.error(f"Error validating Google Sheet URL: {str(e)}")
        return {"valid": False, "error": str(e)}

@api_router.get("/google-sheets-help")
async def get_google_sheets_help():
    """Get help and instructions for Google Sheets integration"""
    try:
        instructions = google_sheets_service.create_sharing_instructions()
        sample_urls = google_sheets_service.get_sample_urls()
        
        return {
            "success": True,
            "instructions": instructions,
            "sample_urls": sample_urls,
            "message": "Google Sheets integration help"
        }
    except Exception as e:
        logging.error(f"Error getting Google Sheets help: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/set-spreadsheet-data")
async def set_spreadsheet_data(data: SpreadsheetData):
    """Set spreadsheet data for processing"""
    try:
        ai_service.set_spreadsheet_data(data.data)
        return {
            "success": True,
            "message": "Spreadsheet data set successfully",
            "rows": len(data.data) - 1,  # Subtract header row
            "columns": len(data.data[0]) if data.data else 0
        }
    except Exception as e:
        logging.error(f"Error setting spreadsheet data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """Process chat message with AI"""
    try:
        result = await ai_service.process_chat_message(message.message)
        
        return ChatResponse(
            success=result.get("success", False),
            response=result.get("response", ""),
            updated_data=result.get("updated_data"),
            function_results=result.get("function_results"),
            session_id=message.session_id,
            error=result.get("error")
        )
        
    except Exception as e:
        logging.error(f"Error processing chat message: {str(e)}")
        return ChatResponse(
            success=False,
            response="I'm sorry, I encountered an error processing your request.",
            error=str(e),
            session_id=message.session_id
        )

@api_router.get("/export-excel")
async def export_excel():
    """Export current spreadsheet data to Excel"""
    try:
        excel_data = ai_service.export_excel()
        
        # Create streaming response
        def generate():
            yield excel_data
        
        return StreamingResponse(
            generate(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=sheetgenie_export.xlsx"}
        )
        
    except Exception as e:
        logging.error(f"Error exporting Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SheetGenie API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

# Include the router in the main app
app.include_router(api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("SheetGenie API starting up...")
    # Initialize AI service with sample data
    sample_data = create_sample_data()
    data_list = [sample_data.columns.tolist()] + sample_data.values.tolist()
    ai_service.set_spreadsheet_data(data_list)
    logger.info("AI service initialized with sample data")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Cleanup on shutdown"""
    logger.info("SheetGenie API shutting down...")
    client.close()