import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

states = df['state'].unique()

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.Label('Select States'),
        dcc.Dropdown(
            id='state',
            options=[{'label': i, 'value': i} for i in states],
            value='',
            placeholder='Select...',
            multi=True
        )
    ],
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}),

    html.Div([
        html.Label('Deaths Reported'),
        dcc.Slider(
            id='deaths-slider',
            min=1,
            max=3000,
            value=500,
            step=None,
            marks={'1': '>1', '500': '>500', '1000': '>1000', '1500': '>1500', '2000': '>2000', '2500': '>2500'}
        ),
    ],
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '20px'}),

    html.Div([
        dcc.Graph(id='deaths-by-date'),
    ],
    style={'width': '95%'}),
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
            text=df_by_state['cases'],
            mode='markers',
            opacity=0.7,
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
            yaxis={'title': 'Deaths', 'titlefont': dict(size=18, color='darkgrey'), 'range': [000, 40000], 'ticks': 'outside'},
            margin={'l': 60, 'b': 90, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
