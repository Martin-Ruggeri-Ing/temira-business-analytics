from csv_service import agregar_horas, agregar_recorrido, cargar_datos
from data_analysis_service import obtener_datos_para_barras_de_frecuencias_agrupadas_por_recorrido, obtener_datos_para_diagrama_de_areas_de_frecuencias_por_hora, obtener_datos_para_grafico_torta
from data_visualization_service import generar_diagrama_de_areas_de_frecuencias_por_hora, generar_diagrama_de_barras_de_frecuencias_agrupadas_por_recorrido, generar_grafico_torta, guardar_en_cache
from encryption_service import get_temp_path_file
from pdf_service import generar_informe_pdf


def main_service(file_csv, pdf_filename):

    # clave_privada = leer_clave('privada')

    # ruta_temporal_archivo_encritado = get_temp_path_encrypted_file(archivo_encriptado)

    # contenido_desencriptado = desencriptar_archivo(clave_privada, ruta_temporal_archivo_encritado)

    ruta_temporal_archivo_desencritado = get_temp_path_file(file_csv)

    datos = cargar_datos(ruta_temporal_archivo_desencritado)

    # Mostrar el diagrama de torta
    datos_para_grafico_torta = obtener_datos_para_grafico_torta(datos)
    fig1 = generar_grafico_torta(datos_para_grafico_torta)


    # Mostrar el diagrama de frecuencias por recorrido
    datos = agregar_recorrido(datos)
    x,y = obtener_datos_para_barras_de_frecuencias_agrupadas_por_recorrido(datos)
    fig2 = generar_diagrama_de_barras_de_frecuencias_agrupadas_por_recorrido(x,y)

    # Mostrar el diagramas de frecuencias
    datos = agregar_horas(datos)
    datos_para_diagrama_de_frecuencias = obtener_datos_para_diagrama_de_areas_de_frecuencias_por_hora(datos)

    fig3 = generar_diagrama_de_areas_de_frecuencias_por_hora(datos_para_diagrama_de_frecuencias)

    # generar el informe PDF
    nombre_conductor = "martin"
    graficos = [fig1, fig2, fig3]
    archivos_cachados = guardar_en_cache(graficos)
    informe_pdf = generar_informe_pdf(archivos_cachados, nombre_conductor, pdf_filename)
    return informe_pdf
