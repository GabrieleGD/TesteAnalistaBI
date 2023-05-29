import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import csv


def mesclar_tabelas (csv_raw_empresa,csv_raw_nivel_atividade,csv_raw_porte,csv_raw_saude_tributaria,csv_raw_simples,csv_clean_historico,colunas_historico):
    
    df_historico = pd.read_csv(csv_raw_empresa, sep=';', usecols=['cnpj'], dtype={'cnpj': str})

    df_historico['data_atualizacao'] = datetime.now()
    
    # Leitura dos arquivos que serão usados
    df_nivel = pd.read_csv(csv_raw_nivel_atividade, sep=';', usecols=['cnpj', 'nivel_atividade'], dtype={'cnpj': str})
    df_porte = pd.read_csv(csv_raw_porte, sep=';', usecols=['cnpj', 'empresa_porte'], dtype={'cnpj': str})
    df_saude = pd.read_csv(csv_raw_saude_tributaria, sep=';', usecols=['cnpj', 'saude_tributaria'], dtype={'cnpj': str})
    df_simples = pd.read_csv(csv_raw_simples, sep=';', usecols=['cnpj', 'optante_simples', 'optante_simei'], dtype={'cnpj': str})
   
    # Mesclagem
    df_historico = pd.merge(df_historico,df_nivel, on='cnpj', how='left')
    df_historico = pd.merge(df_historico,df_porte, on='cnpj', how='left')
    df_historico = pd.merge(df_historico,df_saude, on='cnpj', how='left')
    df_historico = pd.merge(df_historico,df_simples, on='cnpj', how='left')

    # Carregamento
    df_historico.to_csv(csv_clean_historico, index=False,mode='w')

csv_raw_empresa = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\df_empresas.csv' 
csv_raw_nivel_atividade = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\empresas_nivel_atividade.csv'
csv_raw_porte = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\empresas_porte.csv'
csv_raw_saude_tributaria = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\empresas_saude_tributaria.csv'
csv_raw_simples = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\empresas_simples.csv' 

csv_clean_historico = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\fHistoricoEmpresas.csv' 

colunas_historico = ['data_atualizacao','cnpj','nivel_atividade','porte','saude_tributaria','optante_simples','optante_simei']


mesclar_tabelas (csv_raw_empresa,csv_raw_nivel_atividade,csv_raw_porte,csv_raw_saude_tributaria,csv_raw_simples,csv_clean_historico,colunas_historico)