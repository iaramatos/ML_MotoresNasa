# etl_pipeline.py
import pandas as pd
import sqlite3
from prefect import task, flow

# --- Tarefa de Extração ---
@task(log_prints=True)
def extrair_dados_do_banco(caminho_banco: str = 'producao.db') -> pd.DataFrame:
    """Extrai os dados da tabela 'turbofan_data' do banco de dados SQLite."""
    print(f"Conectando ao banco de dados: {caminho_banco}")
    conn = sqlite3.connect(caminho_banco)
    
    try:
        df = pd.read_sql_query("SELECT * FROM turbofan_data", conn)
        print(f"Extração concluída com sucesso. {len(df)} linhas lidas.")
    finally:
        conn.close()
        
    return df

# --- Tarefa de Transformação ---
@task(log_prints=True)
def calcular_rul_e_transformar(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a Vida Útil Remanescente (RUL) para cada motor."""
    print("Iniciando cálculo da RUL...")
    
    # 1. Encontrar o ciclo máximo (ciclo de falha) para cada motor
    max_cycles = df.groupby('unit_number')['time_in_cycles'].transform('max')
    
    # 2. Calcular a RUL subtraindo o ciclo atual do ciclo máximo
    df['rul'] = max_cycles - df['time_in_cycles']
    
    print("Cálculo da RUL concluído. Nova coluna 'rul' adicionada.")
    
    # Poderíamos remover colunas desnecessárias aqui se quiséssemos,
    # mas por enquanto vamos manter todas.
    
    return df

# --- Tarefa de Carregamento ---
@task(log_prints=True)
def carregar_dados_para_csv(df: pd.DataFrame, caminho_saida: str = 'dados_para_ml.csv'):
    """Salva o DataFrame transformado em um arquivo CSV."""
    print(f"Salvando dados transformados em '{caminho_saida}'...")
    df.to_csv(caminho_saida, index=False)
    print("Arquivo salvo com sucesso!")

# --- Flow Principal ---
@flow(name="ETL para Dados de Turbofan")
def etl_flow_principal():
    """Orquestra o processo de ETL: Extrai, Transforma (calcula RUL) e Carrega."""
    dados_brutos = extrair_dados_do_banco()
    dados_transformados = calcular_rul_e_transformar(dados_brutos)
    carregar_dados_para_csv(dados_transformados)

# --- Execução do Flow ---
if __name__ == "__main__":
    etl_flow_principal()