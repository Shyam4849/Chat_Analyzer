import streamlit as st
import preprocessor
import functions
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import matplotlib.font_manager as fm
from streamlit_lottie import st_lottie

# from functions import get_sentiment


def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except:
        return None

# Streamlit page setup
st.set_page_config(page_title="WhatsApp Analyzer", layout="wide")

# Inject Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #0f2027 !important;
        background-image: linear-gradient(to right, #2c5364, #203a43, #0f2027) !important;
    }
    h1, h2, h3, .stMetric, .stMarkdown, .stDataFrame {
        color: #25D366 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Lottie Animation + Logo + Heading
lottie_url = "https://lottie.host/7efb0872-0879-4a46-9cb2-e02e7b865212/zvI3ItkClJ.json"
lottie_json = load_lottieurl(lottie_url)
if lottie_json:
    st_lottie(lottie_json, height=180, key="header-lottie")

st.markdown("""
    <div style="text-align:center; padding: 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="90"/>
        <h1 style="color:#25D366; font-size: 40px;">WhatsApp Chat Analyzer</h1>
        <p style="color:white;">Visualize your chat like never before 📊💬</p>
    </div>
""", unsafe_allow_html=True)

# Seaborn style
sns.set_style("darkgrid")

# Sidebar
st.sidebar.title("🟢 WhatsApp Chat Analyzer 📊")
uploaded_file = st.sidebar.file_uploader("📁 Choose a file")

if uploaded_file is None:
    st.markdown(''' Please export your Whatsapp chat (without media), whether it be a group or an individual/private chat, then click on "Browse Files" and upload it to this platform.''')
    
    st.markdown('''Afterward, kindly proceed to click on the "Analyze" button. This action will generate a veriety of insights concerning your conservation.''')
    
    st.markdown('''You will have the option to select the type of analysis, whether it is an overall analysis or one that specifically focuses on paticular participants' analysis.''')
    
    st.markdown("Thank you!")
    st.markdown("Shyam Kumar Soni")
    
    
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    
    # st.write(bytes_data)
    
    # converting bytes into text
    data = bytes_data.decode("utf-8")
    
    # show text data
    # st.text(data)
    
    # Dataframe
    df = preprocessor.preprocess(data)
    
    # show dataframe
    # st.dataframe(df)
    
    # fetch unique user
    user_details = df['user'].unique().tolist()
    
    # remove Group Notification
    if 'Group Notification' in user_details:
        user_details.remove('Group Notification')
        
    # sorting list
    user_details.sort()
    
    # insert overall option
    user_details.insert(0, 'OverAll')
    
    # drop down to select user
    selected_user = st.sidebar.selectbox("🔍 Show analysis for:", user_details)
    
    if st.sidebar.button("🎯 Analyze"):
        
        num_msgs, num_med, link = functions.fetch_stats(selected_user, df)
        
        # Overall Statistics
        st.title('📈 Overall Basic Statistics')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('💬 Messages')
            st.subheader(num_msgs)
        with col2:
            st.header('📷 Media Shared')
            st.subheader(num_med)
        with col3:
            st.header('🔗 Link Shared')
            st.subheader(link)
            
        # Monthly Timeline
        timeline = functions.monthly_timeline(selected_user, df)
        st.title('🗓 Monthly Timeline')
        
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#0f2027')
        ax.set_facecolor('#0f2027')
        sns.lineplot(data=timeline, x='time', y='msg', marker='o', ax=ax, color='cyan')
        ax.set_title('Messages Over Months', color='white')
        ax.tick_params(colors='white')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
        # Daily Timeline
        timeline = functions.daily_timeline(selected_user, df)
        st.title('📅 Daily Timeline')
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#0f2027')
        ax.set_facecolor('#0f2027')
        sns.lineplot(data=timeline, x='date', y='msg', marker='o', ax=ax, color='orange')
        ax.set_title('Daily Chat Activity', color='white')
        ax.tick_params(colors='white')
        st.pyplot(fig)
        
        # Activity Map
        st.title('📍 Activity Map')
        col1, col2 = st.columns(2)
        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list = functions.activity_map(selected_user, df)
        
        with col1:
            # ACtive Month
            st.header('🗖️ Most Active Month')
            fig, ax = plt.subplots()
            ax.bar(active_month_df['month'], active_month_df['msg'])
            ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green', label = "Highest")
            ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color = 'red', label = 'Lowest')
            plt.xticks(rotation = 90)
            st.pyplot(fig)
            
            
        with col2:
            # Active Day
            st.header('🗖️ Most Active Day')
            fig, ax = plt.subplots()
            ax.bar(active_day_df['day'], active_day_df['msg'])
            ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label = "Highest")
            ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color = 'red', label = 'Lowest')
            plt.xticks(rotation = 90)
            st.pyplot(fig)
            
        # Most Active User
        if selected_user == 'OverAll':
            st.title('🧑‍🤝‍🧑 Most Active Users')
            
            x, percent = functions.most_chaty(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x, color='#DC143C')
                
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)
                
        # Word Cloud
        st.subheader("☁️ Most Common Words")
        df_wc = functions.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#0f2027')
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        
        # Emoji Analyzer
        st.subheader("😄 Emoji Analysis")
        emoji_df = functions.emoji_analysis(selected_user, df)
        #emoji_font = fm.FontProperties(fname="C:/Windows/Fonts/seguiemj.ttf")
        emoji_font = fm.FontProperties(family="Segoe UI Emoji")
        #plt.rcParams['font.family'] = emoji_font.get_name()
        plt.rcParams['font.family'] = emoji_font.get_name()
        if not emoji_df.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                fig, ax = plt.subplots()
                fig.patch.set_facecolor('#0f2027')
                ax.set_facecolor('#0f2027')
                sns.barplot(x=emoji_df[0][:10], y=emoji_df[1][:10], palette="viridis", ax=ax)
                #sns.barplot(x=active_month_df['month'], y=active_month_df['msg'], ax=ax, hue=active_month_df['month'], palette="cool", legend=False)
                ax.set_title("Top Emojis Used", color='white')
                ax.tick_params(colors='white')
                st.pyplot(fig)
            with col2:
                st.dataframe(emoji_df.head(10).rename(columns={0: "Emoji", 1: "Count"}))
            
        # Sentiment Analysis (Will be updated in future)
        # if st.checkbox("Show Sentiment Analysis"):
        #     st.write("Checkbox clicked")  # Debug check
        #     st.write(df.head())           # Check data looks okay
            
        #     try:
        #         df['Sentiment'] = df['msg'].apply(get_sentiment)
        #         st.write("Sentiment column added")
        #         st.dataframe(df[['user','msg', 'Sentiment']])
        #     except Exception as e:
        #         st.error(f"Error in sentiment analysis: {e}")


        # Download CSV
        st.subheader("📅 Download Insights as CSV")
        download_df = df[df['user'] == selected_user] if selected_user != "OverAll" else df
        csv = download_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Chat Data 📁",
            data=csv,
            file_name=f'{selected_user}_chat_insights.csv',
            mime='text/csv'
        )
        
        # Footer
        st.text(' ')
        st.text(' ')
        
        st.text('by - Shyam Kumar Soni')
        # st.write(df.columns)

        