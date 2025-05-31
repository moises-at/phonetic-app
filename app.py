import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Configuración de la API de Gemini (asegúrate de que GEMINI_API_KEY esté configurada en tus variables de entorno)
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"ADVERTENCIA: La variable de entorno GEMINI_API_KEY no está configurada.")
    print(f"Obtén una clave API de: https://aistudio.google.com/app/apikey")
    # Aquí podrías manejar el error de una forma más robusta si quieres, por ejemplo, salir de la app
    # o usar un placeholder si no hay clave. Por ahora, solo imprime la advertencia.

app = Flask(__name__)

# --- NUEVO: Cargar el prompt desde el archivo ---
# Es buena idea cargar esto una sola vez al inicio de la app
try:
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        BASE_PROMPT = f.read()
except FileNotFoundError:
    BASE_PROMPT = "Error: prompt.txt no encontrado. Por favor, crea el archivo."
    print(BASE_PROMPT)
# ------------------------------------------------

# Ruta principal para servir el HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pronunciation', methods=['POST'])
def generate_pronunciation_api():
    """
    Endpoint para generar la pronunciación fonética a partir del texto en inglés.
    """
    try:
        data = request.json
        english_text = data.get('english_text', '').strip()

        if not english_text:
            return jsonify({"error": "Por favor, introduce algún texto para obtener su pronunciación."}), 400

        # --- MODIFICADO: Usa la plantilla cargada y añade el texto ---
        full_prompt = f"{BASE_PROMPT}{english_text}\n"
        # -----------------------------------------------------------

        pronunciation_output = get_gemini_response(full_prompt).strip() # Pasa full_prompt
        return jsonify({"pronunciation": pronunciation_output})

    except Exception as e:
        print(f"Error al generar la pronunciación desde Gemini: {e}")
        return jsonify({"error": f"Error al generar la pronunciación desde Gemini: {e}"}), 500

def get_gemini_response(prompt_text): # Asegúrate de que esta función existe y reciba el prompt
    try:
        response = model.generate_content(prompt_text) # Utiliza el prompt_text que se le pasa
        # Asegúrate de manejar la respuesta si tiene varios candidatos o bloqueos
        if response.candidates:
            return response.text
        else:
            return "No se pudo generar una respuesta. Intenta con otro texto."
    except Exception as e:
        print(f"Error al interactuar con Gemini: {e}")
        raise # Relanza la excepción para que sea capturada por el bloque try/except superior