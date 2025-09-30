import json
import pandas as pd

def load_data(filepath):
    """
    Load JSON data from a file.
    """
    with open(filepath, "r") as f:
        return json.load(f)

def save_timetable(timetable, txt_path, csv_path):
    """
    Save timetable to TXT and CSV.
    """
    # Save TXT
    with open(txt_path, "w") as f:
        for entry in timetable:
            f.write(f"{entry['slot']} - {entry['course']} "
                    f"({entry['faculty']} in Room {entry['room']})\n")

    # Save CSV
    df = pd.DataFrame(timetable)
    df.to_csv(csv_path, index=False)
