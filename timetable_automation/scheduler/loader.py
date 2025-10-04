import pandas as pd
import os

def load_all(data_dir="data_templates"):
    """Loads all CSV templates and Excel databases."""
    def read_any(path):
        if path.endswith(".xlsx"):
            return pd.read_excel(path)
        return pd.read_csv(path)

    data = {
        "courses": read_any(os.path.join(data_dir, "course_data.csv")),
        "faculty": read_any(os.path.join(data_dir, "faculty_availability.csv")),
        # Use the uploaded Excel classroom database instead of CSV:
        "rooms": read_any(os.path.join(data_dir, "classroom_database.xlsx")),
        "students": read_any(os.path.join(data_dir, "student_data.csv")),
        "slots": read_any(os.path.join(data_dir, "slot_mapping_template.csv")),
        "constraints": read_any(os.path.join(data_dir, "constraint_data_template.csv")),
    }
    return data
