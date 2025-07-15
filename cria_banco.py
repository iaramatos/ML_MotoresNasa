# cria_banco.py
import pandas as pd
import sqlite3

# --- Configuração ---
# Nome do arquivo de dados da NASA
NOME_ARQUIVO_DADOS = 'train_FD001.txt'
# Nome que daremos ao nosso banco de dados
NOME_BANCO_DADOS = 'producao.db'
# Nome da tabela que armazenará os dados
NOME_TABELA = 'turbofan_data'

# --- Definição das Colunas (de acordo com a documentação do dataset) ---
# O arquivo .txt não tem cabeçalho, então precisamos definir os nomes das colunas
nomes_colunas = [
    'unit_number', 'time_in_cycles', 'op_setting_1', 'op_setting_2', 'op_setting_3',
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5', 'sensor_6',
    'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12',
    'sensor_13', 'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18',
    'sensor_19', 'sensor_20', 'sensor_21'
]

# --- Lógica Principal ---
# Conecta ao banco de dados (cria o arquivo .db se não existir)
conn = sqlite3.connect(NOME_BANCO_DADOS)
print(f"Banco de dados '{NOME_BANCO_DADOS}' conectado.")

# Carrega os dados do arquivo .txt
# Usamos sep=' ' para indicar que as colunas são separadas por espaços
# Usamos header=None porque o arquivo não tem cabeçalho
# Usamos names=nomes_colunas para atribuir os nomes que definimos
df = pd.read_csv(NOME_ARQUIVO_DADOS, sep='\s+', header=None, names=nomes_colunas)

# O leitor pode criar colunas extras vazias no final, vamos removê-las
df = df.dropna(axis=1, how='all')

print(f"Dados do arquivo '{NOME_ARQUIVO_DADOS}' carregados. {len(df)} linhas encontradas.")

# Salva o DataFrame na tabela do banco de dados
df.to_sql(NOME_TABELA, conn, if_exists='replace', index=False)
print(f"Dados salvos com sucesso na tabela '{NOME_TABELA}'.")

# Fecha a conexão com o banco
conn.close()