# app.py (versão final com exemplos)
import streamlit as st
import pandas as pd
import joblib

# --- Configuração da Página ---
st.set_page_config(
    page_title="Previsão de RUL de Motores",
    page_icon="✈️",
    layout="wide"
)

# --- Carregamento do Modelo ---
@st.cache_resource
def load_model():
    """Carrega o modelo treinado do arquivo .pkl"""
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

col1, col2, col3, col4 = st.columns(4)

# Mensagem de ajuda padrão
help_text = "Exemplo hipotético. O nome real da variável não é público."

with col1:
    st.markdown("**Operacionais**")
    input_data['op_setting_1'] = st.slider("Config. 1 (Ex: Altitude)", -0.005, 0.005, 0.0, step=0.0001, format="%.4f", help=help_text)
    input_data['op_setting_2'] = st.slider("Config. 2 (Ex: Velocidade)", -0.0005, 0.0005, 0.0, step=0.0001, format="%.4f", help=help_text)
    input_data['op_setting_3'] = st.slider("Config. 3 (Ex: Potência %)", 95.0, 105.0, 100.0, help=help_text)
    
    st.markdown("**Sensores 1-5**")
    input_data['sensor_1'] = st.slider("Sensor 1 (Ex: Temp. Fan K)", 470.0, 520.0, 518.67, help=help_text)
    input_data['sensor_2'] = st.slider("Sensor 2 (Ex: Temp. Saída LPC K)", 530.0, 650.0, 642.68, help=help_text)
    input_data['sensor_3'] = st.slider("Sensor 3 (Ex: Temp. Saída HPC K)", 1300.0, 1620.0, 1590.52, help=help_text)
    input_data['sensor_4'] = st.slider("Sensor 4 (Ex: Temp. Turbina K)", 1100.0, 1450.0, 1408.93, help=help_text)
    input_data['sensor_5'] = st.slider("Sensor 5 (Ex: Pressão Fan psia)", 9.0, 15.0, 14.62, help=help_text)

with col2:
    st.markdown("**Sensores 6-11**")
    input_data['sensor_6'] = st.slider("Sensor 6 (Ex: Rotação Fan RPM)", 5.0, 25.0, 21.61, help=help_text)
    input_data['sensor_7'] = st.slider("Sensor 7 (Ex: Pressão Estática psia)", 130.0, 600.0, 553.36, help=help_text)
    input_data['sensor_8'] = st.slider("Sensor 8 (Ex: Temp. Ref. K)", 2000.0, 2400.0, 2388.09, help=help_text)
    input_data['sensor_9'] = st.slider("Sensor 9 (Ex: Rotação Núcleo RPM)", 8300.0, 9250.0, 9054.42, help=help_text)
    input_data['sensor_10'] = st.slider("Sensor 10 (Ex: Razão Comb./Ar)", 1.0, 2.0, 1.3, help=help_text)
    input_data['sensor_11'] = st.slider("Sensor 11 (Ex: Pressão Bypass psia)", 36.0, 50.0, 47.54, help=help_text)

with col3:
    st.markdown("**Sensores 12-16**")
    input_data['sensor_12'] = st.slider("Sensor 12 (Ex: Temp. Saída K)", 120.0, 530.0, 521.72, help=help_text)
    input_data['sensor_13'] = st.slider("Sensor 13 (Ex: Pressão Ref. psia)", 2380.0, 2395.0, 2388.09, help=help_text)
    input_data['sensor_14'] = st.slider("Sensor 14 (Ex: Fluxo Comb. pps)", 8100.0, 8250.0, 8143.75, help=help_text)
    input_data['sensor_15'] = st.slider("Sensor 15 (Ex: Razão Pressão)", 8.0, 9.5, 8.44, help=help_text)
    input_data['sensor_16'] = st.slider("Sensor 16 (Ex: Ajuste Ignição)", 0.01, 0.05, 0.03, help=help_text)

with col4:
    st.markdown("**Sensores 17-21**")
    input_data['sensor_17'] = st.slider("Sensor 17 (Ex: Temp. Turbina Baixa K)", 300.0, 400.0, 393.21, help=help_text)
    input_data['sensor_18'] = st.slider("Sensor 18 (Ex: Temp. Exaustor K)", 2380.0, 2395.0, 2388.0, help=help_text)
    input_data['sensor_19'] = st.slider("Sensor 19 (Ex: Eficiência %)", 98.0, 102.0, 100.0, help=help_text)
    input_data['sensor_20'] = st.slider("Sensor 20 (Ex: Vibração 1 in/s)", 10.0, 40.0, 38.81, help=help_text)
    input_data['sensor_21'] = st.slider("Sensor 21 (Ex: Vibração 2 in/s)", 23.0, 24.0, 23.28, help=help_text)


# --- Seção de Previsão ---
st.divider()

_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    if st.button("✈️ PREVER VIDA ÚTIL REMANESCENTE", type="primary", use_container_width=True):
        features_df = pd.DataFrame([input_data], columns=feature_cols)
        
        with st.spinner('Calculando...'):
            prediction = model.predict(features_df)
        
        st.subheader("Resultado da Previsão:", anchor=False)
        st.metric(label="RUL Estimada (Ciclos Restantes)", value=f"{int(prediction[0])}")