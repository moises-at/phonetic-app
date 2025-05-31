# app.py

import os
from flask import Flask, request, jsonify, render_template
from google import generativeai as genai
import traceback # ¡Añadimos esta importación para depuración!

app = Flask(__name__)

# --- Configuración de la API de Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("ADVERTENCIA: La variable de entorno GEMINI_API_KEY no está configurada.")
    print("Obtén una clave API de: https://aistudio.google.com/app/apikey")
    # En un entorno de producción, esto debería ser un error fatal.
    # raise ValueError("GEMINI_API_KEY environment variable is not set.") 

genai.configure(api_key=GEMINI_API_KEY)

# Función para obtener la respuesta de Gemini (adaptada de pronunapp.txt)
def get_gemini_response(prompt_text):
    """
    Envía el texto de entrada al modelo Gemini para obtener la pronunciación fonética.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        # Aquí capturamos errores específicos de la API de Gemini
        print(f"Error al interactuar con Gemini: {e}")
        traceback.print_exc() # Imprime el traceback completo para depuración
        return f"Error al generar la pronunciación desde Gemini: {e}"

# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """Sirve la página HTML principal."""
    return render_template('index.html')

@app.route('/generate_pronunciation', methods=['POST'])
def generate_pronunciation_api():
    """
    Endpoint para generar la pronunciación fonética a partir del texto en inglés.
    """
    try: # <--- INICIO DEL NUEVO BLOQUE TRY
        data = request.json
        english_text = data.get('english_text', '').strip()

        if not english_text:
            return jsonify({"error": "Por favor, introduce algún texto para obtener su pronunciación."}), 400

        # Construye el prompt para la IA (adaptado de pronunapp.txt)
        prompt = f"""
Instrucciones para Transcripción Fonética de Inglés Americano para Hispanohablantes
Rol: Eres un experto en transcripción fonética del inglés americano, especializado en adaptarla para hablantes nativos de español.

Objetivo: Proporcionar la pronunciación más aproximada del inglés americano utilizando sonidos del español.
Es crucial que la transcripción refleje las concatenaciones de palabras (linking) comunes en el inglés hablado para lograr una pronunciación fluida y natural.
Formato de Salida:

CRUCIAL: recuerda solo dar la salida de la peticion, no reescribas el texto proporcionado por el usuario usuario, es garrafal.
Tu NUNCA TRADUCIRAS concentrate en proporciona la transcripción fonética escrita con letras y sonidos del español.
concentrate en proporciona la transcripción fonética escrita con letras y sonidos del español.
No incluyas explicaciones detalladas.
SUPER IMPORTANTE:Evita usar simbolos como ð, simbolos del alfabeto fonetico internacional o AFI O IPA
Si el texto es una letra de canción o poema, mantén cada línea separada para conservar el ritmo y claridad.
Si hay numeros incluidos, comvierte tambien la pronunciacion de los numeros correspondientes de ese idioma original a la fonetica al español.
Ejemplo:

Input del Usuario (Inglés):
The cycle repeated
As explosions broke in the sky
All that I needed
Was the one thing couldn't find

Output Esperado (Pronunciación):
Dá saikól rripírid
As iksplóushons bróuk in dá skái
Ól dárai nírid
Wás di wán zing cúrent fáind

Ahora, por favor, convierte el siguiente texto en inglés:

    Inglés:
    {english_text}

    """
        
        pronunciation_output = get_gemini_response(prompt).strip()
        return jsonify({"pronunciation": pronunciation_output})

    except Exception as e: # <--- CAPTURA CUALQUIER EXCEPCIÓN
        # Imprime el error en la consola del servidor (tu terminal)
        print(f"Error inesperado en generate_pronunciation_api (capturado): {e}")
        traceback.print_exc() # Imprime el traceback completo para depuración
        # Devuelve una respuesta de error al frontend
        return jsonify({"error": f"Error interno del servidor: {e}"}), 500 # <--- SIEMPRE DEVUELVE UNA RESPUESTA

if __name__ == '__main__':
    app.run(debug=True)