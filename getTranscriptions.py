import re
import os
import json
from langchain_community.document_loaders import YoutubeLoader

# Función para limpiar nombres de archivos eliminando caracteres no válidos
def clean_filename(title):
    return re.sub(r'[\/:*?"<>|]', "", title).strip()

# Función para obtener la transcripción de YouTube
def get_youtube_transcript(url: str, lan: str):
    try:
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=False,
            language=[lan]
        )
        transcript_data = loader.load()
        
        # Extraer solo el texto de la transcripción
        transcript_text = " ".join(doc.page_content for doc in transcript_data)
        return transcript_text

    except Exception as e:
        return None

# Leer el archivo JSON con los videos
name_channel = "Andy Cruz"
input_file = f"links_{name_channel}.json"  # Nombre del archivo con los títulos y URLs
output_folder = f"Transcriptions {name_channel}"  # Carpeta para guardar las transcripciones

# Crear la carpeta si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar el archivo JSON
with open(input_file, "r", encoding="utf-8") as file:
    video_data = json.load(file)

# Procesar cada video del array
for video in video_data:
    try:
        title = video.get("title", "Sin título")
        url = video.get("url", "")

        if not url:
            print(f"⚠️ No hay URL para el video: {title}")
            continue

        filename = f"{clean_filename(title)}.txt"
        filepath = os.path.join(output_folder, filename)

        print(f"🔍 Procesando: {title}")

        # Obtener la transcripción
        transcript = get_youtube_transcript(url, lan="es")

        if transcript:
            # Guardar la transcripción en un archivo
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"✅ Guardado: {filename}")
        else:
            print(f"⚠️ No se pudo obtener la transcripción de: {title}")

    except Exception as e:
        print(f"❌ Error procesando '{title}': {e}")

print("\n🎉 Transcripciones completadas.")