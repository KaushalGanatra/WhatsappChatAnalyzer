import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pages.preprocessor as prep
import pages.helper as helper
import pages.fileread as fileread
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(initial_sidebar_state="expanded")

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.sidebar.title("Welcome User to,")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

logout = st.sidebar.button("Logout")

if logout:
     switch_page("login")
        
if uploaded_file is not None:
    hour_format = st.radio(
        "Select the same Hour format with the hour format in your exported chat",
        ["12 Hours", "24 Hours"],
        captions = ["Ex: 8:05 pm", "Ex: 20:05"])

    if hour_format == '12 Hours':
        pattern = '\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} [ap]m -'
        form = '%d/%m/%y, %I:%M %p -'
    else:
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        form = '%d/%m/%Y, %H:%M - '
        
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = prep.preprocess(data,pattern,form)
    #st.write(df)

    user_list = df['user'].unique().tolist()
    try:
        user_list.remove('group_notifications')
    except:
        pass
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis',user_list)

    if st.sidebar.button('Show Analysis'):

        fileread.upload_file(data)
        
        if df.empty:
            st.write("Choose different hour format")
        else:
            try:
                num_messages,num_words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.header("Total Messages")
                    st.title(num_messages)

                with col2:
                    st.header("Total Words")
                    st.title(num_words)

                with col3:
                    st.header("Media Shared")
                    st.title(num_media_messages)
                    
                with col4:
                    st.header("Links Shared")
                    st.title(num_links)

                if selected_user == 'Overall':
                    st.title('Most Busy Users')
                    x,new_df = helper.most_busy_users(df)
                    fig, ax = plt.subplots()

                    col1, col2 = st.columns(2)

                    with col1:
                        ax.bar(x.index, x.values,color='red')
                        plt.xticks(rotation='vertical')
                        st.pyplot(fig)
                    with col2:
                        st.dataframe(new_df)

                st.title("Wordcloud")
                df_wc = helper.create_wordcloud(selected_user, df)
                st.image(df_wc.to_array(), use_column_width=True)

                most_common_df = helper.most_common_words(selected_user,df)
                fig,ax = plt.subplots()
                ax.barh(most_common_df[0],most_common_df[1])
                plt.xticks(rotation='vertical')
                st.title('Most commmon words')
                st.pyplot(fig)


                emoji_df = helper.emoji_helper(selected_user,df)
                st.title("Emoji Analysis")
                col1,col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig,ax = plt.subplots()
                    ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                    st.pyplot(fig)


                st.title('Activity Map')
                col1,col2 = st.columns(2)

                with col1:
                    st.header("Most busy day")
                    busy_day = helper.week_activity_map(selected_user,df)
                    fig,ax = plt.subplots()
                    ax.bar(busy_day.index,busy_day.values,color='purple')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.header("Most busy month")
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values,color='orange')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                st.title("Weekly Activity Map")
                user_heatmap = helper.activity_heatmap(selected_user,df)
                fig,ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)
                            
                st.title("Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user,df)
                fig,ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'],color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                st.title("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            except:
                pass
                
