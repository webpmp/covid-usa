import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

dates = df['date'].unique()

app = dash.Dash()

app.layout = html.Div([

    html.Div([
        html.Label('Select Dates'),
        dcc.Dropdown(
            id='date',
            options=[{'label': i, 'value': i} for i in dates],
            value='2020-03-01',
            placeholder='Select...',
            multi=True
        )
    ],
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px'}),

    html.Div([
        html.Label('Cases Reported'),
        dcc.Slider(
            id='cases-slider',
            min=1,
            max=3000,
            value=500,
            step=None,
            marks={'1': '>1', '500': '>500', '1000': '>1000', '1500': '>1500', '2000': '>2000', '2500': '>2500'}
        ),
    ],
    style={'width': '20%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-left': '20px'}),

    html.Div([
        dcc.Graph(id='state-vs-death'),
    ],
    style={'width': '95%'}),
])


@app.callback(
    dash.dependencies.Output('state-vs-death', 'figure'),
    [
        dash.dependencies.Input('cases-slider', 'value'),
        dash.dependencies.Input('date', 'value')
    ])
def update_graph(deaths, date):

    filtered_df = df.loc[df["deaths"] > deaths]

    if (date != '' and date is not None):
        filtered_df = filtered_df[df.date.str.contains('|'.join(date))]

    traces = []
    for i in filtered_df.state.unique():
        df_by_state = filtered_df[filtered_df['state'] == i]
        traces.append(go.Scatter(
            x=df_by_state['state'],
            y=df_by_state['deaths'],
            text=df_by_state['date'],
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
            xaxis={'title': 'United States', 'titlefont': dict(size=18, color='darkgrey'), 'zeroline': False, 'ticks': 'outside'},
            yaxis={'title': 'Deaths', 'titlefont': dict(size=18, color='darkgrey'), 'range': [000, 20000], 'ticks': 'outside'},
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)
