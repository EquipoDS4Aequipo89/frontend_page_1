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

df = pd.read_csv('C:/Users/User/OneDrive/Documents/DS4A/project/data/BD_IGAC_20210715_CLEAN.csv')
app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Layout
app.layout = html.Div([

    html.H1("Taxonomic Classification of Soil Profiles", style={'text-align': 'center'}),

    dcc.Graph(id='pie', figure={}),
    html.Br(),
    dcc.Dropdown(id = 'order_boxplot',
                 options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Inceptisol', 'value': 'Inceptisol'},
                        {'label': 'Andisol', 'value': 'Andisol'},
                        {'label': 'Entisol', 'value': 'Entisol'},
                        {'label': 'Molisol', 'value': 'Molisol'},
                        {'label': 'Histosol', 'value': 'Histosol'},
                    ],
                    value='All'
                    ),  
    html.Br(),
    dcc.Graph(id='funnel', figure={}),
    html.Br(),        
    dcc.RadioItems(id = 'var_boxplot',
                 options=[
                        {'label': 'Thickness', 'value': 'SUMA ESPESOR'},
                        {'label': 'Altitude', 'value': 'ALTITUD'},
                    ],
                    value='SUMA ESPESOR'
                    ),     
    dcc.Graph(id='boxplot', figure={}),    
    html.Br(),
    dcc.Graph(id='density_map', figure={}),
    html.Br(),
    dcc.RadioItems(id = 'var_heatmap',
                 options=[
                        {'label': 'Temperature', 'value': 'REGIMEN_TEMPERATURA'},
                        {'label': 'Moisture', 'value': 'REGIMEN_HUMEDAD'},
                    ],
                    value='REGIMEN_TEMPERATURA'
                    ),  
    dcc.Graph(id='heatmap', figure={})      
])

# ------------------------------------------------------------------------------
# Callbacks
@app.callback(
    [Output(component_id='pie', component_property='figure'),
     Output(component_id='funnel', component_property='figure'),
     Output(component_id='boxplot', component_property='figure'),
     Output(component_id='density_map', component_property='figure'),
     Output(component_id='heatmap', component_property='figure'),      
     ],
    [Input(component_id='order_boxplot', component_property='value'),
     Input(component_id='var_boxplot', component_property='value'),
     Input(component_id='var_heatmap', component_property='value'),
     ]
    )

def update_output(order,var_boxplot,var_heatmap):
    
    # Pie chart
    count_orders = df.value_counts('ORDEN').reset_index()
    count_orders.columns = ['Order','Profiles']
    count_orders
    n = len(df)
    
    pie_plot = px.pie(count_orders, values = 'Profiles', names = 'Order', hole = .4)
    pie_plot.update_layout(annotations=[dict(text=n, x=0.5, y=0.5, font_size=20, showarrow=False)])
    
    # Filter data
    if order == 'All':
        df_fig = df.copy()
    else:
        df_fig = df[df['ORDEN']==order]
        
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
    
    return pie_plot, funnel, boxplot, plot_map, heatplot

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)