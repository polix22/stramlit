import streamlit as st
import textwrap
import google.generativeai as genai
import requests

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

GOOGLE_API_KEY = 'AIzaSyAZ0b5gnlfHF0xMJFbGA3gQp6AX7mc5EMk'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.0-pro')

def consulta(context, prompt):
    response = model.generate_content(context + prompt)
    archivo = response.text
    with open("archivo.txt", "w") as f:
        f.write(archivo)
    return response.text

# Título de la aplicación
st.title("Pokedex online")

# Texto de introducción
st.write("Bienvenido a tu pokedex online. Aquí vas a recibir información sobre tus pokemon favoritos, te daremos información sobre los pokemons, como por ejemplo número de pokedex, línea evolutiva, tipo de pokemon, imagen del pokemon y contra qué tipos de pokemon es fuerte y débil.")

# Entrada del prompt del usuario
prompt = st.text_area("Ingresa el número de pokedex o nombre de pokemon: ")

context = "Eres una pokedex actualizada, tienes información de todos los pokemons existentes, con el número de pokedex o el nombre del pokemon devolverás la siguiente información: número de pokedex, nombre, línea evolutiva, tipo o tipos, debilidad de tipo y fuerte contra qué tipo: "

# Botón para mostrar el nombre
if st.button("Buscar"):
    if prompt:
        # Llamar a la API y obtener la respuesta
        response = consulta(context, prompt)
        
        # Obtener el número del Pokémon a partir del prompt
        pokemon_number = None
        
        # Verificar si el prompt es un número
        if prompt.isdigit():
            pokemon_number = int(prompt)
        else:
            # Convertir el nombre a minúsculas y reemplazar espacios por guiones
            pokemon_name = prompt.lower().replace(" ", "-")
            # Hacer una solicitud a la PokeAPI para obtener el ID del Pokémon
            try:
                pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}").json()
                pokemon_number = pokemon_data["id"]
            except Exception as e:
                st.write("No se encontró el Pokémon. Asegúrate de que el nombre sea correcto.")
                st.stop()

        # Mostrar la imagen del Pokémon en la primera columna
        col1, col2 = st.columns(2)
        if pokemon_number:
            col1.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_number}.png", width=200)
        
        # Mostrar la información del Pokémon en la segunda columna
        col2.header("Información del Pokémon")
        col2.write(response)
       
    else:
        st.write("Ingresa el número o nombre del pokemon que deseas buscar.")
