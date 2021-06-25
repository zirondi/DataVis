#API
from dotenv import load_dotenv
from api_helpers import executa_sql
import os

#Dash
from dash.dependencies import Input, Output, State
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
import plotly.express as px

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


#App

app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP], 
        title='Pandemia na Internet: Fumantes',
        meta_tags=[{
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }]
    )

#Styles


#Layout

header = dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        'Pandemia na Internet: Fumantes',
                        className='text-center text-primary mb-4',
                        style={'vertical-align':'middle'},
                    ),
                ],
            xs=12, sm=12, md=12, lg=12, xl=12,
            ),
)

sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Filtros")),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style
                html.Span(className="gg-filters"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                    # 'padding-top':'10vh',
                },
                id="sidebar-toggle",
            ),
            width="auto",
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Lorem ipsum dolor sit amet.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        dbc.Collapse(
                dcc.Dropdown(
                            id='dropdown', 
                            multi=False, 
                            value='Portais',
                            options=[{'label':x, 'value':x}
                                    for x in sorted(channels)],
                        ),
            id="collapse",
        ),
    ],
    id="sidebar",
)

first_row = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(
                            id='publi-dia', 
                            style={'height':'66vh',},
                            figure={}
                        )
                    ],
                    
                    ),
                ],
                xs=12, sm=12, md=12, lg=10, xl=10,
                ),
        ],
        justify='around',
        style={'padding-top':'4vh',},
)

second_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(
                        id='publi-grupo', 
                        style={'height':'33vh',},
                        figure={}
                    ),
                ],
                ),
            ],
            # width={'size':8,},
            xs=12, sm=12, md=12, lg=8, xl=8,
            ),

            dbc.Col([
                dbc.Card([
                    dcc.Graph(
                        id='dist-canal', 
                        style={'height':'33vh',},
                        figure={}
                    ),
                ],
                ),
            ],
            # width={'size':4,},
            xs=12, sm=12, md=12, lg=4, xl=4,
            ),
        ],
        justify='around',
        style={'padding-top':'4vh',},
        )

third_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                ],
                    id='word-cloud', 
                    style={'height':'66vh',},

                ),
            ],
            # width={'size':8,},
            xs=12, sm=12, md=12, lg=8, xl=8,
            ),

            dbc.Col([
                dbc.Card([
                    dash_table.DataTable(
                        id='publi-veiculos',
                    )
                ],
                style={'height':'66vh',},
                ),
            ],
            # width={'size':4,},
            xs=12, sm=12, md=12, lg=4, xl=4,
            ),
        ],
        justify='around',
        style={'padding-top':'4vh',},
        )

fourth_row = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dash_table.DataTable(
                        id='publicacoes',
                    )
                ],
                style={'height':'92vh',},
                ),
            ],
            xs=12, sm=12, md=12, lg=12, xl=12,
            #width={'size':12,},
            ),
        ],
        style={'padding-top':'4vh','padding-bottom':'4.5vh',},
        )

content = dbc.Container([
        first_row,
        second_row,
        third_row,
        fourth_row,],
        id='page-content')

app.layout = dbc.Container(
    [
        header,
        sidebar,
        content,
    ],
    fluid=True,
    )

#Sidebar Callback
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


#publi-dia
@app.callback(
    Output('publi-dia', 'figure'),
    Input('dropdown', 'value'),
)

def update_graph(values):
    # query = {'query':f"SELECT data_ref, COUNT(*) publicacoes FROM stilingue_tabaco WHERE channel IN ({values}.toString()) GROUP BY data_ref"}
    query = {'query':f"SELECT data_ref, COUNT(*) publicacoes FROM stilingue_tabaco WHERE channel ='{values}' GROUP BY data_ref"}
    df = executa_sql(token, url_base, query)
    fig = px.bar(
        df, 
        x="data_ref",
        y="publicacoes",
        labels={
            'data_ref':"Datas",
            'publicacoes': "Publicações",
        },
        title='Publicações por Dia',
        # template='plotly_dark',
    )
    return fig



if __name__ == "__main__":
    app.run_server( 
        port=8050, 
        host='localhost', 
        use_reloader=True,
        debug=True,
        )