import pandas as pd
import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/intro', name="Intro 📋")

titanic_df = pd.read_csv("titanic.csv")


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "width": "100%",
}

sidebar = html.Div(
    [
        html.H2("PositPOC", className="display-4"),
        html.Hr(),
        html.P(
            "Sample Application for POC", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Link(page['name'], href=page['relative_path'], className='btn btn-dark m-2 fs-5')
                for page in dash.page_registry.values()],
            vertical=True,
            pills=True,
        ),
        dash.page_container,
    ],
    style=SIDEBAR_STYLE,
)

layout = html.Div(children=[
    html.Br(),
    html.H1("This is the basic application for Posit connect POC")
], style=CONTENT_STYLE)
