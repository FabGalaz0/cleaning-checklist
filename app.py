import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CSV file path (define once at the top) ---
csv_file = "cleaning_records.csv"

# --- Page Title ---
st.title("🏥  Cleaning Checklist")

# --- Staff & Area Selection ---
st.sidebar.header("Cleaner Information")
staff_name = st.sidebar.text_input("Staff Name")
area = st.sidebar.selectbox("Select Area", ["Ward 1", "Ward 2", "Ward 3", "Kitchen", "Lobby", "Toilets"])

# --- Checklist ---
st.header(f"🧹 Cleaning Tasks for {area}")

tasks = [
    "Floors mopped and free of spills",
    "Bins emptied and replaced with liners",
    "High-touch surfaces disinfected",
    "Bathrooms/toilets cleaned",
    "Supplies restocked (soap, paper towels)",
    "Equipment cleaned and returned"
]

completed_tasks = []
for task in tasks:
    if st.checkbox(task):
        completed_tasks.append(task)

# --- Save Results ---
if st.button("✅ Save Checklist"):
    if staff_name.strip() == "":
        st.warning("Please enter staff name before saving.")
    else:
        # Create a record
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "Staff": staff_name,
            "Area": area,
            "Tasks Completed": ", ".join(completed_tasks),
            "Date/Time": now
        }

        # Save to CSV
        try:
            df = pd.read_csv(csv_file)
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([record])

        df.to_csv(csv_file, index=False)
        st.success("Checklist saved successfully!")

# --- View Records ---
if st.checkbox("📋 Show Completed Records"):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        st.dataframe(df)
    else:
        st.info("No records found yet.")

# --- Download CSV Button ---
if os.path.exists(csv_file):
    st.download_button(
        label="📥 Download Full Checklist CSV",
        data=open(csv_file, "rb").read(),
        file_name="cleaning_records.csv",
        mime="text/csv"
    )
else:
    st.info("No records yet to download.")
