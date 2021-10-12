# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
# from jupyter_dash import JupyterDash
import plotly.graph_objects as go

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

def create_dash1_application(flask_app):
    # dash_app = dash.Dash(__name__)
    dash_app = dash.Dash(server=flask_app,name="Dash1",url_base_pathname="/dash1/")
    dash_app.layout = html.Div(children=[ html.H1('Airline Performance Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', 
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
        Input(component_id='input-year', component_property='value'))
    def get_graph(entered_year):
        # Select 2019 data
        df =  airline_data[airline_data['Year']==int(entered_year)]
        
        # Group the data by Month and compute average over arrival delay time.
        line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

        fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
        fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
        return fig



    




    

