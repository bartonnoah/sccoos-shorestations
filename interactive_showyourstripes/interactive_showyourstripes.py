import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import re

c_to_f = lambda c :(9/5)*c + 32

stations = {'Scripps Pier': {'savename': 'SIO',
                             'data': '../data/SIO_TEMP_20230501.xls',
                             'special_case': False}} #TODO Elena update w/ paths

def interactive_showyourstripes(nice_name, savename, data_filepath, special_case):
    """Generate an interactive #showyourstripes plot
    
    Args:
        nice_name: a string that will be displayed at the top of the generated plot
        save_name: a short name without spaces to save files with, such as SIO
        data_filepath: a filepath leading to an excel sheet, where
            -1st column is the year
            -2nd column is month
            -3rd column is day
            -6th column is sea surface temperature
            -47 row header
        special_case: switch to implement special cases (not yet implemented)
    """
    if special_case:
        raise NotImplementedError("This feature is not yet implemented.")
    
    print('Generating interactive #showyourstripes plot for '+nice_name)
    df=pd.read_excel(data_filepath,skiprows=47, header=None)
    df = df.rename(columns={0: 'year',
                            1: 'month',
                            2: 'day',
                            5: 'sst'})
    df = df[(df['year'] > 1916) & (df['year'] < 2023)] #exclude partial years 1916 & 2023
    df['date'] = pd.to_datetime(df[['year','month','day']])

    climatology = df.groupby(['year']).agg(['min','mean','max']).reset_index()

    #make hover text for chart
    text = []
    for i in range(len(climatology)):
        year = climatology.year[i]
        year_lo = climatology[('sst','min')][i]
        year_lo_f = c_to_f(year_lo)
        year_lo_day = datetime.strftime(df[(df.year == year) & (df.sst == year_lo)].date.iloc[0], '%b %-d')
        year_mean = climatology[('sst','mean')][i]
        year_mean_f = c_to_f(year_mean)
        year_hi = climatology[('sst','max')][i]
        year_hi_f = c_to_f(year_hi)
        year_hi_day = datetime.strftime(df[(df.year == year) & (df.sst == year_hi)].date.iloc[0], '%b %-d')
        #TODO bold year and/or bigger font
        #TODO make record high and low red and blue respectively
        text.append(f'<b>{year}</b><br><br>\
    <span style="color: #a50f15">Warmest: {year_hi:.1f}°C / {year_hi_f:.1f}°F on {year_hi_day}</span><br>\
    Average: {year_mean:.1f}°C / {year_mean_f:.1f}°F <br>\
    <span style="color: #08519c">Coldest: {year_lo:.1f}°C / {year_lo_f:.1f}°F on {year_lo_day}</span><br>')

    colors = ['#67000d', '#a50f15', '#cb181d', '#ef3b2c', '#fb6a4a', '#fc9272', '#fcbba1', '#fee0d2', '#FFFFFF',
            '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'][::-1]
    #I copied these red to blue but colors needs to be blue to red

    def get_color(sst):
        bin_step = (climatology[('sst','mean')].max() - climatology[('sst','mean')].min()) / len(colors)
        color_bins = np.arange(climatology[('sst','mean')].min(),climatology[('sst','mean')].max() + 0.001, bin_step) #stupid fix
        bin = np.min(np.argsort(np.abs(color_bins-sst))[0])
        if bin >= len(colors): return colors[len(colors) - 1] #TODO doublecheck logic
        else: return colors[bin]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for i, sst in enumerate(climatology[('sst','mean')]):
        i += 1917
        fig.add_shape( #make the stripes
            type="rect",
            x0=i,
            y0=0,
            x1=i+1,
            y1=30,
            layer="below",
            line=dict(color="rgba(0,0,0,0)"),
            fillcolor=get_color(sst),
            secondary_y=False)
    
    fig.add_trace(go.Scatter( #plot the annual mean
        x=df.groupby('year')['year'].first(),
        y=climatology[('sst','mean')],
        name='Yearly average',
        mode='lines',
        line=dict(
            width=5,
            color='white'),
        text = text,
        hoverinfo='text',
        showlegend=False),
        secondary_y=False)

    fig.add_trace(go.Scatter( #add an F axis
        x=df.groupby('year')['year'].first(),
        y=climatology[('sst','mean')].apply(c_to_f),
        name='Yearly average',
        mode='lines',
        line=dict(
            width=0,
            color='black'),
        hoverinfo='none',
        showlegend=False),
        secondary_y=True)

    fig.update_layout(title_text='Interannual Sea Surface Temperature Trends at '+nice_name,
        hovermode='x unified',
        plot_bgcolor='white')
    fig.update_xaxes(dict(title='Year', range=[climatology.year.min(), climatology.year.max()], showgrid=False))
    fig.update_yaxes(dict(title='Sea Surface Temperature (°C)', range=[climatology[('sst','mean')].min() - 0.5, climatology[('sst','mean')].max() + 0.5], showgrid=False, side='left'), secondary_y=False)
    fig.update_yaxes(dict(title='Sea Surface Temperature (°F)', range=[c_to_f(climatology[('sst','mean')].min() - 0.5), c_to_f(climatology[('sst','mean')].max() + 0.5)], showgrid=False, side='right'), secondary_y=True)
    pio.write_html(fig, './fig/interactive_showyourstripes_' + savename + '.html')

for key, item in stations.items():
    nice_name = key
    savename = item['savename']
    data_filepath = item['data']
    special_case = item['special_case']
    interactive_showyourstripes(nice_name, savename, data_filepath, special_case)