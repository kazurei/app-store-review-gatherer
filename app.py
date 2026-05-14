##import streamlit as st
##import pandas as pd
##
##from app_store_reviews_reader import AppStoreReviewsReader
##
##st.title("App Store レビュー取得")
##
##app_id = st.text_input(
##    "App ID",
##    "1325457827"
##)
##
##country = st.selectbox(
##    "国",
##    ["jp", "us"]
##)
##
##review_count = st.slider(
##    "取得件数",
##    10,
##    1000,
##    100
##)
##
##if st.button("取得開始"):
##
##    try:
##
##        reader = AppStoreReviewsReader()
##
##        reviews = reader.reviews(
##            app_id=app_id,
##            country=country
##        )
##
##        df = pd.DataFrame(reviews)
##
##        df = df.head(review_count)
##
##        st.success(
##            f"{len(df)}件取得"
##        )
##
##        st.dataframe(df)
##
##        csv = df.to_csv(
##            index=False,
##            encoding="utf-8-sig"
##        ).encode("utf-8-sig")
##
##        st.download_button(
##            "CSVダウンロード",
##            csv,
##            "reviews.csv",
##            "text/csv"
##        )
##
##    except Exception as e:
##        st.error(e)
####import streamlit as st
####import pandas as pd
####from app_store_reviews_reader import AppStoreReviewsReader
####
####st.title("App Store レビュー取得")
####
####app_id = st.text_input(
####    "App ID",
####    "1325457827"
####)
####
####if st.button("取得"):
####
####    reader = AppStoreReviewsReader()
####
####    reviews = reader.reviews(
####        app_id=app_id,
####        country="jp"
####    )
####
####    df = pd.DataFrame(reviews)
####
####    st.dataframe(df)
import streamlit as st
import pandas as pd

from app_store_reviews_reader.app_store_reviews_reader import (
    AppStoreReviewsReader
)

st.title("import成功")