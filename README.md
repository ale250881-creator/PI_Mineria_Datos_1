# PI_Mineria_Datos_1

## Información general

- **Materia:** Minería de Datos I
- **Integrantes:** Pablo Castillo
- **Comisión:** Sede Nodo - Turno Tarde
- **Fecha:** 28/06/2026
- **Dataset:** usuarios de una plataforma de streaming (provisto por la cátedra)

## Objetivo del proyecto

- Aplicar el pipeline completo de Minería de Datos I (inspección, calidad, preparación, EDA y PCA) sobre el dataset de usuarios de streaming provisto por la cátedra.
- Tomar decisiones de preparación justificadas con evidencia observada, no por aplicación automática de técnicas.
- Mantener trazabilidad completa del proceso mediante un log ETL (`logs/pipeline_log.csv`).
- Responder preguntas de análisis concretas definidas por el grupo, distinguiendo evidencia, interpretación y conclusión.
- Comunicar los resultados de forma clara en notebooks técnicos, una aplicación pública en Streamlit y un informe final breve.

## Dataset

- **Origen:** `streaming_users_dirty.json`, provisto por la cátedra (`data/raw/`).
- **Tamaño original:** 8.160 registros, 8 columnas.
- **Unidad de análisis:** cada fila es un usuario de una plataforma de streaming.
- **Columnas:** `user_id`, `age`, `subscription_plan`, `monthly_watch_time_mins`, `country`, `favorite_genre`, `last_login_date`, `customer_support_tickets`.
- **Calidad inicial:** duplicados, categorías inconsistentes y valores fuera de rango — detalle completo en `notebooks/01_inspeccion_inicial.ipynb`.
- **Dataset final:** `data/processed/streaming_users_clean.csv`, resultado del proceso documentado en `notebooks/02_calidad_y_limpieza.ipynb` y `logs/pipeline_log.csv`.

## Estructura del repositorio

```
PI_Mineria_Datos_1/
├── data/{raw,processed}/      # dataset original y dataset final
├── notebooks/                 # 01 inspección → 05 conclusiones
├── app/                        # aplicación Streamlit (Home + 4 páginas)
├── reports/informe_final.pdf  # informe final (máx. 2 páginas)
├── logs/pipeline_log.csv      # log ETL
└── requirements.txt
```

## Preparación y calidad de datos

- **Duplicados:** 160 `user_id` repetidos, eliminados — quedaron 8.000 registros.
- **Categorías inconsistentes:** `subscription_plan`, `country` y `favorite_genre` tenían mayúsculas, abreviaturas, tildes y espacios ocultos distintos para el mismo valor; se normalizaron con mapas de equivalencia.
- **Valores imposibles:** edades fuera de 0-100, consumo negativo, y valores idénticos repetidos en decenas de filas (99.999 / 50.000 en consumo; 99 / 150 en tickets) se convirtieron a NaN.
- **Diagnóstico de faltantes:** se comparó la tasa de falta por `subscription_plan` y `country`. `monthly_watch_time_mins` resultó **MAR** (10.7% de falta en Premium vs. 1.1% en Básico); el resto se trató como **MCAR**.
- **Imputación diferenciada:** mediana global (`age`, `customer_support_tickets`), mediana por plan (`monthly_watch_time_mins`, por ser MAR) y moda (`favorite_genre`). `last_login_date` **no se imputó**: una fecha de "último login" inventada distorsionaría más que dejarla vacía.
- **Retención final:** 98.04% de las filas originales. Detalle paso a paso en `notebooks/02_calidad_y_limpieza.ipynb` y `logs/pipeline_log.csv`.

## Resumen del análisis exploratorio

- Preguntas analizadas: distribución de edad, plan predominante, plan vs. consumo, tickets vs. consumo, género por país, y edad-consumo según plan.
- **Hallazgo principal:** el plan de suscripción organiza el consumo — mediana de 553 min (Básico) a 1.127 min (Premium).
- Dos hipótesis no se sostuvieron con evidencia: ni los tickets de soporte (r≈-0.0016) ni la edad (r≈0 dentro de cada plan) explican el consumo.
- El género favorito no varía de forma relevante por país (Comedia domina en los 7 países, 16%-19%).
- Se documentó un pico anómalo en `age=13` (385 casos) como limitación, sin alterar el dato.
- Detalle completo de cada visualización e interpretación en `notebooks/03_eda.ipynb` y en la página EDA de la aplicación.

## Reducción de dimensionalidad

- **Variables utilizadas:** `age`, `monthly_watch_time_mins`, `customer_support_tickets` y `subscription_plan` (codificada como ordinal).
- **Escalamiento:** `StandardScaler`, obligatorio antes de PCA por la diferencia de varianza entre variables.
- **Varianza explicada:** 60.75% en las 2 primeras componentes (35.6% + 25.2%); sin codo marcado, por la baja correlación entre variables.
- **Interpretación:** PC1 es el eje "plan + consumo" y separa claramente los 3 planes; PC2 combina variables sin relación real entre sí.
- Detalle completo (cargas, justificación de variables excluidas) en `notebooks/04_pca.ipynb` y en la página PCA de la aplicación.

## Visualización interactiva

- Aplicación en Streamlit con 5 páginas: Home, Dataset, EDA, PCA y Conclusiones (`app/Home.py` y `app/pages/`).
- App pública: https://trabajo-mineria-de-datos.streamlit.app/

## Cómo ejecutar localmente

```bash
git clone https://github.com/ale250881-creator/PI_Mineria_Datos_1
cd PI_Mineria_Datos_1
pip install -r requirements.txt
streamlit run app/Home.py
```

Para regenerar `data/processed/` y `logs/pipeline_log.csv` desde cero, correr los notebooks en orden (`01` → `05`) antes de levantar la app.

## Conclusiones

- El hallazgo más sólido del proyecto: `subscription_plan` explica el nivel de consumo, confirmado de forma independiente en el EDA y en PCA.
- Dos hipótesis intuitivas (tickets de soporte y edad) no se sostuvieron con los datos disponibles.
- **Limitaciones principales:** pico anómalo sin explicar en `age=13`, ~4% de `last_login_date` sin imputar, diagnóstico de faltantes acotado a dos variables observadas.
- **Próximos pasos:** indagar el origen del pico en `age=13`, incorporar variables temporales, y explorar reducción de dimensionalidad para variables categóricas (MCA).
- Desarrollo completo en `notebooks/05_conclusiones.ipynb` y `reports/informe_final.pdf`.
