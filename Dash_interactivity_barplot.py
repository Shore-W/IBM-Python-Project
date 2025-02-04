import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children = [ html.H1("Total Number of Flights to the Destination states split by reporting airline", style = {"textAlgin": "center", "color": "#503D36", "font-size": 40}),
                                    html.Div(["Input Year:  ", dcc.Input(id = "input-year", value = "2010", type = "number", style = {"height": "50px", "font-size":35}),],
                                    style = {"font-size": 40}),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id = "bar-plot")),
                                    ])

@app.callback(Output(component_id = "bar-plot", component_property = "figure"), Input(component_id = "input-year", component_property = "value"))

#adding computation to callback function to return a graph
def get_graph(entered_year):
    df = airline_data[airline_data["Year"] == int(entered_year)]

    state_data = df.groupby("DestState")["Flights"].sum().reset_index()

    #create the figure
    fig = px.bar(state_data, x = "DestState", y = "Flights", title = "Total Number of Flights to the destination state split by reporting airline") 
    #go.Figure(data = go.Bar(x=state_data["DestState"], y = state_data["Flights"], mode = "bar", marker = dict(color="blue")))

    fig.update_layout(title = "Flights to Destination State", xaxis_title = "DestState", yaxis_title = "Flights")
    
    return fig

if __name__ == "__main__":
    app.run_server()