# ABRSimulator

## Descripción

Este proyecto convierte un video en múltiples calidades y genera los archivos necesarios para streaming adaptativo MPEG-DASH usando Python y ffmpeg.

## Estructura del proyecto

La estructura de carpetas y archivos es la siguiente:

```
ABRSimulator/
├── app.py                # Aplicación web principal en Flask
├── process_dash.py       # Script para generar segmentos MPEG-DASH usando ffmpeg
├── requirements.txt      # Dependencias de Python
├── README.md             # Documentación del proyecto
├── static/               # Archivos estáticos generados (salida de ffmpeg, manifiestos, etc.)
│   └── output/           # Carpeta donde se guardan los segmentos y el manifiesto DASH
├── templates/            # Plantillas HTML para la aplicación web
│   └── index.html        # Página principal de la aplicación
└── input/                # Carpeta para videos de entrada
    └── sample.mp4        # Video de ejemplo para pruebas
```

- **app.py**: Código de la aplicación web Flask.
- **process_dash.py**: Script que procesa el video y genera los archivos MPEG-DASH.
- **requirements.txt**: Lista de dependencias necesarias para el proyecto.
- **README.md**: Este archivo, con instrucciones y documentación.
- **static/**: Carpeta donde se almacenan los archivos generados y otros recursos estáticos.
- **templates/**: Contiene las plantillas HTML usadas por Flask.
- **input/**: Carpeta donde debes colocar los videos fuente a procesar.

## Tipo de archivo de entrada

El archivo de entrada debe ser un video en formato `.mp4` (u otro formato compatible con ffmpeg) y debe colocarse en la carpeta `input/`.  
Por defecto, el script busca el archivo `input/sample.mp4`, pero puedes cambiar el nombre o la ruta del archivo modificando el parámetro `input_path` en el script `process_dash.py`.

**Recomendaciones:**
- El video debe tener una resolución y calidad suficiente para permitir la generación de las tres variantes (240p, 360p, 720p).
- Si el video debe contiene pista de audio, el script igualmente podría no funcionar correctamente, a no ser que se adjuste los parametros.
- Puedes usar cualquier video compatible con ffmpeg como entrada.

**Ejemplo de estructura esperada:**
```
input/
└── sample.mp4
```

## Contenido de la carpeta `static/output`

Después de ejecutar el script `process_dash.py`, en la carpeta `static/output` encontrarás los siguientes tipos de archivos:

- **manifest.mpd**:  
  Archivo de manifiesto MPEG-DASH. Es un archivo XML que describe la estructura del contenido multimedia, las diferentes calidades disponibles y cómo deben reproducirse los segmentos.

- **segmentos de video (.m4s)**:  
  Archivos binarios que contienen los fragmentos de video y audio en diferentes resoluciones y bitrates. Estos archivos son utilizados por el reproductor para hacer streaming adaptativo.

- **init-stream*.mp4**:  
  Archivos de inicialización para cada pista de video y audio. Contienen la información necesaria para que el reproductor pueda decodificar los segmentos correspondientes.

En resumen, en `static/output` se almacenan todos los archivos necesarios para servir el video en streaming adaptativo MPEG-DASH, incluyendo el manifiesto y los segmentos de cada calidad.


## Instalación

1. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

2. Instala ffmpeg en tu sistema (necesario para el procesamiento de video):
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Explicación del comando ffmpeg

El comando generado en `process_dash.py` realiza lo siguiente:

```bash
ffmpeg -y -i input/sample.mp4 \
-filter_complex "[0:v]split=3[v1][v2][v3];[v1]scale=w=426:h=240[v1out];[v2]scale=w=640:h=360[v2out];[v3]scale=w=1280:h=720[v3out]" \
-map [v1out] -map 0:a? -c:v:0 libx264 -b:v:0 300k -c:a:0 aac -b:a:0 96k \
-map [v2out] -map 0:a? -c:v:1 libx264 -b:v:1 800k -c:a:1 aac -b:a:1 96k \
-map [v3out] -map 0:a? -c:v:2 libx264 -b:v:2 1500k -c:a:2 aac -b:a:2 128k \
-f dash -use_timeline 1 -use_template 1 \
-adaptation_sets "id=0,streams=v id=1,streams=a" static/output/manifest.mpd
```

### ¿Qué hace cada parte?

- `-y`: Sobrescribe archivos de salida sin preguntar.
- `-i input/sample.mp4`: Archivo de entrada.
- `-filter_complex`: Aplica filtros complejos:
  - `[0:v]split=3[v1][v2][v3]`: Divide el video en 3 flujos.
  - `[v1]scale=w=426:h=240[v1out]`: Primer flujo a 426x240.
  - `[v2]scale=w=640:h=360[v2out]`: Segundo flujo a 640x360.
  - `[v3]scale=w=1280:h=720[v3out]`: Tercer flujo a 1280x720.
- `-map [v1out] -map 0:a? ...`: Asocia cada video escalado y el audio original (si existe) a una variante de calidad.
- `-c:v:N libx264`: Codifica video con H.264.
- `-b:v:N ...`: Asigna bitrate a cada variante de video.
- `-c:a:N aac`: Codifica audio en AAC.
- `-b:a:N ...`: Asigna bitrate a cada variante de audio.
- `-f dash`: Formato de salida MPEG-DASH.
- `-use_timeline 1 -use_template 1`: Opciones para el manifiesto DASH.
- `-adaptation_sets ...`: Define los grupos de adaptación (video y audio).
- `static/output/manifest.mpd`: Archivo de manifiesto de salida.

### Resumen

Este comando toma un video, lo convierte a tres resoluciones y bitrates distintos, y genera los archivos necesarios para streaming adaptativo MPEG-DASH


## Ejecución del procesamiento

Para generar los segmentos MPEG-DASH a partir de tu video, ejecuta el siguiente comando en la terminal:

```bash
python process_dash.py
```