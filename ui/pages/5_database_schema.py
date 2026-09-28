import streamlit as st

from components.api import (
    get_tables,
    get_schema
)


st.title("🗄️ Database Schema")

st.write(
    "Explore database tables, columns and data types."
)


try:

    table_response = get_tables()

    tables = table_response.get(
        "tables",
        []
    )

    if not tables:

        st.info(
            "No tables found."
        )

    else:

        selected_table = st.selectbox(
            "Select Table",
            tables
        )

        if selected_table:

            schema = get_schema(
                selected_table
            )

            columns = schema.get(
                "columns",
                []
            )

            st.subheader(
                f"Table: {selected_table}"
            )

            st.dataframe(
                columns,
                use_container_width=True,
                hide_index=True
            )


except Exception as e:

    st.error(
        f"Could not load schema: {e}"
    )