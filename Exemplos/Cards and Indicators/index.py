#API
from dotenv import load_dotenv
from api_helpers import executa_sql
import os

#Dash
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

#Pandas
import pandas as pd

#Token & URL
load_dotenv()
token = os.getenv('TOKEN')
url_base = os.getenv('DOMAIN')

#Data

#Canais de Divulgação
query = {'query':"SELECT channel, COUNT(*) total  FROM stilingue_tabaco  GROUP BY channel"}     
df_total_by_channel = executa_sql(token, url_base, query)
channels = df_total_by_channel['channel'].unique().tolist()
channels.append('Todos')

#App

app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP], 
        title='Cards and Indicators',
        meta_tags=[{
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }]
    )

#Layout




app.layout = dbc.Container([
        dbc.Row([
            #Image
            dbc.Col([
                dbc.Card([
                    html.Img(
                        src='assets/logo.png',
                        #Gambiarra pra "centralizar" a img
                        style={'padding-top':'7vh'},
                    ),
                ],
                className='align-self-center mx-auto',
                style={'height':'33vh',},
                ),
            ],
            xs=12, sm=12, md=12, lg=4, xl=4,
            ),

            #Text
            dbc.Col([
                dbc.Card([
                    html.H1(
                        'Lorem ipsum',
                        className='card-title mb-4',
                        ),
                    html.H4(
                        'Lorem ipsum',
                        className='card-subtitle mb-2 text-muted',
                    ),
                    html.P(
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pretium tempor risus vel laoreet. Sed feugiat massa sed sapien gravida, a varius lorem eleifend. Pellentesque a erat nec diam scelerisque blandit a at urna.',
                        className='card-text',
                        ),
                    html.A(
                        'Link',
                        href='https://bigdata.icict.fiocruz.br/',
                        target='_blank',
                        className='card-link',
                    )
                ],
                style={'height':'33vh',},
                ),
            ],
            xs=12, sm=12, md=12, lg=4, xl=4,
            ),

            #Indicator
            dbc.Col([
                dbc.Card([
                    html.Div(
                        dcc.Dropdown(
                            id='dropdown', 
                            multi=False, 
                            value='Portais',
                            options=[{'label':x, 'value':x}
                                    for x in sorted(channels)],
                        ),
                        className='mx-auto',
                        style={"width": "95%", 'margin':'center', 'padding-top':'1vh'}
                    ),

                    html.Div(
                        dcc.Graph(
                            figure={},
                            id='indicator',
                            style={'height':'15vh',},
                        )
                    ),
                ],
                style={'height':'33vh',},
                ),
            ],
            xs=12, sm=12, md=12, lg=4, xl=4,
            ),
        ],
        justify='around',
        style={'padding-top':'33vh',},
        ),
    ],
    fluid=True,
    )

@app.callback(
    Output('indicator', 'figure'),
    Input('dropdown', 'value'),
)

def update_graph(value):

    if value == 'Todos':
        query = {'query':f"SELECT COUNT(*) publicacoes FROM stilingue_tabaco"}
        df = executa_sql(token, url_base, query)
        num = df.loc[0].at['publicacoes']
    else:
        query = {'query':f"SELECT COUNT(*) publicacoes FROM stilingue_tabaco WHERE channel='{value}'"}
        df = executa_sql(token, url_base, query)
        num = df.loc[0].at['publicacoes']
    
    fig = {'data': [go.Indicator(
                mode='number',
                value=num,
                number={'valueformat': ',',
                        'font': {'size': 100}},
            )]
        }
    return fig

if __name__ == "__main__":
    app.run_server( 
        port=8050, 
        host='localhost', 
        use_reloader=True,
        debug=True,
        )