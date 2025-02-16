from dash import Dash, html, dcc, callback, Output, Input
import humanize
import locale
import dash_bootstrap_components as dbcc
from backend.backPostgresOne_ import *
from plots.PlotsStatics import *


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
humanize.i18n.activate("pt_BR")

app = Dash('Dashboard Ecommerce',assets_folder='assets', title='ecommerce')


with  open('backend\\queries-states.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


#----------

# cartão
produto , receita , vendendor, cliente = Melhores()

# lineplot
seriePedidos = SerieHistoricaPedidos()
pizzaSeller  = pieVendendor() 
topCategoria = Top10Categorias()
# map
clientes = DistribuicaoCliente()

# barplot
ano2017, ano2018 = VendasSemanas()


app.layout = [
    html.Link(rel="stylesheet", href='assets\\style.css'),
    html.Div([
        html.Div([
            html.Div(
                dbcc.Card([
                    dbcc.CardHeader("Receita Total dos últimos 3 anos", className='pText'),
                    dbcc.CardBody([
                        html.H2(humanize.intword(receita)),
                    ])
            ]),  className='textDiv1'),
            html.Div(
                dbcc.Card([
                    dbcc.CardHeader("Categória preferida", className='pText'),
                    dbcc.CardBody([
                        html.H2(humanize.intword(produto[0])),
                    ])
            ]),  className='textDiv2'),
            html.Div(
                dbcc.Card([
                    dbcc.CardHeader("Estado com maior número de vendedor", className='pText'),
                    dbcc.CardBody([
                        html.H2(humanize.intword(data.get(vendendor[0], 'oi'), "%0.3f")),
                    ]),
            ]),  className='textDiv2')
            ,
            html.Div(
                dbcc.Card([
                    dbcc.CardHeader("Estado com maior número de clientes", className='pText'),
                    dbcc.CardBody([
                        html.H2(humanize.intword(data.get(cliente[0], 'oi'), "%0.3f")),
                    ]),

            ]),  className='textDiv2')

        ], className='containerText'),
        html.Div(
            html.Div([
                html.Div(dcc.Graph(figure=LinePlotPedidos(seriePedidos), className='Graph1'), className='DivGraph1'),
                html.Div([
                        dcc.Graph(figure=PiePlot(pizzaSeller), className='Graph1'),
                    ], className='DivGraph2'),
                html.Div(dcc.Graph(figure=Top10Categoria(topCategoria),  className='Graph1'), className='DivGraph3')
            ], className='DivMainPlots'),
        ),
        html.Div([
            html.Div(dcc.Graph(figure=plotSemanas(ano2017, ano2018), className='Graph1'), className='DivGraph4'),
            html.Div(dcc.Graph(figure=plotMaps(clientes), className='GraphMap'), className='DivGraphMaps'),
        ], className='DivMainPlots'),

    ])

]



if __name__ == '__main__':

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    humanize.i18n.activate("pt_BR")
    

    app.run(debug=True)