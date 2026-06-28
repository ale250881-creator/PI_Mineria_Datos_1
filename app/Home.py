import streamlit as st

st.set_page_config(page_title="Streaming Users — Proyecto Integrador", page_icon="🎬", layout="wide")

st.title("🎬 Análisis de Usuarios de una Plataforma de Streaming")

st.markdown("""
**Integrantes:** _completar nombre y apellido de cada integrante_
**Comisión:** _completar_
**Fecha:** _completar_

### Contexto
Este proyecto analiza el comportamiento de usuarios de una plataforma de streaming
(plan de suscripción, consumo, género favorito, soporte) a partir de un dataset provisto
por la cátedra, aplicando un pipeline completo de inspección, calidad de datos, análisis
exploratorio y reducción de dimensionalidad (PCA).

🔗 **Repositorio:** _completar enlace al repo de GitHub_
""")

st.info("Usá el menú de la izquierda para navegar entre las secciones: Dataset, EDA, PCA y Conclusiones.")
