import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import pandas as pd

# import data
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

states = df['state'].unique()

# when using custom css, add __name__
app = dash.Dash(__name__)

# dropdown for state selection
app.layout = html.Div([
    html.Div([
        html.Label('State'),
        dcc.Dropdown(
            id='state',
            options=[{'label': i, 'value': i} for i in states],
            value='',
            placeholder='Select States...',
            multi=True
        )
    ],
    style={'width': '25%', 'display': 'inline-block', 'margin-bottom': '20px'}),
# slideer for filtering by number of deaths
    html.Div([
        html.Label('Total Deaths'),
        dcc.Slider(
            id='deaths-slider',
            min=1,
            max=3000,
            value=500,
            step=None,
            marks={'1': '>1', '500': '>500', '1000': '>1000', '1500': '>1500', '2000': '>2000', '2500': '>2500'}
        ),
    ],
    style={'width': '35%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '20px'}),

    html.Div([
        dcc.Graph(id='deaths-by-date'),
    ],
    style={'width': '85%'}),
])


@app.callback(
    dash.dependencies.Output('deaths-by-date', 'figure'),
    [
        dash.dependencies.Input('deaths-slider', 'value'),
        dash.dependencies.Input('state', 'value')
    ])
def update_graph(deaths, state):

    filtered_df = df.loc[df["deaths"] > deaths]

    if (state != '' and state is not None):
        filtered_df = filtered_df[df.state.str.contains('|'.join(state))]

    traces = []
    for i in filtered_df.state.unique():
        df_by_state = filtered_df[filtered_df['state'] == i]
        traces.append(go.Scatter(
            x=df_by_state['date'],
            y=df_by_state['deaths'],
#           text=df_by_state['cases'],      # remove covid cases data
            mode='markers',
            opacity=0.6,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date', 'titlefont': dict(size=18, color='darkgrey'), 'zeroline': False, 'ticks': 'outside'},
            yaxis={'title': 'Total Deaths', 'titlefont': dict(size=18, color='darkgrey'), 'range': [000, 35000], 'ticks': 'outside'},
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
