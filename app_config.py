# -*- coding: utf-8 -*-

params = {}

params['title'] = "An adaptive nearest neighbor classifier"


_DEPLOY_LOCALLY = True

if not _DEPLOY_LOCALLY:
    params['data_pfx'] = '/var/www/aknn-classifier/'
else:
    params['data_pfx'] = '/Users/akshay/github/aknn-classifier/'

params['bg_color'] = '#000000'


params['plot_data_df_path'] = [params['data_pfx'] + "notMNIST/notMNIST_vizdf.csv", params['data_pfx'] + "single_cell/tabula_vizdf.csv"]
params['raw_datamat_path'] = [params['data_pfx'] + "notMNIST/notMNIST_small_data.npz", params['data_pfx'] + "notMNIST/notMNIST_small_data.npz"]
params['nbrs_path'] = [params['data_pfx'] + "notMNIST/notMNIST_small_nbrs_1000.npy", params['data_pfx'] + "single_cell/tabula_subset_nbrs_1000.npy"]
params['label_names'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


#'Adaptive k (# neighbors)', 'Predicted labels'
params['default_color_var'] = 'Labels'
params['display_ID_var'] = 'cell_IDs'

# params['dataset_options'] = [x.split('/')[-1].split('.')[0] for x in params['plot_data_df_path']]
params['dataset_options'] = ["notMNIST", "Tabula Muris"]

params['bg_color'] = '#000000'

params['legendgroup'] = False
params['display_coordinates'] = { 'x': 'hUMAP_x',  'y': 'hUMAP_y' }
params['qnorm_plot'] = True
params['continuous_color'] = False



# ======================================================
# ================== Colors and sizes ==================
# ======================================================

# Custom colorscales.
cmap_jumbo = ["#f7ff00","#ff8300","#f000ff","#001eff","#33ccff","#74ee15","#fb9a99","#ff3300","#cab2d6","#e6194b","#3cb44b","#ffe119","#4363d8","#f58231","#911eb4","#46f0f0","#d220c8","#bcf60c","#fabebe","#008080","#e6beff","#9a6324","#fffac8","#aaffc3","#808000","#ffd8b1","#000075","#7d87b9","#bec1d4"]

# Perceptually uniform blackbody, good for black background as in https://github.com/kennethmoreland-com/kennethmoreland-com.github.io/blob/master/color-advice/black-body/black-body.ipynb
cmap_custom_blackbody = [[0.0, "#000000"], [0.39, "#b22222"], [0.58, "#e36905"], [0.84, "#eed214"], [1.0, "#ffffff"]]

# Default discrete colormap for <= 20 categories, from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/. See also http://phrogz.net/css/distinct-colors.html and http://tools.medialab.sciences-po.fr/iwanthue/
cmap_custom_discrete = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
                        '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#bdbdbd', 
                        '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', 
                        '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']#, '#7d87b9', '#bec1d4', '#d6bcc0']

# Custom cubehelix do-it-all sequential palette, from [x for x in zip(np.arange(21)/20, sns.color_palette("cubehelix", 21).as_hex())]
cmap_cubehelix = [(0.0, '#100713'), (0.05, '#19122b'), (0.1, '#1a213e'), (0.15, '#17344c'), (0.2, '#15494e'), (0.25, '#185b48'), (0.3, '#256b3d'), (0.35, '#3c7632'), (0.4, '#5a7a2f'), (0.45, '#7e7a36'), (0.5, '#a1794a'), (0.55, '#bc7967'), (0.6, '#ce7d8c'), (0.65, '#d486af'), (0.7, '#d295d0'), (0.75, '#caa9e7'), (0.8, '#c4bdf1'), (0.85, '#c2d2f3'), (0.9, '#c8e4f0'), (0.95, '#d6f0ef'), (1.0, '#ebf9f3')]

# Custom red/blue diverging for black background, from sns.diverging_palette(0, 255, s=99, l=65, n=20, center='dark').as_hex()
cmap_custom_rdbu_diverging = [(0.0, '#fe6d91'), (0.05263157894736842, '#e76585'), (0.10526315789473684, '#d05d7a'), (0.15789473684210525, '#b7546d'), (0.21052631578947367, '#9e4c61'), (0.2631578947368421, '#854454'), (0.3157894736842105, '#6e3c48'), (0.3684210526315789, '#54333b'), (0.42105263157894735, '#3d2b30'), (0.47368421052631576, '#242323'), (0.5263157894736842, '#232324'), (0.5789473684210527, '#2b313d'), (0.631578947368421, '#323e54'), (0.6842105263157895, '#3b4c6e'), (0.7368421052631579, '#425985'), (0.7894736842105263, '#4b679e'), (0.8421052631578947, '#5374b6'), (0.8947368421052632, '#5b82cf'), (0.9473684210526315, '#628fe7'), (1.0, '#6a9cfe')]

# Custom yellow/blue diverging for black background, from the following code:
# x = sns.diverging_palette(227, 86, s=98, l=77, n=20, center='dark').as_hex(); [s for s in zip(np.arange(len(x))/(len(x)-1), x)]
cmap_custom_ylbu_diverging = [(0.0, '#3acdfe'), (0.05263157894736842, '#37bbe6'), (0.10526315789473684, '#35a9cf'), (0.15789473684210525, '#3295b6'), (0.21052631578947367, '#2f829e'), (0.2631578947368421, '#2d6f85'), (0.3157894736842105, '#2a5d6e'), (0.3684210526315789, '#274954'), (0.42105263157894735, '#25373d'), (0.47368421052631576, '#222324'), (0.5263157894736842, '#232322'), (0.5789473684210527, '#363621'), (0.631578947368421, '#474720'), (0.6842105263157895, '#5a5a1e'), (0.7368421052631579, '#6b6b1d'), (0.7894736842105263, '#7e7e1c'), (0.8421052631578947, '#8f901b'), (0.8947368421052632, '#a2a21a'), (0.9473684210526315, '#b3b318'), (1.0, '#c4c417')]
cmap_custom_orpu_diverging = [(0.0, '#c2b5fe'), (0.05263157894736842, '#b1a5e6'), (0.10526315789473684, '#a096cf'), (0.15789473684210525, '#8e85b6'), (0.21052631578947367, '#7c759e'), (0.2631578947368421, '#6a6485'), (0.3157894736842105, '#59556e'), (0.3684210526315789, '#464354'), (0.42105263157894735, '#35343d'), (0.47368421052631576, '#232324'), (0.5263157894736842, '#242323'), (0.5789473684210527, '#3d332a'), (0.631578947368421, '#544132'), (0.6842105263157895, '#6e523a'), (0.7368421052631579, '#856041'), (0.7894736842105263, '#9e7049'), (0.8421052631578947, '#b67f50'), (0.8947368421052632, '#cf8f58'), (0.9473684210526315, '#e79d5f'), (1.0, '#feac66')]


if 'colorscale_discrete' not in params:
    params['colorscale_discrete'] = ["#bdbdbd", "#f7ff00", "#ff8300", "#f000ff", "#001eff", "#33ccff", "#74ee15", "#33a02c", "#fb9a99", "#ff3300", "#cab2d6", 
                                     '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0'] # cmap_custom_discrete
if 'colorscale_continuous' not in params:
    params['colorscale_continuous'] = 'Viridis'

params['colorscale'] = params['colorscale_continuous'] if params['continuous_color'] else params['colorscale_discrete']

params['hover_edges'] = ""
params['edge_color'] = 'rgb(255,255,255)'
params['edge_width'] = 1
params['incl_edges'] = False
params['three_dims'] = False

params['sel_marker_size'] = 7.0
params['marker_size'] = 4.0
params['bg_marker_opacity'] = 0.5
params['marker_opacity'] = 1.0
params['font_color'] = 'white'

params['legend_bgcolor'] = '#000000'
params['legend_bordercolor'] = 'white'
# params['legend_borderwidth'] = 2
params['legend_font_color'] = 'white'
params['legend_font_size'] = 16
params['hm_font_size'] = 6


# Some things are best left to depend on the size of the data - opacity changes with number of points plotted!