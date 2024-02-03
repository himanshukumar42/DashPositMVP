import pandas as pd
import dash
from dash import dcc, html, callback

import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/distribution', name="Distribution 📊")

df = pd.read_csv("data/uploaded_file.csv")


def create_distribution(col_name="Age"):
    return px.histogram(data_frame=df, x=col_name, height=600)


columns = df.columns
dd = dcc.Dropdown(id="dist_column", options=columns, value=columns.tolist()[0], clearable=False)


layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])


@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column):
    return create_distribution(dist_column)
