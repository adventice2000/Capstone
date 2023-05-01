# Import required libraries

import pandas as pd

import dash

import dash_html_components as html

import dash_core_components as dcc

from dash.dependencies import Input, Output

import plotly.express as px

# Read the airline data into pandas dataframe

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()

min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application

app = dash.Dash(__name__)

#group the launch site from the spacex dataframe

LaunchSiteGroup = spacex_df.groupby('Launch Site', as_index = False).first()

# Create an app layout

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',

style={'textAlign': 'center', 'color': '#503D36',

'font-size': 40}),

# TASK 1: Add a dropdown list to enable Launch Site selection

# The default select value is for ALL sites

# dcc.Dropdown(id='site-dropdown',...)

dcc.Dropdown(id='site-dropdown',

options=[

{'label': 'All Sites', 'value': 'ALL'},

{'label': LaunchSiteGroup['Launch Site'][0], 'value': LaunchSiteGroup['Launch Site'][0]},

{'label': LaunchSiteGroup['Launch Site'][1], 'value': LaunchSiteGroup['Launch Site'][1]},

{'label': LaunchSiteGroup['Launch Site'][2], 'value': LaunchSiteGroup['Launch Site'][2]},

{'label': LaunchSiteGroup['Launch Site'][3], 'value': LaunchSiteGroup['Launch Site'][3]}

],

value='ALL',

placeholder="Select a Launch Site here",

searchable=True

),

html.Br(),

# TASK 2: Add a pie chart to show the total successful launches count for all sites

# If a specific launch site was selected, show the Success vs. Failed counts for the site

html.Div(dcc.Graph(id='success-pie-chart')),

html.Br(),

html.P("Payload range (Kg):"),

# TASK 3: Add a slider to select payload range

#dcc.RangeSlider(id='payload-slider',...)

dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks={0: '0', 
                                                        2000: '2 000', 
                                                        4000: '4 000', 
                                                        6000: '6 000', 
                                                        8000: '8 000', 
                                                        10000: '10 000'},
                                                value = [min_payload, max_payload]
                                                ),

# TASK 4: Add a scatter chart to show the correlation between payload and launch success

html.Div(dcc.Graph(id='success-payload-scatter-chart')),

])

# TASK 2:

# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output

# Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),

Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):

    filtered_df=spacex_df[spacex_df['Launch Site']== entered_site]

    filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')

    if entered_site == 'ALL':

        fig = px.pie(spacex_df, values='class',

        names='Launch Site',

        title='Success Count for all launch sites')

        return fig

    else:

        # return the outcomes piechart for a selected site

        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total success launches for site {entered_site}")

        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output # iris is a pandas DataFrame

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),

[Input(component_id='site-dropdown', component_property='value'),

Input(component_id='payload-slider', component_property='value')]

)

def get_scatter(site, payload):
    low, high = payload[0], payload[1]
    
    if site == 'ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                        color='Booster Version Category',
                        title='Payload vs. Success for All Sites')
        return fig
    else:
        filtered_df=spacex_df[spacex_df['Launch Site']== site]
        secondFilter_df =filtered_df[filtered_df['Payload Mass (kg)'].between(low,high)]
        fig = px.scatter(secondFilter_df, x="Payload Mass (kg)", y="class", 
                        color='Booster Version Category',
                        title='Payload vs. Success for Site '+ site
                        )
        return fig
# Run the apps

if __name__ == '__main__':

    app.run_server()