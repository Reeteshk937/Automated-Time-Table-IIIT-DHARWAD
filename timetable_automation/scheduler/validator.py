def validate_templates(data):
    errors = []

    if "Room Number" not in data["rooms"].columns:
        errors.append("⚠️ Missing 'Room Number' column in classroom database")
    if "Type" not in data["rooms"].columns:
        errors.append("⚠️ Missing 'Type' column in classroom database")

    # Existing checks
    for name, df in data.items():
        if df.isnull().any().any():
            errors.append(f"⚠️ Missing values in {name} data")

    return errors
