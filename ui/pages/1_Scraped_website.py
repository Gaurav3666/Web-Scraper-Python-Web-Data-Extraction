import streamlit as st

from components.api import scrape_website


st.title("🔍 Scrape Website")

st.write(
    "Enter a website URL and scrape its available data."
)



# URL INPUT

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)


# SCRAPE BUTTON


if st.button(
    "🚀 Start Scraping",
    type="primary",
    use_container_width=True
):

    if not url.strip():

        st.warning(
            "Please enter a website URL."
        )

        st.stop()


    with st.spinner(
        "Scraping website... Please wait."
    ):

        try:

            clean_url = url.strip()

            # URL VALIDATION
        

            if not (
                clean_url.startswith("http://")
                or clean_url.startswith("https://")
            ):

                st.error(
                    "❌ Invalid URL"
                )

                st.info(
                    "Please enter a valid website URL "
                    "starting with http:// or https://"
                )

                st.stop()



            # SCRAPE WEBSITE
    

            result = scrape_website(
                clean_url
            )


        except TimeoutError:

            st.error(
                "⏱️ Request Timed Out"
            )

            st.info(
                "The website took too long to respond. "
                "Please try again later."
            )

            st.stop()


        except ConnectionError:

            st.error(
                "🌐 Connection Failed"
            )

            st.info(
                "The website could not be reached. "
                "Please check the URL or your internet connection."
            )

            st.stop()


        except Exception as e:

            st.error(
                "❌ Scraping Failed"
            )

            st.info(
                "Something unexpected happened while "
                "scraping this website."
            )

            with st.expander(
                "🔧 Technical Error Details"
            ):

                st.code(
                    str(e)
                )

            st.stop()


   
    # SUCCESS
   

    st.success(
        "Website scraped successfully!"
    )



    # BASIC RESULT DATA
   

    record_id = result.get(
        "record_id"
    )


    scraped_url = result.get(
        "url",
        clean_url
    )


    data = result.get(
        "data",
        {}
    )



    # EXTRACT SOURCES


    html_data = data.get(
        "html"
    ) or {}


    # IMPORTANT:
    # Links are extracted here only once.
    links = html_data.get(
        "links",
        []
    )


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



    # SCRAPING METHOD DETECTION


    scraping_method = (
        "🌐 Requests + BeautifulSoup"
    )


    method_description = (
        "Data was extracted directly from "
        "the initial HTML response."
    )


    if dynamic_data:

        rendered = dynamic_data.get(
            "rendered",
            False
        )


        if rendered:

            scraping_method = (
                "⚡ Dynamic / Playwright"
            )

            method_description = (
                "The website required browser-based "
                "rendering to access its content."
            )

        else:

            scraping_method = (
                "🌐 Requests + BeautifulSoup"
            )

            method_description = (
                "Browser rendering was not required."
            )


    elif json_data is not None:

        scraping_method = (
            "🔌 Direct JSON / API"
        )

        method_description = (
            "The website returned data directly "
            "as a JSON/API response."
        )


    elif embedded_data:

        scraping_method = (
            "📜 Embedded JavaScript"
        )

        method_description = (
            "Structured data was found inside "
            "JavaScript code."
        )


    elif json_ld:

        scraping_method = (
            "🧩 JSON-LD"
        )

        method_description = (
            "Structured JSON-LD data was found "
            "inside the HTML."
        )



    # BASIC INFORMATION


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "### 🆔 Record ID"
        )

        st.metric(
            "Record",
            record_id
        )


    with col2:

        st.markdown(
            "### 🌐 Website"
        )

        st.code(
            scraped_url
        )



    # PAGE TITLE


    title = html_data.get(
        "title"
    )


    if title:

        st.markdown(
            "### 📄 Page Title"
        )

        st.info(
            title
        )


   
    # SCRAPING METHOD
 

    st.markdown(
        "### 🔍 Scraping Method"
    )


    col1, col2 = st.columns(
        [1, 2]
    )


    with col1:

        st.success(
            scraping_method
        )


    with col2:

        st.info(
            method_description
        )


    
    # WEBSITE ANALYSIS
  

    st.divider()


    st.markdown(
        "## 🌐 Website Analysis"
    )


    st.caption(
        "Summary of the information detected during scraping."
    )


   
    # HTML DATA


    headings = html_data.get(
        "headings",
        []
    )


    paragraphs = html_data.get(
        "paragraphs",
        []
    )


    images = html_data.get(
        "images",
        []
    )



    # FIRST ROW


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📄 Page Title",
            "Found" if title else "Not Found"
        )


    with col2:

        st.metric(
            "🔤 Headings",
            len(headings)
        )


    with col3:

        st.metric(
            "📝 Paragraphs",
            len(paragraphs)
        )


    with col4:

        st.metric(
            "🔗 Links",
            len(links)
        )


    st.write("")


   
    # SECOND ROW
    

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🖼️ Images",
            len(images)
        )


    with col2:

        st.metric(
            "🔌 JSON / API",
            "Found" if json_data is not None else "Not Found"
        )


    with col3:

        st.metric(
            "🧩 JSON-LD",
            "Found" if json_ld else "Not Found"
        )


    with col4:

        st.metric(
            "📜 Embedded JS",
            "Found" if embedded_data else "Not Found"
        )


    # -----------------------------------------------------
    # BROWSER RENDERING
    # -----------------------------------------------------

    browser_rendered = False


    if dynamic_data:

        browser_rendered = dynamic_data.get(
            "rendered",
            False
        )


    st.write("")


    if browser_rendered:

        st.success(
            "⚡ Browser Rendered: Yes — Playwright was used."
        )

    else:

        st.info(
            "⚡ Browser Rendered: No — browser rendering was not required."
        )


    # ANALYSIS SUMMARY
   

    st.markdown(
        "### 📊 Analysis Summary"
    )


    analysis_col1, analysis_col2 = st.columns(2)


    with analysis_col1:

        st.write(
            f"**Total Headings:** {len(headings)}"
        )

        st.write(
            f"**Total Paragraphs:** {len(paragraphs)}"
        )

        st.write(
            f"**Total Links:** {len(links)}"
        )

        st.write(
            f"**Total Images:** {len(images)}"
        )


    with analysis_col2:

        st.write(
            f"**JSON/API:** "
            f"{'Available' if json_data is not None else 'Not Available'}"
        )

        st.write(
            f"**JSON-LD:** "
            f"{'Available' if json_ld else 'Not Available'}"
        )

        st.write(
            f"**Embedded JavaScript:** "
            f"{'Available' if embedded_data else 'Not Available'}"
        )

        st.write(
            f"**Browser Rendering:** "
            f"{'Used' if browser_rendered else 'Not Used'}"
        )


    st.divider()


  
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

           
            # HEADINGS
           

            st.markdown(
                "### 🔤 Headings"
            )


            if headings:

                st.caption(
                    f"{len(headings)} heading(s) found"
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

                st.caption(
                    f"{len(paragraphs)} paragraph(s) found"
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

                st.caption(
                    f"{len(links)} link(s) found"
                )


                            # SEARCH LINKS
                search = st.text_input(
                    "🔎 Search links",
                    key=f"scrape_links_{record_id}",
                    placeholder="Search link name or URL..."
                )


                if search:

                    search_text = search.lower()

                    filtered_links = []


                    for link in links:

                        # New format:
                        # {
                        #     "text": "About",
                        #     "url": "https://..."
                        # }

                        if isinstance(link, dict):

                            link_text = str(
                                link.get(
                                    "text",
                                    ""
                                )
                            )


                            link_url = str(
                                link.get(
                                    "url",
                                    ""
                                )
                            )


                            if (
                                search_text in link_text.lower()
                                or search_text in link_url.lower()
                            ):

                                filtered_links.append(
                                    link
                                )


                        # Old format:
                        # "https://example.com/about"

                        else:

                            if (
                                search_text
                                in str(link).lower()
                            ):

                                filtered_links.append(
                                    link
                                )


                else:

                    filtered_links = links


                              # LINK COUNT
                    st.write(
                    f"Showing "
                    f"{min(len(filtered_links), 100)} "
                    f"of "
                    f"{len(links)} "
                    f"links"
                )


                              # DISPLAY LINKS
                    for index, link in enumerate(
                    filtered_links[:100],
                    start=1
                ):

                    # New dictionary format
                        if isinstance(link, dict):

                            link_text = link.get(
                            "text",
                            "Untitled Link"
                        )


                        link_url = link.get(
                            "url",
                            "URL not available"
                        )


                        st.markdown(
                            f"**{index}. {link_text}**"
                        )


                        st.caption(
                            str(link_url)
                        )


                    # Old string format
                    else:

                        st.markdown(
                            f"**{index}. Untitled Link**"
                        )


                        st.caption(
                            str(link)
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

                st.caption(
                    f"{len(images)} image(s) found"
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
                    "Browser-based rendering was used "
                    "to access the website content."
                )

            else:

                st.info(
                    "Browser rendering was not required."
                )