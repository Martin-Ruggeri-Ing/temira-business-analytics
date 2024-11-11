from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from uuid import UUID
from reportlab.lib.pagesizes import letter


from main_service import main_service

app = FastAPI()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import FileResponse
from uuid import UUID
from main_service import main_service

app = FastAPI()

# Primera API: recibe un ID y un archivo CSV, y devuelve el path del PDF generado
@app.post("/generate_pdf_path")
async def generate_pdf_path(id: UUID = Form(...), csv_file: UploadFile = File(...)):
    # Validar el tipo de archivo
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    # Leer el contenido del archivo y generar el PDF
    try:
        pdf_filename = f"{id}_pdf.pdf"
        pdf_path = main_service(csv_file.file, pdf_filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el CSV: {str(e)}")
    return {"pdf_path": pdf_path}

# Segunda API: recibe el path del PDF en el cuerpo de la solicitud y devuelve el PDF
@app.post("/get_pdf")
async def get_pdf(pdf_path: str = Body(...)):
    # Verificar si el archivo existe
    try:
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.split("/")[-1]
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al encontrar el archivo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")