from dash import html, dcc, Dash, callback, Input, Output
import plotly.express as px
import pandas as pd

house_price_df = pd.read_csv('data.csv')


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


def create_pie_chart():
    house_cnt = house_price_df.groupby("city").count()[["price"]] \
        .rename(columns={"price": "Count"}).reset_index()
    fig = px.pie(house_cnt, values=house_cnt.Count, names=house_cnt.city, hole=0.5)
    fig.update_traces(marker={"line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


def create_bar_chart(col_name):
    fig = px.bar(house_price_df, x="city", y=col_name, color="city", barmode="group")
    fig.update_traces(marker={"line": {"width": 2, "color": "black"}})
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0})
    return fig


hist_drop = dcc.Dropdown(id="hist_column", options=[{"label": col, "value": col} for col in house_price_df.columns],
                         value="bedrooms",
                         clearable=False, className="text-dark p-2")
x_axis = dcc.Dropdown(id="x_axis", options=[{"label": col, "value": col} for col in house_price_df.columns],
                      value="sqft_living",
                      clearable=False, className="text-dark p-2")
y_axis = dcc.Dropdown(id="y_axis", options=[{"label": col, "value": col} for col in house_price_df.columns],
                      value="price",
                      clearable=False, className="text-dark p-2")
avg_drop = dcc.Dropdown(id="avg_drop", options=[{"label": col, "value": col} for col in house_price_df.columns],
                        value="price",
                        clearable=False, className="text-dark p-2")

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(__name__, external_stylesheets=external_css)

sidebar = html.Div([
    html.Br(),
    html.H3("Sidebar", className="text-center fw-bold fs-2"),
    html.Br(),
    html.H3("Histogram Dropdown", className="fs-4"),
    hist_drop,
    html.Br(),
    html.H3("Scatter Chart Dropdowns", className="fs-4"),
    x_axis, y_axis,
    html.Br(),
    html.H3("Bar Chart Dropdown", className="fs-4"),
    avg_drop
], className="col-2 bg-dark text-white", style={"height": "100vh"}
)

main_content = html.Div([
    html.Br(),
    html.H2("House Price Dataset Analysis", className="text-center fw-bold fs-1"),
    html.Div([
        dcc.Graph(id="histogram", className="col-5"),
        dcc.Graph(id="scatter_chart", className="col-5")
    ], className="row"),
    html.Div([
        dcc.Graph(id="bar_chart", className="col-5"),
        dcc.Graph(id="pie_chart", figure=create_pie_chart(), className="col-5"),
    ], className="row"),
], className="col", style={"height": "100vh", "background-color": "#e5ecf6"}
)

app.layout = html.Div([
    html.Div([sidebar, main_content], className="row")
], className="container-fluid", style={"height": "100vh"})


@callback(Output("histogram", "figure"), [Input("hist_column", "value"), ])
def update_histogram(hist_column):
    return create_histogram(hist_column)


@callback(Output("scatter_chart", "figure"), [Input("x_axis", "value"), Input("y_axis", "value"), ])
def update_scatter(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)


@callback(Output("bar_chart", "figure"), [Input("avg_drop", "value"), ])
def update_bar(avg_drop):
    return create_bar_chart(avg_drop)


if __name__ == "__main__":
    app.run(debug=True)
