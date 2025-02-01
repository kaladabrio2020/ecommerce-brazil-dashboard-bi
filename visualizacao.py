from dash import Dash, html, dcc, callback, Output, Input


from backend.backPostgresOne_ import *
from plots.PlotsStatics import *

app = Dash('Dashboard Ecommerce',assets_folder='assets')


app.layout = [
    html.Link(rel="stylesheet", href='assets\\style.css'),
    html.H1(children='Dados de Ecommerce Brasil', style={'textAlign':'center'}),
]



if __name__ == '__main__':
    
    app.run(debug=True)