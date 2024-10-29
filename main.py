from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse
from fpdf import FPDF
import os

app = FastAPI()

# Directorio para guardar PDFs generados temporalmente
TEMP_DIR = "temp_pdfs"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/generate_pdf/")
async def generate_pdf(
    request: Request,
    id: str,
    file: UploadFile = File(...)
):
    # # Verificar el origen de la solicitud
    # if request.client.host != "127.0.0.1" or request.client.port != 8080:
    #     raise HTTPException(status_code=403, detail="Request origin not allowed")
    
    # Generar un PDF vacío
    pdf_path = os.path.join(TEMP_DIR, f"{id}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"PDF generated for ID: {id}", ln=True, align="C")
    pdf.output(pdf_path)

    # Devolver el archivo PDF generado
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{id}.pdf")