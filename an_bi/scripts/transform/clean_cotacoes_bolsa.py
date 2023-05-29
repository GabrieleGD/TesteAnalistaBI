import pandas as pd
import datetime

def filtrar_ultimas_cotacoes(csv_raw, colunas, csv_clean,sufixo):
    
    #Leitura dos arquivos que serão usados
    empresas_df = pd.read_csv('C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\dimEmpresas_bolsa.csv', sep=',', usecols=['id', 'cd_acao_rdz'])
    df = pd.read_csv(csv_raw,sep =';')    
    df = df[colunas]   
           
    #Formatações
    df['dt_pregao'] = pd.to_datetime(df['dt_pregao'], format='%Y%m%d').dt.date
    df['vl_volume'] = df['vl_volume'].apply(lambda x: '{:.2f}'.format(x))
    df['cd_acao_com_sufixo'] = df['cd_acao'] + sufixo
    
    # Filtros 
    maior_data = df['dt_pregao'].max()
    df = df[df['dt_pregao'] == maior_data]
    df = df[df['tp_merc'] == 10]

    #Mesclagem    
    df = pd.merge(df, empresas_df, on='cd_acao_rdz', how='left')
    df = df.rename(columns={'id': 'id_empresa'})

    #Carregamento
    df.to_csv(csv_clean, index=False,mode='w')

   
csv_raw = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\raw\\cotacoes_bolsa.csv'
colunas = ['dt_pregao','cd_acao', 'tp_merc','vl_abertura','vl_maximo','vl_minimo','vl_medio','vl_fechamento','qt_tit_neg','vl_volume','cd_acao_rdz']
csv_clean = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\fCotacoes.csv'
sufixo = '.SA'

filtrar_ultimas_cotacoes(csv_raw, colunas, csv_clean,sufixo)