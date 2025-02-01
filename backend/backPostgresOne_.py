import json
import pandas as pd
import psycopg2 as pg

con =  pg.connect("dbname='ecommerce' user='postgres' host='127.0.0.1' port='5432' password='datascience007'")


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
