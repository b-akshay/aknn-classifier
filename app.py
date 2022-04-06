# -*- coding: utf-8 -*-
"""
Dash application (Dash [Python] <- Plotly <- React.js <- D3.js)
Author: Akshay Balsubramani
"""

import base64, io, os, time, json
import numpy as np, scipy as sp, pandas as pd, dash, scipy.sparse
from dash.dependencies import Input, Output, State
import dash_core_components as dcc, dash_html_components as html
import app_config, app_lib, building_block_divs, aknn_alg



# =========================================================
# ================== Initialize Dash app ==================
# =========================================================

# Load gene embedded coordinates.
plot_data_df = pd.read_csv(app_config.params['plot_data_df_path'][0], sep="\t", index_col=False)
# graph_adj = sp.sparse.load_npz(app_config.params['adj_mat_path'])

raw_data = sp.sparse.load_npz(app_config.params['raw_datamat_path'][0])
nbr_list_sorted_small = np.load(app_config.params['nbrs_path'][0])


app = dash.Dash(__name__)
if not app_config._DEPLOY_LOCALLY:
    app.config.update({'routes_pathname_prefix':'/aknn/', 'requests_pathname_prefix':'/aknn/'})

server=app.server
app.layout = building_block_divs.create_div_mainapp(
    more_colorvars=['Predicted labels', 'Adaptive k (# neighbors)', 'Adaptive k quantile']
)

def calc_clicked_idx(clickData, data_df, plot_dimension):
    dim_names = ['x', 'y']
    dim_cols = ['hUMAP_x', 'hUMAP_y']
    if plot_dimension == '3D':
        dim_names = ['x', 'y', 'z']
        dim_cols = ['3D_hUMAP_x', '3D_hUMAP_y', '3D_hUMAP_z']
    # Convert the point clicked into a float64 array and select its data
    click_point_coords = np.array([clickData['points'][0][i] for i in dim_names]).astype(np.float64)
    bool_mask_click = data_df.loc[:, dim_cols].eq(click_point_coords).all(axis=1)
#     if not bool_mask_click.any():
#         return None
    return data_df[bool_mask_click].index[0]



# =====================================================
# ===================== Callbacks =====================
# =====================================================


@app.callback(
    Output('test-select-data', 'children'),
    [Input('landscape-plot', 'clickData')]
)
def display_test(
    clickData
):
    return ""#"***CLICKED DATA***\n{}".format(json.dumps(clickData, indent=2))


@app.callback(
    Output('display-nbr-fracs', 'figure'),
    [Input('landscape-plot', 'clickData'), 
     Input('slider-confidence-param', 'value'), 
     Input('main-landscape-dimension', 'value'), 
     Input('landscape-plot', 'figure')]
)
def display_nbr_fracs(clickData, conf_param, plot_dimension, scatter_fig):
    toret_fig = {
        'data': [], 
        'layout': building_block_divs.create_scatter_layout([])
    }
    if not clickData or ('points' not in clickData) or (scatter_fig is None) or (len(scatter_fig['data']) <= 1):
        return toret_fig
    clicked_idx = calc_clicked_idx(clickData, plot_data_df, plot_dimension)
    thresholds = conf_param/np.sqrt(np.arange(nbr_list_sorted_small.shape[1])+1)
    (pred_label, adaptive_k_ndx, fracs_labels) = aknn_alg.aknn(nbr_list_sorted_small[clicked_idx,:], plot_data_df['Labels'], thresholds)
    for i in range(len(app_config.params['label_names'])):
        lbl_name = app_config.params['label_names'][i]
        lbl_color = app_config.params['colorscale_discrete'][i]
        new_trace = scatter_fig['data'][i]
        new_trace.update({
            'x': np.arange(len(thresholds)) + 1, 
            'y': fracs_labels[i, :], 
            'mode': 'lines+markers'
        })
        new_trace['line'] = { 'color': new_trace['marker']['color'], 'width': 3.0 }
        toret_fig['data'].append(new_trace)
    return toret_fig



@app.callback(
    Output('display-datapoint', 'figure'),
    [Input('landscape-plot', 'clickData'), 
     Input('main-landscape-dimension', 'value')]
)
def display_click_image(
    clickData, 
    plot_dimension
):
    toret_fig = {
        'data': [], 
        'layout': {
            'margin': { 'l': 0, 'r': 0, 'b': 0, 't': 30 }, 
            'clickmode': 'event+select',  # https://github.com/plotly/plotly.js/pull/2944/
            'hovermode': 'closest', 
            'uirevision': 'Default dataset', 
            'xaxis': {
                'showticklabels': True, 'side': 'top', 
                'tickcolor': app_config.params['legend_bgcolor'], 
                'tickfont': { 'family': 'sans-serif', 'size': app_config.params['hm_font_size'], 'color': app_config.params['legend_font_color'] }, 
                'showgrid': False, 'showline': False, 'zeroline': False, 'visible': False
            }, 
            'yaxis': {
                'automargin': True, 'showticklabels': False, 'autorange': 'reversed', 
                'showgrid': False, 'showline': False, 'zeroline': False, 'visible': False
            }, 
            'plot_bgcolor': app_config.params['bg_color'], 
            'paper_bgcolor': app_config.params['bg_color']
        }
    }
    if not clickData:
        return toret_fig
    clicked_idx = calc_clicked_idx(clickData, plot_data_df, plot_dimension)
    image_np = raw_data[:, clicked_idx].toarray().reshape(28, 28).astype(np.float64)
    hm_traces = [{ 
        "zmax": 255, "zmin": 0,
        'z': image_np, # 'x': hm_feat_names, 
        'hoverinfo': 'text', 'text': 'z', 
        'colorscale': 'Greys', 
        'colorbar': {
            'len': 0.3, 'thickness': 20, 
            'xanchor': 'left', 'yanchor': 'top', 
            'title': 'Image', 'titleside': 'top', 
            'ticks': 'outside', 
            'titlefont': building_block_divs.colorbar_font_macro, 
            'tickfont': building_block_divs.colorbar_font_macro
        }, 
        'type': 'heatmap'
    }]
    toret_fig['data'] = hm_traces
    return toret_fig


"""
Update the main graph panel with selected points annotated, using the given dataset.
"""
def highlight_landscape_func(
    data_df, 
    marker_size=app_config.params['marker_size'], 
    style_selected=building_block_divs.style_selected, 
    color_var=app_config.params['default_color_var'], # Could be an array of continuous colors!
    colorscale=app_config.params['colorscale'], 
    looked_up_ndces=[], 
    highlight_selected=False, 
    absc_arr=None, 
    ordi_arr=None, 
    three_dim_plot=False, 
    continuous_var=False
):
    annots = []
    for point_ndx in looked_up_ndces:
        absc = absc_arr[point_ndx]
        ordi = ordi_arr[point_ndx]
        annots.append({
            'x': absc, 'y': ordi,
            'xref': 'x', 'yref': 'y', 
            'font': { 'color': 'white', 'size': 15 }, 
            'arrowcolor': 'white', 'showarrow': True, 
            'arrowhead': 2, 'arrowwidth': 2, 'arrowsize': 2, 
            'ax': 0, 'ay': -50 
        })
    toret = app_lib.build_main_scatter(
        data_df, 
        color_var, 
        colorscale, 
        highlight=highlight_selected, 
        annots=annots, 
        marker_size=marker_size, 
        style_selected=style_selected, 
        three_dim_plot=three_dim_plot, 
        continuous_var=continuous_var
    )
    return toret


"""
Update the main graph panel.
"""
@app.callback(
    Output('landscape-plot', 'figure'), 
    [Input('landscape-color', 'value'), 
     Input('sourcedata-select', 'value'), 
     Input('slider-confidence-param', 'value'), 
     Input('slider-marker-size-factor', 'value'), 
     Input('main-landscape-dimension', 'value')]
)
def update_landscape(
    color_scheme,          # Feature(s) selected to plot as color.
    sourcedata_select, 
    confidence_param, 
    marker_size, 
    plot_dimension
):
    dataset_names = app_config.params['dataset_options']
    ndx_selected = dataset_names.index(sourcedata_select) if sourcedata_select in dataset_names else 0
    data_df = pd.read_csv(app_config.params['plot_data_df_path'][ndx_selected], sep="\t", index_col=False)
    nbr_list_sorted = np.load(app_config.params['nbrs_path'][ndx_selected])

    point_ndces_to_select = []
    absc_arr = data_df[app_config.params['display_coordinates']['x']]
    ordi_arr = data_df[app_config.params['display_coordinates']['y']]
    
    continuous_var=False
    cscale = app_config.params['colorscale_discrete']
    # Check if a continuous feature is chosen to be plotted.
    if (color_scheme in ['Adaptive k (# neighbors)', 'Adaptive k quantile', 'Predicted labels']):
        # pred_labels, adaptive_ks = aknn_alg.predict_nn_rule(nbr_list_sorted, data_df['Labels'], margin=confidence_param, mode='ovr')
        pred_labels_name = 'Predicted labels (A = {:.1f})'.format(confidence_param)
        adaptive_ks_name = 'Adaptive k (A = {:.1f})'.format(confidence_param)
        data_df['Adaptive k (# neighbors)'] = data_df[adaptive_ks_name].values
        data_df['Predicted labels'] = data_df[pred_labels_name].values
        adak_q = sp.stats.rankdata(data_df[adaptive_ks_name].values)
        data_df['Adaptive k quantile'] = adak_q/np.max(adak_q)
        if (color_scheme in ['Adaptive k (# neighbors)', 'Adaptive k quantile']): 
            cscale = app_config.params['colorscale_continuous']
            continuous_var = True
        elif (color_scheme == 'Predicted labels'):
            cscale = app_config.params['colorscale_discrete']
    elif (color_scheme in ['Labels']):    # color_scheme is a col ID indexing a discrete column.
        cscale = app_config.params['colorscale_discrete']
    return highlight_landscape_func(
        data_df, 
        color_var=color_scheme, 
        colorscale=cscale, 
        looked_up_ndces=point_ndces_to_select, 
        absc_arr=absc_arr, 
        ordi_arr=ordi_arr, 
        marker_size=marker_size, 
        three_dim_plot=(plot_dimension == '3D'), 
        continuous_var=continuous_var
    )

            

# =======================================================
# ===================== Run the app =====================
# =======================================================

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)