import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import csv
import re


def obter_dados_b3 (csv_clean,csv_enrich,colunas,empresas_df):
    df = pd.read_csv(csv_clean,sep =',')
    df = df[colunas]   

    acao = df['cd_acao_com_sufixo'].unique().tolist()
    data_ontem = datetime.now() - timedelta(days=2)
    data_hoje = datetime.now()
    data_ontem = data_ontem.strftime('%Y-%m-%d')
    data_hoje = data_hoje.strftime('%Y-%m-%d')
    novos_registros = []

    for symbol in acao:
        acao = yf.Ticker(symbol)        
        historico = acao.history(start=data_ontem, end=data_hoje)        
        
        if not historico.empty:            
            valor_abertura = historico['Open'].iloc[0]
            valor_abertura = round(valor_abertura,2)
            valor_fechamento = historico['Close'].iloc[0]
            valor_fechamento = round(valor_fechamento,2)
            quantidade_negociada = historico['Volume'].iloc[0]
            data_pregao = historico.index[0].strftime('%Y-%m-%d')
            cd_acao = symbol.split('.')[0]
            tp_merc = 10
            cd_acao_rdz = symbol[:4]
            vl_maximo = historico['High'].max()
            vl_maximo = round(vl_maximo, 2)
            vl_minimo = historico['Low'].min()
            vl_minimo = round(vl_minimo, 2)
            vl_medio = historico['Close'].mean()
            vl_medio = round(vl_medio, 2)
            vl_volume = vl_medio*quantidade_negociada
            
        
        
            # Cria um novo registro com os valores obtidos
            novo_registro = {'cd_acao': cd_acao,
                            'dt_pregao': data_pregao,
                            'tp_merc': tp_merc,
                            'vl_abertura': valor_abertura,   
                            'vl_maximo': vl_maximo,        
                            'vl_minimo': vl_minimo,      
                            'vl_medio': vl_medio,       
                            'vl_fechamento': valor_fechamento,
                            'qt_tit_neg': quantidade_negociada,
                            'vl_volume': vl_volume,
                            'cd_acao_rdz':cd_acao_rdz,
                            'cd_acao_com_sufixo': symbol}
            
            novos_registros.append(novo_registro)

    df_existente = pd.read_csv(csv_clean)

    df_novos_registros = pd.DataFrame(novos_registros)

    df_atualizado = pd.concat([df_existente, df_novos_registros], ignore_index=True)

    df_atualizado = pd.merge(df_atualizado, empresas_df, on='cd_acao_rdz', how='left')
    
    df_atualizado = df_atualizado.rename(columns={'id': 'id_empresa'})

    df_atualizado['vl_volume'] = df_atualizado['vl_volume'].apply(lambda x: '{:.2f}'.format(x))

    df_atualizado.to_csv(csv_enrich, index=False)

csv_clean = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\fCotacoes.csv'  
csv_enrich = 'C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\enrich\\fCotacoes.csv'  
colunas = ['dt_pregao','cd_acao', 'tp_merc','vl_abertura','vl_maximo','vl_minimo','vl_medio','vl_fechamento','qt_tit_neg','vl_volume','cd_acao_rdz','cd_acao_com_sufixo']
empresas_df = pd.read_csv('C:\\projetos_bi\\testeAnalistaBI-main\\an_bi\\files\\clean\\dimEmpresas_bolsa.csv', sep=',', usecols=['id', 'cd_acao_rdz'])

obter_dados_b3 (csv_clean,csv_enrich,colunas,empresas_df)