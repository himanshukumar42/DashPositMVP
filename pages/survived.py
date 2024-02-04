import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import os

dash.register_page(__name__, title="survived", path='/survived', name="Survived Count 📊")

try:
    path = os.path.join(os.getcwd(), "data", 'uploaded_file.csv')
    df = pd.read_csv(path)
except Exception as e:
    print(str(e))
    df = None



def create_bar_chart(col_name="Sex"):
    fig = px.histogram(data_frame=df, x=col_name, color=col_name,
                       histfunc="count", barmode='group', height=600)
    fig = fig.update_layout(bargap=0.5)
    return fig


columns = df.columns
dd = dcc.Dropdown(id="sel_col", options=columns, value=columns.tolist()[2], clearable=False)

layout = html.Div(children=[
    html.Br(),
    dd,
    dcc.Graph(id="bar_chart")
])


@callback(Output("bar_chart", "figure"), [Input("sel_col", "value"), ])
def update_bar_chart(sel_col):
    return create_bar_chart(sel_col)
