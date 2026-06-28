import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset", page_icon="🗂️")


@st.cache_data
def cargar_datos():
    return pd.read_csv("data/processed/streaming_users_clean.csv")


@st.cache_data
def cargar_log():
    return pd.read_csv("logs/pipeline_log.csv")


df = cargar_datos()
log = cargar_log()

st.title("🗂️ El dataset")

st.markdown(
    "Cada fila representa un **usuario** de una plataforma de streaming. Las columnas "
    "registran su plan de suscripción, edad, país, género favorito, consumo mensual, "
    "tickets de soporte y fecha de último ingreso."
)

col1, col2, col3 = st.columns(3)
col1.metric("Usuarios", f"{len(df):,}")
col2.metric("Columnas", df.shape[1])
col3.metric("Retención final", f"{log['Retención (%)'].iloc[-1]:.2f}%")

st.divider()

st.subheader("Calidad inicial y transformaciones aplicadas")
st.markdown(
    "El dataset original (`data/raw/streaming_users_dirty.json`) tenía **160 `user_id` "
    "duplicados**, categorías inconsistentes (mayúsculas/minúsculas, abreviaturas, espacios "
    "ocultos) y valores imposibles (edades negativas o de 150 años, minutos de consumo "
    "negativos o de 99.999, hasta 150 tickets de soporte). El proceso completo de detección y "
    "tratamiento, paso a paso, está en `notebooks/02_calidad_y_limpieza.ipynb`; el resumen "
    "queda registrado acá:"
)
st.dataframe(log, use_container_width=True, hide_index=True)

st.divider()

st.subheader("Vista previa del dataset procesado")
st.dataframe(df.head(10), use_container_width=True)

st.caption(
    "Detalle completo de cada decisión (evidencia → acción aplicada → impacto observado) en "
    "notebooks/01_inspeccion_inicial.ipynb y notebooks/02_calidad_y_limpieza.ipynb."
)
