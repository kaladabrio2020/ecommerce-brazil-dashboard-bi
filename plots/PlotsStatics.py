import numpy as np
import pandas as pd
import seaborn as sea
import plotly.express as px
import plotly.graph_objects as go
import humanize
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
humanize.i18n.activate("pt_BR")

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

def LinePlotPedidos(data):

    fig = go.Figure(
        go.Scatter(
            x = data['data'],
            y = data['pedidos'],
            name = 'Série histórica',
            hovertemplate='Série histórica<br> Data = %{x}<br> Valor = %{y}<extra></extra>',
            line=dict(color='royalblue')

        )
    )
    fig.add_traces(
        go.Scatter(
            x=data['data'].iloc[9:], 
            y=data['pedidos'].rolling(10).mean().dropna(),
            name = 'Média Móvel',
            hovertemplate='Média Móvel<br>Data = %{x}<br> Valor = %{y}<extra></extra>',
            line=dict(
                color='tomato',
                width=4,
                dash='dot'
            )
            )
    )
    fig.update_layout(
        title = dict(
            text = 'Série histórica do número de pedidos',
            font = dict(
                size = 12,
                color='black'   
            )
        ),
        legend = dict(
            borderwidth=0,
            orientation='h',
            entrywidth=100,
            font = dict(
                size=12,
                color='black'
            )
        ),

        xaxis=dict(
            tickfont = dict(
                size = 12,
                color='black'
            ),
            showgrid=False,
        ),
        yaxis=dict(
            tickfont = dict(
                size = 12,
                color='black'
            ),
            showgrid=True,
            zeroline=False,
            gridcolor='black',
            griddash='dot',
        ),
        autosize=True,
        margin=dict(l=45, r=10, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor="rgba(0,0,0,0)",
        template='simple_white',



    )

    fig.update_traces(
           hoverlabel=dict(
                font = dict(
                     family = 'Arial', 
                     size   = 15, 
                     color  = 'black'),
                align = 'left',
        ))
    return fig


def PiePlot(data):
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
        hovertemplate='<br>%{text}<br>%{customdata}<br>%{value}<br>%{percent}<extra></extra>',

        marker = dict(
            colors = sea.color_palette(palette='pastel', n_colors=10)
        )
    )
    fig.update_layout(
        title = dict(
            text='Proporção de vendedores',
            font=dict(
                color='black',
                size =12
            )
        ),
        legend = dict(
            visible=True,
            title  =dict(
                text='Estados'
            ),
            font   =dict(
                size=10
            ) 
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor="white",
        font  = {'size': 12, 'color': 'black'},
    )
    return fig

def Top10Categoria(data):
    fig = go.Figure(
        go.Bar(
            x = data['tota_receita'][::-1],
            y = data['product_category_name'][::-1],
            text =data['tota_receita'][::-1].apply(lambda x: humanize.intword(x, "%0.2f").replace('thousand','mil') if 'thousand' in humanize.intword(x, "%0.3f") else  humanize.intword(x, "%0.2f")), 
            orientation='h'
        )
    )

    fig.update_traces(
        marker_line_color='black',
        marker_line_width=0.5,
        marker = dict(
            color = ['lightblue']*7 + ['royalblue']*3
        ),
        hovertemplate="%{x}<br>%{y}<extra></extra>"
    )
    fig.update_layout(
        title = dict(
            text = 'Top 10 Categória com maior receita',
            font=dict( size=12 )
            
        ),
        xaxis = dict(
            visible=False
        ),
        autosize=True,
        template='simple_white',
        margin=dict(l=160, r=0, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor="rgba(0,0,0,0)",

    )
    return fig

def plotMaps(df):
    brazil = df
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
    
        title = dict(
            text = 'Distribuição de Clientes',
            xanchor = 'left',
            y = 0.96,
            font = dict(
                size = 12,
                color='black'   
            )
        ),
        hovermode='closest',
        mapbox_zoom =100,
        mapbox_style="carto-voyager",
    
        margin={"r":0,"t":10,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0, 0,0,0)', 
        dragmode    =False,
        autosize=True
    )
    return fig

def plotSemanas(ano2017, ano2018):
    
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
        textposition='inside'
    )
    fig.update_layout(
        barmode='stack',
        hovermode='x',
        title = dict(
            text = 'Quantidade de vendas por semana',
            font = dict(
                size = 12,
                color='black'   
            )
        ),
        yaxis = dict(
            visible=False
        ),
        legend = dict(
            borderwidth=0.5,
            orientation='h',
            x=0.7,
            y=1.2,
            entrywidth =0,
            font = dict(
                size=8,
                color='black'
            )
        ),
        margin=dict(l=5, r=5, t=50, b=20),
        template='simple_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0, 0,0,0)', 
        dragmode    =False,
        )
    return fig