# -*- coding: utf-8 -*-
"""
Dash application (Dash [Python] <- Plotly <- React.js <- D3.js)
Author: Akshay Balsubramani
"""

import base64, io, os, time, json
import numpy as np, scipy as sp, pandas as pd, dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc, dash_html_components as html
import app_config



# ================================================================
# =================== Component styles/layouts ===================
# ================================================================

legend_font_macro = {
    'family': 'sans-serif', 
    'size': app_config.params['legend_font_size'], 
    'color': app_config.params['legend_font_color'] 
}

colorbar_font_macro = {
    'family': 'sans-serif', 
    'size': 8, 
    'color': app_config.params['legend_font_color'] 
}

hm_font_macro = {
    'family': 'sans-serif', 
    'size': 8, 
    'color': app_config.params['legend_font_color'] 
}

style_unselected = {  'marker': {  'size': 2.5,  'opacity': 1.0 } }

style_selected = { 'marker': { 'size': 6.0, 'opacity': 1.0 } }

style_text_box = {
    'textAlign': 'center', 
    'width': '100%', 
    'border': 'thin lightgrey solid', 
    'color': app_config.params['font_color']
}

style_legend = {
    'font': legend_font_macro, 
    'padding': 0, 
    'margin': 0, 
    'border': 'thin lightgrey solid', 
    'traceorder': 'normal', 
    'orientation': 'h'
}



# ===========================================================
# =================== Create main app div ===================
# ===========================================================

"""
Main layout.
"""

def create_div_mainapp():
    return html.Div(
        className="container", 
        children=[
            html.Div(
                className='row', 
                children=[
                    html.H1(
                        id='title', 
                        children=app_config.params['title'], 
                        style={ 'textAlign': 'center', 'width': '100%', 'color': app_config.params['font_color'] }
                    )]
            ), 
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="four columns",
                        children=[
                            html.Div(
                                className="row",
                                children=[
                                    dcc.RadioItems(
                                        id='select-statistic', 
                                        options=[{'label': v, 'value': v} for v in 
                                                 ['z', 't', 'LR', 'MMD', 'kNN', 'Loss conv.'] ], 
                                        style=legend_font_macro, 
                                        labelStyle={
                                            'display': 'inline-block', 
                                            'margin-right': '5px'
                                        }, 
                                        value='z'
                                    ), 
                                    dcc.RadioItems(
                                        id='select-lambda-dist', 
                                        options=[{'label': v, 'value': v} for v in 
                                                 ['Robbins', 'Constant'] ], 
                                        style=legend_font_macro, 
                                        labelStyle={
                                            'display': 'inline-block', 
                                            'margin-right': '5px'
                                        }, 
                                        value='Robbins'
                                    )
                                ]
                            )], 
                        style=style_text_box
                    ), 
                    html.Div(
                        className="eight columns",
                        children=[
                            dcc.Graph(
                                id='main-pval',
                                config={ 'displaylogo': False, 'displayModeBar': True }, 
                                style={ 'height': '40vh', 'padding-bottom': '10px' }
                            )]
                    )]
            ), 
            html.Div([ html.Pre(id='test-select-data', style={ 'color': app_config.params['font_color'], 'overflowX': 'scroll' } ) ]),     # For testing purposes only!
            html.Div(
                className='row', 
                children=[ 
                    dcc.Markdown(
                        """Queries? Requests? Contact [Akshay Balsubramani](abalsubr@stanford.edu). """ 
                        + """Source [repository](https://github.com/b-akshay/aknn-classifier)."""
                        )], 
                style={
                    'textAlign': 'center', 
                    'color': app_config.params['font_color'], 
                    'padding-bottom': '10px'
                }
            ), 
            dcc.Store(
                id='stored-stats', 
                data=[]
            )
        ],
        style={ 
            'width': '100vw', 
            'max-width': 'none'
        }
    )



# =========================================================
# ================== Initialize Dash app ==================
# =========================================================

app = dash.Dash(__name__)    #, external_stylesheets=external_stylesheets)
if not app_config._DEPLOY_LOCALLY:
    app.config.update({'routes_pathname_prefix':'/aknn/', 'requests_pathname_prefix':'/aknn/'})

server=app.server
app.layout = create_div_mainapp()



# =====================================================
# ===================== Callbacks =====================
# =====================================================

@app.callback(
    Output('main-pval', 'figure'), 
    [Input('stored-stats', 'data')]
)
def update_main_plot(sts):
    num_mc_experts = 10000
    maxtime = 3000
    return { 
        'data': [{
            'name': 'P-values', 
            'x': np.zeros(4), 
            'y': np.zeros(4), 
            'mode': 'lines', 
            'type': 'scatter' 
        }], 
        'layout': {
            'showlegend': False, 
            'title': 'Precision-recall curve', 
            'titlefont': { 'family': 'sans-serif', 'color': app_config.params['legend_font_color'], 'size': 20}, 
            'clickmode': 'event+select',
            'hovermode': 'closest', 
            'uirevision': 'Default dataset',     # https://github.com/plotly/plotly.js/pull/3236
            'xaxis': {
                'title': 'Recall', 'titlefont': legend_font_macro, 'automargin': True, 
                'showticklabels': True, 'tickfont': legend_font_macro
            }, 
            'yaxis': {
                'title': 'Precision', 'titlefont': legend_font_macro, 'showticklabels': True, 'tickfont': legend_font_macro
            }, # 'legend': { 'y': '1.1', 'font': legend_font_macro, 'orientation': 'h' }, 
            'plot_bgcolor': app_config.params['bg_color'], 
            'paper_bgcolor': app_config.params['bg_color'], 
            'showlegend': False
        }
    }

            

# =======================================================
# ===================== Run the app =====================
# =======================================================

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)