#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:49:55 2019

@author: adelhassen
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
NBA ='https://s3.amazonaws.com/programmingforanalytics/NBA_data.xlsx'
nba=pd.read_excel(NBA)

total = nba['Points_per_game'] + nba['Rebounds_per_game'] + nba['Assists_per_game']
nba['total'] = total

numericalval = nba.columns.values[4:]
options_dropdown = [{'label':x, 'value':x} for x in numericalval]

app = dash.Dash(__name__)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

numerical_features = ['total','Points_per_game','Rebounds_per_game','Assists_per_game']

dd_x_var = dcc.Dropdown(
    id = 'x-var',
    options= [
        {'label': 'Total', 'value': 'total'},
        {'label': 'Points Per Game', 'value': 'Points_per_game'},
        {'label': 'Rebounds Per Game', 'value': 'Rebounds_per_game'},
        {'label': 'Assists Per Game', 'value': 'Assists_per_game'}],
    value='total'
)  

div_x_var = html.Div(
        children=[html.H4('Variable for x axis: '), dd_x_var],
        className="six columns"
        )

trace = go.Scatter(
        x = nba['Age'],
        y = nba['Salary'],
         mode='markers'
         )

layout = go.Layout(
        title = 'Relationship Between Age and Salary of NBA Player',
        xaxis = dict(title='Age'),
        yaxis = dict(title='Salary')
        )

figure = go.Figure(
        data = [trace],
        layout = layout
        )

trace = go.Histogram(
        x = nba['Salary'], nbinsx = 10
        )

layout = go.Layout(
        title = 'Player Salary',
        xaxis = dict(title='Salary'),
        yaxis = dict(title='Count')
        )

figure2 = go.Figure(
        data = [trace],
        layout = layout
        )


app.layout = html.Div(children = [
        html.H1('NBA player match infomation'),
        html.H2('Analysis'),
        html.P("Nowadays, the NBA has become more and more popular around the world, what followed is the salary of NBA stars rising up rapidly. The NBA restricts team spending on salaries unsing a salary cap, meaning all teams in this league use nearly the same amount of money to build a team which could win the final championship. Based on the context, how to spend money sensibly and reasonably is the most important thing in every team managers' and coaches' mind."),
        html.P("To fix the problem we mentioned above, our group decided to help team managers and coaches to analyze the NBA players' performance and their salaries from 5 aspects: player efficiency, Scatter Plot: Age and Salary, Histogram for Salary, Filterable Table, and Compare players' performance by statistics. Usingour graphs and plots, we could decide which player is the most efficient and who's the most cost-effective star for the given season."),
        html.H3('1. Player Efficiency'),
        html.P("This bar chart compares players performance and efficieny my measuring how much time it takes a player to reach a certain number of points, rebounds, and assists"),
        html.P("Note: A darker color means less minutes played per game, suggesting higher efficiency if two players averaged the same number of points."),
        html.P("Note: Total is the sum of points, rebounds, and assists."),
        html.Div(
                children=[div_x_var],
                className="row"
                ), 
        dcc.Graph(id='bar'),
        html.H3('2. Scatter Plot: Age and Salary'),
        html.P('We developed an application to analyze NBA players basic information. For example, we generated a scatter plot coparing age and salary'), 
        dcc.Graph(id='my-scatter', figure=figure),
        html.H3('3. Histogram for Salary'),
        html.P('This histogram shows the distribution of player salary.'),
        dcc.Graph(id='histogram', figure = figure2),
        html.H3('4. Filterable Table'),
        html.P("This table is filterable by typing in the second row 'filter data' respectively"), 
        html.P("Instrutions to use the interactive table:"),
        html.P("1) Input the data in the column you want to filter, and then press enter; "),
        html.P("2) If you want to undo the filter, just delete the data you type, and then press enter;"),
        html.P("3) You can sort each column;"),
        html.P("4) You can delete columns and rows;"),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in nba.columns
        ],
        data=nba.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 20,
    ),   
        html.H3("5. Compare players' performance by statistics"),  
        html.P("This part helps you compare all NBA players from different aspects(wins, scores, rebounds...),You can select any two statistics and all these 20 NBA player's certain performance will come out. What's more, once we could plot 2 dimensions to compare, which may help a coach make their desicion quickly."), 
            html.Div([

        html.Div([
            dcc.Dropdown(
                id='xcol',
                options=options_dropdown,
                value='Wins'
            )
        ],
        style={'width': '15%'}),

        html.Div([
            dcc.Dropdown(
                id='ycol',
                options=options_dropdown,
                value='Losses'
            )
        ],style={'width': '15%'})
    ]),

    dcc.Graph(id='graph'),
    
    html.H3("Short conclusion"),
    html.P("1. Based on all this information, we know that James Harden is the most efficient players in this league; he ranks No.1 in both scoring and assisting."),    
    html.P("2. Giannis Antetokounmpo is the the most valuable player(stats are on par with James Harden's but Giannis won more games than Harden)."),
    html.P("3. Devin Booker is the most cost-efficienct player, because his stats are amongst the top 10 players but his salary is lower than everyone except Donovan Mitchell(because he is still in rookie contact)."),
])

@app.callback(
        Output(component_id='bar', component_property='figure'),
        [Input(component_id='x-var', component_property='value')])

def barplot(x_col):
    figure = px.bar(nba, x = nba[x_col], y = "Name", orientation = 'h', color = 'Minutes_played_per_game', hover_name = 'Name', title = "Player Efficiency" )
    
    return figure
  
def update_graph(xaxis, yaxis):  

    return {
        'data': [dict(
            x=nba[xaxis],
            y=nba[yaxis],
            mode='markers',
            marker={
                'size': 12,
                'opacity': 0.3,
                'line': {'width': 0.3, 'color': 'black'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis
            },
            yaxis={
                'title': yaxis
            },
            margin={'l': 50, 'b': 50, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
        
@app.callback(
    Output('graph', 'figure'),
    [Input('xcol', 'value'),
     Input('ycol', 'value')
     ])
def update_graph1(xaxis, yaxis):
    

    return {
        'data': [dict(
            x=nba[xaxis],
            y=nba[yaxis],
            mode='markers',
            marker={
                'size': 12,
                'opacity': 0.3,
                'line': {'width': 0.3, 'color': 'black'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis
            },
            yaxis={
                'title': yaxis
            },
            margin={'l': 50, 'b': 50, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }        
    
if __name__ == '__main__':
    app.run_server(debug=False)