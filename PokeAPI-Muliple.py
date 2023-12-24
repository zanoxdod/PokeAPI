# Info API: https://pokeapi.co/docs/v2

import requests
import json
import openpyxl
import pandas as pd
from datetime import datetime

def consultar_pokemones(numeros_pokemon, formato='json'):
    resultados = []

    for numero in numeros_pokemon:
        datos_pokemon = consultar_pokemon(numero)
        resultados.append(datos_pokemon)

    # Calcular la altura promedio y agregar al final de los resultados
    altura_promedio = calcular_altura_promedio(resultados)
    resultados.append({'Altura Promedio del listado': altura_promedio})

    # Imprimir por consola
    imprimir_por_consola(resultados)

    # Nomenclatura archivo de salida
    fecha_hora_actual = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    nombre_archivo = f"{fecha_hora_actual}_pokemons_list"

    if formato == 'json':
        guardar_json(resultados, nombre_archivo)
    elif formato == 'excel':
        guardar_excel(resultados, nombre_archivo)
    else:
        print(f"Formato '{formato}' no válido. Use 'json' o 'excel.'")

def consultar_pokemon(numero):
    url = f'https://pokeapi.co/api/v2/pokemon/{numero}/'
    datos_pokemon = {}

    try:
        # Realizar la solicitud GET a la API
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # Convertir la respuesta a formato JSON
            data = response.json()

            # Almacenar información del Pokémon
            datos_pokemon['Nombre'] = data['name']
            datos_pokemon['ID'] = data['id']
            datos_pokemon['Habilidades'] = [habilidad['ability']['name'] for habilidad in data['abilities']]
            datos_pokemon['Altura'] = data['height']
            datos_pokemon['Tipos'] = [tipo['type']['name'] for tipo in data['types']]
        else:
            print(f"Error: No se pudo obtener información del Pokémon {numero}. Código de respuesta: {response.status_code}")

    except Exception as e:
        print(f"Error al realizar la solicitud para el Pokémon {numero}: {e}")

    return datos_pokemon

def calcular_altura_promedio(resultados):
    alturas = [pokemon.get('Altura', 0) for pokemon in resultados]
    altura_promedio = sum(alturas) / len(alturas) if len(alturas) > 0 else 0
    return round(altura_promedio, 2)  # Redondear a 2 decimales

def imprimir_por_consola(resultados):
    for i, resultado in enumerate(resultados, start=1):
        print(f"\nResultado para Pokémon {i}:")
        for clave, valor in resultado.items():
            if isinstance(valor, list):
                print(f"{clave}: {', '.join(valor)}")
            else:
                print(f"{clave}: {valor}")
        print("")

def guardar_json(resultados, nombre_archivo):
    with open(f'{nombre_archivo}.json', 'w') as file:
        json.dump(resultados, file, indent=2)
    print(f"\nDatos guardados en '{nombre_archivo}.json'")

def guardar_excel(resultados, nombre_archivo):
    df = pd.DataFrame(resultados)
    df.to_excel(f'{nombre_archivo}.xlsx', index=False)
    print(f"\nDatos guardados en '{nombre_archivo}.xlsx'")

# Indicar ID o Nombre del/los Pokémon deseados:
numeros_pokemon = [10, 890]

# Consultar información de varios Pokémon y guardar en JSON
#consultar_pokemones(numeros_pokemon, formato='json')

# Consultar información de varios Pokémon y guardar en Excel
consultar_pokemones(numeros_pokemon, formato='excel')