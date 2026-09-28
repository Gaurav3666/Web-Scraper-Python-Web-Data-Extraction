import csv
import io
import json

import streamlit as st

from components.api import get_data


st.title("📥 CSV Export")

st.write(
    "Export scraped records into a CSV file."
)


try:

    response = get_data()

    records = response.get(
        "data",
        []
    )

    if not records:

        st.info(
            "No data available for export."
        )

    else:

        st.success(
            f"{len(records)} record(s) available."
        )

        if st.button(
            "📄 Generate CSV",
            type="primary",
            use_container_width=True
        ):

            output = io.StringIO()

            writer = csv.writer(
                output
            )

            writer.writerow([
                "id",
                "url",
                "title",
                "data",
                "created_at",
                "updated_at"
            ])

            for record in records:

                writer.writerow([
                    record["id"],
                    record["url"],
                    record["title"],
                    json.dumps(
                        record["data"],
                        default=str
                    ),
                    record["created_at"],
                    record["updated_at"]
                ])

            csv_data = output.getvalue()

            st.success(
                "CSV generated successfully!"
            )

            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name="scraped_data.csv",
                mime="text/csv",
                use_container_width=True
            )


except Exception as e:

    st.error(
        f"CSV export failed: {e}"
    )