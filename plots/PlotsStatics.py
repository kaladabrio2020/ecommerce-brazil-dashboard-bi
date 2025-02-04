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
        margin=dict(l=0, r=5, t=50, b=0),
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
        margin=dict(l=0, r=0, t=40, b=0),
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
            text =data['tota_receita'][::-1].apply(lambda x: humanize.intword(x).replace('thousand','mil') if 'thousand' in humanize.intword(x) else  humanize.intword(x)), 
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
        template='simple_white',
        margin=dict(l=10, r=0, t=40, b=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor="rgba(0,0,0,0)",

    )
    return fig