import streamlit as st
import pandas as pd
import feedparser

st.set_page_config(
    page_title="App Store Review Scraper",
    layout="wide"
)

st.title("App Store レビュー取得")

app_id = st.text_input(
    "App ID",
    "1325457827"
)

country = st.selectbox(
    "国",
    ["jp", "us"],
    index=0
)

review_count = st.slider(
    "取得件数",
    10,
    500,
    100
)

if st.button("レビュー取得"):

    try:

        # Apple RSS Review Feed
        url = (
            f"https://itunes.apple.com/"
            f"{country}/rss/customerreviews/"
            f"id={app_id}/sortBy=mostRecent/json"
        )

        feed = feedparser.parse(url)

        entries = feed.entries

        reviews = []

        for entry in entries[:review_count]:

            review = {
                "author": entry.get("author", ""),
                "title": entry.get("title", ""),
                "review": entry.get("summary", ""),
                "published": entry.get("published", "")
            }

            reviews.append(review)

        if len(reviews) == 0:
            st.warning("レビュー取得失敗")
            st.stop()

        df = pd.DataFrame(reviews)

        st.success(f"{len(df)}件取得")

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False,
            encoding="utf-8-sig"
        ).encode("utf-8-sig")

        st.download_button(
            "CSVダウンロード",
            data=csv,
            file_name="appstore_reviews.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(e)