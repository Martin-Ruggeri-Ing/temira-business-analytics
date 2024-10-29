# main.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from uuid import UUID
import pandas as pd

from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    message: str
    file_name: str
    id: str

app = FastAPI()

@app.post("/generate_pdf", response_model=FileUploadResponse)
async def upload_csv(id: UUID = Form(...), csv_file: UploadFile = File(...)):
    # Validar el tipo de archivo
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    # Leer el contenido del archivo
    try:
        df = pd.read_csv(csv_file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el CSV: {str(e)}")
    
    # Responder éxito
    return FileUploadResponse(
        message="Archivo CSV subido y procesado correctamente",
        file_name=csv_file.filename,
        id=str(id)
    )