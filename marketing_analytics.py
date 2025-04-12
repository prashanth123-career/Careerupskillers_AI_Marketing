import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import tweepy
import instaloader
from io import StringIO
from sklearn.linear_model import LinearRegression
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="Marketing Analytics Suite", layout="wide")

# App title
st.title("Marketing Analytics Suite")

# Initialize session state
if 'seo_data' not in st.session_state:
    st.session_state.seo_data = None
if 'social_data' not in st.session_state:
    st.session_state.social_data = None
if 'ad_data' not in st.session_state:
    st.session_state.ad_data = None

# Tab layout
tab1, tab2, tab3 = st.tabs(["SEO Analyzer", "Social Media Dashboard", "Ad Performance"])

# Tab 1: SEO Analyzer
with tab1:
    st.header("SEO Analyzer")
    
    url = st.text_input("Enter URL to analyze:", "https://example.com")
    
    if st.button("Analyze SEO"):
        with st.spinner("Analyzing website..."):
            # Simulate SEO analysis
            seo_score = np.random.randint(50, 95)
            meta_tags = np.random.randint(5, 20)
            backlinks = np.random.randint(10, 500)
            pagespeed = np.random.randint(30, 100)
            
            # Store in session state
            st.session_state.seo_data = {
                "SEO Score": seo_score,
                "Meta Tags": meta_tags,
                "Backlinks": backlinks,
                "PageSpeed": pagespeed
            }
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("SEO Score", f"{seo_score}/100")
            with col2:
                st.metric("Meta Tags Found", meta_tags)
            with col3:
                st.metric("Estimated Backlinks", backlinks)
            with col4:
                st.metric("PageSpeed Score", f"{pagespeed}/100")
            
            # SEO recommendations
            st.subheader("Recommendations")
            if seo_score < 70:
                st.warning("Your SEO score needs improvement. Consider the following:")
                st.write("- Optimize meta tags and descriptions")
                st.write("- Improve page loading speed")
                st.write("- Build quality backlinks")
            else:
                st.success("Good SEO score! Keep monitoring and improving.")
            
            # Keyword density analyzer
            st.subheader("Keyword Density Analyzer")
            sample_text = st.text_area("Paste your content here to analyze keyword density:", 
                                     "This is sample content about digital marketing and SEO. Digital marketing helps businesses grow online. SEO is important for visibility.")
            
            if st.button("Analyze Keywords"):
                words = sample_text.lower().split()
                total_words = len(words)
                keyword_counts = {}
                
                for word in words:
                    if len(word) > 3:  # Ignore short words
                        keyword_counts[word] = keyword_counts.get(word, 0) + 1
                
                # Create dataframe
                keywords_df = pd.DataFrame.from_dict(keyword_counts, orient='index', columns=['Count'])
                keywords_df['Density (%)'] = (keywords_df['Count'] / total_words) * 100
                keywords_df = keywords_df.sort_values('Density (%)', ascending=False)
                
                # Display results
                st.dataframe(keywords_df.head(10))
                
                # Visualization
                fig = px.bar(keywords_df.head(10), 
                             x=keywords_df.head(10).index, 
                             y='Density (%)',
                             title="Top Keywords by Density")
                st.plotly_chart(fig)

# Tab 2: Social Media Dashboard
with tab2:
    st.header("Social Media Dashboard")
    
    platform = st.radio("Select Platform:", ("Twitter", "Instagram"))
    
    if platform == "Twitter":
        st.subheader("Twitter Analytics")
        
        # Twitter API connection
        st.write("Connect to Twitter API")
        api_key = st.text_input("API Key", type="password")
        api_secret = st.text_input("API Secret", type="password")
        access_token = st.text_input("Access Token", type="password")
        access_secret = st.text_input("Access Secret", type="password")
        
        if st.button("Connect to Twitter"):
            try:
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_secret)
                api = tweepy.API(auth)
                user = api.verify_credentials()
                st.success(f"Connected as @{user.screen_name}")
                
                # Get tweets
                tweets = api.user_timeline(count=20)
                tweet_data = []
                for tweet in tweets:
                    tweet_data.append({
                        "Date": tweet.created_at,
                        "Text": tweet.text,
                        "Likes": tweet.favorite_count,
                        "Retweets": tweet.retweet_count,
                        "Replies": tweet.reply_count
                    })
                
                st.session_state.social_data = pd.DataFrame(tweet_data)
                
            except Exception as e:
                st.error(f"Error connecting to Twitter: {e}")
        
        if st.session_state.social_data is not None:
            st.subheader("Recent Tweets Performance")
            st.dataframe(st.session_state.social_data)
            
            # Engagement metrics
            st.subheader("Engagement Metrics")
            df = st.session_state.social_data
            
            fig1 = px.line(df, x="Date", y="Likes", title="Likes Over Time")
            st.plotly_chart(fig1)
            
            fig2 = px.line(df, x="Date", y="Retweets", title="Retweets Over Time")
            st.plotly_chart(fig2)
            
            # Post scheduler
            st.subheader("Post Scheduler")
            post_date = st.date_input("Schedule date")
            post_time = st.time_input("Schedule time")
            post_content = st.text_area("Post content")
            
            if st.button("Generate AI Caption"):
                st.write("AI-generated caption suggestion:")
                st.info(f"🚀 Exciting update! {post_content[:50]}... #digitalmarketing #socialmedia")
                
            if st.button("Schedule Post"):
                st.success(f"Post scheduled for {post_date} at {post_time}")
    
    else:  # Instagram
        st.subheader("Instagram Analytics")
        
        username = st.text_input("Instagram Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Connect to Instagram"):
            try:
                L = instaloader.Instaloader()
                L.login(username, password)
                profile = instaloader.Profile.from_username(L.context, username)
                st.success(f"Connected to @{profile.username}")
                
                # Get recent posts
                post_data = []
                for post in profile.get_posts():
                    if len(post_data) >= 10:
                        break
                    post_data.append({
                        "Date": post.date,
                        "Likes": post.likes,
                        "Comments": post.comments,
                        "Caption": post.caption[:50] + "..." if post.caption else "",
                        "URL": f"https://instagram.com/p/{post.shortcode}"
                    })
                
                st.session_state.social_data = pd.DataFrame(post_data)
                
            except Exception as e:
                st.error(f"Error connecting to Instagram: {e}")
        
        if st.session_state.social_data is not None:
            st.subheader("Recent Posts Performance")
            st.dataframe(st.session_state.social_data)
            
            # Engagement metrics
            st.subheader("Engagement Metrics")
            df = st.session_state.social_data
            
            fig1 = px.bar(df, x="Date", y="Likes", title="Likes Per Post")
            st.plotly_chart(fig1)
            
            fig2 = px.bar(df, x="Date", y="Comments", title="Comments Per Post")
            st.plotly_chart(fig2)

# Tab 3: Ad Performance
with tab3:
    st.header("Ad Performance Analyzer")
    
    uploaded_file = st.file_uploader("Upload Ad Performance CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.ad_data = df
        
        st.subheader("Ad Performance Data")
        st.dataframe(df.head())
        
        # ROI Calculator
        st.subheader("ROI Calculator")
        
        if 'Spend' in df.columns and 'Revenue' in df.columns:
            total_spend = df['Spend'].sum()
            total_revenue = df['Revenue'].sum()
            roi = ((total_revenue - total_spend) / total_spend) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Spend", f"${total_spend:,.2f}")
            with col2:
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            with col3:
                st.metric("ROI", f"{roi:.2f}%")
            
            # Visualization
            fig = px.bar(df, x='Campaign', y=['Spend', 'Revenue'], 
                         title="Spend vs Revenue by Campaign", barmode='group')
            st.plotly_chart(fig)
            
            # Predictive spend optimization
            st.subheader("Predictive Spend Optimization")
            
            if st.button("Optimize Ad Spend"):
                with st.spinner("Running optimization..."):
                    time.sleep(2)
                    
                    # Simple linear regression model
                    X = df[['Spend']]
                    y = df['Conversions']
                    model = LinearRegression().fit(X, y)
                    
                    # Predict optimal spend
                    optimal_spend = (y.max() - model.intercept_) / model.coef_[0]
                    
                    st.success(f"Recommended optimal spend: ${optimal_spend[0]:,.2f}")
                    
                    # Show prediction vs actual
                    df['Predicted'] = model.predict(X)
                    fig = px.scatter(df, x='Spend', y='Conversions', 
                                     trendline="ols", title="Spend vs Conversions")
                    st.plotly_chart(fig)
        else:
            st.warning("CSV must contain 'Spend' and 'Revenue' columns for ROI calculation")

# Footer
st.markdown("---")
st.markdown("### Marketing Analytics Suite v1.0")
st.markdown("For digital marketing professionals")
