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
import plotly.graph_objects as go

#Pandas
import pandas as pd

# import wordcloud
# https://www.kaggle.com/mehmetkasap/plotly-scatter-bar-pie-chart-and-word-cloud

#Token & URL
load_dotenv()
token = os.getenv('TOKEN')
url_base = os.getenv('DOMAIN')

#Data

#Canais de Divulgação
query = {'query':"SELECT channel, COUNT(*) total  FROM stilingue_tabaco  GROUP BY channel"}     
df_total_by_channel = executa_sql(token, url_base, query)
channels = df_total_by_channel['channel'].unique().tolist()

#Grupos de Keyword
query = {'query': f"SELECT grupo.keyword, COUNT(*) total from stilingue_tabaco GROUP BY grupo.keyword"}
df_total_by_keyword = executa_sql(token, url_base, query)
keywords = df_total_by_keyword['grupo.keyword'].unique().tolist()

#helpers

def query_string_fomatter(values):
    sep = "', '"
    query = sep.join(values)
    return query    


#App

app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.MATERIA], 
        title='Pandemia na Internet: Fumantes',
        meta_tags=[{
            'name': 'viewport', 
            'content': 'width=device-width, initial-scale=1'
        }]
    )

#Styles

#Empty

#Layout

sidebar_header = dbc.Row(
        [
            dbc.Col(html.H2("Filtros"), className='text-left'),
            dbc.Col(
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className='gg-filters'),
                    className='navbar-toggler',
                    style={
                        'color': 'rgba(0,0,0,.5)',
                        'border-color': 'rgba(0,0,0,.1)',
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
                ],
                id="blurb",
            ),
            html.Div(
                [
                    html.H4(
                        'Tipo de Publicação',
                        style={'padding-top':'1vh',}
                        ),
                    dcc.Dropdown(
                        id='dropdown-publi', 
                        multi=True, 
                        value=channels,
                        optionHeight=35,
                        options=[{'label':x, 'value':x}
                                for x in sorted(channels)],
                        searchable=False,
                        clearable=False,
                        style={'margin':'center', 'padding-top':'1vh'}
                        ),
                    html.H4(
                        'Grupos',
                        style={'padding-top':'1vh'},
                        ),
                    dcc.Dropdown(
                        id='dropdown-keyword',
                        multi=True,
                        value=keywords,
                        optionHeight=35,
                        options=[{'label':x, 'value':x}
                                for x in sorted(keywords)],
                        searchable=False,
                        clearable=False,
                        style={'margin':'center', 'padding-top':'1vh'}
                    ),
            ],
            )

        ],
        id="sidebar",
    )

header = dbc.Row(
            dbc.Col(
                [
                    html.H1(
                        'Pandemia na Internet: Fumantes',
                        className='text-center text-primary',
                        style={'vertical-align':'middle'},
                    ),
                ],
            xs=12, sm=12, md=12, lg=12, xl=12,
            ),
    )

first_row = dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.Spinner(
                            dcc.Graph(
                                figure={},
                                id='publi-indicator',
                            ),
                            spinnerClassName = 'text-primary'
                        ),
                    ],
                    ),
                ],
                xs=12, sm=12, md=12, lg=2, xl=2,
                ),
        ],
        justify='around',
        style={'padding-top':'4vh',},
    )

#Tudo que não for a Navbar precisa ter/estar numa div com o nome page-content
app.layout = dbc.Container(
    [
        sidebar,
        html.Div(
        [
            header,
            first_row,
        ],
        id='page-content'
        ),
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

#
@app.callback(
    [
    Output('publi-indicator', 'figure'),
    ],

    [
    Input('dropdown-publi', 'value'),
    Input('dropdown-keyword', 'value'),
    ]
)
def update_graph(
    dropdown_publi, 
    dropdown_keywords,
    ):
    where_string = f"WHERE channel in ('{query_string_fomatter(dropdown_publi)}') AND grupo.keyword in ('{query_string_fomatter(dropdown_keywords)}')"

    query_publi_ind = {'query':f"SELECT COUNT(*) publicacoes FROM stilingue_tabaco {where_string}"}

    df_ind = executa_sql(token, url_base, query_publi_ind)


    #publi-indicator
    num = df_ind.loc[0].at['publicacoes']
    publi_indicator = [{'data': [go.Indicator(
        mode = 'number',
        value = num,
        number = {'valueformat': ',',
                'font': {'size': 40}},
    )],
    'layout': go.Layout(
        title = {
            'text': 'Publicações'
            },
            ),
        }]

    return publi_indicator

#Server
if __name__ == "__main__":
    app.run_server( 
        port=8050, 
        host='localhost', 
        use_reloader=True,
        debug=True,
        )