import json
import humanize
import locale

from src.data.getData import (
    Melhores,
    SerieHistoricaPedidos,
    proporcaoVendedores,
    Top10Categorias,
    DistribuicaoCliente,
    VendasSemanas
)
from src.graphics.plots import (
    SerieHistoricaPedidosPlot,
    proporcaoVendedoresPlot,
    Top10CategoriasPlot,
    DistribuicaoClientePlot,
    VendasSemanasPlot
)


from dash import Dash, dcc, _dash_renderer, html
import dash_mantine_components as dmc


#--- Humanize
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
humanize.i18n.activate("pt_BR")
#---

_dash_renderer._set_react_version('18.2.0')
app = Dash('Ecommerce',title='Ecommerce', external_stylesheets=[dmc.styles.ALL])


# Queries
with  open('backend\\queries-states.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# Configs plots

configs = {'displaylogo': False, 'displayModeBar':False}


# cartão
produto , receita , vendendor, cliente = Melhores()

# Figuras Linha 1
seriePlot = SerieHistoricaPedidosPlot(SerieHistoricaPedidos())
piePlot   = proporcaoVendedoresPlot(proporcaoVendedores())
top10Plot = Top10CategoriasPlot(Top10Categorias())


# Figuras Linha 2
mapplot = DistribuicaoClientePlot(DistribuicaoCliente())
barplot = VendasSemanasPlot(VendasSemanas())

#----- HTML CARDS
cards = dmc.Grid([
    dmc.GridCol([   
        dmc.Card([
            dmc.CardSection([
                dmc.Text("Receita total dos últimos 3 meses", size="sm")
            ], withBorder=True, inheritPadding=True, py="xs"),
            dmc.Text(humanize.intword(receita), fw=500, size="lg")
        ], withBorder=True, shadow="sm", radius="md")
    ], span=2.5), 
    #-----------
    dmc.GridCol([
        dmc.Card([
            dmc.CardSection([
                dmc.Text("Categoria preferida", size="sm")
            ], withBorder=True, inheritPadding=True, py="xs"),
            dmc.Text(humanize.intword(produto[0]), fw=500, size="lg")
        ], withBorder=True, shadow="sm", radius="md")
    ], span=2),  
    #-----------
    dmc.GridCol([
        dmc.Card([
            dmc.CardSection([
                dmc.Text("Estado com maior número de vendedor", size="sm")
            ], withBorder=True, inheritPadding=True, py="xs"),
            dmc.Text(humanize.intword(data.get(vendendor[0], 'oi'), "%0.3f"), fw=500, size="lg")
        ], withBorder=True, shadow="sm", radius="md")
    ], span=2.8),
    #-----------
    dmc.GridCol([
        dmc.Card([
            dmc.CardSection([
                dmc.Text("Estado com maior número de clientes", size="sm")
            ], withBorder=True, inheritPadding=True, py="xs"),
            dmc.Text(humanize.intword(data.get(cliente[0], 'oi'), "%0.3f"), fw=500, size="lg")
        ], withBorder=True, shadow="sm", radius="md")
    ], span=2.7),
], gutter="xs", align="stretch", justify='center' )


#----- Line 1 Plotsp
plotsL1 = dmc.Grid([
    dmc.GridCol([
        dmc.Paper([
            dcc.Graph(figure=seriePlot, config=configs),
        ], p="xs", shadow="xl", mt="md", withBorder=True)
    ], span=4),
    dmc.GridCol([
        dmc.Paper([
            dcc.Graph(figure=piePlot, config=configs),
        ], p="xs", shadow="xl", mt="md", withBorder=True)        
    ], span=4),
    dmc.GridCol([
        dmc.Paper([
            dcc.Graph(figure=top10Plot, config=configs),
        ], p="xs", shadow="xl", mt="md", withBorder=True)        
    ], span=4),
])
#------ line 2 plots
plotsL2 = dmc.Grid([
    dmc.GridCol([
        dmc.Paper([
            dcc.Graph(figure=mapplot, config=configs),
        ], p="xs", shadow="xl", mt="md", withBorder=True)
    ], span=4.5),
    dmc.GridCol([
        dmc.Paper([
            dcc.Graph(figure=barplot, config=configs),
        ], p="xs", shadow="xl", mt="md", withBorder=True)        
    ], span=4)
], justify='center',  align="stretch")


#------ LAYOUT
app.layout = dmc.MantineProvider([

    dmc.Grid([
            dmc.GridCol([cards]),
            dmc.GridCol([plotsL1]),
            dmc.GridCol([plotsL2])
        ], gutter='xs', style={'padding': '5px'}),      
])


if __name__ == '__main__': app.run(debug=True)