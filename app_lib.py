# Application-specific routines for working with (smallish matrices of) data.
# Author: Akshay Balsubramani

import base64, io, os, time, json, numpy as np, scipy as sp, pandas as pd
import app_config, building_block_divs



# =======================================================
# ================== Utility functions ==================
# =======================================================

def quantile_norm(dtd):
    qtiles = np.zeros(len(dtd))
    nnz_ndces = np.nonzero(dtd)[0]
    qtiles[nnz_ndces] = sp.stats.rankdata(dtd[nnz_ndces])/len(nnz_ndces)
    return qtiles


# Input: Anndata or h5 with data in it.
def load_data(data_path):
    if 'h5ad' in data_path:
        return anndata.read_h5ad(data_path)
    else:
        return pd.read_csv(data_path, sep="\t", index_col=False)



# =========================================================
# =================== Main scatter plot ===================
# =========================================================

"""
(Data, layout) for the main graph panel.
Color_var is either a field of the plotting df, or a numpy array.
"""

# Here selected_point_ids is a list of unique string IDs of points. 
def traces_scatter(
    data_df, 
    color_var, 
    colorscale, 
    selected_point_ids, 
    marker_size=app_config.params['marker_size'], 
    style_selected=building_block_divs.style_selected, 
    continuous_var=False, 
    three_dim_plot=False
):
    traces_list = []
    display_ndces = app_config.params['display_coordinates']
    cumu_color_dict = {}
    # Check to see if color_var is continuous or discrete and plot points accordingly
    if continuous_var:     # Color_var is an array, not a col index.
        continuous_color_var = data_df[color_var]
        colorbar_title = 'Adaptive k'
        max_magnitude = np.percentile(continuous_color_var, 99)
        trace_info = { 
            'name': 'Data', 
            'x': data_df[display_ndces['x']], 
            'y': data_df[display_ndces['y']], 
            'hoverinfo': 'text', 
            'mode': 'markers', 
            'marker': {
                'size': marker_size, 
                'opacity': app_config.params['marker_opacity'], 
                'symbol': 'circle', 
                'showscale': True, 
                'colorbar': {
                    'len': 0.3, 
                    'thickness': 20, 
                    'xanchor': 'right', 
                    'yanchor': 'top', 
                    'title': colorbar_title,
                    'titleside': 'top',
                    'ticks': 'outside', 
                    'titlefont': building_block_divs.colorbar_font_macro, 
                    'tickfont': building_block_divs.colorbar_font_macro
                }, 
                'color': continuous_color_var, 
                'colorscale': colorscale, 
                #'cmin': -max_magnitude, 
                'cmax': max_magnitude
            }, 
            'selected': style_selected, 
            'type': 'scattergl'
        }
        if not three_dim_plot:
            trace_info.update({'type': 'scattergl'})
        else:
            trace_info.update({
                'type': 'scatter3d', 
                'x': data_df['3D_hUMAP_x'], 
                'y': data_df['3D_hUMAP_y'], 
                'z': data_df['3D_hUMAP_z']
            })
        traces_list.append(trace_info)
    else:    # Categorical color scheme, one trace per color
        cnt = 0
        for idx, val in data_df.groupby(color_var):
            if app_config.params['legendgroup']:
                legendgroup = idx.split('_')[0]
            else:
                legendgroup = idx
            if legendgroup not in cumu_color_dict:
                trace_color = colorscale[cnt]
                cnt += 1
                cumu_color_dict[legendgroup] = trace_color
            trace_opacity = 1.0
            trace_info = {
                'name': str(idx), 
                'x': val[display_ndces['x']], 
                'y': val[display_ndces['y']], 
                'hoverinfo': 'text+name', 
                # 'text': point_ids_this_trace, 
                'mode': 'markers', 
                'opacity': trace_opacity, 
                'marker': {
                    'size': marker_size, 
                    'opacity': app_config.params['marker_opacity'] if str(idx) != 'Other' else app_config.params['bg_marker_opacity'], 
                    'symbol': 'circle', 
                    'color': trace_color
                }, 
                'legendgroup': legendgroup, 
                'selected': style_selected
            }
            if not three_dim_plot:
                trace_info.update({'type': 'scattergl'})
            else:
                trace_info.update({
                    'type': 'scatter3d', 
                    'x': val['3D_hUMAP_x'], 
                    'y': val['3D_hUMAP_y'], 
                    'z': val['3D_hUMAP_z']
                })
            traces_list.append(trace_info)
    return traces_list


def layout_scatter(annots):
    display_ndces = app_config.params['display_coordinates']
    new_layout = building_block_divs.create_scatter_layout(annots)
    return new_layout


def build_main_scatter(
    data_df, 
    color_var, 
    colorscale, 
    highlight=False, 
    marker_size=app_config.params['marker_size'], 
    annots=[], 
    three_dim_plot=False, 
    selected_point_ids=[], 
    style_selected=building_block_divs.style_selected, 
    continuous_var=False
):
    if highlight:
        style_selected['marker']['color'] = 'white'
    else:
        style_selected['marker'].pop('color', None)    # Remove color if exists
    trace_list = traces_scatter(
        data_df, 
        color_var, 
        colorscale, 
        selected_point_ids, 
        three_dim_plot=three_dim_plot, 
        marker_size=marker_size, 
        style_selected=style_selected, 
        continuous_var=continuous_var
    )
    return { 
        'data': trace_list, 
        'layout': layout_scatter(annots)
    }