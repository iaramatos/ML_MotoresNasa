# app.py
import streamlit as st
import pandas as pd
import joblib

# --- Configuração da Página ---
st.set_page_config(
    page_title="Previsão de RUL de Motores",
    page_icon="✈️",
    layout="wide"  # Usando layout 'wide' para melhor visualização
)

# --- Carregamento do Modelo ---
# Carrega o modelo treinado que salvamos anteriormente
@st.cache_resource
def load_model():
    try:
        model = joblib.load("modelo_rul.pkl")
        return model
    except FileNotFoundError:
        return None

model = load_model()

if model is None:
    st.error("❌ Arquivo do modelo 'modelo_rul.pkl' não encontrado. Por favor, treine o modelo primeiro executando 'training_pipeline_v2.py'.")
    st.stop()


# --- Interface do Usuário ---
st.title("⚙️ Previsão de Vida Útil Remanescente (RUL)")
st.write(
    "Insira os dados dos sensores de um motor para prever sua vida útil restante. Os valores abaixo estão pré-ajustados com médias do dataset."
)

# Dicionário para armazenar as entradas do usuário
input_data = {}

# Lista de features que o modelo espera na ordem correta
feature_cols = [
    'op_setting_1', 'op_setting_2', 'op_setting_3', 'sensor_1', 'sensor_2', 'sensor_3', 
    'sensor_4', 'sensor_5', 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 
    'sensor_11', 'sensor_12', 'sensor_13', 'sensor_14', 'sensor_15', 'sensor_16', 
    'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21'
]

# --- Seção de Inputs com Sliders ---
st.subheader("Parâmetros de Entrada")

# Organizando os sliders em colunas para uma interface mais limpa
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Operacionais**")
    input_data['op_setting_1'] = st.slider("Config. 1", -0.005, 0.005, 0.0, step=0.0001, format="%.4f")
    input_data['op_setting_2'] = st.slider("Config. 2", -0.0005, 0.0005, 0.0, step=0.0001, format="%.4f")
    input_data['op_setting_3'] = st.slider("Config. 3", 95.0, 105.0, 100.0)
    
    st.markdown("**Sensores 1-5**")
    input_data['sensor_1'] = st.slider("Sensor 1", 470.0, 520.0, 518.67)
    input_data['sensor_2'] = st.slider("Sensor 2", 530.0, 650.0, 642.68)
    input_data['sensor_3'] = st.slider("Sensor 3", 1300.0, 1620.0, 1590.52)
    input_data['sensor_4'] = st.slider("Sensor 4", 1100.0, 1450.0, 1408.93)
    input_data['sensor_5'] = st.slider("Sensor 5", 9.0, 15.0, 14.62)

with col2:
    st.markdown("**Sensores 6-11**")
    input_data['sensor_6'] = st.slider("Sensor 6", 5.0, 25.0, 21.61)
    input_data['sensor_7'] = st.slider("Sensor 7", 130.0, 600.0, 553.36)
    input_data['sensor_8'] = st.slider("Sensor 8", 2000.0, 2400.0, 2388.09)
    input_data['sensor_9'] = st.slider("Sensor 9", 8300.0, 9250.0, 9054.42)
    input_data['sensor_10'] = st.slider("Sensor 10", 1.0, 2.0, 1.3)
    input_data['sensor_11'] = st.slider("Sensor 11", 36.0, 50.0, 47.54)

with col3:
    st.markdown("**Sensores 12-16**")
    input_data['sensor_12'] = st.slider("Sensor 12", 120.0, 530.0, 521.72)
    input_data['sensor_13'] = st.slider("Sensor 13", 2380.0, 2395.0, 2388.09)
    input_data['sensor_14'] = st.slider("Sensor 14", 8100.0, 8250.0, 8143.75)
    input_data['sensor_15'] = st.slider("Sensor 15", 8.0, 9.5, 8.44)
    input_data['sensor_16'] = st.slider("Sensor 16", 0.01, 0.05, 0.03)

with col4:
    st.markdown("**Sensores 17-21**")
    input_data['sensor_17'] = st.slider("Sensor 17", 300.0, 400.0, 393.21)
    input_data['sensor_18'] = st.slider("Sensor 18", 2380.0, 2395.0, 2388.0)
    input_data['sensor_19'] = st.slider("Sensor 19", 98.0, 102.0, 100.0)
    input_data['sensor_20'] = st.slider("Sensor 20", 10.0, 40.0, 38.81)
    input_data['sensor_21'] = st.slider("Sensor 21", 23.0, 24.0, 23.28)


# --- Seção de Previsão ---
st.divider()

# Botão centralizado para previsão
_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    if st.button("✈️ PREVER VIDA ÚTIL REMANESCENTE", type="primary", use_container_width=True):
        # 1. Criar um DataFrame com os dados de entrada na ordem correta
        features_df = pd.DataFrame([input_data], columns=feature_cols)
        
        # 2. Fazer a previsão
        with st.spinner('Calculando...'):
            prediction = model.predict(features_df)
        
        # 3. Mostrar o resultado
        st.subheader("Resultado da Previsão:", anchor=False)
        st.metric(label="RUL Estimada (Ciclos Restantes)", value=f"{int(prediction[0])}")