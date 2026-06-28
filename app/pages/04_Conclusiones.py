import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="✅")

st.title("✅ Conclusiones")

st.subheader("Hallazgos principales")

st.success(
    "**El plan de suscripción organiza el consumo de los usuarios.** Confirmado de forma "
    "independiente en el EDA (mediana de 553 min en Básico vs. 1.127 min en Premium) y en "
    "PCA (PC1, 35.6% de la varianza, dominado por plan y consumo)."
)
st.info(
    "Dos hipótesis intuitivas **no se sostuvieron** con los datos: ni los tickets de soporte "
    "(correlación ≈0 con el consumo) ni la edad (correlación ≈0 dentro de cada plan) explican "
    "el comportamiento de uso."
)
st.info(
    "El género favorito **no varía de forma relevante por país** — Comedia domina en los 7 "
    "países (16% a 19%), sin una preferencia regional marcada."
)

st.divider()
st.subheader("Limitaciones")
st.markdown("""
- El pico anómalo en `age = 13` (385 usuarios, 5 veces más que cualquier edad vecina) no pudo
  explicarse con la información disponible.
- `last_login_date` retiene ~4% de valores faltantes sin imputar — no se pudo analizar
  recencia de actividad para esos usuarios.
- El diagnóstico de mecanismo de falta (MCAR/MAR/MNAR) solo se contrastó contra dos variables
  observadas (`subscription_plan`, `country`); no puede descartarse una dependencia con
  variables no incluidas en el dataset.
- PCA se aplicó solo sobre variables numéricas/ordinales; `country` y `favorite_genre`
  quedaron fuera de esa técnica por ser categóricas sin orden natural.

El alcance de estas conclusiones está condicionado por la información disponible y por las
decisiones documentadas durante el proceso.
""")

st.divider()
st.subheader("Próximos pasos")
st.markdown("""
- Indagar el origen del pico en `age = 13` con la fuente del dataset.
- Incorporar variables temporales (fecha de alta, historial de actividad) para analizar
  evolución, no solo una foto fija del estado actual.
- Explorar técnicas de reducción de dimensionalidad para variables categóricas (MCA) si se
  quisiera incorporar `country` y `favorite_genre` al análisis conjunto con las numéricas.
""")

st.divider()
st.caption(
    "Desarrollo completo de cada conclusión (evidencia → interpretación → conclusión) en "
    "notebooks/05_conclusiones.ipynb."
)
