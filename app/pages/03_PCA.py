import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.set_page_config(page_title="PCA", page_icon="🧭")

ORDEN_PLAN = ['Básico', 'Estándar', 'Premium']
VARIABLES = ['age', 'monthly_watch_time_mins', 'customer_support_tickets', 'plan_ordinal']


@st.cache_data
def cargar_datos():
    df = pd.read_csv("data/processed/streaming_users_clean.csv")
    orden_plan = {'Básico': 0, 'Estándar': 1, 'Premium': 2}
    df['plan_ordinal'] = df['subscription_plan'].map(orden_plan)
    return df


@st.cache_data
def calcular_pca(df):
    X = df[VARIABLES]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA()
    componentes = pca.fit_transform(X_scaled)
    return componentes, pca.explained_variance_ratio_ * 100


df = cargar_datos()
componentes, varianza = calcular_pca(df)
varianza_acum = np.cumsum(varianza)

st.title("🧭 Reducción de dimensionalidad (PCA)")

st.markdown("""
### Variables utilizadas
`age`, `monthly_watch_time_mins`, `customer_support_tickets` y `subscription_plan`
(codificada como ordinal: Básico=0, Estándar=1, Premium=2 — tiene un orden real).
Se excluyeron `country` y `favorite_genre` por ser categóricas sin orden natural, y
`last_login_date` por no ser numérica y retener valores faltantes sin imputar.

### Escalamiento aplicado
`StandardScaler` (obligatorio antes de PCA, Clase 8): sin escalar, `monthly_watch_time_mins`
(varianza ≈240.000) domina por completo sobre las demás variables (varianza entre 0.6 y 137).
""")

st.divider()
st.subheader("Varianza explicada")

col1, col2 = st.columns(2)
col1.metric("Varianza retenida (PC1 + PC2)", f"{varianza_acum[1]:.1f}%")
col2.metric("Componente más fuerte", f"PC1 ({varianza[0]:.1f}%)")

# Visualización 1 — Scree plot
fig1, ax1 = plt.subplots(figsize=(6, 4))
etiquetas = [f"PC{i+1}" for i in range(len(VARIABLES))]
ax1.bar(etiquetas, varianza, color="#4C72B0", label="Varianza explicada")
ax1.plot(etiquetas, varianza_acum, color="#C44E52", marker="o", label="Varianza acumulada")
ax1.set_ylabel("Varianza (%)")
ax1.legend()
st.pyplot(fig1)

st.markdown(
    "**Interpretación:** no hay un codo marcado — la varianza se reparte de forma "
    "relativamente pareja entre las primeras tres componentes (35.6%, 25.2%, 24.8%), reflejo "
    "de que solo dos de las cuatro variables originales están correlacionadas entre sí "
    "(`monthly_watch_time_mins` y `plan_ordinal`, r=0.42). Se retienen **2 componentes "
    f"({varianza_acum[1]:.1f}%)** para poder visualizar el resultado en un plano, no como una "
    "reducción exhaustiva de la dimensionalidad original."
)

st.divider()
st.subheader("Usuarios proyectados en las 2 primeras componentes")

# Visualización 2 — Scatter PC1 vs PC2
df_pca = pd.DataFrame(componentes[:, :2], columns=["PC1", "PC2"])
df_pca["subscription_plan"] = df["subscription_plan"].values

fig2, ax2 = plt.subplots(figsize=(7, 6))
sns.scatterplot(
    data=df_pca, x="PC1", y="PC2", hue="subscription_plan",
    hue_order=ORDEN_PLAN, alpha=0.4, s=20, ax=ax2,
)
ax2.set_xlabel(f"PC1 ({varianza[0]:.1f}% de la varianza)")
ax2.set_ylabel(f"PC2 ({varianza[1]:.1f}% de la varianza)")
st.pyplot(fig2)

st.markdown(
    "**Interpretación:** los tres planes se separan con claridad a lo largo de **PC1**, "
    "confirmando que esa componente captura el eje plan-consumo. No hay separación por plan "
    "en PC2 — esa componente combina `age` y `customer_support_tickets`, dos variables sin "
    "relación real entre sí (correlación original ≈0). PCA no encontró una segmentación "
    "nueva: confirmó, de forma más compacta, el hallazgo central del EDA."
)

st.divider()
st.caption(
    "Detalle completo del análisis (selección de variables, cargas de cada componente) en "
    "notebooks/04_pca.ipynb."
)
