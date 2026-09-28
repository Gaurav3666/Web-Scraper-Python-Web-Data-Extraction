import streamlit as st


from components.api import (
    get_data,
    update_record
)


st.title("✏️ Update Record")

st.write(
    "Update the title, headings and paragraphs of an existing record."
)


# GET ALL RECORDS


try:

    response = get_data()

    records = response.get(
        "data",
        []
    )

except Exception as e:

    st.error(
        f"Unable to load records: {e}"
    )

    st.stop()



# CHECK RECORDS


if not records:

    st.info(
        "No scraped records available."
    )

    st.stop()



# SELECT RECORD


record_options = {}


for record in records:

    record_id = record.get(
        "id"
    )

    title = record.get(
        "title"
    ) or "Untitled"

    label = f"{record_id} - {title}"

    record_options[label] = record_id


selected_label = st.selectbox(
    "Select Record ID",
    list(record_options.keys())
)


selected_id = record_options[
    selected_label
]



# FIND SELECTED RECORD


selected_record = None


for record in records:

    if record.get("id") == selected_id:

        selected_record = record

        break


if selected_record is None:

    st.error(
        "Selected record not found."
    )

    st.stop()



# GET CURRENT DATA


current_title = selected_record.get(
    "title",
    ""
)


current_data = selected_record.get(
    "data",
    {}
)


html_data = current_data.get(
    "html",
    {}
) or {}


current_headings = html_data.get(
    "headings",
    []
) or []


current_paragraphs = html_data.get(
    "paragraphs",
    []
) or []



# TITLE


st.subheader("📝 Title")


new_title = st.text_input(
    "Title",
    value=current_title
)


# HEADINGS


st.subheader("📌 Headings")


new_headings_text = st.text_area(
    "Headings",
    value="\n".join(
        str(heading)
        for heading in current_headings
    ),
    height=180,
    help="Write one heading per line."
)



# PARAGRAPHS


st.subheader("📄 Paragraphs")


new_paragraphs_text = st.text_area(
    "Paragraphs",
    value="\n\n".join(
        str(paragraph)
        for paragraph in current_paragraphs
    ),
    height=300,
    help="Separate different paragraphs using a blank line."
)



# UPDATE BUTTON


st.divider()


if st.button(
    "💾 Update Record",
    type="primary",
    use_container_width=True
):

   
    # VALIDATE TITLE


    if not new_title.strip():

        st.warning(
            "Title cannot be empty."
        )

        st.stop()


    # PREPARE HEADINGS


    new_headings = [

        heading.strip()

        for heading in new_headings_text.splitlines()

        if heading.strip()
    ]



    # PREPARE PARAGRAPHS


    new_paragraphs = [

        paragraph.strip()

        for paragraph in new_paragraphs_text.split("\n\n")

        if paragraph.strip()
    ]


    # UPDATE


    try:

        result = update_record(

            int(selected_id),

            new_title.strip(),

            new_headings,

            new_paragraphs
        )


        st.success(
            result.get(
                "message",
                "Record updated successfully."
            )
        )


        st.write(
            f"Updated Record ID: {selected_id}"
        )


    except Exception as e:

        st.error(
            f"Update failed: {e}"
        )