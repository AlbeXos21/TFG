import pymysql
import pandas as pd

# Conectar con la base de datos creada en `estructura.sql`
conexion = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="reviews"
)

cursor = conexion.cursor()

# Leer el CSV
df = pd.read_csv("../api_steam/datos_todos_articulos_steam.csv")

print(df)
# Insertar datos en la tabla productos
for _, fila in df.iterrows():
    sql = "INSERT INTO productos (IDAPP, NOMBRE) VALUES (%s, %s) ON DUPLICATE KEY UPDATE NOMBRE = VALUES(NOMBRE)"
    valores = (fila["IDAPP"], fila["NOMBRE"])
    cursor.execute(sql, valores)

# Confirmar cambios y cerrar conexión
conexion.commit()
conexion.close()

print(" Datos cargados correctamente desde CSV a MySQL.")