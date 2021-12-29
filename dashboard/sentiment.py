import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
# from jupyter_dash import JupyterDash
import plotly.graph_objects as go

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot') # optional: for ggplot-like style

# check for latest version of Matplotlib
# print ('Matplotlib version: ', mpl.__version__) 
topic_v=pd.read_csv('topic_v.csv')
topic_tb=pd.read_csv('topic_tb.csv')

import seaborn as sns

def create_sentiment_application(flask_app):
    dash_app = dash.Dash(server=flask_app,name="sentiment",url_base_pathname="/sentiment/")
    
    dash_app.layout = html.Div(children=[html.H1('Topic-wise Sentiment Analysis Dashboard', 
                                    style={'textAlign': 'center', 'color': '#0d0d0d',
                                    'font-size': 40}),
                                    html.Div(["Input Topic: ", dcc.Input(id='input-topic', value='1', 
                                    type='number', style={'height':'25px', 'font-size': 25}),], 
                                    style={'font-size': 25}),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='line-plot')),
                                    ])
    
    init_callbacks(dash_app)
    return dash_app

def init_callbacks(dash_app):
    @dash_app.callback( Output(component_id='line-plot', component_property='figure'),
               Input(component_id='input-topic', component_property='value'))

    def get_graph(entered_topic):
        if int(entered_topic) > 0 and int(entered_topic) < 8:
            df1 = topic_tb[str(entered_topic)]
            df2 =  topic_v[str(entered_topic)]
            fig={
                'data': [
                    {'x':['neutral','positive','negative'] , 'y': df1, 'type': 'bar', 'name': 'Text-Blob'},
                    {'x':['neutral','positive','negative'], 'y': df2, 'type': 'bar', 'name': 'Vader'} ]
                }
        return fig
