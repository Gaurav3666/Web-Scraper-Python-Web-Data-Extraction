import streamlit as st

from components.api import delete_record


st.title("🗑️ Delete Record")

st.warning(
    "Deleting a record is permanent."
)


record_id = st.number_input(
    "Record ID",
    min_value=1,
    step=1
)


confirm = st.checkbox(
    "I understand that this record will be permanently deleted."
)


if st.button(
    "🗑️ Delete Record",
    type="primary",
    use_container_width=True
):

    if not confirm:

        st.warning(
            "Please confirm deletion first."
        )

    else:

        try:

            result = delete_record(
                int(record_id)
            )

            st.success(
                result.get(
                    "message",
                    "Record deleted successfully."
                )
            )

        except Exception as e:

            st.error(
                f"Delete failed: {e}"
            )