import base64
import io
import os

from dash.dependencies import Input, Output
import pandas as pd
import dash
from dash import html, dash_table, dcc, callback
import dash_bootstrap_components as dbc
import uuid

dash.register_page(__name__, path='/dataset', name="Dataset 📋")

df = None

layout = html.Div(children=[
    html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False,
    ),
    html.Br(),
    dash_table.DataTable(id='datatable',
                         page_size=10,
                         style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black",
                                     "font-size": "11px", "text-align": "left"},
                         style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white",
                                       "padding": "10px", "font-size": "18px"},
                         ),
])


def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    global df
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    file_path = f'{os.getcwd()}/data/uploaded_file.csv'
    df.to_csv(file_path, index=False)
    return df.to_dict('records')


@callback(Output('datatable', 'data'), [Input('upload-data', 'contents')])
def update_table(contents):
    if contents is None:
        global df
        df = pd.read_csv("data/uploaded_file.csv").to_dict('records')
        return df

    children = parse_contents(contents)
    return children
