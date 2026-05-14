import streamlit as st
import pandas as pd
import requests

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

        # Apple RSS JSON
        url = (
            f"https://itunes.apple.com/"
            f"{country}/rss/customerreviews/"
            f"id={app_id}/json"
        )

        response = requests.get(url)

        if response.status_code != 200:
            st.error(
                f"HTTP Error: {response.status_code}"
            )
            st.stop()

        data = response.json()

        entries = data["feed"]["entry"]

        reviews = []

        # 最初の1件はアプリ情報なので除外
        for entry in entries[1:review_count + 1]:

            review = {
                "author": entry["author"]["name"]["label"],
                "title": entry["title"]["label"],
                "review": entry["content"]["label"],
                "rating": entry["im:rating"]["label"],
                "version": entry["im:version"]["label"],
                "updated": entry["updated"]["label"]
            }

            reviews.append(review)

        if len(reviews) == 0:
            st.warning("レビューが取得できませんでした")
            st.stop()

        df = pd.DataFrame(reviews)

        st.success(
            f"{len(df)}件取得しました"
        )

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