# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_csv('data/BD_IGAC_20210715_CLEAN.csv')
app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Layout
app.layout = html.Div([

    html.Div(className = 'header',
    children = [html.H1(children = "Taxonomic Classification of Soil Profiles", 
    className = 'title')]
            ),
    
    
    html.Div(children=[
        html.Div(className='column',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
    html.H2('About', style = {'text-align': 'center'}),
    html.P('The Agustin Codazzi Geographical Institute (IGAC, for its acronym in Spanish), produces and coordinates geographical, cadastral and agrological information of Colombia, and carries out the inventory of the soil characteristics. The study of the soil characteristics involves the process of taxonomic order based on chemical and physical properties. Assertive soil classification allows for better recommendations on soil uses, analyze the phenomena that occur on it, and prevent or mitigate erosive effects that can impact on soil productivity and lead to other environmental problems. This tool allows to explore some of the characteristics of the soil profiles collected in the Cundiboyacense region and to classify the soil taxonomy automatically, using parameters collected in the field.',
           style = {'text-align': 'justify'}),
    html.Br(), 
    dcc.Graph(id='density_map', figure={}),
                                  ]),
    html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  
    html.H2('Taxonomic Order, Subgroup, and Classification', style = {'text-align': 'center'}),
    html.Div(
        children = [
            html.P('Taxonomic order', style = {'text-align': 'center'}),
            dcc.Graph(id='pie', figure={}),
            html.P('Subgroups and taxonomic classification', style = {'text-align': 'center'}),
            dcc.Graph(id='sun', figure={}),
        ],style={'columnCount': 2}),
    html.H2('Soil characteristics', style = {'text-align': 'center'}),
    html.P('Select the variable:', style = {'text-align': 'left'}),
    dcc.RadioItems(id = 'var_boxplot',
                                                 options=[
                        {'label': 'Thickness', 'value': 'SUMA ESPESOR'},
                        {'label': 'Altitude', 'value': 'ALTITUD'},
                        {'label': 'Horizons', 'value': 'N_HORIZONS'},
                        ],
                    value='SUMA ESPESOR'),
    
    
    html.Div(
        children = [
            dcc.Graph(id='plot3d', figure={}),
            dcc.Graph(id='boxplot', figure={}),
        ],style={'columnCount': 2}),
    
                                  ])
                     ])
        ])

])

# ------------------------------------------------------------------------------
# Callbacks
@app.callback(
    [Output(component_id='pie', component_property='figure'),
     Output(component_id='density_map', component_property='figure'),  
     Output(component_id='sun', component_property='figure'),
     Output(component_id='plot3d', component_property='figure'),
     Output(component_id='boxplot', component_property='figure')
     ],
    [Input(component_id='var_boxplot', component_property='value')]
    )

def update_output(var):
    
    # Pie chart
    count_orders = df['ORDEN'].value_counts().reset_index()
    count_orders.columns = ['Order','Profiles']
    count_orders
    n = len(df)
    
    pie_plot = px.pie(count_orders, values = 'Profiles', names = 'Order', hole = .4,
                      color_discrete_sequence=px.colors.qualitative.Prism)
    pie_plot.update_layout(annotations=[dict(text=n, x=0.5, y=0.5, font_size=20, showarrow=False)])
        
    pie_plot.update_layout(
        margin=dict(l=50,r=50,b=50,t=50,pad=4))
    # Density map
    plot_map = px.density_mapbox(df, lat='LATITUD', lon='LONGITUD', radius=2,
                        center=dict(lat=4.8, lon=-74), zoom=8,
                        mapbox_style="open-street-map",
                        color_continuous_scale=px.colors.sequential.Viridis)
    
    plot_map.update_layout(
        width=750,
        height=750,
        margin=dict(l=50,r=50,b=100,t=10,pad=4))
  
    # Sun plot
    classes = df.groupby(['SUBGRUPO','CLASIFICACION_TAXONOMICA']).size().to_frame()
    classes.columns = ['COUNT']
    classes = classes.reset_index()
    
    sun_plot = px.sunburst(classes,
                           path=['SUBGRUPO','CLASIFICACION_TAXONOMICA'],
                           values='COUNT')
    
    sun_plot.update_layout(
        margin=dict(l=50,r=50,b=50,t=50,pad=4))
    # 3D plot
    plot_3d = px.scatter_3d(df, x = 'LONGITUD',y = 'LATITUD',z = var,
                            color = var)
    
    # Boxplot
    boxplot = px.box(df,x='ORDEN', y=var, color = 'ORDEN',
                     category_orders = {'ORDEN':count_orders['Order']},
                     color_discrete_sequence=px.colors.qualitative.Prism,
                     )
    
    return pie_plot, plot_map, sun_plot, plot_3d, boxplot

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)