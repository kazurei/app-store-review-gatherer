import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="App Store Large Review Scraper",
    layout="wide"
)

st.title("App Store 大量レビュー取得")

app_id = st.text_input(
    "App ID",
    "1606356401"
)

country = st.selectbox(
    "国",
    ["jp", "us"],
    index=0
)

max_reviews = st.number_input(
    "最大取得件数",
    min_value=100,
    max_value=50000,
    value=10000,
    step=200
)

if st.button("取得開始"):

    all_reviews = []

    progress = st.progress(0)

    try:

        page = 1

        while len(all_reviews) < max_reviews:

            url = (
                f"https://itunes.apple.com/"
                f"{country}/rss/customerreviews/"
                f"page={page}/id={app_id}/sortby=mostrecent/json"
            )

            response = requests.get(url)

            if response.status_code != 200:
                break

            data = response.json()

            if "feed" not in data:
                break

            if "entry" not in data["feed"]:
                break

            entries = data["feed"]["entry"]

            if len(entries) <= 1:
                break

            # 最初はアプリ情報
            for entry in entries[1:]:

                try:

                    review = {
                        "author": entry["author"]["name"]["label"],
                        "title": entry["title"]["label"],
                        "review": entry["content"]["label"],
                        "rating": entry["im:rating"]["label"],
                        "version": entry["im:version"]["label"],
                        "updated": entry["updated"]["label"]
                    }

                    all_reviews.append(review)

                    if len(all_reviews) >= max_reviews:
                        break

                except:
                    continue

            page += 1

            progress.progress(
                min(len(all_reviews) / max_reviews, 1.0)
            )

            time.sleep(0.5)

        if len(all_reviews) == 0:

            st.warning("レビュー取得失敗")

        else:

            df = pd.DataFrame(all_reviews)

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