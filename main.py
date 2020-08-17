# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from dateutil.parser import parse
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
time_series_covid19_confirmed_global= 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
time_series_covid19_confirmed_US = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
time_series_covid19_deaths_US = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
time_series_covid19_deaths_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
time_series_covid19_recovered_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
#Create DF from csv files
confirmed_US = pd.read_csv(time_series_covid19_confirmed_US)
confirmed_global = pd.read_csv(time_series_covid19_confirmed_global)
deaths_US = pd.read_csv(time_series_covid19_deaths_US)
deaths_global = pd.read_csv(time_series_covid19_deaths_global)
recovered_global = pd.read_csv(time_series_covid19_recovered_global)

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def find_indexes_columns (table_df):
  index_cols = []
  for columns_name in table_df.columns.to_list():
    if not is_date(columns_name):
      index_cols.append(columns_name)
  return index_cols
def load_df (df_name):
    returned_df = pd.DataFrame()
    if df_name == "US_Confirmed":
        returned_df = pd.melt(confirmed_US,id_vars=find_indexes_columns(confirmed_US), var_name = "Date", value_name="Confirmed_cases")
    elif df_name =="Global_Confirmed":
        returned_df = pd.melt(confirmed_global,id_vars=find_indexes_columns(confirmed_global), var_name = "Date", value_name="Confirmed_cases")
    return returned_df
    #deaths_US_melted = pd.melt(deaths_US,id_vars=find_indexes_columns(deaths_US), var_name="Date", value_name="number_of_deaths")
    #deaths_global_melted = pd.melt(deaths_global,id_vars=find_indexes_columns(deaths_global), var_name="Date", value_name="number_of_deaths")
    #recovered_global = pd.melt(recovered_global, id_vars=find_indexes_columns(recovered_global), var_name="Date", value_name="number_of_deaths")




#fig = px.bar(confirmed_US_melted, x="Date", y="Confirmed_cases", color="Province_State")

app.layout = html.Div(children=[
    html.H1(children='''
        Coronavirus Disease (COVID-19) Dashboard
    '''),
    html.Div(id="Confirmed_cases_updated"),
    dcc.Dropdown(
        id = 'data_scale',
        options = [
            {"label":"Global", "value":"Global"},
            {"label":"US", "value":"US"}
        ],
        value = "US"
    ),
    html.Div(id="Selected_scale"),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
])

@app.callback(
    dash.dependencies.Output("Selected_scale", "children"),
    [dash.dependencies.Input("data_scale", "value")]
)
def data_scale_set(data_scale):
    df_table = pd.DataFrame()
    if data_scale == "US":
        df_table = load_df("US_Confirmed")
    elif data_scale == "Global":
        df_table = load_df("Global_Confirmed")
    return dash_table.DataTable(
        id="data_table",
        columns = [{"name":i, "id":i} for i in df_table.columns],
        data = df_table.head().to_dict("record")
    )

@app.callback(
    dash.dependencies.Output("Confirmed_cases_updated", "children"),
    [dash.dependencies.Input("interval-component","n_intervals")]
)
def global_confirmed_cases(n):
    df = load_df("Global_Confirmed")
    max_date = max(df["Date"])
    Total_cases = df[df["Date"]== max_date].Confirmed_cases.sum()
    return Total_cases

if __name__ == '__main__':
    app.run_server(debug=True)