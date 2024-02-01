from dash import html, dcc, Dash, callback, Input, Output
import dash
import plotly.express as px
import pandas as pd
import base64
import io

house_price_df = pd.DataFrame()


def create_histogram(col_name):
    fig = px.histogram(house_price_df, x=col_name, nbins=50)
    fig.update_traces(marker={"line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


def create_scatter_chart(x_axis, y_axis):
    fig = px.scatter(house_price_df, x=x_axis, y=y_axis)
    fig.update_traces(marker={"size": 12, "line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


def create_pie_chart(df, col_name, price_col):
    house_cnt = df.groupby(col_name).count()[[price_col]].rename(columns={price_col: "Count"}).reset_index()
    fig = px.pie(house_cnt, values=house_cnt["Count"], names=house_cnt[col_name], hole=0.5)
    fig.update_traces(marker={"line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


def create_bar_chart(df, x_axis, col_name):
    fig = px.bar(df, x=x_axis, y=col_name, color=x_axis, barmode="group")
    fig.update_traces(marker={"line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))


external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(__name__, external_stylesheets=external_css)

sidebar = html.Div([
    html.Br(),
    html.H3("PositPOC", className="text-center fw-bold fs-2"),
    html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select CSV File')
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
        multiple=False
    ),
    html.Br(),
    html.H3("Histogram", className="fs-4"),
    dcc.Dropdown(id="hist_column", options=[], value=None, clearable=False, className="text-dark p-2"),
    html.Br(),
    html.H3("ScatterChart", className="fs-4"),
    dcc.Dropdown(id="x_axis", options=[], value=None, clearable=False, className="text-dark p-2"),
    dcc.Dropdown(id="y_axis", options=[], value=None, clearable=False, className="text-dark p-2"),
    html.Br(),
    html.H3("BarChart", className="fs-4"),
    dcc.Dropdown(id="avg_drop", options=[], value=None, clearable=False, className="text-dark p-2")
], className="col-2 bg-primary text-white", style={"height": "100vh"})


@app.callback([Output('hist_column', 'options'),
               Output('x_axis', 'options'),
               Output('y_axis', 'options'),
               Output('avg_drop', 'options')],
              [Input('upload-data', 'contents')])
def update_dropdown_options(contents):
    global house_price_df
    if contents is None:
        raise dash.exceptions.PreventUpdate

    house_price_df = parse_contents(contents)
    options = [{'label': col, 'value': col} for col in house_price_df.columns]

    return options, options, options, options


main_content = html.Div([
    html.Br(),
    html.H2("Dynamic Dataset Analysis", className="text-center fw-bold fs-1"),
    html.Div([
        dcc.Graph(id="histogram", className="col-5"),
        dcc.Graph(id="scatter_chart", className="col-5")
    ], className="row"),
    html.Div([
        dcc.Graph(id="bar_chart", className="col-5"),
        # dcc.Graph(id="pie_chart", figure=create_pie_chart(), className="col-5"),
    ], className="row"),
], className="col", style={"height": "100vh", "background-color": "#e5ecf6"})

app.layout = html.Div([
    html.Div([sidebar, main_content], className="row")
], className="container-fluid", style={"height": "100vh"})


# Updated callback to update the charts based on user selections
@app.callback(Output("histogram", "figure"),
              [Input("hist_column", "value")])
def update_histogram(hist_column):
    if hist_column is None:
        raise dash.exceptions.PreventUpdate
    return create_histogram(hist_column)


@app.callback(Output("scatter_chart", "figure"),
              [Input("x_axis", "value"),
               Input("y_axis", "value")])
def update_scatter(x_axis, y_axis):
    if x_axis is None or y_axis is None:
        raise dash.exceptions.PreventUpdate
    return create_scatter_chart(x_axis, y_axis)


@app.callback(Output("bar_chart", "figure"),
              [Input("x_axis", "value"),
               Input("avg_drop", "value")])
def update_bar(x_axis, avg_drop):
    if x_axis is None or avg_drop is None:
        raise dash.exceptions.PreventUpdate
    return create_bar_chart(house_price_df, x_axis, avg_drop)


if __name__ == "__main__":
    app.run_server(debug=True)
