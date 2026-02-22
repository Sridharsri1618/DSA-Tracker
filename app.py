import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="DSA Problem Tracker", layout="wide")

# ---------- Sidebar ----------
st.sidebar.title("Navigation")
menu = st.sidebar.selectbox("", ["Manage Problems", "Analytics"])

FILE = "dsa_data.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "ID", "Title", "Platform",
        "Topic", "Difficulty",
        "Status", "Date", "Notes"
    ])
    df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)

# ================= MANAGE =================
if menu == "Manage Problems":

    st.title("📘 DSA Problem Tracker")

    # -------- Add Problem --------
    with st.expander("➕ Add Problem", expanded=False):
        with st.form("add_form"):
            col1, col2 = st.columns(2)

            with col1:
                pid = st.text_input("Problem ID")
                title = st.text_input("Title")
                platform = st.selectbox(
                    "Platform",
                    ["LeetCode", "HackerRank", "CodeStudio", "GeeksforGeeks", "Other"]
                )

                topic = st.selectbox(
                    "Topic",
                    [
                        "Array",
                        "LinkedList",
                        "Stack",
                        "Queue",
                        "Tree",
                        "Binary Tree",
                        "BST",
                        "Graph",
                        "DP",
                        "Greedy",
                        "Sliding Window",
                        "Recursion",
                        "Backtracking",
                        "Other"
                    ]
                )

            with col2:
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
                status = st.selectbox("Status", ["Solved", "Unsolved"])
                date = st.date_input("Date", datetime.today())
                notes = st.text_area("Notes")

            submit = st.form_submit_button("Add Problem")

            if submit:
                new_row = pd.DataFrame([[
                    pid, title, platform, topic,
                    difficulty, status, date, notes
                ]], columns=df.columns)

                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(FILE, index=False)
                st.success("Problem Added Successfully 🚀")

    st.markdown("---")

    # -------- View Problems --------
    if not df.empty:

        topics = ["All"] + sorted(df["Topic"].dropna().unique().tolist())
        selected_topic = st.selectbox("Filter by Topic", topics)

        filtered_df = df if selected_topic == "All" else df[df["Topic"] == selected_topic]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("### 🗑 Delete Problem")

        delete_id = st.selectbox(
            "Select Problem ID to Delete",
            df["ID"].unique()
        )

        if st.button("Delete Selected Problem"):
            df = df[df["ID"] != delete_id]
            df.to_csv(FILE, index=False)
            st.success("Problem Deleted Successfully ✅")
            st.rerun()

    else:
        st.warning("No problems added yet.")

# ================= ANALYTICS =================
elif menu == "Analytics":

    st.title("📊 Analytics Dashboard")

    if df.empty:
        st.warning("No data available.")
    else:
        total = len(df)
        solved = len(df[df["Status"] == "Solved"])
        progress = int((solved / total) * 100) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Problems", total)
        col2.metric("Solved", solved)
        col3.metric("Progress %", f"{progress}%")

        topic_data = df["Topic"].value_counts().reset_index()
        topic_data.columns = ["Topic", "Count"]

        fig = px.pie(topic_data, names="Topic", values="Count",
                     hole=0.4, title="Topic-wise Distribution")
        st.plotly_chart(fig, use_container_width=True)

        diff_data = df["Difficulty"].value_counts().reset_index()
        diff_data.columns = ["Difficulty", "Count"]

        fig2 = px.bar(diff_data, x="Difficulty", y="Count",
                      title="Difficulty Distribution")
        st.plotly_chart(fig2, use_container_width=True)