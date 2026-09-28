import streamlit as st

from components.api import get_data


st.title("📊 Scraped Data")

st.write(
    "Explore scraped website data from different available sources."
)


# LOAD DATA


try:

    response = get_data()

    records = response.get(
        "data",
        []
    )

except Exception as e:

    st.error(
        f"Could not load data: {e}"
    )

    st.stop()



# NO DATA


if not records:

    st.info(
        "No scraped records found."
    )

    st.stop()


# SUMMARY

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Records",
        len(records)
    )


with col2:

    st.metric(
        "Websites",
        len(
            set(
                record["url"]
                for record in records
            )
        )
    )


with col3:

    st.metric(
        "Storage",
        "PostgreSQL"
    )


st.divider()



# SEARCH AND FILTER


st.subheader(
    "🔎 Search & Filter"
)


col1, col2 = st.columns(
    [2, 1]
)


with col1:

    search_query = st.text_input(
        "Search records",
        placeholder="Search by website URL or page title..."
    )


with col2:

    method_filter = st.selectbox(
        "Filter by scraping method",
        [
            "All Methods",
            "🌐 Standard HTML",
            "⚡ Dynamic / Playwright",
            "🔌 Direct JSON / API",
            "🧩 JSON-LD",
            "📜 Embedded JavaScript"
        ]
    )



# FILTER RECORDS


filtered_records = []


for current_record in records:

    record_url = current_record.get(
        "url",
        ""
    )


    record_title = current_record.get(
        "title",
        ""
    ) or ""


    record_data = current_record.get(
        "data",
        {}
    )


    if not isinstance(
        record_data,
        dict
    ):
        record_data = {}


    json_data = record_data.get(
        "json"
    )


    json_ld = record_data.get(
        "json_ld",
        []
    )


    embedded_data = record_data.get(
        "embedded_data",
        []
    )


    dynamic_data = record_data.get(
        "dynamic"
    )



    # DETERMINE SCRAPING METHOD
 

    if (
        isinstance(
            dynamic_data,
            dict
        )
        and dynamic_data.get(
            "rendered"
        ) is True
    ):

        record_method = (
            "⚡ Dynamic / Playwright"
        )

    elif json_data is not None:

        record_method = (
            "🔌 Direct JSON / API"
        )

    elif embedded_data:

        record_method = (
            "📜 Embedded JavaScript"
        )

    elif json_ld:

        record_method = (
            "🧩 JSON-LD"
        )

    else:

        record_method = (
            "🌐 Standard HTML"
        )



    # SEARCH FILTER


    search_matches = True


    if search_query.strip():

        query = search_query.lower().strip()

        search_matches = (
            query in record_url.lower()
            or query in record_title.lower()
        )



    # METHOD FILTER


    method_matches = True


    if method_filter != "All Methods":

        method_matches = (
            record_method == method_filter
        )


    # FINAL FILTER
 

    if search_matches and method_matches:

        filtered_records.append(
            {
                "record": current_record,
                "method": record_method
            }
        )



# FILTER RESULT


st.divider()


st.markdown(
    "### 📋 Filter Results"
)


st.write(
    f"Showing **{len(filtered_records)}** "
    f"of **{len(records)}** records."
)


if not filtered_records:

    st.warning(
        "No records match your search/filter."
    )

    st.stop()



# SELECT RECORD

record_options = {}


for item in filtered_records:

    current_record = item["record"]

    title = current_record.get(
        "title"
    ) or "Untitled"


    method = item["method"]


    label = (
        f"#{current_record['id']} — "
        f"{title} — "
        f"{method}"
    )


    record_options[label] = current_record


selected_record = st.selectbox(
    "Select a scraped record",
    list(
        record_options.keys()
    )
)


record = record_options[
    selected_record
]



# BASIC INFORMATION


st.divider()


st.subheader(
    f"Record #{record['id']}"
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "### 🌐 Website"
    )

    st.code(
        record["url"]
    )


with col2:

    st.markdown(
        "### 📄 Title"
    )

    st.write(
        record.get("title")
        or "No title available"
    )


st.caption(
    f"Created: {record['created_at']}"
)


st.caption(
    f"Updated: {record['updated_at']}"
)



# EXTRACT DATA SOURCES


data = record.get(
    "data",
    {}
)


html_data = data.get(
    "html"
) or {}


json_data = data.get(
    "json"
)


json_ld = data.get(
    "json_ld",
    []
)


embedded_data = data.get(
    "embedded_data",
    []
)


dynamic_data = data.get(
    "dynamic"
)



# SOURCE TABS


(
    tab_html,
    tab_json,
    tab_jsonld,
    tab_js,
    tab_dynamic
) = st.tabs(
    [
        "🌐 HTML",
        "🔌 JSON / API",
        "🧩 JSON-LD",
        "📜 Embedded JavaScript",
        "⚡ Dynamic"
    ]
)



# HTML TAB


with tab_html:

    st.subheader(
        "HTML Data"
    )


    if not html_data:

        st.info(
            "No HTML data was extracted."
        )

    else:

        html_title = html_data.get(
            "title"
        )


        headings = html_data.get(
            "headings",
            []
        )


        paragraphs = html_data.get(
            "paragraphs",
            []
        )


        links = html_data.get(
            "links",
            []
        )


        images = html_data.get(
            "images",
            []
        )



        # TITLE


        st.markdown(
            "### 📄 Page Title"
        )


        if html_title:

            st.info(
                html_title
            )

        else:

            st.write(
                "No title found."
            )


        # HEADINGS
 

        st.markdown(
            "### 🔤 Headings"
        )


        if headings:

            st.write(
                f"{len(headings)} heading(s) found."
            )


            for index, heading in enumerate(
                headings[:100],
                start=1
            ):

                st.write(
                    f"**{index}.** {heading}"
                )

        else:

            st.info(
                "No headings found."
            )



        # PARAGRAPHS


        st.markdown(
            "### 📝 Paragraphs"
        )


        if paragraphs:

            st.write(
                f"{len(paragraphs)} paragraph(s) found."
            )


            for paragraph in paragraphs[:30]:

                st.write(
                    paragraph
                )

        else:

            st.info(
                "No paragraphs found."
            )



        # LINKS


        st.markdown(
            "### 🔗 Links"
        )


        if links:

            st.write(
                f"{len(links)} link(s) found."
            )


            link_search = st.text_input(
                "Search links",
                key=f"link_search_{record['id']}",
                placeholder="Search for a link..."
            )


            if link_search:

                filtered_links = [
                    link
                    for link in links
                    if link
                    and link_search.lower()
                    in link.lower()
                ]

            else:

                filtered_links = links


            st.write(
                f"Showing "
                f"{min(len(filtered_links), 100)} "
                f"of {len(links)} links."
            )


            for index, link in enumerate(
                filtered_links[:100],
                start=1
            ):

                st.write(
                    f"{index}. {link}"
                )

        else:

            st.info(
                "No links found."
            )



        # IMAGES

        st.markdown(
            "### 🖼️ Images"
        )


        if images:

            st.write(
                f"{len(images)} image(s) found."
            )


            for index, image in enumerate(
                images[:50],
                start=1
            ):

                st.write(
                    f"{index}. {image}"
                )

        else:

            st.info(
                "No images found."
            )


# JSON / API TAB

with tab_json:

    st.subheader(
        "JSON / API Data"
    )


    if json_data is None:

        st.info(
            "No direct JSON/API response was detected."
        )

    else:

        st.success(
            "JSON/API data detected."
        )


        st.json(
            json_data
        )


# JSON-LD TAB

with tab_jsonld:

    st.subheader(
        "JSON-LD Structured Data"
    )


    if not json_ld:

        st.info(
            "No JSON-LD data found."
        )

    else:

        st.success(
            f"{len(json_ld)} JSON-LD object(s) found."
        )


        for index, item in enumerate(
            json_ld,
            start=1
        ):

            with st.expander(
                f"JSON-LD Object {index}"
            ):

                st.json(
                    item
                )


# EMBEDDED JAVASCRIPT TAB

with tab_js:

    st.subheader(
        "Embedded JavaScript Data"
    )


    if not embedded_data:

        st.info(
            "No embedded JavaScript data found."
        )

    else:

        st.success(
            f"{len(embedded_data)} "
            f"embedded data object(s) found."
        )


        for index, item in enumerate(
            embedded_data,
            start=1
        ):

            with st.expander(
                f"Embedded Data {index}"
            ):

                st.json(
                    item
                )


# DYNAMIC TAB

with tab_dynamic:

    st.subheader(
        "Dynamic / Browser Rendered Data"
    )


    if not dynamic_data:

        st.info(
            "No dynamic rendering information available."
        )

    else:

        rendered = dynamic_data.get(
            "rendered",
            False
        )


        if rendered:

            st.success(
                "This website was rendered using Playwright."
            )


            st.write(
                "The page required browser-based rendering "
                "to access its content."
            )

        else:

            st.info(
                "No browser rendering was required."
            )