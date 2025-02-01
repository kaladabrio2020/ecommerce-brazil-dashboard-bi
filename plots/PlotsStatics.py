import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def sellerCity(df: pd.DataFrame):
    fig = go.Figure(
        go.Pie(
            labels=df['estados'],
            values=df['quantidade_vendedores'],
            hole=.3
        )
    )


    fig.update_layout(
        title='Quantidade de vendedores por Estados',
        legend=dict(
            title='Estados'
        ),
    )
    fig.update_traces(
        hovertemplate='<br>Estado : %{label}<br>Vendedores : %{value}'
    )

    return fig

def receitaVendas(df: pd.DataFrame):
    fig = px.bar(
        df,
        x='ano',
        y='receita',
        title='Receita Total por Cidade dos Vendedores',
        labels={'receita_total': 'Receita Total (R$)'}
    )
    
    return fig
