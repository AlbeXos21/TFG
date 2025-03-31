import requests
import csv
import re

# Obtener la lista de aplicaciones de Steam
response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")

if response.status_code == 200:
    articulos_steam = response.json()
    valores_unicos = set()  # Usamos un set para evitar duplicados
    
    # Lista de palabras clave a filtrar con mejor delimitación
    palabras_clave = r"\b(|Pack|Edition|Demo|Expansion|DLC|Music|Soundtrack|Skin|Sound Track|Wallpapers|Trailer|Costume|Deluxe|Set|Bundle|Outfit|Character|Playtest|Test|Tool|Bonus|Pass|OST|Server|Pre[- ]?Order|Beta|Content)\b"

    for articulo in articulos_steam["applist"]["apps"]:
        nombre = articulo["name"].strip()

        # 1️ Filtrar nombres vacíos y nombres con palabras clave exactas
        if nombre and not re.search(palabras_clave, nombre, re.IGNORECASE):

            # 2️ Filtrar nombres que comiencen con minúscula
            if not re.match(r"^[a-z]", nombre):

                # 3️ Filtrar nombres en japonés/chino/coreano
                if not re.search(r"[\u3040-\u30FF\u4E00-\u9FFF]", nombre):

                    # 4️ Filtrar nombres que contienen guion " - "
                    if " - " not in nombre:

                        # Agregar al set como una tupla (appid, nombre)
                        valores_unicos.add((articulo["appid"], nombre.replace("\n", "")))

    # Escribir los valores únicos en el archivo CSV
    with open("datos_todos_articulos_steam.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["IDAPP", "NOMBRE"])
        writer.writerows(valores_unicos)

    print(f"Total de nombres únicos filtrados: {len(valores_unicos)}")

else:
    print(" Error:", response.status_code)
