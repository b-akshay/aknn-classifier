# -*- coding: utf-8 -*-
# Generic front-end code for making biological dataset browsing interfaces.
# Author: Akshay Balsubramani


import dash_core_components as dcc, dash_html_components as html
import app_config, numpy as np


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

style_unselected = { 'marker': { 'size': 3.0, 'opacity': 0.7 } }

style_selected = { 'marker': { 'size': 6.0, 'opacity': 122.2 } }

style_outer_dialog_box = {
    # 'user-select': 'none', '-moz-user-select': 'none', '-webkit-user-select': 'none', '-ms-user-select': 'none', 
    'padding': 5, 
    # 'margin': 5, 
    # 'borderRadius': 5, 
    'border': 'thin lightgrey solid'
}

style_invis_dialog_box = {
    # 'user-select': 'none', '-moz-user-select': 'none', '-webkit-user-select': 'none', '-ms-user-select': 'none', 
    'padding': 5, 'margin': 5
}

style_text_box = {
    'textAlign': 'center', 
    'width': '100%', 
    'color': app_config.params['font_color']
}

style_upload = {
    'width': '100%', 
    'border': 'thin lightgrey solid',
    'textAlign': 'center', 
    'color': app_config.params['font_color'], 
    'padding-top': '5px', 
    'padding-bottom': '5px'
}

style_legend = {
    'font': legend_font_macro, 
    # bgcolor=app_config.params['legend_bgcolor'], 
    # 'borderwidth': app_config.params['legend_borderwidth'], 
    'padding': 0, 
    'margin': 0, 
    'border': 'thin lightgrey solid', 
    'traceorder': 'normal', 
    'orientation': 'h'
}


def create_scatter_layout(annotations):
    return {
        'margin': { 'l': 0, 'r': 0, 'b': 0, 't': 20}, 
        'clickmode': 'event+select',  # https://github.com/plotly/plotly.js/pull/2944/
        'hovermode': 'closest', 
        'uirevision': 'Default dataset',     # https://github.com/plotly/plotly.js/pull/3236
        'xaxis': {
            'automargin': True, 
            'showticklabels': False, 
            'showgrid': False, 'showline': False, 'zeroline': False, #'visible': False, 
            'style': {'display': 'none'}
        }, 
        'yaxis': {
            'automargin': True, 
            'showticklabels': False, 
            'showgrid': False, 'showline': False, 'zeroline': False, #'visible': False, 
            'style': {'display': 'none'}
        }, 
        'legend': style_legend, 
        'annotations': annotations, 
        'plot_bgcolor': app_config.params['bg_color'], 
        'paper_bgcolor': app_config.params['bg_color']
    }



# ================================================================
# =================== Component divs: cosmetic ===================
# ================================================================


# Default dataset first in the given list of dataset options.
def create_div_cosmetic_panel():
    return html.Div(
        className='row', 
        children=[
            html.Div(
                className='one column', 
                children=[
                    html.P(
                        "Interface options: ", 
                        style=style_text_box
                    )], 
                style={'padding-top': '10px'}
            ), 
            html.Div(
                className='two columns', 
                children=[
                    dcc.Slider(
                        id='slider-marker-size-factor',
                        min=0, max=8, step=0.2, 
                        value=app_config.params['marker_size']
                    ), 
                    html.Div(
                        id='display-marker-size-factor', 
                        children='Marker size', 
                        style={
                            'textAlign': 'center', 
                            'color': app_config.params['font_color'], 
                            'padding-top': '10px'
                        }
                    )]
            ), 
            html.Div(
                className='three columns', 
                children=[
                    dcc.RadioItems(
                        id='main-landscape-dimension', 
                        options=[ 
                            {'label': '2D plot', 'value': '2D'}, 
                            {'label': '3D plot', 'value': '3D'}
                        ], 
                        style=legend_font_macro, 
                        labelStyle={ 'display': 'inline-block', 'margin-right': '5px' }, 
                        value='2D'
                    )]
            )
        ], 
        style=style_outer_dialog_box
    )



# ==================================================================
# =================== Aggregating component divs ===================
# ==================================================================



def create_div_landscapes():
    return html.Div(
        className="eight columns",
        children=[
            dcc.Graph(
                id='landscape-plot',
                config={'displaylogo': False, 'displayModeBar': True}, 
                style={ 'height': '100vh'}
            )#, 
#             html.Div(
#                 className="row", 
#                 children=[
#                     html.Div(
#                         className="four columns", 
#                         children=[
#                             html.A(
#                                 html.Button(
#                                     id='download-layout-button', 
#                                     children='Export layout', 
#                                     style=style_text_box, 
#                                     n_clicks='0', n_clicks_timestamp='0'
#                                 ), 
#                                 id='download-layout-link',
#                                 download="selected_layout.csv", 
#                                 href="", target="_blank", 
#                                 style={ 'width': '100%', 'textAlign': 'center', 'color': app_config.params['font_color'] }
#                             )], 
#                         style=style_invis_dialog_box
#                     )]
#             )
        ]
    )


def create_div_show_datapoint():
    return html.Div(
        className="row",
        children = [
            dcc.Graph(
                id='display-datapoint', 
                style={ 'height': '35vh', 'padding-bottom': '20px' }, 
                config={'displaylogo': False, 'displayModeBar': True}
            )]
    )


def create_div_show_nbrs():
    return html.Div(
        className="row",
        children = [
            dcc.Graph(
                id='display-nbr-fracs', 
                style={ 'height': '45vh' }, 
                config={'displaylogo': False, 'displayModeBar': True}
            )]
    )


def create_div_sidepanels():
    return html.Div(
        className='four columns', 
        children=[
            create_div_show_datapoint(), 
            create_div_show_nbrs()
        ],
        style=style_invis_dialog_box
    )


# Default dataset first in the given list of dataset options.
def create_div_select_dataset(dataset_options):
    return html.Div(
        className='four columns', 
        children=[
            html.Div(
                className='four columns', 
                children=[
                    html.P(
                        "Browse dataset: ", 
                        style=style_text_box
                    )], 
                style={'padding-top': '10px'}
            ), 
            html.Div(
                className='eight columns', 
                children=[
                    dcc.Dropdown(
                        id='sourcedata-select', 
                        options = [ {'value': dn, 'label': dn} for dn in dataset_options ], # style={'height': '30px'}, 
                        value=dataset_options[0], 
                        clearable=False
                    )]
            )], 
        style=style_outer_dialog_box
    )


def create_div_mainctrl(more_colorvars):
    return html.Div(
        className='row', 
        children=[
            html.Div(
                className='two columns', 
                children=[
                    dcc.Dropdown(
                        id='landscape-color', 
                        options = [{
                            'value': app_config.params['default_color_var'], 
                            'label': app_config.params['default_color_var']
                        }] + [
                            {'value': n, 'label': n} for n in more_colorvars
                        ], 
                        value=app_config.params['default_color_var'], 
                        placeholder="Select colors to plot", 
                        clearable=False
                    )], 
                style={ 'padding-right': '25px' }
            ), 
            html.Div(
                className='four columns', 
                children=[
                    dcc.Slider(
                        id='slider-confidence-param',
                        min=0, max=9.5, step=0.5, 
                        value=1.0
                    ), 
                    html.Div(
                        children='1-NN (Abstain less) <------   Confidence parameter   ------> Abstain more', 
                        style={
                            'textAlign': 'center', 
                            'color': app_config.params['font_color'], 
                            'padding-top': '10px'
                        }
                    )
                ], 
                style={ 'padding': 2, 'margin': 2}
            ), 
            html.Div(
                className='two columns', 
                children=[
                    html.Div(
                        className='eight columns', 
                        children=[
                            dcc.RadioItems(
                                id='select-knn-alg', 
                                options=[ 
                                    # {'label': 'Non-adaptive', 'value': 'nonadaptive'}, 
                                    {'label': 'AKNN', 'value': 'ovr'}#, 
                                    #{'label': 'AKNN-UCB', 'value': 'ucb'}
                                ], 
                                style=legend_font_macro, 
                                labelStyle={ 'display': 'inline-block', 'margin-right': '5px' }, 
                                value='ovr'
                            )]
                    )]
            ), 
            create_div_select_dataset(app_config.params['dataset_options'])
        ]
    )


"""
Main layout.
"""

def create_div_mainapp(
    more_colorvars=[]
):
    return html.Div(
        className="container", 
        children=[
            html.Div(
                className='row', 
                children=[
                    html.H1(
                        id='title', children=app_config.params['title'], 
                        style=style_text_box
                    )]
            ), 
            create_div_mainctrl(more_colorvars), 
            html.Div(
                className="row", 
                children=[
                    create_div_landscapes(), 
                    create_div_sidepanels()
                ]
            ), 
            create_div_cosmetic_panel(), 
            html.Div([ html.Pre(id='test-select-data', style={ 'color': app_config.params['font_color'], 'overflowX': 'scroll' } ) ]),     # For testing purposes only!
            html.Div(
                className='row', 
                children=[ 
                    dcc.Markdown(
                        """Source [repository](aknn-classifier)."""  # TODO insert signature. (https://github.com/b-akshay/aknn-classifier)."""
                    )], 
                style={
                    'textAlign': 'center', 
                    'color': app_config.params['font_color'], 
                    'padding-bottom': '10px'
                }
            )
        ],
        style={ 
            'width': '100vw', 
            'max-width': 'none'
        }
    )