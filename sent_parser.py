import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
import os
# import pendulum as pen
from textblob import TextBlob


df = pd.read_csv('https://raw.githubusercontent.com/Frankdew1995/text_sentiment_parser/master/Lan_Code.csv')

app = dash.Dash('Sentiment Parser')

server = app.server

# app.head = [
#
#     html.Title('hello')
# ]

app.layout = html.Div([

            html.H3('A simple text sentiment parsing app based off Dash and TextBlob'),

            html.Div([
                html.H5('Select your language:'),
                dcc.Dropdown(id='lan-selector',
                    options=[{'label':i[0],'value':i[1]} for i in zip(df['Language'],df['Code'])],
                    value ='en')


            ],style={'width':'50%'}),

            html.Br(),
            dcc.Textarea(
                id= 'text-widget',
                placeholder='Paste your texts here',
                value="you're so beautiful.",
                style={'width':'100%','height':250},

            ),
            html.Button(id='trigger',n_clicks=0,children='Submit'),
            html.Br(),
            html.P(html.Strong('The polarity value is a float within the range [-1.0, 1.0] where -1 is very negative, \
            0 is neutral and 1 is very positive. The subjectivity is a \
            float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.')),

            dcc.Graph(id='sentiment_graph'),


], className='container')


@app.callback(Output('sentiment_graph','figure'),
                [Input('trigger','n_clicks'),
                Input('lan-selector','value')],
                [State('text-widget','value')])
def parse_sentiment(clicks,language,text):
    if language == 'en':
        Blob = TextBlob(text)
    else:
        Blob = TextBlob(text).translate(from_lang=language, to='en')
    Polarity = round(Blob.sentiment.polarity,3)
    Subjectivity = round(Blob.sentiment.subjectivity,3)
    trace1 = go.Bar(
        x=['Polarity'],
        y=[Polarity],
        name='Polarity')

    trace2 = go.Bar(
        x=['Subjectivity'],
        y=[Subjectivity],
        name='Subjectivity')
    traces = [trace1, trace2]


    return {
        'data':traces,
        'layout':go.Layout(
                title='Hey, polarity index is {} and subjectivity index is {}'.format(Polarity,Subjectivity))



    }
    # fig = go.Figure(data=data, layout=layout)


my_css_url = "https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css"
app.css.append_css({
    "external_url": my_css_url
})






if __name__ == '__main__':

    app.run_server(debug=True)
