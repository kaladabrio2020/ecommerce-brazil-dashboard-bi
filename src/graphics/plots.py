import plotly.graph_objects as go
import humanize
import geobr
import numpy as np
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
humanize.i18n.activate("pt_BR")

def SerieHistoricaPedidosPlot(data):
    fig = go.Figure(
        go.Scatter(
            x = data['data'],
            y = data['pedidos'],
            name = 'Série histórica',
            hovertemplate='Data : %{x}<br>Valor : %{y}<extra></extra>',
            line=dict(color='royalblue')
        )
    )
    fig.update_layout(
        template = 'simple_white',
        font = dict(
            family="Inter, sans-serif",
        ),
        title = dict(
            text = 'Série Historica do número de pedido',
            font = dict(
                weight="bold",   
                size=16
            ),
            automargin=True,
        ),
        yaxis = dict(
            showgrid=True,
            zeroline=False,
            gridcolor='black',
            griddash='dot',
        ),
        margin = dict(
            r = 20,
            l = 0,
            b = 0,
            t = 50
        ),
        height = 300 
    )
    return fig

import seaborn as sea
def proporcaoVendedoresPlot(data):
    fig = go.Figure(
        go.Pie(
            labels=data['completo'],
            values=data['quantidade_vendedores'],
            hovertext=data['todos_estados'],
            customdata=data['completo'],

        )
    )
    fig.update_traces(
        textinfo='percent',
        hovertemplate='<br>%{text} - %{customdata} <br>%{value}<br>%{percent}<extra></extra>',

        marker = dict(
            colors = sea.color_palette(palette='pastel', n_colors=10),
            line = dict(width=1)
        )
    )
    fig.update_layout(
        font = dict(
            family="Inter, sans-serif",
        ),
        title = dict(
            text='Proporção de vendedores',
            font = dict(
                weight="bold",   
                size=16,
                color='black'
            ),
            automargin=True,
        ),
        legend = dict(
            visible=True,
            title  = dict(
                text = 'Estados'
            )
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height = 300
    )
    return fig

def Top10CategoriasPlot(data):
    text_ = data['tota_receita'][::-1].apply(lambda x: humanize.intword(x, "%0.2f").replace('thousand','mil') if 'thousand' in humanize.intword(x, "%0.3f") else  humanize.intword(x, "%0.2f"))
    fig = go.Figure(
        go.Bar(
            y=data['product_category_name'][::-1],
            x=data['tota_receita'][::-1],
            hovertemplate='Categoria : %{x}<br>Receita : %{y}<extra></extra>',
            text=text_,
            customdata=data['tota_receita'][::-1],
            orientation='h',
            )
        )
    fig.update_traces(
        hovertemplate="%{customdata}<br>%{y}<extra></extra>",
        hoverlabel = dict(
            bgcolor = 'white'  
        ),
        marker = dict(
            color = ['lightblue']*7 + ['royalblue']*3
        )
    )
    fig.update_layout(
        template = 'simple_white',
        font = dict(
            family="Inter, sans-serif",
        ),
        title = dict(
            text = 'Top 10 Categória com maior receita',
            font=dict( 
                size=16,
                weight='bold' 
            ),
            automargin = True
            
        ),
        xaxis = dict(
            visible=False
        ),
        autosize=True,
        margin = dict(
            r = 10,
            l = 0,
            b = 10,
            t = 50
        ),
        height = 300
    )
    return fig

def DistribuicaoClientePlot(data):
    brazil = data
    fig = go.Figure(
        go.Choropleth(
            geojson=brazil.__geo_interface__,
            locations=brazil.index,
            z=np.sqrt(brazil['count']),
            text=brazil['abbrev_state'],
            customdata=np.stack([brazil['name_state'], brazil['count'].apply(lambda x: humanize.intword(x).replace('thousand', 'mil'))], axis=1),
            colorscale = 'Reds',
            zmin=50,
            zmax=2000
        )
    )
    fig.update_traces(
        hovertemplate='Estados : %{customdata[0]}-%{text}<br>Clientes : %{customdata[1]}<extra></extra>',
        showscale=False,

    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_scale=10,
        bgcolor= 'rgba(0,0,0,0)'
    
    )
    fig.update_layout(
        font = dict(
            family="Inter, sans-serif",
        ),
        title = dict(
            text = 'Distribuição de Clientes',   
            font = dict(
                size = 16,
                color='black',
                weight='bold'
            ),
            automargin = True
        ),
        hovermode='closest',
        mapbox_zoom =600,
        mapbox_style="carto-positron",
    
        margin={"r":0,"t":50,"l":0,"b":0},
        dragmode    =False,
        autosize=True,
        height = 350
    )
    return fig

def VendasSemanasPlot(data):
    ano2018, ano2017 = data
    
    numero2018 = ano2018['quantidade_vendas'].apply(lambda x: humanize.intword(x).replace('thousand', 'mil'))
    numero2017 = ano2017['quantidade_vendas'].apply(lambda x: humanize.intword(x).replace('thousand', 'mil'))


    fig = go.Figure(data=[
        go.Bar(
            x=ano2017['semana'].str.replace('-feira', ''),
            y=ano2017['quantidade_vendas'],
            text=numero2017,
            name='2017',
            customdata=ano2017['quantidade_vendas'],
            marker_color='salmon',
            hovertemplate='Semana : %{x}<br>Quantidade de vendas : %{customdata}<extra></extra>'
        ),
        go.Bar(
            x=ano2018['semana'].str.replace('-feira', ''),
            y=ano2018['quantidade_vendas'],
            text=numero2018,
            name='2018',
            marker_color='royalblue',
            customdata=ano2018['quantidade_vendas'],
            hovertemplate='Semana : %{x}<br>Quantidade de vendas : %{customdata}<extra></extra>'
        )
    ])
    fig.update_traces(
        textposition='outside',
        cliponaxis=False,
    )
    fig.update_layout(
        barmode='stack',
        hovermode='x unified',
        font = dict(
            family="Inter, sans-serif",
        ),
        title = dict(
            text = 'Quantidade de vendas por semana',
            font = dict(
                size = 16,
                color='black',  
                weight='bold'
            ),
            automargin = True
        ),
        yaxis = dict(
            visible=False
        ),
        legend = dict(
            borderwidth=0.5,
            x=0.9,
            y=1.2,
            entrywidth =0,
            title = dict(
                text = 'Ano'
            ),
            font = dict(
                size=8,
                color='black'
            )
        ),
        margin=dict(l=5, r=5, t=50, b=5),
        template='simple_white',
        dragmode    =False,
        height = 350
        )
    return fig