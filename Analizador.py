import os
from pydub import AudioSegment
import eyed3

def analyze_audio_file(file_path):
    try:
        # Cargar el archivo de audio
        audio = AudioSegment.from_file(file_path)
        audio_info = eyed3.load(file_path)

        # Obtener metadatos de la canción
        bitrate = audio.frame_rate * audio.frame_width * 8
        duration = audio.duration_seconds
        channels = audio.channels
        sample_width = audio.sample_width
        sample_rate = audio.frame_rate

        # Obtener BPM si está disponible
        bpm = None
        if audio_info.tag is not None and audio_info.tag.bpm:
            bpm = audio_info.tag.bpm

        # Crear la carpeta "Analizados" si no existe
        analyzed_dir = os.path.join(os.path.dirname(file_path), "Analizados")
        os.makedirs(analyzed_dir, exist_ok=True)

        # Guardar los datos en un archivo de texto
        output_file_name = os.path.splitext(os.path.basename(file_path))[0] + "_Analizado.txt"
        output_file = os.path.join(analyzed_dir, output_file_name)
        with open(output_file, "w") as f:
            f.write(f"File: {os.path.basename(file_path)}\n")
            f.write(f"Bitrate: {bitrate} bps\n")
            f.write(f"Duration: {duration:.2f} seconds\n")
            f.write(f"Channels: {channels}\n")
            f.write(f"Sample Width: {sample_width} bytes\n")
            f.write(f"Sample Rate: {sample_rate} Hz\n")
            if bpm:
                f.write(f"BPM: {bpm}\n")
            else:
                f.write("BPM: Not available\n")

        print(f"Analysis saved to {output_file}")

    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")

def select_audio_file(directory_path):
    # Listar archivos de audio en la carpeta
    audio_files = [f for f in os.listdir(directory_path) if f.endswith((".mp3", ".wav", ".flac"))]

    if not audio_files:
        print("No hay archivos de audio en la carpeta.")
        return None

    # Mostrar lista de archivos
    print("Archivos de audio disponibles:")
    for idx, filename in enumerate(audio_files, 1):
        print(f"{idx}. {filename}")

    # Seleccionar archivo
    file_index = int(input("Selecciona el número del archivo que quieres analizar: ")) - 1
    if 0 <= file_index < len(audio_files):
        return os.path.join(directory_path, audio_files[file_index])
    else:
        print("Selección no válida.")
        return None

if __name__ == "__main__":
    directory = "Media"
    selected_file = select_audio_file(directory)
    if selected_file:
        analyze_audio_file(selected_file)
