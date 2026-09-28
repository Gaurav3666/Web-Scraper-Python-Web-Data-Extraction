import streamlit as st


def load_styles():

    st.markdown(
        """
        <style>

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 30px;
            border-radius: 18px;
            margin-bottom: 25px;
            background: linear-gradient(
                135deg,
                #111827,
                #1f2937
            );
        }

        .hero h1 {
            color: white;
            font-size: 38px;
            margin-bottom: 8px;
        }

        .hero p {
            color: #d1d5db;
            font-size: 17px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            margin-top: 20px;
            margin-bottom: 15px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )