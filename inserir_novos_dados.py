import pandas as pd
import sqlite3

def adicionar_nova_leitura_motor(dados_novos):
    """
    Conecta ao banco de dados de produção e anexa novos dados.
    
    Args:
        dados_novos (pd.DataFrame): um DataFrame com as novas linhas de dados.
    """
    conn = sqlite3.connect('producao.db')
    try:
        # Usamos 'append' para adicionar as novas linhas sem apagar as antigas
        dados_novos.to_sql('turbofan_data', conn, if_exists='append', index=False)
        print(f"{len(dados_novos)} novas leituras adicionadas com sucesso ao banco de dados.")
    finally:
        conn.close()

if __name__ == "__main__":
    # SIMULAÇÃO: Imagine que estes são dados novos de sensores chegando
    # para o motor 100, nos ciclos 201 e 202.
    # No mundo real, estes dados viriam de outro sistema.
    novas_leituras = {
        'unit_number': [100, 100],
        'time_in_cycles': [201, 202],
        'op_setting_1': [0.002, 0.0021],
        'op_setting_2': [0.0003, 0.0003],
        'op_setting_3': [100.0, 100.0],
        'sensor_1': [518.67, 518.67],
        'sensor_2': [643.1, 643.2],
        'sensor_3': [1595.2, 1595.8],
        'sensor_4': [1415.5, 1416.2],
        'sensor_5': [14.62, 14.62],
        'sensor_6': [21.61, 21.61],
        'sensor_7': [552.8, 552.7],
        'sensor_8': [2388.1, 2388.12],
        'sensor_9': [9065.1, 9068.3],
        'sensor_10': [1.3, 1.3],
        'sensor_11': [47.6, 47.65],
        'sensor_12': [521.1, 521.0],
        'sensor_13': [2388.11, 2388.13],
        'sensor_14': [8138.2, 8139.0],
        'sensor_15': [8.45, 8.46],
        'sensor_16': [0.03, 0.03],
        'sensor_17': [394, 395],
        'sensor_18': [2388, 2388],
        'sensor_19': [100.0, 100.0],
        'sensor_20': [38.7, 38.68],
        'sensor_21': [23.18, 23.15]
    }
    df_novos = pd.DataFrame(novas_leituras)
    
    adicionar_nova_leitura_motor(df_novos)