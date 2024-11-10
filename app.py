import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns

st.set_page_config(layout="wide")


# Splash screen (visible until a file is uploaded)
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

if st.session_state['uploaded_file'] is None:
    # CSS for center-aligned image

    st.image("image/WhatsApp Image 2024-11-05 at 8.26.22 PM.jpeg", use_column_width=True)



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file =st.sidebar.file_uploader("Choose a file")
flag=True
if uploaded_file is not None:
    if not uploaded_file.name.endswith(".txt"):
        st.sidebar.error("Error: The uploaded file is not a text file. Please upload a valid text file.")
        flag=False

    try:
        if flag:
            st.session_state['uploaded_file'] = uploaded_file        #imposter
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode("utf-8")
            df = preprocessor.preprocessor(data)

            group_df = df.copy()

            user_list = df['user'].unique().tolist()
            if "group_notification" in user_list:
                user_list.remove("group_notification")


            user_list.sort()
            user_list.insert(0,"OverAll")
            selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

            users = df['user'].unique().tolist()


            try:
                if st.sidebar.button("Show Analysis"):
                    st.markdown("<h2 style='padding-bottom: 0;'>📎 General Features</h2>", unsafe_allow_html=True)
                    st.markdown("---")

                    col1, col2, col3, col4= st.columns(4)
                    a,b,c,d,e = helper.fetch_total(selected_user, df)


                    with col1:
                        st.markdown("<h3 style='font-size: 30px;'>Total Message</h3>",unsafe_allow_html=True)
                        st.markdown(f"<h1 style='font-size: 39px;'>{a}</h1>", unsafe_allow_html=True)
                        # st.title(a)
                        st.markdown("---")

                    with col2:
                        st.markdown("<h3 style='font-size: 30px;'>Media Shared</h3>",unsafe_allow_html=True)
                        st.markdown(f"<h1 style='font-size: 39px;'>{d}</h1>", unsafe_allow_html=True)
                        # st.title(d)
                        st.markdown("---")

                    with col3:
                        st.markdown("<h3 style='font-size: 30px;'>Link Shared</h3>",unsafe_allow_html=True)
                        st.markdown(f"<h1 style='font-size: 39px;'>{e}</h1>", unsafe_allow_html=True)
                        # st.title(e)
                        st.markdown("---")

                    with col4:
                        st.markdown("<h3 style='font-size: 30px;'>First Convo</h3>",unsafe_allow_html=True)
                        st.markdown(f"<h1 style='font-size: 38px;'>{b}</h1>", unsafe_allow_html=True)
                        # st.title(b)
                        st.markdown("---")


                    col1, col2, col3, col4 = st.columns(4)
                    if selected_user == "OverAll":

                        if "group_notification" in users:
                            with col1:
                                st.markdown("<h3 style='font-size: 30px;'>Group Notifi</h3>", unsafe_allow_html=True)
                                st.markdown(f"<h1 style='font-size: 39px;'>{df['user'].value_counts().group_notification}</h1>", unsafe_allow_html=True)
                                st.markdown("---")
                        else:
                            with col1:
                                st.markdown("<h3 style='font-size: 30px;'>Group Notifi</h3>", unsafe_allow_html=True)
                                st.markdown(f"<h1 style='font-size: 39px;'>{'0'}</h1>", unsafe_allow_html=True)
                                st.markdown("---")

                        with col2:
                            st.markdown("<h3 style='font-size: 30px;'>Total Words</h3>",unsafe_allow_html=True)
                            st.markdown(f"<h1 style='font-size: 38px;'>{c}</h1>", unsafe_allow_html=True)
                            st.markdown("---")

                        if "group_notification" in users:
                            with col3:
                                st.markdown("<h3 style='font-size: 30px;'>Total Members</h3>", unsafe_allow_html=True)
                                st.markdown(f"<h1 style='font-size: 38px;'>{(len(df['user'].unique().tolist()))-1}</h1>", unsafe_allow_html=True)
                                st.markdown("---")
                        else:
                            with col3:
                                st.markdown("<h3 style='font-size: 30px;'>Total Members</h3>", unsafe_allow_html=True)
                                st.markdown(f"<h1 style='font-size: 38px;'>{len(df['user'].unique().tolist())}</h1>", unsafe_allow_html=True)
                                st.markdown("---")


                        with col4:
                            st.markdown("<h3 style='font-size: 30px;'>Group Name</h3>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='font-size: 30px; margin-bottom: 5%;'>{helper.group_name(uploaded_file.name)}</h2>", unsafe_allow_html=True)
                            st.markdown("---")



                # Group level analysis
                    if selected_user == "OverAll":
                        top_user, new_df = helper.fetch_top_user(df)
                        st.markdown("<h2 style='padding-bottom: 0;'>📎 Top Users</h2>",unsafe_allow_html=True)
                        st.markdown("---")

                        fig, ax = plt.subplots(figsize=(6.3,4.3))

                        col=st.columns(2)

                        with col[0]:

                            ax.bar(top_user.index,top_user.values,color=["#007BA7",'#99FFFF'],alpha=0.8)
                            plt.xticks(rotation='vertical')
                            ax.set_ylabel('no. of messages')

                            st.pyplot(fig)

                        with col[1]:
                            st.dataframe(new_df,use_container_width=True)

            #Frequenct Words

                    st.markdown("<h2 style='padding-bottom: 0;'>📎 Frequent Words</h2>", unsafe_allow_html=True)
                    st.divider()

                    col1, col2 = st.columns(2)
                    df_wc, new_df = helper.top_words(selected_user, df)
                    with col1:
                        fig, ax = plt.subplots(figsize=(4,4))

                        ax.imshow(df_wc)
                        st.pyplot(fig)

                    with col2:
                        st.markdown("<br>",unsafe_allow_html=True)
                        st.dataframe(new_df,use_container_width=True)


            # EMOJI SECTION*888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888


                    new_df = helper.emojis_count(selected_user, df)

                    if new_df.empty:
                       pass
                    else:
                        st.markdown("<h2 style='padding-bottom: 0;'>📎 Frequent Emojis</h2>", unsafe_allow_html=True)
                        st.divider()
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("<br>",unsafe_allow_html=True)
                            fig, ax = plt.subplots(figsize=(6.3,5.1))

                            ax.bar(new_df['Emojis'].tolist()[:10],new_df['Frequency'].tolist()[:10],color=['#4682B4'],alpha=0.7,edgecolor="black")
                            ax.set_xlabel('Emojis',fontsize=14)
                            ax.set_ylabel('Frequency',fontsize=14)

                            st.pyplot(fig)

                        with col2:
                            st.dataframe(new_df,use_container_width=True)

            #Message Deleted
                    dl = helper.delete_messages(selected_user, df)
                    if dl.empty:
                        pass
                    else:
                        if selected_user == "OverAll":
                            st.markdown("<h2 style='padding-bottom: 0;'>📎 Deleted Message</h2>", unsafe_allow_html=True)
                            st.divider()

                            col1, col2 =st.columns(2)

                            with col1:
                                # st.markdown("<br>",unsafe_allow_html=True)
                                fig,ax = plt.subplots()

                                # plt.pie(dl['count'].tolist(),labels=dl['user'].tolist())
                                x = dl['count'].tolist()
                                y = dl['user'].tolist()
                                c = ["#4682B4","#5F9EA0","#708090","#008080","#000080","#20B2AA","#D3D3D3","#4B0082"]
                                ex = [0.01 for _ in range(len(x[:10]))]
                                ax.pie(x[:10], explode=ex, colors=c, autopct="%0.1f%%", shadow=False, radius=1, labeldistance=1,
                                        startangle=90, textprops={"fontsize": 8}, counterclock=False)

                                plt.legend(y[:10], loc="center left", bbox_to_anchor=(0.9, 0.5))
                                ax.set_xlabel("% of message deleted by Users",fontsize=13)
                                plt.show()
                                st.pyplot(fig)

                            with col2:
                                st.dataframe(dl.iloc[:10,:],use_container_width=True)

            #Heat_Map Actvity
                    st.markdown("<h2 style='padding-bottom: 0;'>📎 Weekly Timeline</h2>",
                                unsafe_allow_html=True)
                    st.divider()

                    heat_df = helper.heatmaps_(selected_user,df)
                    fig, ax = plt.subplots(figsize=(20, 6))
                    sns.heatmap(heat_df,cmap="GnBu_r",alpha=0.96, ax=ax)
                    st.pyplot(fig)
                    plt.yticks(rotation="horizontal")


            #Monthly Timeline
                    st.markdown("<h2 style='padding-bottom: 0;'>📎 Monthly Timeline</h2>", unsafe_allow_html=True)
                    st.divider()

                    col1 , col2 = st.columns(2)
                    tl=helper.timeline(selected_user,df)
                    with col1:
                        fig, ax =plt.subplots()

                        ax.plot(tl['month'].tolist(),tl['no. of message'].tolist(),c="#5F9EA0")
                        plt.xticks(rotation='vertical')

                        st.pyplot(fig)

                    with col2:
                        st.dataframe(tl,use_container_width=True)


        #Only Analysis
                    st.markdown("<h2 style='padding-bottom: 0;'>📎 Other Analysis</h2>", unsafe_allow_html=True)
                    st.divider()

                    col1, col2 = st.columns(2)
                    day_name,day_timeline = helper.weekly_timeline(selected_user, df)
                    with col1:
                        st.subheader("Week-Days Activities")

                        fig , ax = plt.subplots()

                        ax.barh(day_name.index,day_name.values,color="#20B2AA")
                        ax.set_xlabel("no. of messages")

                        st.pyplot(fig)

                    with col2:
                        st.subheader("Daily Timeline")


                        fig , ax = plt.subplots(figsize=(5,3.3))

                        ax.plot(day_timeline.index,day_timeline.values,color="royalblue")
                        plt.xticks(rotation="vertical")
                        ax.set_ylabel("no. of messages")
                        st.pyplot(fig)

                    if selected_user == "OverAll" and len(user_list) > 3:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Group Notifications")
                            st.markdown("<br>",unsafe_allow_html=True)
                            temp = helper.notification(group_df)

                            fig, ax = plt.subplots()

                            ex = [0.01 for _ in range(len(temp['Counts'].tolist()))]
                            ax.pie(temp['Counts'],labels=temp['Group Notification'],colors=["#008080","#000080","#20B2AA","#D3D3D3","#4B0082","#4682B4","#5F9EA0","#708090"],explode=ex,autopct="%0.1f%%",radius=1.3,textprops={"fontsize": 12})

                            st.pyplot(fig)

                        with col2:
                            st.subheader("Monthly Activities")
                            st.markdown("<br>",unsafe_allow_html=True)
                            temp=helper.monthlyactivity(selected_user,df)

                            fig, ax = plt.subplots(figsize=(5,3.6))

                            ax.bar(temp['month'],temp['message'])
                            plt.xticks(rotation="vertical")

                            st.pyplot(fig)

                    st.markdown("<br><br><h6 style= 'text-align : center;'>All rights reserved. © 2024 Ayush Kumar</h6>",unsafe_allow_html=True)

            except Exception as processing_error:
                # Catch and display any errors that occur during data processing
                st.error(f"Error during processing: {str(processing_error)}")


    except UnicodeDecodeError:
        st.sidebar.error("Error: The uploaded file is not a text file. Please upload a valid text file.")











