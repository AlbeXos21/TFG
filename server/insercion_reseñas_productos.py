import requests
import urllib.parse
import pymysql
# Funcion para obtener las reseñas positivas de un producto solicitado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def obtener_reseñas_positivas(producto,cursor,reviews_positivas):
    cursor_encoded = urllib.parse.quote(cursor) if cursor else "*"
    # Obtener la lista de aplicaciones de Steam
    response = requests.get(f"https://store.steampowered.com/appreviews/{producto}?json=1&num_per_page=100&language=english&review_type=positive&cursor={cursor_encoded}")

    if response.status_code == 200:
        reviews = response.json()
        cursor = reviews["cursor"]
        for review in reviews["reviews"]:
            
            if len(str(review["review"]).strip().split(" "))>=10 and len(str(review["review"]).strip().split(" "))<300:
                reviews_positivas.add(review["review"])

        
        return cursor

# Funcion para obtener las reseñas negativas de un producto solicitado
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def obtener_reseñas_negativas(producto,cursor,reviews_negativas):
    cursor_encoded = urllib.parse.quote(cursor) if cursor else "*"
    # Obtener la lista de aplicaciones de Steam
    response = requests.get(f"https://store.steampowered.com/appreviews/{producto}?json=1&num_per_page=100&language=english&review_type=negative&cursor={cursor_encoded}")

    if response.status_code == 200:
        reviews = response.json()
        cursor = reviews["cursor"]
       
        for review in reviews["reviews"]:
            if len(str(review["review"]).strip().split(" ")) and len(str(review["review"]).strip().split(" "))<300:
                reviews_negativas.add(review["review"])

        return cursor


# Funcion para obtener el numero total de reseñas positivas y negativas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def obtener_num_total_reseñas(producto):

    response = requests.get(f"https://store.steampowered.com/appreviews/{producto}?json=1&language=english")
    
    if response.status_code == 200:
        num_reviews=list()
        reviews = response.json()
        num_reviews.append(reviews["query_summary"]["total_positive"])
        num_reviews.append(reviews["query_summary"]["total_negative"])
        return num_reviews

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Funcion Principal : Hilo de Ejecucion
def insercion_reseñas(producto):
    num_reviews_todos=obtener_num_total_reseñas(producto)

    cursor_positivo="*"
    cursor_negativo="*"

    reviews_positivas = set()
    reviews_negativas = set()

    print("RESEÑAS POSITIVAS")

    for i in range(3):
        cursor_positivo = obtener_reseñas_positivas(producto,cursor_positivo,reviews_positivas)

    print("Obtenidas ",len(reviews_positivas)," reseñas positivas")

    print("RESEÑAS NEGATIVAS")
 
    for i in range(3):
        cursor_negativo = obtener_reseñas_negativas(producto,cursor_negativo,reviews_negativas)
   

    print("Obtenidas ",len(reviews_negativas)," reseñas negativas")

    reseñas = reviews_positivas | reviews_negativas


    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="reviews"
    )

    cursor = conexion.cursor()

    for review in reviews_positivas:
        sql = "INSERT INTO reseñas (IDPRODUCTO, RESEÑA, CALIFICACION, TIPO) VALUES (%s, %s ,NULL,%s)"
        valores = (int(producto), review,int(1))
        cursor.execute(sql, valores)

    for review in reviews_negativas:
        sql = "INSERT INTO reseñas (IDPRODUCTO, RESEÑA, CALIFICACION, TIPO) VALUES (%s, %s ,NULL,%s)"
        valores = (int(producto), review,int(2))
        cursor.execute(sql, valores)

    conexion.commit()
    conexion.close() 

    
    print("Todo Finalizado con EXITO!") 


    
      
    