import streamlit as st

from components.api import get_data
from components.styles import load_styles


st.set_page_config(
    page_title="WebScrape Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_styles()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------


# --------------------------------------------------
# HERO
# --------------------------------------------------



# --------------------------------------------------
# GET DATABASE DATA
# --------------------------------------------------

try:

    response = get_data()

    records = response.get(
        "data",
        []
    )

    total_records = len(records)

    websites = len(
        set(
            record["url"]
            for record in records
        )
    )

    api_status = "Connected"

except Exception:

    records = []

    total_records = 0

    websites = 0

    api_status = "Disconnected"

import streamlit as st

from components.api import get_data
from components.styles import load_styles


st.set_page_config(
    page_title="WebScrape Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_styles()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🌐 WebScrape Pro")

    st.caption(
        "Dynamic Website Scraper"
    )

    st.divider()

    st.markdown(
        """
        ### Platform

        🔍 Website Scraping

        📊 Data Management

        ✏️ Update Records

        🗑️ Delete Records

        🗄️ Database Schema

        📥 CSV Export
        """
    )

    st.divider()

    st.caption("Frontend: Streamlit")
    st.caption("Backend: FastAPI")
    st.caption("Database: PostgreSQL")


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <h1>🌐 WebScrape Pro</h1>

        <p>
        A generic website scraping and data management
        platform built with Python.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# GET DATABASE DATA
# --------------------------------------------------

try:

    response = get_data()

    records = response.get(
        "data",
        []
    )

    total_records = len(records)

    websites = len(
        set(
            record["url"]
            for record in records
        )
    )

    api_status = "Connected"

except Exception:

    records = []

    total_records = 0

    websites = 0

    api_status = "Disconnected"


# --------------------------------------------------
# ANALYZE SCRAPING TYPES
# --------------------------------------------------

dynamic_records = 0
static_records = 0

json_records = 0
json_ld_records = 0
embedded_js_records = 0


for record in records:

    data = record.get("data", {})

    if not isinstance(data, dict):
        continue

    # ----------------------------------------------
    # Dynamic / Playwright
    # ----------------------------------------------

    dynamic_data = data.get(
        "dynamic"
    )

    if (
        isinstance(dynamic_data, dict)
        and dynamic_data.get("rendered") is True
    ):
        dynamic_records += 1

    else:
        static_records += 1

    # ----------------------------------------------
    # JSON / API
    # ----------------------------------------------

    if data.get("json") is not None:
        json_records += 1

    # ----------------------------------------------
    # JSON-LD
    # ----------------------------------------------

    if data.get("json_ld"):
        json_ld_records += 1

    # ----------------------------------------------
    # Embedded JavaScript
    # ----------------------------------------------

    if data.get("embedded_data"):
        embedded_js_records += 1


# --------------------------------------------------
# MAIN METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Records",
        total_records
    )


with col2:

    st.metric(
        "Websites",
        websites
    )


with col3:

    st.metric(
        "Dynamic Websites",
        dynamic_records
    )


with col4:

    st.metric(
        "Static / Standard",
        static_records
    )


st.divider()


# --------------------------------------------------
# SYSTEM STATUS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">System Status</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    if api_status == "Connected":

        st.success(
            "🟢 FastAPI — Connected"
        )

    else:

        st.error(
            "🔴 FastAPI — Disconnected"
        )


with col2:

    st.success(
        "🟢 PostgreSQL — Configured"
    )


with col3:

    st.info(
        "🐍 Python Scraper — Active"
    )


st.divider()


# --------------------------------------------------
# SCRAPING ANALYSIS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Scraping Analysis</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        f"""
        ### 🔌 JSON / API

        **{json_records}**

        Records containing direct
        JSON/API data.
        """
    )


with col2:

    st.info(
        f"""
        ### 🧩 JSON-LD

        **{json_ld_records}**

        Records containing
        structured JSON-LD data.
        """
    )


with col3:

    st.info(
        f"""
        ### 📜 Embedded JavaScript

        **{embedded_js_records}**

        Records containing
        embedded JavaScript data.
        """
    )


st.divider()


# --------------------------------------------------
# PROJECT FEATURES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Project Features</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    st.info(
        """
        ### 🔍 Web Scraping

        Scrape data from user-provided
        website URLs.

        Supports HTML, JSON, embedded
        data and JavaScript-rendered pages.
        """
    )

    st.info(
        """
        ### 🔄 CRUD Operations

        Create, read, update and delete
        scraped records through REST APIs.
        """
    )


with col2:

    st.info(
        """
        ### 🗄️ PostgreSQL

        Scraped information is stored
        securely in PostgreSQL using JSONB.
        """
    )

    st.info(
        """
        ### 📥 CSV Export

        Export stored scraping data
        into a CSV file.
        """
    )


# --------------------------------------------------
# RECENT RECORDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Recent Records</div>',
    unsafe_allow_html=True
)


if records:

    for record in records[:5]:

        data = record.get(
            "data",
            {}
        )

        dynamic_data = (
            data.get("dynamic", {})
            if isinstance(data, dict)
            else {}
        )

        is_dynamic = (
            isinstance(dynamic_data, dict)
            and dynamic_data.get("rendered") is True
        )

        scraping_type = (
            "⚡ Dynamic / Playwright"
            if is_dynamic
            else "🌐 Standard / HTML"
        )

        with st.expander(
            f"#{record['id']} — "
            f"{record['title'] or 'Untitled'}"
        ):

            st.write(
                f"**URL:** {record['url']}"
            )

            st.write(
                f"**Scraping Type:** {scraping_type}"
            )

            st.write(
                f"**Created:** {record['created_at']}"
            )

else:

    st.info(
        "No records available. Start by scraping a website."
    )