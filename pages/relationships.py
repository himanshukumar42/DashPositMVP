import pandas as pd
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import os

dash.register_page(__name__, title="relationship", path='/relationship', name="Relationship 📈")

try:
    path = os.path.join(os.getcwd(), "data", 'uploaded_file.csv')
    df = pd.read_csv(path)
except Exception as e:
    print(str(e))
    df = None

def create_scatter_chart(x_axis="Age", y_axis="Fare"):
    return px.scatter(data_frame=df, x=x_axis, y=y_axis, height=600)


columns = df.columns

x_axis = dcc.Dropdown(id="x_axis", options=columns, value=columns.tolist()[0], clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=columns, value=columns.tolist()[1], clearable=False)

layout = html.Div(children=[
    html.Br(),
    "X-Axis", x_axis,
    "Y-Axis", y_axis,
    dcc.Graph(id="scatter")
])


@callback(Output("scatter", "figure"), [Input("x_axis", "value"), Input("y_axis", "value"), ])
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)
