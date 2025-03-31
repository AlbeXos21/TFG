import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import save_npz
from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm
import spacy

custom_stopwords = ['game','just','like','fun','play','good','better','ever','best']


nltk.download('stopwords')
stop_words = stopwords.words('english')
stop_words.extend(custom_stopwords)



def analisisTF_IDF(reseñas, idproducto, ngram=1, vectorizer=None, use_svd=True, n_components=50):
    """
    Optimiza el cálculo de TF-IDF para grandes volúmenes de texto y muestra las palabras más relevantes.
    """
    # Asegurar que `reseñas` sea una lista de strings y limpiar datos incorrectos
    if isinstance(reseñas, tuple):
        reseñas = list(reseñas)

    # Limpiar reseñas: asegurarse de que cada elemento sea un string
    reseñas = [str(reseña) if not isinstance(reseña, str) else reseña for reseña in reseñas]

    # Crear el vectorizador si no se ha proporcionado uno preentrenado
    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            stop_words=stop_words,  # Usar el idioma inglés para eliminar stopwords
            ngram_range=(ngram, ngram),  # Unigramas y bigramas
            max_features=1000,  # Limitar vocabulario a 1000 términos más relevantes
            dtype=np.float32  # Usar float32 para optimizar memoria
        )
        tfidf_matrix = vectorizer.fit_transform(reseñas)
    else:
        tfidf_matrix = vectorizer.transform(reseñas)

    # Mostrar las palabras más relevantes en el corpus (esto es un gráfico o lista)
    palabras_clave = crear_grafico_TF_IDF(vectorizer, idproducto, ngram, tfidf_matrix, 10)

    # Aplicar reducción de dimensionalidad con TruncatedSVD (Latent Semantic Analysis - LSA)
    if use_svd:
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)
    else:
        tfidf_matrix_reduced = tfidf_matrix

    # Convertir a DataFrame SOLO si usamos SVD (para mostrar los componentes reducidos)
    if use_svd:
        # Asegurarse de que el número de columnas coincida con los componentes reducidos
        n_components_actual = tfidf_matrix_reduced.shape[1]
        df_tfidf = pd.DataFrame(tfidf_matrix_reduced, columns=[f"Comp_{i}" for i in range(n_components_actual)])
    else:
        df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    return list(palabras_clave)



def crear_grafico_TF_IDF(vectorizer, idproducto,ngram,tfidf_matrix, top_n=20):
    """
    Muestra las palabras con mayor peso TF-IDF en el corpus.
    """
    # Obtener los nombres de las palabras
    feature_names = np.array(vectorizer.get_feature_names_out())

    # Sumar todas las puntuaciones de TF-IDF por palabra
    sum_tf_idf = np.array(tfidf_matrix.sum(axis=0)).flatten() 

    # Ordenar palabras por peso de TF-IDF (de mayor a menor)
    sorted_indices = np.argsort(sum_tf_idf)[::-1]
    top_words = feature_names[sorted_indices][:top_n]
    top_values = sum_tf_idf[sorted_indices][:top_n]

    # Define la ruta de la carpeta
    carpeta = Path("../web/SteamSA-Polarization/public/") / str(idproducto)

    # Crea la carpeta solo si no existe
    carpeta.mkdir(parents=True, exist_ok=True)

       # Graficar los valores
    plt.figure(figsize=(10,5.5))
    plt.barh(top_words[::-1], top_values[::-1], color="skyblue")
    plt.xlabel("Puntuación TF-IDF")
    plt.ylabel("Palabra")
    plt.title(f"Top Palabras con Mayor Peso TF-IDF n-gram {ngram}")
    archivo = carpeta / f"graficoTF_IDF_{ngram}.png"
    plt.savefig(archivo, bbox_inches="tight", dpi=200)
    return top_words


def analisisBM25(reseñas, idproducto, vectorizer=None, use_svd=True, n_components=50):
    """
    Optimiza el cálculo de BM25 para grandes volúmenes de texto y muestra las palabras más relevantes.

    - `reseñas`: Lista de textos a analizar.
    - `idproducto`: ID del producto para etiquetar la salida.
    - `vectorizer`: Vectorizador preentrenado (para evitar recalculado).
    - `use_svd`: Si True, reduce dimensionalidad con SVD (LSA) para optimización.
    - `n_components`: Número de dimensiones a reducir (ajustable según dataset).

    Retorna:
    - `bm25_matrix_reduced`: Matriz BM25 optimizada.
    - `vectorizer`: El vectorizador entrenado.
    """

    # Asegurar que `reseñas` sea una lista de strings y limpiar datos incorrectos
    if isinstance(reseñas, tuple):
        reseñas = list(reseñas)
    
    reseñas = [str(r[0]) if isinstance(r, tuple) else str(r) for r in reseñas if isinstance(r, (str, tuple))]

    # Tokenizar las reseñas, eliminando stopwords
    tokenized_reseñas = []
    for r in reseñas:
        tokens = r.split()
        # Eliminar stopwords
        tokens = [token for token in tokens if token.lower() not in stop_words]
        tokenized_reseñas.append(tokens)

    # Crear el BM25
    bm25 = BM25Okapi(tokenized_reseñas)

    # Calcular las puntuaciones BM25 para cada documento
    bm25_matrix = np.array([bm25.get_scores(doc) for doc in tokenized_reseñas])

    # Mostrar las palabras más relevantes con la función de TF-IDF
    mostrar_palabras_importantes_bm25(bm25, tokenized_reseñas, 10,idproducto)

    # Aplicar reducción de dimensionalidad con TruncatedSVD (Latent Semantic Analysis - LSA)
    if use_svd:
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        bm25_matrix_reduced = svd.fit_transform(bm25_matrix)
    else:
        bm25_matrix_reduced = bm25_matrix

    # Convertir a DataFrame SOLO si usamos SVD (para mostrar los componentes reducidos)
    if use_svd:
        df_bm25 = pd.DataFrame(bm25_matrix_reduced, columns=[f"Comp_{i}" for i in range(n_components)])
    else:
        df_bm25 = pd.DataFrame(bm25_matrix, columns=[f"Doc_{i}" for i in range(len(reseñas))])

    return bm25_matrix_reduced, bm25


def mostrar_palabras_importantes_bm25(bm25, tokenized_reseñas, top_n=20, idproducto=None):
    """
    Muestra y grafica las palabras con mayor puntuación BM25 en el corpus.
    """
    # Obtén todas las palabras de los tokenizados
    all_tokens = [token for doc in tokenized_reseñas for token in doc]

    # Crear un conjunto único de palabras
    unique_tokens = set(all_tokens)

    # Calcular la frecuencia de cada palabra en el corpus
    word_frequencies = {token: all_tokens.count(token) for token in unique_tokens}

    # Ordenar palabras por frecuencia
    sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Extraer listas de palabras y frecuencias
    words, frequencies = zip(*sorted_words)

    # Graficar las palabras más importantes
    plt.figure(figsize=(10,5.5))
    plt.barh(words[::-1], frequencies[::-1], color='skyblue')  # Invertir para mostrar en orden descendente
    plt.xlabel("Frecuencia")
    plt.ylabel("Palabras")
    plt.title(f"Top {top_n} Palabras más relevantes según BM25")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    # Guardar la imagen
    carpeta = Path("../web/SteamSA-Polarization/public") / str(idproducto)
    carpeta.mkdir(parents=True, exist_ok=True)  # Asegurar que la carpeta existe

    ruta_imagen = carpeta / "graficoBM25.png"
    plt.savefig(ruta_imagen, bbox_inches="tight", dpi=200)



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


# Cargar spaCy para POS tagging
nlp = spacy.load("en_core_web_lg")

# Cargar Sentence Transformers en GPU
model = SentenceTransformer('BAAI/bge-small-en-v1.5', device='cuda')

def detectar_criterios(reseñas, genero, ratio,umbral=0.67):
    criterios_genero = criterios[genero]
    criterios_textos = list(criterios_genero.values())
    criterios_keys = list(criterios_genero.keys())
    diccionario_notas = {key: {"notas": 0 , "apariciones": 0} for key in criterios_keys}
    # Paso 1: Embeddings de criterios una sola vez (cacheable)
    embeddings_criterios = model.encode(criterios_textos, device='cuda')

    resultados_batch = []

    for reseña in reseñas:
        resultado = {criterio: {"match": False, "palabra": None, "score": 0} for criterio in criterios_genero}

        # Extraer palabras clave de la reseña
        doc = nlp(reseña[0])
        palabras = [token.text for token in doc if not token.is_stop and token.has_vector and token.pos_ in ["NOUN", "VERB", "ADJ"]]
        if not palabras:
            continue

        # Paso 2: Embeddings en batch de las palabras de la reseña
        embeddings_palabras = model.encode(palabras, device='cuda')

        # Paso 3: Comparar cada palabra con cada criterio
        for idx_palabra, palabra in enumerate(palabras):
            vec_palabra = embeddings_palabras[idx_palabra]
            for idx_criterio, criterio in enumerate(criterios_keys):
                vec_criterio = embeddings_criterios[idx_criterio]
                sim = dot(vec_palabra, vec_criterio) / (norm(vec_palabra) * norm(vec_criterio))
                if sim >= umbral and sim > resultado[criterio]["score"]:
                    resultado[criterio] = {"match": True, "palabra": palabra, "score": sim}
                    porcentaje = 1

                    if ratio >= 0.6:
                        match ratio:
                            case r  if r < 0.75:
                                porcentaje = 1.5
                            case r  if 0.75 <= r < 0.85 :
                                porcentaje = 1.75
                            case r  if r > 0.85 :
                                porcentaje = 2 
                         
                        nota = reseña[1] * porcentaje
                        if nota > 10:
                               nota = 10 
                        diccionario_notas[criterio]["notas"] += nota

                    else:

                        diccionario_notas[criterio]["notas"] += reseña[1]  

                    diccionario_notas[criterio]["apariciones"] += 1

                    resultados_batch.append(resultado)  
    return diccionario_notas
    

def graficar_medias(idproducto, datos):
    # Calcular medias
    medias = {}
    for grupo in datos:
        for criterio, valores in grupo.items():
            media = valores["notas"] / valores["apariciones"] if valores["apariciones"] > 0 else 0
            medias[criterio] = round(media, 2)

    criterios = list(medias.keys())
    valores = list(medias.values())

    carpeta = Path("../web/SteamSA-Polarization/public/") / str(idproducto)

    # Crear figura y eje
    fig, ax = plt.subplots()
    barras = ax.bar(criterios, valores)

    # Mostrar la media encima de cada barra
    for barra, valor in zip(barras, valores):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, altura + 0.1, f"{valor:.2f}", 
                ha='center', va='bottom', fontsize=9)

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Media (notas / apariciones)")
    plt.title("Media por criterio")
    plt.tight_layout()

    # Guardar como SVG
    plt.savefig(carpeta / "grafico_criterios.svg", format="svg")
    plt.close()

    print(f"Gráfico guardado en: {carpeta}/grafico_criterios.svg")

