# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:\python\dashboard_coursera\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(min_payload,max_payload)
#print(spacex_df.head())

opt = [{'label': 'All Sites', 'value': 'All Sites'}]
for i in spacex_df['Launch Site'].unique():
    opt.append({'label':i, 'value':i})


#print(opt)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection

                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=opt,
                                                value='All Sites',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),

                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10000, step=100,
                                                    marks = {0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'},
                                                    value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site-dropdown',component_property='value')]
)
def get_pie_chart(entered_site):
    if (entered_site == 'All Sites'):
        df  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, names = 'Launch Site',title = 'Total Success Launches By all sites')
    else:
        df  = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(df, names = 'class',title = 'Total Success Launches for site '+entered_site)
    return fig

@app.callback(
     Output(component_id='success-payload-scatter-chart', component_property='figure'),
     [Input(component_id='site-dropdown',component_property='value'),
      Input(component_id="payload-slider", component_property="value")]
)
def get_sccater(entered_site, paylod_slider):
    low, high = paylod_slider
    if (entered_site == 'All Sites'):
        #df  = spacex_df[spacex_df['class'] == 1]
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)']<high) 
        #df = spacex_df.loc[spacex_df['Payload Mass (kg)'] > low & spacex_df['Payload Mass (kg)']<high ]
        fig = px.scatter(spacex_df[mask], x = 'Payload Mass (kg)', y = 'class', color='Booster Version Category')
    else:
        df  = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)']<high) 
        fig = px.scatter(df[mask], x = 'Payload Mass (kg)', y = 'class', color='Booster Version Category')
    return fig


if __name__ == '__main__':
    app.run_server()
