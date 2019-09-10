# Standard Library Imports
import colorsys

# Third Party Imports
import numpy as np
import plotly.graph_objs as go

html_colors = {
    'dark': '#cccccc',#'#BAC7DD',
    'medium': '#474A59',
    'light': '#dddddd', #'#FF5D73',

    'blue-accent': "#6A87D5",
    'red-accent': "#FF5D73",

    'white': "#f9f9f9",
    'black': "#000000",

    'grey': "#f2f3f4",
    'text': "#aaaaaa"
}

# graph_colors = [
#     [255,0,0],          #red
#     [0,0,255],          #blue
#     [0,216,0],          #green
#     [237,193,0],        #yellow
#     [0,244,244],        #light blue
#     [175,0,155],        #purple
#     [0,0,0],            #black
#     [252,126,0],        #oragne
#     [0,106,255],        #seablue
#     [132,132,132],      #gray
# ]

graph_colors = [
    [204,37,41],        #red
    [57,106,177],       #blue
    [62,150,81],        #green
    [218,124,48],       #orange
    [107,76,154],       #purple
    [10,10,10],         #white
    [204,194,16],       #gold
]


def create_colours(num_colours):
    """Create colour scheme for large number of classes"""
    colours = []
    for i in np.arange(0., 360., 360. / num_colours):
        hue = i / 360.
        lightness = (50 + np.random.rand() * 10) / 100.
        saturation = (90 + np.random.rand() * 10) / 100.
        colour = colorsys.hls_to_rgb(hue, lightness, saturation)
        colours.append([int(colour[0]*100), int(colour[1]*100), int(colour[2]*100)])
    return colours


def load_data(features, labels, text=None, names=None):
    """Verify and load data into dictionary"""
    global graph_colors

    # Convert to list
    if not isinstance(features, list):
        features.tolist()
    if not isinstance(labels, list):
        labels.tolist()

    # Number of samples and names
    n_samples = len(features)
    n_classes = len(set(labels))

    # Defualt text and name values
    if not text:
        text = ['' for i in range(n_samples)]
    if not names:
        names = [f'class_{i}' for i in range(n_classes)]

    # Consitency Checks
    if n_samples != len(labels) or n_samples != len(text):
        raise ValueError("features, labels, and/or text are inconsitent")
    if n_classes > len(graph_colors):
        graph_colors = create_colours(n_classes)
    if n_classes != len(names):
        raise ValueError("names are inconsitent with labels")
    
    # Output Dictionary
    out_dict = {}
    out_dict['features'] = features
    out_dict['labels'] = labels
    out_dict['text'] = text
    out_dict['names'] = names
    out_dict['graph_colors'] = graph_colors

    return out_dict


def Scatter3d(features, labels, 
              text=None,
              names=None,
              title='',
              xaxis_label='x',
              yaxis_label='y',
              zaxis_label='z',
              point_size=10,
              showgrid=True
              ):
    """Plotly 3d scatter"""
    global html_colors

    # Load data
    input_dict = load_data(features, labels, text, names)
    features = np.array(input_dict['features'])
    labels = input_dict['labels']
    text = input_dict['text']
    names = input_dict['names']
    graph_colors = input_dict['graph_colors']

    # Create trace indices for each class
    trace_indices = []
    for label in set(labels):
        trace_indices.append([i for i, x in enumerate(labels) if x == label])

    # Create plots for each class
    data = []
    for i, idx in enumerate(trace_indices):
        trace = go.Scatter3d(
            x=features[idx,0],
            y=features[idx,1],
            z=features[idx,2],
            mode='markers',
            name=names[i],
            text=[text[i] for i in idx],
            marker=dict(
                color='rgb({}, {}, {})'.format(*graph_colors[i]),
                size=point_size,
                symbol='circle'
            )
        )
        data.append(trace)

    if showgrid:
        ticks = 'outside'
    else:
        ticks = ''
        xaxis_label=''
        yaxis_label=''
        zaxis_label=''

    # Layout
    layout = go.Layout(
        title=title,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50
        ),
        scene=dict(
            xaxis=dict(
                color=html_colors['grey'],
                gridcolor=html_colors["light"],
                zerolinecolor=html_colors["dark"],
                showgrid=showgrid,
                zeroline=showgrid,
                showline=showgrid,
                ticks='',
                showticklabels=False,
                title=''
            ),
            yaxis=dict(
                color=html_colors['grey'],
                gridcolor=html_colors["light"],
                zerolinecolor=html_colors["dark"],
                showgrid=showgrid,
                zeroline=showgrid,
                showline=showgrid,
                ticks='',
                showticklabels=False,
                title=''
            ),
            zaxis=dict(
                color=html_colors['grey'],
                gridcolor=html_colors["light"],
                zerolinecolor=html_colors["dark"],
                showgrid=showgrid,
                zeroline=showgrid,
                showline=showgrid,
                ticks='',
                showticklabels=False,
                title=''
            ),
        ),
        plot_bgcolor=html_colors['grey'],
        paper_bgcolor=html_colors['grey'],
        font=dict(
            color=html_colors['text']
        )
    )

    return go.Figure(data=data, layout=layout)


def Scatter2d(features, labels, 
              text=None,
              names=None,
              title='',
              xaxis_label='x',
              yaxis_label='y',
              point_size=10,
              showgrid=True
              ):
    """Plotly 2d scatter"""
    global html_colors

    # Load data
    input_dict = load_data(features, labels, text, names)
    features = np.array(input_dict['features'])
    labels = input_dict['labels']
    text = input_dict['text']
    names = input_dict['names']
    graph_colors = input_dict['graph_colors']

    # Create trace indices for each class
    trace_indices = []
    for label in set(labels):
        trace_indices.append([i for i, x in enumerate(labels) if x == label])

    # Create plots for each class
    data = []
    for i, idx in enumerate(trace_indices):
        trace = go.Scatter(
            x=features[idx,0],
            y=features[idx,1],
            mode='markers',
            name=names[i],
            text=[text[i] for i in idx],
            marker=dict(
                color='rgb({}, {}, {})'.format(*graph_colors[i]),
                size=point_size,
                symbol='circle'
            )
        )
        data.append(trace)

    if showgrid:
        ticks = 'outside'
    else:
        ticks = ''
        xaxis_label=''
        yaxis_label=''

    # Layout
    layout = go.Layout(
        title=title,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=50
        ),
        xaxis=dict(
            color=html_colors['grey'],
            gridcolor=html_colors["light"],
            zerolinecolor=html_colors["dark"],
            showgrid=showgrid,
            zeroline=showgrid,
            showline=showgrid,
            ticks='',
            showticklabels=False,
            title=''
        ),
        yaxis=dict(
            color=html_colors['grey'],
            gridcolor=html_colors["light"],
            zerolinecolor=html_colors["dark"],
            showgrid=showgrid,
            zeroline=showgrid,
            showline=showgrid,
            ticks='',
            showticklabels=False,
            title=''
        ),
        plot_bgcolor=html_colors['grey'],
        paper_bgcolor=html_colors['grey'],
        font=dict(
            color=html_colors['text']
        )
    )

    return go.Figure(data=data, layout=layout)