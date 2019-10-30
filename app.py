# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import numpy as np
from pandas import  DataFrame,Series

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)


server = app.server
app.title = 'NYC Airbnb'

#free mapbox token
mapbox_access_token = 'pk.eyJ1IjoicHRyYnIiLCJhIjoiY2sxdndvbXV0MDgzeDNucDBsZWdyeHk2dyJ9.MOUSTruAnpBcM7v627LpBw'

# load csv file into dataframe
map_data_df = pd.read_csv('./data/dashFile_Airbnb_1000.csv')
map_data_df.drop(columns=["Unnamed: 0","id","calculated_host_listings_count"],inplace=True)
map_data_df['longitude']=round(map_data_df['longitude'],5)
map_data_df['latitude']=round(map_data_df['latitude'],5)

# declare the colors for the legend and the different data points on the map
colormap={1:'#ad4242',2:'#42ad59',3:'#425bad',4:'#a442ad',5:'#42ada4'}


#  layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color='#191A1A'),
    titlefont=dict(color='#191A1A', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=100
    ),
    hovermode='closest',
    plot_bgcolor='#f7f7f7',
    paper_bgcolor='#f7f7f7',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = 12
layout_table['margin-top'] = 20


# functions


def gen_map(aux_df,map_style):

    # groupby returns a dictionary mapping the values and the layout of the map 
    layout = go.Layout(
        clickmode='event+select',
        height=502,
        showlegend=True,
        autosize=True,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox= go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center= go.layout.mapbox.Center(lon=-73.91251,lat=40.7342),
            pitch=0,
            zoom=9.5,
            style=map_style,
        ),

        legend=dict(
            bgcolor="#f7f7f7",
            orientation="v",
            font=dict(color="black"),
            x=0,
            y=1,
        
          
        )
    ) 

    # split the data into different price_cats otherwise the legend doesn't get the difference between the datapoints
    # if nothing is selected an error occur'S on the page so use 'try' to just display an empty map  
    try:
        aux_df_cat1=aux_df.loc[aux_df['price_cat'].isin([1])]
        aux_df_cat2=aux_df.loc[aux_df['price_cat'].isin([2])]
        aux_df_cat3=aux_df.loc[aux_df['price_cat'].isin([3])]
        aux_df_cat4=aux_df.loc[aux_df['price_cat'].isin([4])]
        aux_df_cat5=aux_df.loc[aux_df['price_cat'].isin([5])]
    

     # if there are values for latitude and longitude return them
      # give back the dataFrames seperatly that plotly creates a legend entry for each set
        data= [
            {"type": "scattermapbox",
            
            "lat": list(aux_df_cat1['latitude']),
            "lon": list(aux_df_cat1['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Price: {}$ <br>Host ID: {}".format(i,j,k)]
                            for i,j,k in zip(aux_df_cat1['name'], aux_df_cat1['price'],aux_df_cat1['host_id'])],
            "mode": "markers",
            "name": '<50$',
            "marker": {
                "size": 6,
                "opacity": 1,
                "color":colormap[1]
                },
            },
            
            
            {"type": "scattermapbox",
            
            "lat": list(aux_df_cat2['latitude']),
            "lon": list(aux_df_cat2['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Price: {}$ <br>Host ID: {}".format(i,j,k)]
                            for i,j,k in zip(aux_df_cat2['name'], aux_df_cat2['price'],aux_df_cat2['host_id'])],
            "mode": "markers",
            "name": '50$-100$',
            "marker": {
                "size": 6,
                "opacity": 1,
                "color":colormap[2]
                },
            },


            {"type": "scattermapbox",
            
            "lat": list(aux_df_cat3['latitude']),
            "lon": list(aux_df_cat3['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Price: {}$ <br>Host ID: {}".format(i,j,k)]
                            for i,j,k in zip(aux_df_cat3['name'], aux_df_cat3['price'],aux_df_cat3['host_id'])],
            "mode": "markers",
            "name": '100$-200$',
            "marker": {
                "size": 6,
                "opacity": 1,
                "color":colormap[3]
                },
            },


            {"type": "scattermapbox",
            
            "lat": list(aux_df_cat4['latitude']),
            "lon": list(aux_df_cat4['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Price: {}$ <br>Host ID: {}".format(i,j,k)]
                            for i,j,k in zip(aux_df_cat4['name'], aux_df_cat4['price'],aux_df_cat4['host_id'])],
            "mode": "markers",
            "name": '200$-300$',
            "marker": {
                "size": 6,
                "opacity": 1,
                "color":colormap[4]
                },
            },   



            {"type": "scattermapbox",
            
            "lat": list(aux_df_cat5['latitude']),
            "lon": list(aux_df_cat5['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Price: {}$ <br>Host ID: {}".format(i,j,k)]
                            for i,j,k in zip(aux_df_cat5['name'], aux_df_cat5['price'],aux_df_cat5['host_id'])],
            "mode": "markers",
            "name": '>300$',
            "marker": {
                "size": 6,
                "opacity": 1,
                "color":colormap[5]
                },
            },    
         ]

        return{ 'data':data, 'layout':layout}


    # no values forlatitude and longitude -> return an empty map
    except:
        return{
            "data":[{
                 "type": "scattermapbox",
            }],
            "layout": layout
         }


# layout of the application:
app.layout = html.Div(
    html.Div([
         html.Div([
                html.Div([
                    html.H1(children='Airbnb New York City',
                            style={'textAlign': 'center','marginBottom':0},
                            ),
                        ],className='twelve columns'),
                       
                html.Div(children='''
                        This demonstrator uses a reduced Kaggle dataset.
                        ''',
                        className='twelve columns', style={'textAlign': 'center','marginTop':0,'marginBottom': 0}
                )
            ], className="row"
        ),


        # Selectors
        html.Div(
            [
                html.Div([
                    html.Div([
                    
                        html.H6('Choose Boroughs:',style={'marginTop':0,'marginBottom':0}),
                        dcc.Checklist(
                                id = 'boroughs',
                                options=[
                                    {'label': 'Manhattan', 'value': 'Manhattan'},
                                    {'label': 'Bronx', 'value': 'Bronx'},
                                    {'label': 'Queens', 'value': 'Queens'},
                                    {'label': 'Brooklyn', 'value': 'Brooklyn'},
                                    {'label': 'Staten Island', 'value': 'Staten Island'}
                                ],
                                value=['Manhattan','Bronx','Queens','Brooklyn','Staten Island'],
                                labelStyle={'display': 'inline-block'}
                            ),
                        ] ,className='pretty_container_boroughs')
                    ],className='six columns',style={'marginTop': 0,'marginBottom':0}
                ),


                # Price category slider
                html.Div([
                    html.Div([
                    
                        html.H6('Price Category:',style={'marginTop':11,'marginBottom':0}),
                            dcc.Slider(
                                        id='slider',
                                        min=1,
                                        max=5,
                                        step=None,
                                        marks={
                                            1: '<50$',
                                            2: '<100$',
                                            3: '<200$',
                                            4: '<300$',
                                            5: 'all',
                                        },
                                        value=3,        
                            ), 
                    ],className='pretty_container_slider')     
                ], className='six columns', style={'marginTop': 0,'margin-Bottom':0}
                ),
            ],className='row'
        ),



        # Map + table
        html.Div([
                 html.Div(
                     children=[
                         # Map-header
                         html.Div(
                             id ='map-header',
                             children=[
                                 html.Div([
                                    html.H6('Map:',style={'marginTop':0,'marginBottom':0}),
                                        dcc.RadioItems(
                                            id='mapbox-view-selector',
                                            options=[
                                                {"label": "light", "value": "light"},
                                                {"label": "satellite", "value": "satellite"},
                                                {"label": "basic", "value": "basic"},
                                            ],
                                            value= "light",labelStyle={'display': 'inline-block'}
                                        ),
                                
                                        dcc.Graph(
                                            id='Map-graph',
                                            figure={
                                                "layout":{
                                                    'paper_bgcolor':"#f7f7f7",
                                                    "plot_bgcolor":"#f7f7f7",
                                                }
                                            },
                                            config={'scrollZoom': True, "displayModeBar":True},
                                        ),
                                 ],className= "pretty_container")
                             ],
                         ),  
                     ], className = "six columns"
                 ),
                 html.Div([
                     html.Div([
                            dcc.Input(
                                    id='id_input',
                                    placeholder='Enter host_id...',
                                    type='number',
                                    value=''
                            ),

                            html.Button('Submit', id='button',style={'margin-left':10}),  

                            dt.DataTable(  
                                id='datatable',
                                columns=[{"name": i, "id": i} for i in map_data_df.columns],
                                fixed_rows={ 'headers': True, 'data': 0 },
                                style_table=layout_table,
                                style_cell={'width': '165px'},
                                # data is an array of dicts with the headline as keys and the specific rows as 
                                # values (len of the array is the number of rows in the table)
                                data=map_data_df.to_dict('records'),
                            ),   
                    ],className="pretty_container")
                ],className="six columns"),
                
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='bar-graph'    
                        )
                    ],className='pretty_container')
                ], className= 'twelve columns'
                ),
                
            ], className="row "),
            html.Div([
                html.Div([
                        dcc.Markdown('Developed by **Peter Bauer**'),
                ],className='twelve columns',style={'textAlign': 'center','marginTop': 15,'fontSize': 18})
            ],className='row')
    ]))



# Callbacks:

@app.callback(
    Output('Map-graph', 'figure'),
    [Input('datatable', 'data'),Input('mapbox-view-selector','value')])
    

# Here data = value(datatable) and map_style = value(mapbox_view_selector)    
def map_selection(data,map_style):

    aux_df = pd.DataFrame(data)
    return gen_map(aux_df,map_style)


@app.callback(
    Output('datatable','data'),
    [Input('slider','value'),
     Input('boroughs','value'),
     Input('button','n_clicks')],
    [State('id_input','value')]
)
# Here money = value(datatable) and borough = value(borough)
def data_table(money,boroughs,button,id_input):

    ctx = dash.callback_context
    
    if  ctx.triggered[0]['prop_id'] == "button.n_clicks":
        id_input =[id_input]
        return_data=  map_data_df.loc[map_data_df['host_id'].isin(id_input)].to_dict('records')
        return return_data

    else:
        money= np.arange(1,money+1,dtype=int)
        return_data= map_data_df.loc[map_data_df['price_cat'].isin(money)]
        return_data= return_data.loc[map_data_df['neighbourhood_group'].isin(boroughs)]
        return_data=return_data.to_dict('records')
        return return_data


@app.callback(
    Output('bar-graph','figure'),
    [Input('slider','value'),
    Input('boroughs','value')]
)
def bar_data(slider_value,boroughs_value):
    #crate an array out of the slider_value integer
    slider_value = np.arange(1,slider_value+1,dtype=int)

    # create a DataFrame
    bar_df = DataFrame(columns=boroughs_value, index=slider_value)

    # fill the DataFrame with values
    for elm in boroughs_value:
        
        tmp_data_out = map_data_df.loc[map_data_df['neighbourhood_group'].isin([elm])]
        
        for value in slider_value:
            
            tmp_data_in = tmp_data_out.loc[tmp_data_out['price_cat'].isin([value])]
            
            count=tmp_data_in['neighbourhood_group'].value_counts().tolist()
            if len(count)==0:
                count=0
            elif len(count)==1:
                count=count[0]
            else:
                print('Error to many values for coount in list')
            
            bar_df[elm][value]=count

    data=[]
    cat_list=['<50$','50$-100$','100$-200$','200$-300$','>300$']
    
    # create the dict out of the DataFrame and the cat list
    for counter,value in enumerate(slider_value):
        tmp_dict = {'x':bar_df.columns,'y':bar_df.loc[counter+1,:].tolist(),'type':'bar','name':cat_list[counter],'marker':{'color':colormap[counter+1]}} 
        data.append(tmp_dict)
   
    figure={

        'data':data,
        'layout':{
            'title':'Counter of rentals in your selected price category',
            'plot_bgcolor':'#f7f7f7',
            'paper_bgcolor':'#f7f7f7',         
        }

    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
    