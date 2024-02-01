import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
}

sidebar = html.Div(
    [
        html.H2("Main Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Posit Connect POC", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/intro", active="exact"),
                dbc.NavLink("Dataset", href="/dataset", active="exact"),
                dbc.NavLink("Relationship", href="/relationship", active="exact"),
                dbc.NavLink("Distribution", href="/distribution", active="exact"),
                dbc.NavLink("Survived", href="/survived", active="exact"),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname:
        return [
            html.Br(),
            html.Div(children=[
                dcc.Link(page['name'], href=page['relative_path'], className='btn btn-primary m-2 fs-5')
                for page in dash.page_registry.values()
            ]),
            dash.page_container
        ]
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
