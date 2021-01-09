sentiment_labels = ['Positive','Negative','Neutral','Mixed']
sentiment_colors = [
    "#4169E1", "#F7464A", "#FDB45C", "#46BFBD"
    ]

def get_sentiment_chart_values(data) -> tuple:
    sentiment_score = data['SentimentScore']
    overall = data['Sentiment']
    values = [
        sentiment_score['Positive']*100,
        sentiment_score['Negative']*100,
        sentiment_score['Neutral']*100,
        sentiment_score['Mixed']*100,
    ]
    return overall , values