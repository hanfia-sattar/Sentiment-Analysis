import streamlit as st
import pandas as pd
import plotly.express as px
from reddit_sentiment_analysis import analyze_reddit_comments

def plot_sentiment_bar(df):
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    fig = px.bar(sentiment_counts, x='Sentiment', y='Count', 
                 title="Sentiment Distribution of Comments",
                 labels={'Count': 'Number of Comments'},
                 color='Sentiment',
                 hover_data=['Count'],
                 text='Count')
    fig.update_traces(textposition='outside')
    return fig

def plot_sentiment_pie(df):
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    fig = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                 title="Sentiment Distribution of Comments (%)",
                 hover_data=['Count'], 
                 labels={'Count': 'Number of Comments'})
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def main():
    st.title("Reddit Comment Sentiment Analysis")

    url = st.text_input("Enter the URL of the Reddit post:")

    if st.button("Analyze"):
        if url:
            with st.spinner("Fetching and analyzing comments..."):
                df = analyze_reddit_comments(url)

                # Display results
                st.subheader("Results")
                st.write(f"Total comments analyzed: {len(df)}")

                # Display the DataFrame
                st.dataframe(df)

                # Plot sentiment distribution (Bar Chart)
                st.subheader("Sentiment Distribution (Count)")
                fig_bar = plot_sentiment_bar(df)
                st.plotly_chart(fig_bar, use_container_width=True)

                # Plot sentiment distribution (Pie Chart)
                st.subheader("Sentiment Distribution (%)")
                fig_pie = plot_sentiment_pie(df)
                st.plotly_chart(fig_pie, use_container_width=True)

                # Download link for CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name="reddit_comments_analyzed.csv",
                    mime="text/csv",
)

        else:
            st.error("Please enter a valid Reddit post URL.")

if __name__ == "__main__":
    main()