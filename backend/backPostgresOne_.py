import json
import geobr
import numpy as np
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine

con = create_engine("postgresql+psycopg2://postgres:datascience007@localhost/ecommerce")

def BestSellerState():
    with open('backend\\queries.json', 'r') as file:
        data = json.load(file)
    query = data['queries']

    curr = con.cursor()
    
    curr.execute(query["SomaTotalVendendores"])
    con.commit()
    return pd.read_sql_query(query["SomaTotalVendendoresAgrupamendo"], con=con)



def melhorReceitaAnos():
    with open('backend\\queries.json', 'r') as file:
        data = json.load(file)
    query = data['queries']['receitaTotalNosAnos']

    return pd.read_sql_query(query, con=con)


def Melhores():
    with open('backend\\queries.json', 'r') as file:
        data = json.load(file)
    query = data['queries']

    produtoMaisVendido= pd\
        .read_sql_query(query['produtoMaisVendido'], con=con).values[0]
    
    receitaTotal = pd\
        .read_sql_query(query['receitaTotal'], con=con).values[0]

    receitaTotalNosAnos = pd\
        .read_sql_query(query['receitaTotalNosAnos'], con=con).values[0]

    estadoMaiorVendendor = pd\
        .read_sql_query(query['estadoComMaisVendedores'], con=con).values[0]
    
    estadoMaiorCliente = pd\
        .read_sql_query(query['estadoComMaisVendedores'], con=con).values[0]
    

    return produtoMaisVendido, receitaTotal, estadoMaiorVendendor, estadoMaiorCliente


def SerieHistoricaPedidos():
    with open('backend\\queries.json', 'r') as file:
        data = json.load(file)
    query = data['queries']

    series = pd\
        .read_sql_query(query["seriesHistoricaPedidos"], con=con)
    
    series['data_'] = pd.to_datetime(series['data_'])
    dicionario = {
        'data':[],
        'pedidos':[]
        }
 
    for i in series['data_'].dt.year.unique():
        x_ = series.loc[series['data_'].dt.year==i]
        
        range_ = pd.date_range(start=x_['data_'].min(), end=x_['data_'].max(), freq='W')
        
    
        for i, j in zip(x_['data_'], x_['count']):
            L = abs(i - range_).days
            dicionario['data'].append(range_[np.argmin(L)])
            dicionario['pedidos'].append(j)
        
    data = pd.DataFrame(dicionario)
    data = data.groupby(['data'])['pedidos'].sum().reset_index()
    return data
    
from sqlalchemy import text
    
def pieVendendor():

    with open('backend\\queries.json') as file:
        data = json.load(file)
    
    with open('backend\\queries-states.json', encoding='utf-8') as file:
        states = json.load(file)
    
    
    query = data['queries']
    with con.connect() as conection:
        conection.execute(text(query['SomaTotalVendendores']))
        conection.commit()

    data=pd.read_sql_query(query["SomaTotalVendendoresAgrupamendo"], con=con)
    data['completo'] = data['estados'].apply(lambda x:'Outros Estados' if states.get(x)==None else states.get(x))

    return data

def Top10Categorias(end=2016, start=2018):
    with open('backend\\queries.json') as file:
        data = json.load(file)

    query = data["queries"]

    data  = pd.read_sql_query(sql=query['receitaCategoria'], con=con)

    return data

def DistribuicaoCliente():
    brazil = geobr.read_state(year=2010, simplified=True)

    with open('backend\\queries.json') as file:
        data = json.load(file)

    query = data["queries"]

    data  = pd.read_sql_query(sql=query['distribuicaoClientes'], con=con)
    
    return pd.merge(brazil, data, how='left', left_on='abbrev_state', right_on='geolocation_state').fillna(0)



def VendasSemanas():
    with open('backend\\queries.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    query = data['queries']
    # Lendo as semanas
    data  = pd.read_sql_query(sql=query["Semanas"], con=con)
    
    data['ano'] = pd.to_datetime(data['ano'])
    # Renomeando as semanas
    data['semana'] = data['ano'].dt.day_name('pt').apply(lambda x:x.replace('\udce7','ç').replace('\udce1','á'))
    
    # Pegando apenas o ano
    data['ano'] = data['ano'].dt.year
    
    # Ordenando as semanas
    ordem = pd.CategoricalDtype(
        categories=["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"], 
    ordered=True)
    
    # 
    data = data.loc[data['ano'] != 2016].groupby(['ano', 'semana'])['quantidade_vendas'].sum().reset_index()

    #
    pd.options.mode.copy_on_write = True 

    ano2018 = data.loc[data['ano'] == 2018]
    ano2018 = data.iloc[
        ano2018['semana'].astype(ordem).sort_values().index, :
    ]

    ano2017 = data.loc[data['ano'] == 2017]
    ano2017 = data.iloc[
        ano2017['semana'].astype(ordem).sort_values().index, :
    ]

    return (ano2017, ano2018)