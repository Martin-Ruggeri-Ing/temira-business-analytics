from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from uuid import UUID
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = FastAPI()

@app.post("/generate_pdf")
async def upload_csv(id: UUID = Form(...), csv_file: UploadFile = File(...)):
    # Validar el tipo de archivo
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    # Leer el contenido del archivo
    try:
        df = pd.read_csv(csv_file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el CSV: {str(e)}")
    
    # Crear el contenido del PDF usando el encabezado del CSV
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.drawString(100, 750, "Encabezado del CSV:")
    headers = ", ".join(df.columns)
    pdf.drawString(100, 730, headers)
    pdf.save()
    pdf_buffer.seek(0)
    
    # Generar el nombre del PDF a partir del nombre del CSV
    pdf_filename = os.path.splitext(csv_file.filename)[0] + ".pdf"

    # Enviar el PDF como respuesta usando StreamingResponse
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={pdf_filename}",
            "X-File-ID": str(id)
        }
    )