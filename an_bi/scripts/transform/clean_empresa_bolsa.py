import pandas as pd

def limpar_empresas_bolsa(csv_raw, colunas, csv_clean):
    
    df = pd.read_csv(csv_raw,sep =';')
    
    df = df[colunas]
   
    df['tx_cnpj'] = df['tx_cnpj'].str.replace('[^0-9]', '', regex=True) 
  
    df.to_csv(csv_clean, index=False,mode='w')
    
   
csv_raw = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\empresas_bolsa.csv'
colunas = ['id','cd_acao_rdz', 'nm_empresa','setor_economico','subsetor','segmento','cd_acao','tx_cnpj']
csv_clean = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\dimEmpresas_bolsa.csv'

limpar_empresas_bolsa(csv_raw, colunas, csv_clean)