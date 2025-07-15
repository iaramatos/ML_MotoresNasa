# training_pipeline.py
import pandas as pd
import sqlite3
from prefect import task, flow
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# --- Tarefa de Extração (mesma de antes) ---
@task(log_prints=True, retries=3, retry_delay_seconds=10)
def extrair_dados_do_banco(caminho_banco: str = 'producao.db') -> pd.DataFrame:
    """Extrai os dados da tabela 'turbofan_data' do banco de dados SQLite."""
    print(f"Conectando ao banco de dados: {caminho_banco}")
    with sqlite3.connect(caminho_banco) as conn:
        df = pd.read_sql_query("SELECT * FROM turbofan_data", conn)
    print(f"Extração concluída com sucesso. {len(df)} linhas lidas.")
    return df

# --- Tarefa de Transformação (mesma de antes) ---
@task(log_prints=True)
def calcular_rul_e_transformar(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a Vida Útil Remanescente (RUL) para cada motor."""
    print("Iniciando cálculo da RUL...")
    max_cycles = df.groupby('unit_number')['time_in_cycles'].transform('max')
    df['rul'] = max_cycles - df['time_in_cycles']
    print("Cálculo da RUL concluído. Nova coluna 'rul' adicionada.")
    return df

# --- NOVA TAREFA: Treinamento do Modelo ---
@task(log_prints=True)
def treinar_modelo_de_regressao(df: pd.DataFrame) -> None:
    """Treina um modelo de regressão para prever a RUL e o salva."""
    print("Iniciando treinamento do modelo...")

    # 1. Seleção de Features (colunas de entrada) e Target (alvo)
    # Vamos remover colunas que não são sensores e a própria RUL
    features = df.drop(columns=['unit_number', 'time_in_cycles', 'rul'])
    target = df['rul']

    # 2. Divisão em Dados de Treino e Teste
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    print(f"Dados divididos: {len(X_train)} para treino, {len(X_test)} para teste.")

    # 3. Treinamento do Modelo
    # RandomForestRegressor é um bom modelo para começar
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    print("Treinando o RandomForestRegressor...")
    model.fit(X_train, y_train)
    print("Treinamento concluído.")

    # 4. Avaliação do Modelo
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Avaliação do Modelo - Erro Médio Absoluto (MAE): {mae:.2f} ciclos")

    # 5. Salvar o modelo treinado
    caminho_modelo = 'modelo_rul.pkl'
    joblib.dump(model, caminho_modelo)
    print(f"Modelo salvo com sucesso em '{caminho_modelo}'.")

# --- Flow Principal Atualizado ---
@flow(name="ML Pipeline de Treinamento de RUL")
def ml_pipeline_flow():
    """Orquestra o processo completo: ETL e Treinamento do Modelo."""
    dados_brutos = extrair_dados_do_banco()
    dados_transformados = calcular_rul_e_transformar(dados_brutos)
    treinar_modelo_de_regressao(dados_transformados) # Adicionamos o passo de treinamento

# --- Execução do Flow ---
if __name__ == "__main__":
    ml_pipeline_flow()