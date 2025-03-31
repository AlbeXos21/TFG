# Sistema de Análisis de Sentimientos y Polarización en Reseñas de Videojuegos

Este proyecto es una aplicación para el análisis automático de sentimientos y polarización de reseñas de videojuegos. El sistema procesa grandes volúmenes de reseñas obtenidas de la API de Steam y proporciona información valiosa sobre la percepción de los usuarios respecto a los videojuegos, ayudando a los desarrolladores a tomar decisiones informadas.

## Descripción

El sistema permite:

- Cargar y procesar reseñas de videojuegos desde la API de Steam.
- Analizar el sentimiento de las reseñas (positivo, negativo o neutral).
- Detectar patrones de polarización en las reseñas, identificando contrastes o valoraciones extremas.
- Almacenar los resultados en una base de datos MySQL.
- Generar gráficos de polaridad y aspectos destacados de los videojuegos analizados.

## Características principales

- **Análisis de Sentimientos**: Clasificación de las reseñas en positivas, negativas y neutrales.
- **Análisis de Polarización**: Detección de opiniones extremas o contrastadas entre los usuarios.
- **Base de Datos Relacional**: Utilización de MySQL para almacenar los productos, reseñas y gráficas generadas.
- **Generación de Reportes Visuales**: Gráficos generados a partir de los datos de las reseñas.

## Tecnologías utilizadas

- **Frontend**: React
- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Librerías de NLP**: PyTorch, Hugging Face Transformers
- **Modelo de Lenguaje**: Llama 3.2 3B (Fine-tuned)
- **Gráficas**: Matplotlib, Seaborn
- **Control de Versiones**: Git y GitHub

## Instalación

Sigue estos pasos para instalar y ejecutar el sistema en tu entorno local.

### Requisitos previos

- **Python 3.x** (recomendado instalar en un entorno virtual)
- **Node.js** y **npm**
- **MySQL**

### Instrucciones

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/AlbeXos21/TFG.git
   cd tu_repositorio
