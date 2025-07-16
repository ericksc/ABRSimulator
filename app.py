from flask import Flask, render_template

# Se crea una instancia de la aplicación Flask
app = Flask(__name__)

# Se define la ruta principal de la aplicación web ("/")
@app.route("/")
def index():
    """
    Renderiza la página principal. 
    Returns the 'index.html' template when the root URL is accessed.
    """
    # Cuando un usuario accede a la raíz, se renderiza el archivo 'index.html'
    return render_template("index.html")

# Si el archivo se ejecuta directamente, inicia el servidor en modo debug
if __name__ == "__main__":
    app.run(debug=True)
