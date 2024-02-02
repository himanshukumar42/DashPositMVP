import json

from dash import html, dcc, Dash, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import flask
import requests

house_price_df = pd.read_csv('data.csv')

X = house_price_df[['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition']]
y = house_price_df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


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
app = Dash(__name__, external_stylesheets=external_css, suppress_callback_exceptions=True)
API_KEY = "gad7P8EaZ7v19XXVGLgwYHcWtJ4gyrwn"

sidebar = html.Div([
    html.Br(),
    html.H3("House Price", className="text-center fw-bold fs-2"),
    html.Br(),
    html.H3("Histogram", className="fs-4"),
    hist_drop,
    html.Br(),
    html.H3("Scatter Chart", className="fs-4"),
    x_axis, y_axis,
    html.Br(),
    html.H3("Bar Chart", className="fs-4"),
    avg_drop
], className="col-2 bg-primary text-white", style={"height": "100vh"}
)

main_content = html.Div([
    html.Br(),
    html.H2("House Price Dataset Analysis", className="text-center fw-bold fs-1"),
    dcc.Tabs(id="tabs", value="charts", children=[
        dcc.Tab(children=[], label="Charts", value="charts", className="bg-primary text-white w-25"),
        dcc.Tab(children=[], label="Prediction", value="prediction", className="bg-primary text-white w-25 mx-auto"),
    ], className="p-4 m-3"),
    html.Div(id="tabs-content"),
    dbc.Modal(
        [
            dbc.ModalHeader("Authorization Error"),
            dbc.ModalBody("You are not authorized to view this content."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-button", className="ml-auto")
            ),
        ],
        id="modal",
        centered=True,
        size="sm",
    ),
    html.Br(),
], className="col", style={"height": "100vh", "background-color": "white"}
)

app.layout = html.Div([
    html.Div([sidebar, main_content], className="row")
], className="container-fluid", style={"height": "100vh"})

charts_tab_layout = html.Div([
            html.Br(),
            html.Div([
                dcc.Graph(id="histogram", className="col-5"),
                dcc.Graph(id="scatter_chart", className="col-5")
            ], className="row"),
            html.Div([
                dcc.Graph(id="bar_chart", className="col-5"),
                dcc.Graph(id="pie_chart", figure=create_pie_chart(), className="col-5"),
            ], className="row"),
    ])
prediction_tab_layout = html.Div([
    html.Br(),
    html.Label('Number of Bedrooms', style={'margin-bottom': '10px'}),
    dcc.Input(id='bedrooms-input', type='number', value=3, style={'margin-bottom': '20px'}),

    html.Label('Number of Bathrooms', style={'margin-bottom': '10px'}),
    dcc.Input(id='bathrooms-input', type='number', value=2, style={'margin-bottom': '20px'}),

    html.Label('Square Footage (Living)', style={'margin-bottom': '10px'}),
    dcc.Input(id='sqft-living-input', type='number', value=1500, style={'margin-bottom': '20px'}),

    html.Label('Square Footage (Lot)', style={'margin-bottom': '10px'}),
    dcc.Input(id='sqft-lot-input', type='number', value=4000, style={'margin-bottom': '20px'}),

    html.Label('Number of Floors', style={'margin-bottom': '10px'}),
    dcc.Input(id='floors-input', type='number', value=1, style={'margin-bottom': '20px'}),

    html.Label('Waterfront (0 for No, 1 for Yes)', style={'margin-bottom': '10px'}),
    dcc.Input(id='waterfront-input', type='number', value=0, style={'margin-bottom': '20px'}),

    html.Label('View (0 for No, 1 for Yes)', style={'margin-bottom': '10px'}),
    dcc.Input(id='view-input', type='number', value=0, style={'margin-bottom': '20px'}),

    html.Label('Condition', style={'margin-bottom': '10px'}),
    dcc.Input(id='condition-input', type='number', value=3, style={'margin-bottom': '20px'}),

    html.Br(),

    html.H1(id='predicted-price-output')
], style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'}),


@callback(Output("histogram", "figure"), [Input("hist_column", "value"), ])
def update_histogram(hist_column):
    return create_histogram(hist_column)


@callback(Output("scatter_chart", "figure"), [Input("x_axis", "value"), Input("y_axis", "value"), ])
def update_scatter(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)


@callback(Output("bar_chart", "figure"), [Input("avg_drop", "value"), ])
def update_bar(avg_drop):
    return create_bar_chart(avg_drop)


@callback(
    Output('predicted-price-output', 'children'),
    [Input('bedrooms-input', 'value'),
     Input('bathrooms-input', 'value'),
     Input('sqft-living-input', 'value'),
     Input('sqft-lot-input', 'value'),
     Input('floors-input', 'value'),
     Input('waterfront-input', 'value'),
     Input('view-input', 'value'),
     Input('condition-input', 'value'), ]
)
def update_predicted_price(bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition):
    predicted_price = model.predict([[bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition]])[0]
    return f'Predicted Price: ${predicted_price:.2f}'


@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(selected_tab):
    user_metadata = get_credentials(flask.request)
    username = user_metadata.get("user")
    if username is None:
        return {"message": "Not Accessible"}
    user_details = get_user_details(username)
    user_role = user_details["results"][0]["user_role"]
    if selected_tab == 'charts' and user_role in ["viewer", "administrator", "publisher"]:
        return charts_tab_layout

    elif selected_tab == 'prediction' and user_role == "administrator":
        return prediction_tab_layout

    else:
        return dbc.Modal("You are not authorized to view this content.", id="modal", is_open=True)


def get_user_details(username):
    url = f"http://52.66.134.63/__api__/v1/users?prefix={username}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': API_KEY,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)


def get_credentials(req):
    credential_header = req.headers.get("RStudio-Connect-Credentials")
    if not credential_header:
        return {}
    return json.loads(credential_header)


if __name__ == "__main__":
    app.run(debug=True)
