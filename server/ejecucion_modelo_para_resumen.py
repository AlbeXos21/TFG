import time
import torch
from transformers import pipeline
from insercion_reseñas_productos import insercion_reseñas
import pymysql
# 🔹 Optimización para procesar varias reseñas a la vez
torch.backends.cuda.matmul.allow_tf32 = True
torch.cuda.empty_cache()


model_id = "unsloth/llama-3.2-3b-instruct-unsloth-bnb-4bit"  # Modelo BART entrenado en resúmenes

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)


def requestToSummary(words, context, title):
    instruction = ("You will be given a set of 20 keywords related to a video game. "
                   "The order of the words is important: the ones that appear first are the most relevant. "
                   "Using only those words, create a clear and coherent summary of the game, respecting the order of importance. "
                   "The summary should be detailed enough to convey the main aspects of the game, such as its plot, mechanics, and gameplay, "
                   "but it should be concise and precise. The summary must not exceed 100 words.")

    prompt = f"{instruction}\n\nTitle: {title}\n\nKeywords: {words}\n\nContext: {context}\n\nAnswer:"

    torch.cuda.empty_cache()  # 🔹 Limpia memoria antes de inferencia

    # 🔹 Genera predicciones en paralelo
    outputs = pipe(
        prompt,
        max_new_tokens=150,  
        temperature=0.75,  
        batch_size=1,  
    )

    # 🔍 Verificamos la salida
    generated_text = outputs[0]["generated_text"].split("Answer:")[1]

    return generated_text
    
    
