import json
import subprocess

# URL del canal de YouTube
name_channel = "Andy Cruz"
channel_url = "https://www.youtube.com/@AndyCruz7/videos"

# Ejecutar yt-dlp para obtener metadata completa
result = subprocess.run(
    ["yt-dlp", "-J", channel_url],
    capture_output=True,
    text=True
)

# Convertir la salida en JSON
data = json.loads(result.stdout)

# Crear un array con títulos y enlaces
video_info = [
    {
        "title": entry.get("title", "Sin título"),
        "url": entry.get("webpage_url", "")
    }
    for entry in data.get("entries", [])
]

# Guardar como archivo .json
with open(f"links_{name_channel}.json", "w", encoding="utf-8") as f:
    json.dump(video_info, f, ensure_ascii=False, indent=2)

print("Archivo JSON creado con éxito.")
