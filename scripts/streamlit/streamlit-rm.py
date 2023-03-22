import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


tweets_dash_final =pd.read_csv('https://raw.githubusercontent.com/john-adeojo/royalmail-dash/main/data/02_intermediate/tweets_dash.csv')


# Define a function to assign emojis based on emotion
def get_emoji(sentiment):
    if sentiment == "positive":
        return "😁"
    elif sentiment == "neutral":
        return "😐"
    elif sentiment == "negative":
        return "😡"
    else:
        return "❓"

# Apply the get_emoji function to the 'emotion' column
tweets_dash_final['emoji'] = tweets_dash_final['sentiment'].apply(get_emoji)

def create_map(tweets_dash_final):
    # Create a base map centered on the UK
    map = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

    # Assuming you have a list of topics
    topics = ['Customer Service', 'Philately', 'Politics', 'Royal Reply', 'Royal Mail Jobs', 'Financial News']
    topic_layer_groups = {}

    # Create a LayerGroup for each topic and add it to the map
    for topic in topics:
        topic_layer_groups[topic] = folium.FeatureGroup(name=topic)
        map.add_child(topic_layer_groups[topic])

    # Loop through each row in the DataFrame and add a marker with an emoji to the appropriate layer
    for index, row in tweets_dash_final.iterrows():
        lat, lon = row['latitude'], row['longitude']
        emoji = row['emoji']
        topic = row['topic']
        cleaned_text = row['cleaned_text']

        marker = folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(html=f"""<div style="font-size:24px;">{emoji}</div>"""),
            tooltip=cleaned_text
        )
        topic_layer_groups[topic].add_child(marker)

    # Add layer control to switch between layers
    map.add_child(folium.LayerControl())

    return map


# Streamlit app
st.title("Topic & Sentiment Map of #royalmail Tweets")
st.markdown("### Produced by [John Adeojo](https://www.john-adeojo.com/)")


map = create_map(tweets_dash_final)
folium_static(map, width=2000, height=600)
st.text('This is for prototyping purposes only')
st.text('Data is between jan-2023 and mar-2023')