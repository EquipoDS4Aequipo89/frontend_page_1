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
                                  html.H2('Choose a Taxonomic Order', style = {'text-align': 'left'}),
                                  dcc.Dropdown(id = 'order_boxplot',
                                               options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Inceptisol', 'value': 'Inceptisol'},
                        {'label': 'Andisol', 'value': 'Andisol'},
                        {'label': 'Entisol', 'value': 'Entisol'},
                        {'label': 'Molisol', 'value': 'Molisol'},
                        {'label': 'Histosol', 'value': 'Histosol'}],
                    value='All'),
                                      
                                html.P('Subgroups and taxonomic classification', style = {'text-align': 'center'}),
                                dcc.Graph(id='sun', figure={}),
                                html.Br(),
                                html.Div(    
                                  children =[
                                      html.Div(className='one columns',
                                               children = [html.Br()]),
                                      html.Div(className='four columns',
                                          children = [
                                      html.P('Select the variable:', style = {'text-align': 'left'}),
                                dcc.Dropdown(id = 'var_barplot',
                                               options=[
                        {'label': 'Forma Terreno', 'value': 'FORMA_TERRENO'},
                        {'label': 'Clase Pendiente', 'value': 'CLASE_PENDIENTE'},
                        {'label': 'Drenaje Natural', 'value': 'DRENAJE_NATURAL'},
                        {'label': 'Familia Textural', 'value': 'FAMILIA_TEXTURAL'},
                        {'label': 'Epipedon', 'value': 'EPIPEDON'},
                        {'label': 'Clima Ambiental', 'value': 'CLIMA_AMBIENTAL'},
                        ],
                    value='FORMA_TERRENO')]),
                                      html.Div(className='four columns',
                                          children = [
                                html.P('Categories:', style = {'text-align': 'left'}),
                                dcc.Slider(id = 'num_bars',min=1,max=15,step=1,value=5)
                                ])
                                ],style={'columnCount': 1}),
                                dcc.Graph(id='bar', figure={}),
                              ]),
                     
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children =[
                                  html.Br(),
                                  html.Br(),
                                  html.Br(),
                              html.Div(
                              children=[
                                  html.P('Taxonomic Order Profiles in each Horizon', style = {'text-align': 'center'}),
                                  dcc.Graph(id='funnel', figure={}),
                                  html.Br(),        
                                  dcc.RadioItems(id = 'var_boxplot',
                                                 options=[
                        {'label': 'Thickness', 'value': 'SUMA ESPESOR'},
                        {'label': 'Altitude', 'value': 'ALTITUD'},],
                    value='SUMA ESPESOR'),     
                    dcc.Graph(id='boxplot', figure={}),    
                    html.Br(),
                    html.P('Location of Samples by Taxonomic Order', style = {'text-align': 'center'}),
                    dcc.Graph(id='density_map', figure={}),
                    html.Br(),
                    dcc.RadioItems(id = 'var_heatmap',
                                   options=[
                        {'label': 'Temperature', 'value': 'REGIMEN_TEMPERATURA'},
                        {'label': 'Moisture', 'value': 'REGIMEN_HUMEDAD'},
                    ],
                    value='REGIMEN_TEMPERATURA'
                    ),  
                    dcc.Graph(id='heatmap', figure={}),
                    ],style={'columnCount': 2})])])
                                  ])
                                  ])

# ------------------------------------------------------------------------------
# Callbacks
@app.callback(
    [Output(component_id='sun', component_property='figure'),
     Output(component_id='bar', component_property='figure'),
     Output(component_id='funnel', component_property='figure'),
     Output(component_id='boxplot', component_property='figure'),
     Output(component_id='density_map', component_property='figure'),
     Output(component_id='heatmap', component_property='figure'),      
     ],
    [Input(component_id='order_boxplot', component_property='value'),
     Input(component_id='var_boxplot', component_property='value'),
     Input(component_id='var_heatmap', component_property='value'),
     Input(component_id='var_barplot', component_property='value'),
     Input(component_id='num_bars', component_property='value')
     ]
    )

def update_output(order,var_boxplot,var_heatmap,var_barplot,num_bars):

    # Filter data
    if order == 'All':
        df_fig = df.copy()
    else:
        df_fig = df[df['ORDEN']==order]

    
    # Sun plot
    classes = df_fig.groupby(['SUBGRUPO','CLASIFICACION_TAXONOMICA']).size().to_frame()
    classes.columns = ['COUNT']
    classes = classes.reset_index()
    
    sun_plot = px.sunburst(classes,
                           path=['SUBGRUPO','CLASIFICACION_TAXONOMICA'],
                           values='COUNT')
    
    sun_plot.update_layout(
        margin=dict(l=50,r=50,b=50,t=50,pad=4))
    
    # Bar chart
    frecuencies = df_fig[var_barplot].value_counts().reset_index()
    frecuencies.columns = [var_barplot,'Profiles']
    barplot = px.bar(frecuencies[:num_bars], x = var_barplot, y = 'Profiles')

    # Funnel plot
    count_horizons = df_fig[['FLAG_H1',
                             'FLAG_H2',
                             'FLAG_H3',
                             'FLAG_H4',
                             'FLAG_H5',
                             'FLAG_H6']].sum().to_frame()
    count_horizons.index = range(1,7)
    count_horizons.columns = ['Profiles'] 
    funnel = px.funnel(count_horizons)
    funnel.update_layout(yaxis_title="Horizons",
                  legend_title=None)
    
    # Boxplot
    boxplot = px.box(df_fig,x='N_HORIZONS', y=var_boxplot)
    
    # Density map
    plot_map = px.density_mapbox(df_fig, lat='LATITUD', lon='LONGITUD', radius=2,
                        center=dict(lat=4.8, lon=-74), zoom=7,
                        mapbox_style="carto-darkmatter")
    
    # Heat map
    heat = pd.pivot_table(data = df_fig,
               index = 'N_HORIZONS',
               columns = var_heatmap,
               values = 'CODIGO',
               aggfunc = 'count',
               fill_value = 0)
    heatplot = px.imshow(heat)
    
    return sun_plot, barplot, funnel, boxplot, plot_map, heatplot

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)