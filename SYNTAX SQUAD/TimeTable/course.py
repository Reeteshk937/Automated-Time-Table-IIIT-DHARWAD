def create_course(code, name, credits, faculty, semester):
    """
    Create a course dictionary.
    """
    return {
        "code": code,
        "name": name,
        "credits": credits,
        "faculty": faculty,
        "semester": semester
    }
