import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA", page_icon="📊")

ORDEN_PLAN = ['Básico', 'Estándar', 'Premium']


@st.cache_data
def cargar_datos():
    return pd.read_csv("data/processed/streaming_users_clean.csv")


df = cargar_datos()

st.title("📊 Análisis Exploratorio de Datos")
st.markdown(
    "Distribuciones y relaciones encontradas en el dataset de usuarios, ya limpio y preparado "
    "(ver `notebooks/02_calidad_y_limpieza.ipynb` y `notebooks/03_eda.ipynb` para el detalle "
    "completo del proceso)."
)
st.divider()

# ───────────────────────── Univariado ─────────────────────────
st.header("Análisis univariado")

st.subheader("1. Distribución de la edad")
fig1, ax1 = plt.subplots(figsize=(7, 4))
ax1.hist(df["age"], bins=20, color="#4C72B0", edgecolor="white")
ax1.set_xlabel("Edad")
ax1.set_ylabel("Cantidad de usuarios")
st.pyplot(fig1)
st.metric("Edad mediana", f"{df['age'].median():.0f} años")
st.markdown(
    "**Interpretación:** la edad se distribuye de forma simétrica, centrada en ~33 años "
    "(Q1≈25, Q3≈41) — el grueso de la audiencia es adulta joven/adulta. Se detectó un pico "
    "aislado en `age = 13` (385 casos, 5 veces más que cualquier edad vecina), documentado "
    "como limitación de calidad de datos en el informe final."
)

st.subheader("2. Plan de suscripción predominante")
conteo_plan = df["subscription_plan"].value_counts().reindex(ORDEN_PLAN)
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(x=conteo_plan.index, y=conteo_plan.values, order=ORDEN_PLAN, color="#4C72B0", ax=ax2)
ax2.set_xlabel("Plan")
ax2.set_ylabel("Cantidad de usuarios")
st.pyplot(fig2)
st.markdown(
    "**Interpretación:** el plan **Básico domina con el 45%** de los usuarios, seguido por "
    "Estándar (35%) y Premium (20%). La mayoría de la base de usuarios paga el plan más "
    "económico, no el de mayor valor."
)

st.divider()

# ───────────────────────── Bivariado ─────────────────────────
st.header("Análisis bivariado")

st.subheader("3. Consumo según plan de suscripción")
fig3, ax3 = plt.subplots(figsize=(7, 5))
sns.boxplot(data=df, x="subscription_plan", y="monthly_watch_time_mins", order=ORDEN_PLAN, ax=ax3)
ax3.set_xlabel("Plan")
ax3.set_ylabel("Minutos mensuales")
st.pyplot(fig3)
st.markdown(
    "**Interpretación:** hay una relación clara y ordenada entre plan y consumo: la mediana "
    "pasa de 553 min (Básico) a 840 min (Estándar) a 1.127 min (Premium) — el plan Premium "
    "consume prácticamente el doble que el Básico. El plan no es solo una etiqueta de precio: "
    "está asociado a un comportamiento de uso real."
)

st.subheader("4. Género favorito por país")
ct = pd.crosstab(df["country"], df["favorite_genre"], normalize="index").mul(100).round(1)
fig4, ax4 = plt.subplots(figsize=(9, 5))
sns.heatmap(ct, annot=True, fmt=".1f", cmap="Blues", cbar_kws={"label": "% dentro del país"}, ax=ax4)
ax4.set_xlabel("Género favorito")
ax4.set_ylabel("País")
st.pyplot(fig4)
st.markdown(
    "**Interpretación:** no hay una preferencia marcada por país — las proporciones de cada "
    "género se mantienen parecidas en los 7 países (diferencias menores a 3 puntos "
    "porcentuales en casi todos los casos). **Comedia** es el género más elegido en todos "
    "ellos (16% a 19%): el gusto por género parece transversal a la región, no específico de "
    "ningún país."
)

st.divider()

# ───────────────────────── Multivariado ─────────────────────────
st.header("Análisis multivariado")

st.subheader("5. Edad vs. consumo, según plan de suscripción")
planes_sel = st.multiselect("Filtrar por plan:", ORDEN_PLAN, default=ORDEN_PLAN)
df_filtrado = df[df["subscription_plan"].isin(planes_sel)]

fig5, ax5 = plt.subplots(figsize=(8, 6))
if len(df_filtrado) > 0:
    sns.scatterplot(
        data=df_filtrado, x="age", y="monthly_watch_time_mins", hue="subscription_plan",
        hue_order=[p for p in ORDEN_PLAN if p in planes_sel], alpha=0.4, s=20, ax=ax5,
    )
ax5.set_xlabel("Edad")
ax5.set_ylabel("Minutos mensuales")
st.pyplot(fig5)
st.markdown(
    "**Interpretación:** los planes forman bandas horizontales claramente separadas, y esa "
    "separación se mantiene estable en todas las edades — el plan explica el nivel de "
    "consumo, la edad no. Dentro de cada plan, la correlación entre edad y consumo es "
    "prácticamente nula (todas cerca de 0)."
)

st.divider()
st.caption(
    "Estos resultados se desarrollan con mayor profundidad, incluyendo el análisis de "
    "tickets de soporte vs. consumo (sin relación encontrada), en notebooks/03_eda.ipynb."
)
