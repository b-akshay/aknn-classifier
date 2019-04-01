# -*- coding: utf-8 -*-

params = {}

params['title'] = "An adaptive nearest neighbor classifier"


_DEPLOY_LOCALLY = True

if not _DEPLOY_LOCALLY:
    params['data_pfx'] = '/var/www/aknn-classifier/'
else:
    params['data_pfx'] = '/Users/akshay/github/aknn-classifier/'

params['bg_color'] = '#000000'


# ======================================================
# ================== Colors and sizes ==================
# ======================================================

# Custom colorscales.

cmap_celltypes = ["#f7ff00","#fabebe","#ff8300","#f000ff","#74ee15","#4363d8","#001eff","#ff3300","#cab2d6","#008080","#808000","#bcf60c","#bec1d4","#fb9a99","#ffd8b1","#3cb44b","#bc5300","#ffe119","#33ccff","#911eb4","#46f0f0","#d220c8","#e6beff","#e6194b","#aaffc3","#000075"]

# Perceptually uniform blackbody, good for black background as in https://github.com/kennethmoreland-com/kennethmoreland-com.github.io/blob/master/color-advice/black-body/black-body.ipynb
cmap_custom_blackbody = [[0.0, "#000000"], [0.39, "#b22222"], [0.58, "#e36905"], [0.84, "#eed214"], [1.0, "#ffffff"]]

# Default discrete colormap for <= 20 categories, from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/. See also http://phrogz.net/css/distinct-colors.html and http://tools.medialab.sciences-po.fr/iwanthue/
cmap_custom_discrete = ["#bdbdbd", 
                        '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
                        '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', 
                        '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', 
                        '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']#, '#7d87b9', '#bec1d4', '#d6bcc0']
# Custom red/blue diverging for black background, from https://gka.github.io/palettes
cmap_custom_rdbu_diverging = [[0.0, '#0000ff'], [0.1111, '#442dfa'], [0.2222, '#6b59e0'], [0.3333, '#6766a3'], [0.4444, '#323841'], [0.5555, '#483434'], 
                              [0.6666, '#b3635b'], [0.7777, '#ee5d49'], [0.8888, '#ff3621'], [1.0, '#ff0000']]
# Custom yellow/blue diverging for black background:
cmap_custom_ylbu_diverging = [[0.0, '#0008ff'], [0.1111, '#0048ff'], [0.2222, '#4042ff'], [0.3333, '#35557c'], [0.4444, '#0f1010'], [0.5555, '#0f1010'], 
                              [0.6666, '#787c21'], [0.7777, '#a9ac00'], [0.8888, '#d3d200'], [1.0, '#fffa00']]


params['hover_edges'] = ""
params['edge_color'] = 'rgb(255,255,255)'
params['edge_width'] = 1
params['incl_edges'] = False
params['three_dims'] = False

params['marker_size_factor'] = 3.5
params['marker_opacity_factor'] = 1.0
params['font_color'] = 'white'

params['legend_bgcolor'] = '#000000'
params['legend_bordercolor'] = 'white'
# params['legend_borderwidth'] = 2
params['legend_font_color'] = 'white'
params['legend_font_size'] = 16
params['hm_font_size'] = 6

params['upload_img_path'] = params['data_pfx'] + 'assets/upload.png'
params['download_img_path'] = params['data_pfx'] + 'download.png'

# Some things are best left to depend on the size of the data - opacity changes with number of points plotted!
