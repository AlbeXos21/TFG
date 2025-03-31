import time
import torch
from transformers import pipeline
from insercion_reseñas_productos import insercion_reseñas
import pymysql
import re
# 🔹 Optimización para procesar varias reseñas a la vez
torch.backends.cuda.matmul.allow_tf32 = True
torch.cuda.empty_cache()


model_id = "../IA/Llama-3.2-3B-ReviewsFineTuning"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)


def requestToLLM(instruction, requests, batch_size):
    
    if not requests:
        raise ValueError("La lista de reseñas está vacía.")

    prompts = [f"{instruction}\n\nReview: {review[1]}\n\nRating:" for review in requests]

    if not prompts:
        raise ValueError("Los prompts generados están vacíos.")

    torch.cuda.empty_cache()  # 🔹 Limpia memoria antes de inferencia

    while batch_size >= 4:
        try:
            print(f"🔹 Probando batch_size={batch_size}...")

            t = time.time()

            # 🔹 Genera predicciones en paralelo
            outputs = pipe(
                prompts,
                max_new_tokens=2,  # 🔹 Solo devuelve el rating
                temperature=0.7,
                batch_size=batch_size,  # 🚀 Aumentamos batch_size para mejor rendimiento
                truncation=True
            )

            t = time.time() - t
            print(f"✅ Procesado en {t:.3f} segundos con batch_size={batch_size}")

            # 🔹 Extraer respuestas
            ratings = []

            for i, output in enumerate(outputs):
                generated_text = output[0]["generated_text"]
                
                if "Rating:" in generated_text:
                    rating_part = generated_text.split("Rating:")[-1].strip()
                    if rating_part:
                        rating = rating_part.split()[0]
                    else:
                        rating = 5
                else:
                    rating = 5

                ratings.append((requests[i][0], requests[i][1], rating))


            # 🔹 Mostrar resultados
            conexion = conectar_db()
            cursor = conexion.cursor()
            for request in ratings:
                resultado = re.sub(r'[^0-9]', '', str(request[2]))
                if resultado == '':
                    resultado=5
                cursor.execute("UPDATE reseñas SET CALIFICACION = %s WHERE IDRESEÑA = %s", (resultado, request[0]))
                conexion.commit()
            conexion.close()
            break
        except torch.cuda.OutOfMemoryError:
            print(f"🚨 batch_size={batch_size} agotó la VRAM. Probando con batch_size={batch_size // 2}")
            torch.cuda.empty_cache()
            batch_size //= 2  # 🔹 Reducir el batch y probar de nuevo


# 🔹 Conectar a MySQL sin DictCursor
def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="reviews",
    )