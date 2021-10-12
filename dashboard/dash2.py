import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

def create_dash2_application(flask_app):
    dash_app = dash.Dash(server=flask_app,name="Dash2",url_base_pathname="/dash2/")

    dash_app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Dash: A web application framework for your data.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='example-graph-2',
            figure=fig
        )
    ])
    return dash_app
    


