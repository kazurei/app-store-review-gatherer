import streamlit as st
import pandas as pd
from app_store_scraper import AppStore
import time

st.set_page_config(page_title="App Store Review Scraper", layout="wide")

st.title("App Store レビュー取得ツール")

st.write("App Store のレビューを取得してCSV保存できます。")

# 入力欄
app_name = st.text_input(
    "アプリ名",
    value="ウマ娘 プリティーダービー"
)

app_id = st.text_input(
    "App ID",
    value="1325457827"
)

country = st.selectbox(
    "国",
    ["jp", "us"],
    index=0
)

review_count = st.number_input(
    "取得件数",
    min_value=1,
    max_value=5000,
    value=500,
    step=100
)

# 実行
if st.button("レビュー取得開始"):

    with st.spinner("レビュー取得中..."):

        try:
            app = AppStore(
                country=country,
                app_name=app_name,
                app_id=int(app_id)
            )

            # レビュー取得
            app.review(
                how_many=review_count
            )

            reviews = app.reviews

            if len(reviews) == 0:
                st.warning("レビューを取得できませんでした。")
            else:

                df = pd.DataFrame(reviews)

                # 必要列だけ残す
                keep_columns = [
                    "date",
                    "rating",
                    "title",
                    "review",
                    "userName"
                ]

                existing_columns = [
                    col for col in keep_columns
                    if col in df.columns
                ]

                df = df[existing_columns]

                st.success(f"{len(df)} 件取得しました。")

                st.dataframe(df)

                # CSV保存
                csv = df.to_csv(
                    index=False,
                    encoding="utf-8-sig"
                ).encode("utf-8-sig")

                st.download_button(
                    label="CSVダウンロード",
                    data=csv,
                    file_name=f"{app_name}_reviews.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"エラー: {e}")