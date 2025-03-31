from flask import Flask, request,jsonify
import pymysql
from insercion_reseñas_productos import insercion_reseñas
from analisis_estadistico import analisis
from flask_cors import CORS
from ejecucion_modelo_paralelizado_real import requestToLLM
from ejecucion_modelo_para_resumen import requestToSummary
import requests
from datetime import datetime
from pathlib import Path
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# 🔹 Conectar a MySQL sin DictCursor
def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="reviews",
    )

# 🔹 Ruta principal
@app.route('/')
def home():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT IDAPP,NOMBRE,MEDIA FROM productos WHERE ESTADO = 1 ORDER BY FECHA DESC LIMIT 4")
    juegos = cursor.fetchall()
    juegos_final = list()
    for j in juegos:
        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 1",j[0])
        tipo1 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 2",j[0])
        tipo2 = cursor.fetchone()[0]

        nuevo_j = list(j) + [tipo1, tipo2]
        juegos_final.append(nuevo_j)

    juegos_vendidos = [{"IDAPP": j[0], "NOMBRE": j[1],"MEDIA": j[2],"RPOS":j[3],"RNEG":j[4]} for j in juegos_final]
    juegos_lista = {"juegos": juegos_vendidos}
    return jsonify(juegos_lista)  # Devolver datos en JSON


instruction = """You are an AI assistant who classifies video game reviews with scores from 1-10, with 1 being a horrible review and 10 being a wonderful review. only 1-10"""

criterios = {

    "Adventure": {
        "Story/Plot": "quality and depth of the main storyline, narrative coherence, and plot twists",
        "World Design": "creativity and richness of maps, environments, and level structure",
        "Characters": "complexity and development of main and secondary characters, including their motivations and arcs"
    },
    "Action": {
        "Gameplay": "responsiveness and fluidity of controls, as well as the design of core gameplay mechanics",
        "Enemies and Bosses": "variety, challenge, and creativity in enemies and boss fights",
        "Art Design/Graphics": "visual fidelity, artistic style, and overall graphical impact of the game"
    },
    "RPG": {
        "Customization": "depth of character customization, including skills, appearance, and equipment options",
        "Story and Characters": "engagement and complexity of the narrative, alongside character writing and progression",
        "Combat System and Quests": "variety and balance of combat mechanics and quest design"
    },
    "Strategy": {
        "Resource Management": "complexity and efficiency in managing game resources and economy",
        "Level Design": "strategic depth and creativity in map layouts and level architecture",
        "Tactics and Balance": "importance of tactical decisions, class balance, and overall gameplay fairness"
    },
    "Simulation": {
        "Realistic Scenarios": "authenticity and attention to detail in recreating real-world environments and situations",
        "Decision Making": "weight and consequences of player choices within the game systems",
        "Interactivity and Development": "player agency and freedom, as well as progression and development throughout the simulation"
    },
    "Sports": {
        "Realism": "authentic representation of physics, gameplay dynamics, and sports culture",
        "Gameplay": "responsiveness and accuracy of controls, as well as smooth gameplay mechanics",
        "Game Modes": "diversity and quality of available modes, including single-player and multiplayer options"
    }
}

@app.route('/producto/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # 🔹 Consulta SQL con la ID
    cursor.execute("SELECT * FROM productos WHERE IDAPP = %s", (id_producto,))
    producto = cursor.fetchone()
    palabras_clave=[]
    if producto[2] == 0:

        insercion_reseñas(id_producto)

        conexion.close()
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT IDRESEÑA,RESEÑA FROM reseñas WHERE IDPRODUCTO = %s",(id_producto))
        reseñas = cursor.fetchall()
    
        requestToLLM(instruction,reseñas,16)

        #   Codigo para cambiar el ESTADO del Videojuego a que ya ha sido tratado
        cursor.execute(f"UPDATE productos SET ESTADO = 1 WHERE IDAPP = {id_producto}")
        conexion.commit()

        #  Codigo para enviar estado actual del Videojuego
        cursor.execute("SELECT * FROM productos WHERE IDAPP = %s", (id_producto,))
        producto = cursor.fetchone()

        palabras_clave= analisis.analisisTF_IDF(reseñas,id_producto)
        palabras_clave_2=analisis.analisisTF_IDF(reseñas,id_producto,2)
        palabras_clave.extend(palabras_clave_2)
        
        cursor.execute("SELECT RESEÑA,CALIFICACION, TIPO FROM reseñas WHERE IDPRODUCTO = %s",(id_producto))
        reseñas = cursor.fetchall()

        analisis.analisisBM25(reseñas,id_producto)
    

        info = obtener_informacion_producto(id_producto)
        generos = info[0]
        descargar_video(info[3],f"trailer_{id_producto}",id_producto)
        cursor.execute("SELECT RESEÑA,CALIFICACION FROM reseñas WHERE IDPRODUCTO = %s",(id_producto))
        reseñas = list(cursor.fetchall())
        ratio_notas = obtener_ratio_notas(id_producto)
        reseñas_lista = list()
        generos_filtrados = [g for g in list(criterios.keys()) if g in generos]

        generos_subida = list("000000")

        for g in generos_filtrados:

            if g == "Adventure":
                generos_subida[0] = "1"
            if g == "Action":
                generos_subida[1] = "1"
            if g == "RPG":
                generos_subida[2] = "1"
            if g == "Strategy":
                generos_subida[3] = "1"
            if g == "Simulation":
                generos_subida[4] = "1"
            if g == "Sports":
                generos_subida[5] = "1"
        generos_subida = ''.join(generos_subida)


        info = obtener_informacion_producto(id_producto)
        generos = info[0]
        descargar_video(info[3],f"trailer_{id_producto}",id_producto)
        cursor.execute("SELECT RESEÑA,CALIFICACION FROM reseñas WHERE IDPRODUCTO = %s",(id_producto))
        reseñas = list(cursor.fetchall())
        ratio_notas = obtener_ratio_notas(id_producto)
        reseñas_lista = list()
        generos_filtrados = [g for g in list(criterios.keys()) if g in generos]

        generos_subida = list("000000")

        for g in generos_filtrados:

            if g == "Adventure":
                generos_subida[0] = "1"
            if g == "Action":
                generos_subida[1] = "1"
            if g == "RPG":
                generos_subida[2] = "1"
            if g == "Strategy":
                generos_subida[3] = "1"
            if g == "Simulation":
                generos_subida[4] = "1"
            if g == "Sports":
                generos_subida[5] = "1"
        generos_subida = ''.join(generos_subida)


        for reseña in reseñas:
            reseñas_lista.append([f"{info[1]} {reseña[0]}",reseña[1]])
        criterios_especificos = list()
        for g in generos_filtrados:
            criterios_especificos.append(analisis.detectar_criterios(reseñas_lista,g,ratio_notas))
        media = 0
        num_elementos=len(criterios_especificos*3)

        for criterio_genero in criterios_especificos:
            for criterio in criterio_genero.values():
                media= media + criterio["notas"]/criterio["apariciones"]
               
        media = media / num_elementos
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        resumen = requestToSummary(palabras_clave,info[1],info[2])

        cursor.execute("UPDATE productos SET FECHA = %s, MEDIA = %s, RESUMEN = %s, GENEROS = %s WHERE IDAPP = %s",(fecha_formateada,round(media,1),resumen,generos_subida,id_producto))
        conexion.commit()
# 🔹 Aumentamos el límite para evitar cortes prematuros
        analisis.graficar_medias(id_producto,criterios_especificos)

        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 1",(id_producto))
        reseñas_positivas = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 2",(id_producto))
        reseñas_negativas = cursor.fetchone()     
        conexion.close()  # Cerrar conexión

        return jsonify({"ESTADO": producto[2],"RPOS":reseñas_positivas[0],"RNEG":reseñas_negativas[0],"MEDIA":round(media,1),"RESUMEN":resumen,"GENEROS":generos_subida})  # Código 404 si no existe
    else:
        

        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 1",(id_producto))
        reseñas_positivas = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM reseñas WHERE IDPRODUCTO = %s AND TIPO = 2",(id_producto))
        reseñas_negativas = cursor.fetchone()     
        cursor.execute("SELECT MEDIA,RESUMEN,GENEROS FROM productos WHERE IDAPP = %s",(id_producto))
        media = cursor.fetchone() 
        info = obtener_informacion_producto(id_producto)
        cursor.execute("SELECT IDRESEÑA,RESEÑA FROM reseñas WHERE IDPRODUCTO = %s",(id_producto))
        reseñas = cursor.fetchall()

        conexion.close()  # Cerrar conexión
        

        return jsonify({"ESTADO": producto[2],"RPOS":reseñas_positivas[0],"RNEG":reseñas_negativas[0],"MEDIA":media[0],"RESUMEN":media[1],"GENEROS":media[2]})  # Código 404 si no existe


@app.route('/busqueda', methods=['POST'])
def guardar_dato():
    try:
        # Obtener el JSON enviado desde React
        data = request.get_json()
        valor_recibido = data.get('valor', '')  # Obtener el valor del JSON
        
        conexion = conectar_db()
        cursor = conexion.cursor()

        # 🔹 Consulta SQL para verificar que tengo calificacion en una reseña de esa ID
        cursor.execute("SELECT IDAPP,NOMBRE,MEDIA FROM productos WHERE NOMBRE LIKE %s ORDER BY IDAPP DESC LIMIT 5", ("%"+valor_recibido+"%",))
        productos = cursor.fetchall()

        juegos_obtenidos = [{"IDAPP": p[0], "NOMBRE": p[1], "NOTA": p[2]} for p in productos]

        # Responder con un mensaje de éxito
        return jsonify({"juegos": juegos_obtenidos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --------------------------------------------------------------------------------------------------------------------------------


def obtener_informacion_producto(idproducto):

    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={idproducto}&l=english")
    lista_generos = list()

    if response.status_code == 200:
        articulo_steam = response.json()
        if(articulo_steam[f"{idproducto}"]["success"] and articulo_steam[f"{idproducto}"]["data"]["type"] == "game" ):
            for articulo in articulo_steam[f"{idproducto}"]["data"]["genres"]:
                lista_generos.append(articulo["description"]) 
        return lista_generos,articulo_steam[f"{idproducto}"]["data"]["short_description"] ,articulo_steam[f"{idproducto}"]["data"]["name"],articulo_steam[f"{idproducto}"]["data"]["movies"][0]["webm"]["max"]
    
    else:
     print(" Error:", response.status_code)



def obtener_ratio_notas(idproducto):

    response = requests.get(f"https://store.steampowered.com/appreviews/{idproducto}?json=1")

    if response.status_code == 200:
        articulo_steam = response.json()
        return articulo_steam["query_summary"]["total_positive"]/articulo_steam["query_summary"]["total_reviews"]

    else:
     print(" Error:", response.status_code)

def descargar_video(url, nombre_archivo, idproducto):
    # Crear la carpeta si no existe
    carpeta = Path(f"../web/SteamSA-Polarization/public/{idproducto}")
    carpeta.mkdir(parents=True, exist_ok=True)

    # Descargar el video
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Definir el nombre del archivo y guardarlo
        nombre_archivo = carpeta / "trailer.webm"  # Guardar el archivo en la carpeta

        # Abrir el archivo en modo binario y escribir los datos
        with open(nombre_archivo, 'wb') as f:
            f.write(response.content)
        
        print(f"Descarga completada: {nombre_archivo}")
    else:
        print("Error al descargar el archivo. Código de respuesta:", response.status_code)



# 🔹 Ejecutar Flask correctamente
if __name__ == '__main__':
    app.run(debug=False)



