# Ejecutar este script para generar segmentos MPEG-DASH a partir de un video.
# Asegúrate de tener FFmpeg instalado y configurado en tu sistema.
import os
import subprocess


def generate_mpeg_dash(
    input_path: str = "input/sample.mp4",
    output_dir: str = "static/output"
) -> None:
    """Generate MPEG-DASH segments from a video file.
    Args:
        input_path (str): Path to the input video file.
        output_dir (str): Directory where the output DASH files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-filter_complex",
        "[0:v]split=3[v1][v2][v3];" +
        "[v1]scale=w=426:h=240[v1out];" +
        "[v2]scale=w=640:h=360[v2out];" +
        "[v3]scale=w=1280:h=720[v3out]",
        "-map", "[v1out]", "-map", "0:a", "-c:v:0", "libx264", "-b:v:0", "300k",
        "-c:a:0", "aac", "-b:a:0", "96k",
        "-map", "[v2out]", "-map", "0:a", "-c:v:1", "libx264", "-b:v:1", "800k",
        "-c:a:1", "aac", "-b:a:1", "96k",
        "-map", "[v3out]", "-map", "0:a", "-c:v:2", "libx264", "-b:v:2", "1500k",
        "-c:a:2", "aac", "-b:a:2", "128k",
        "-f", "dash",
        "-use_timeline", "1", "-use_template", "1",
        "-adaptation_sets", "id=0,streams=v id=1,streams=a",
        os.path.join(output_dir, "manifest.mpd")
    ]

    subprocess.run(command, check=True)

if __name__ == "__main__":
    generate_mpeg_dash()
