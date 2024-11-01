from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from uuid import UUID
from reportlab.lib.pagesizes import letter
import os

from main_service import main_service

app = FastAPI()

@app.post("/generate_pdf")
async def upload_csv(id: UUID = Form(...), csv_file: UploadFile = File(...)):
    # Validar el tipo de archivo
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    # Leer el contenido del archivo
    try:
        pdf_filename = f"{id}_pdf.pdf"
        pdf_path = main_service(csv_file.file, pdf_filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el CSV: {str(e)}")

    # Enviar el PDF como respuesta usando StreamingResponse
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_filename
    )

if __name__ == "__main__":
    import uvicorn
    # para poder hacer debug en el código
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")