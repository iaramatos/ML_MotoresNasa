# training_pipeline_v2.py
import pandas as pd
import sqlite3
import numpy as np
from prefect import task, flow
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# As tarefas 'extrair_dados_do_banco' e 'calcular_rul_e_transformar' continuam iguais.
@task(log_prints=True, retries=3, retry_delay_seconds=10)
def extrair_dados_do_banco(caminho_banco: str = 'producao.db') -> pd.DataFrame:
    with sqlite3.connect(caminho_banco) as conn:
        df = pd.read_sql_query("SELECT * FROM turbofan_data", conn)
    return df

@task(log_prints=True)
def calcular_rul_e_transformar(df: pd.DataFrame) -> pd.DataFrame:
    max_cycles = df.groupby('unit_number')['time_in_cycles'].transform('max')
    df['rul'] = max_cycles - df['time_in_cycles']
    return df

@task(log_prints=True)
def treinar_modelo_de_regressao_v2(df: pd.DataFrame) -> None:
    """Treina um modelo com uma separação de dados mais realista."""
    print("Iniciando treinamento do modelo v2...")

    # --- NOVA LÓGICA DE SEPARAÇÃO ---
    # Vamos treinar com os primeiros 80 motores e testar com os últimos 20.
    total_engines = df['unit_number'].nunique()
    train_engines = list(range(1, int(total_engines * 0.8) + 1)) # Motores para treino
    test_engines = list(range(int(total_engines * 0.8) + 1, total_engines + 1)) # Motores para teste

    train_df = df[df['unit_number'].isin(train_engines)]
    test_df = df[df['unit_number'].isin(test_engines)]

    print(f"Divisão por motores: {len(train_engines)} para treino, {len(test_engines)} para teste.")

    # 1. Seleção de Features e Target
    features_cols = [col for col in df.columns if col not in ['unit_number', 'time_in_cycles', 'rul']]
    
    X_train = train_df[features_cols]
    y_train = train_df['rul']
    
    X_test = test_df[features_cols]
    y_test = test_df['rul']
    
    # 2. Treinamento do Modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    print("Treinando o RandomForestRegressor...")
    model.fit(X_train, y_train)
    print("Treinamento concluído.")

    # 3. Avaliação do Modelo nos motores NUNCA VISTOS
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Avaliação do Modelo V2 - Erro Médio Absoluto (MAE): {mae:.2f} ciclos")

    # 4. Salvar o modelo treinado
    caminho_modelo = 'modelo_rul.pkl'
    joblib.dump(model, caminho_modelo)
    print(f"Modelo (V2) salvo com sucesso em '{caminho_modelo}'.")

@flow(name="ML Pipeline de Treinamento de RUL v2")
def ml_pipeline_flow_v2():
    dados_brutos = extrair_dados_do_banco()
    dados_transformados = calcular_rul_e_transformar(dados_brutos)
    treinar_modelo_de_regressao_v2(dados_transformados)

if __name__ == "__main__":
    ml_pipeline_flow_v2()