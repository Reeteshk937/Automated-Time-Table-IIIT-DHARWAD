import os
import sys
import pandas as pd
import openpyxl
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, escape

# --- Configuration ---
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = BASE_DIR / "output_timetables"
TEMPLATE_DIR = BASE_DIR / "templates"

# Define available semesters and sections
DATA = {
    'semesters': [
        {'file': 'sem1_timetable.xlsx', 'name': 'Semester 1'},
        {'file': 'sem3_timetable.xlsx', 'name': 'Semester 3'},
        {'file': 'sem5_timetable.xlsx', 'name': 'Semester 5'},
        {'file': 'sem7_timetable.xlsx', 'name': 'Semester 7'}
    ],
    'sections': ['Section A', 'Section B', 'Student View', 'Faculty View']
}

def setup_environment():
    """Create necessary directories."""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(TEMPLATE_DIR, exist_ok=True)
        return True
    except Exception as e:
        print(f"ERROR: Failed to create directories: {str(e)}")
        return False

# HTML Templates
DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timetable Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8fafc; }
        .sidebar { background: #1e3a8a; min-height: 100vh; color: #fff; padding: 20px; }
        .sidebar .form-label { color: #fff; }
        .sidebar .form-select { background: #2563eb; border: none; color: #fff; margin-bottom: 1rem; }
        .sidebar .form-select option { color: #000; }
        .card { border: none; border-radius: 16px; box-shadow: 0 4px 16px rgba(31,38,135,0.08); }
        .card-title { color: #2563eb; }
        .btn-primary { background: #2563eb; border: none; }
        .btn-primary:hover { background: #1e40af; }
        .table-section { margin-top: 2rem; }
    </style>
</head>
<body>
<div class="container-fluid">
    <div class="row">
        <nav class="col-md-2 d-none d-md-block sidebar">
            <div class="text-center mb-4">
                <h3>Dashboard</h3>
            </div>
            <form>
                <div class="mb-3">
                    <label class="form-label" for="semesterSelect">Semester</label>
                    <select class="form-select" id="semesterSelect">
                        <option value="all">All Semesters</option>
                        {% for sem in semesters %}
                        <option value="{{ sem }}">{{ sem }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label" for="sectionSelect">Section</label>
                    <select class="form-select" id="sectionSelect">
                        <option value="all">All Sections</option>
                        <option value="Section A">Section A</option>
                        <option value="Section B">Section B</option>
                        <option value="Student View">Student View</option>
                        <option value="Faculty View">Faculty View</option>
                    </select>
                </div>
            </form>
        </nav>

        <main class="col-md-10 ms-sm-auto px-md-4">
            <div class="d-flex justify-content-between align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h1 class="h2">Timetable Dashboard</h1>
                <div>
                    <button class="btn btn-primary" onclick="window.location.reload()">Refresh</button>
                    <button class="btn btn-outline-secondary" onclick="window.print()">Print All</button>
                </div>
            </div>

            <div class="row g-4 mb-4">
                <div class="col-md-3">
                    <div class="card p-3 text-center">
                        <div class="card-title fs-5">Total Timetables</div>
                        <div class="display-6">{{ stats.total_timetables }}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 text-center">
                        <div class="card-title fs-5">Total Courses</div>
                        <div class="display-6">{{ stats.total_courses }}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 text-center">
                        <div class="card-title fs-5">Classrooms</div>
                        <div class="display-6">{{ stats.total_classrooms }}</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 text-center">
                        <div class="card-title fs-5">Faculty</div>
                        <div class="display-6">{{ stats.total_faculty }}</div>
                    </div>
                </div>
            </div>

            <div class="table-section">
                <h3>All Timetables</h3>
                <div class="list-group" id="timetableList">
                    {% for link in semester_links %}
                    <div class="list-group-item d-flex justify-content-between align-items-center" 
                         data-semester="{{ link.semester }}" 
                         data-section="{{ link.section }}">
                        <span>{{ link.name }}</span>
                        <a href="{{ link.file }}" class="btn btn-sm btn-primary" target="_blank">Open</a>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <script>
                const semesterSelect = document.getElementById('semesterSelect');
                const sectionSelect = document.getElementById('sectionSelect');
                const timetableList = document.getElementById('timetableList');

                function filterTimetables() {
                    const sem = semesterSelect.value;
                    const sec = sectionSelect.value;
                    const items = timetableList.children;

                    for (const item of items) {
                        const matchesSem = sem === 'all' || item.dataset.semester === sem;
                        const matchesSec = sec === 'all' || item.dataset.section === sec;
                        item.style.display = matchesSem && matchesSec ? '' : 'none';
                    }
                }

                semesterSelect.addEventListener('change', filterTimetables);
                sectionSelect.addEventListener('change', filterTimetables);
            </script>
        </main>
    </div>
</div>
</body>
</html>
"""

SEMESTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: #f8fafc; 
            font-family: system-ui, -apple-system, sans-serif;
        }
        .container { 
            background: #fff; 
            margin: 40px auto; 
            padding: 32px; 
            border-radius: 20px; 
            box-shadow: 0 8px 32px rgba(31,38,135,0.12); 
            max-width: 1200px; 
        }
        h1 { 
            color: #2563eb; 
            text-align: center; 
            margin-bottom: 32px;
        }
        .btn { margin: 8px 8px 8px 0; }
        .table { 
            background: #fff;
            margin-top: 20px;
        }
        .table th {
            background: #e5edff;
            color: #1e3a8a;
        }
        .table-hover tbody tr:hover {
            background-color: #f8fafc;
        }
        @media print {
            .btn { display: none; }
            .container { 
                box-shadow: none;
                margin: 0;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
<div class="container">
    <a href="index.html" class="btn btn-outline-primary">← Back to Dashboard</a>
    <h1>{{ sem_name }} - {{ section }}</h1>
    <div class="text-center mb-4">
        <button class="btn btn-primary" onclick="window.print()">Print</button>
    </div>
    {{ table | safe }}
</div>
</body>
</html>
"""

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True
)

def generate_table(df):
    """Generate HTML table from DataFrame."""
    try:
        return df.to_html(
            index=False,
            classes='table table-bordered table-hover table-striped align-middle',
            escape=True,
            na_rep=''
        )
    except Exception as e:
        print(f"ERROR: Failed to generate table: {str(e)}")
        return '<div class="alert alert-danger">Failed to generate table</div>'

def process_semester(filepath, sem_name):
    """Process a semester Excel file."""
    try:
        if not filepath.exists():
            print(f"[WARNING] Missing file: {filepath.name}")
            return None

        df_dict = pd.read_excel(filepath, sheet_name=None)
        semester_data = []

        for section, df in df_dict.items():
            if section not in DATA['sections']:
                continue

            # Generate HTML table
            html_table = generate_table(df)
            out_name = f"{filepath.stem}_{section.replace(' ', '_')}.html"
            
            # Create semester page using template
            template = env.get_template('semester.html')
            html = template.render(
                title=f"{sem_name} - {section}",
                sem_name=sem_name,
                section=section,
                table=html_table
            )

            # Write semester page
            output_path = OUTPUT_DIR / out_name
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)

            semester_data.append({
                'name': f"{sem_name} - {section}",
                'file': out_name,
                'semester': sem_name,
                'section': section
            })

        return semester_data

    except Exception as e:
        print(f"ERROR: Failed to process {filepath}: {str(e)}")
        return None

def collect_stats():
    """Collect statistics from timetables."""
    stats = {
        'total_timetables': 0,
        'total_courses': set(),
        'total_classrooms': set(),
        'total_faculty': set()
    }

    for sem in DATA['semesters']:
        filepath = OUTPUT_DIR / sem['file']
        if not filepath.exists():
            continue

        try:
            df_dict = pd.read_excel(filepath, sheet_name=None)
            for df in df_dict.values():
                stats['total_timetables'] += 1
                if 'Course' in df.columns:
                    stats['total_courses'].update(df['Course'].dropna().unique())
                if 'Classroom' in df.columns:
                    stats['total_classrooms'].update(df['Classroom'].dropna().unique())
                if 'Faculty' in df.columns:
                    stats['total_faculty'].update(df['Faculty'].dropna().unique())
        except Exception as e:
            print(f"ERROR: Failed to collect stats from {filepath}: {str(e)}")

    return {
        'total_timetables': stats['total_timetables'],
        'total_courses': len(stats['total_courses']),
        'total_classrooms': len(stats['total_classrooms']),
        'total_faculty': len(stats['total_faculty'])
    }

def generate_html_files():
    """Generate all HTML files including the dashboard."""
    try:
        # Setup environment
        if not setup_environment():
            return False

        # Create templates directory and write template files
        os.makedirs(TEMPLATE_DIR, exist_ok=True)

        dashboard_path = TEMPLATE_DIR / 'dashboard.html'
        semester_path = TEMPLATE_DIR / 'semester.html'

        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(DASHBOARD_TEMPLATE)
        with open(semester_path, 'w', encoding='utf-8') as f:
            f.write(SEMESTER_TEMPLATE)

        # Process each semester timetable
        semester_data = []
        for sem_info in DATA['semesters']:
            filepath = OUTPUT_DIR / sem_info['file']
            if not filepath.exists():
                print(f"[WARNING] Skipping missing file: {filepath.name}")
                continue

            try:
                wb = openpyxl.load_workbook(filepath)
                for sheet in DATA['sections']:
                    if sheet in wb.sheetnames:
                        df = pd.read_excel(filepath, sheet_name=sheet)
                        
                        # Generate HTML table
                        html_table = generate_table(df)

                        # Create output filename
                        output_name = f"{sem_info['file'].replace('.xlsx', '')}_{sheet.replace(' ', '_')}.html"
                        
                        # Create semester page using template
                        template = env.get_template('semester.html')
                        html = template.render(
                            title=f"{sem_info['name']} - {sheet}",
                            sem_name=sem_info['name'],
                            section=sheet,
                            table=html_table
                        )

                        # Write the file
                        output_path = OUTPUT_DIR / output_name
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(html)

                        # Store metadata for dashboard
                        semester_data.append({
                            'name': f"{sem_info['name']} - {sheet}",
                            'file': output_name,
                            'semester': sem_info['name'],
                            'section': sheet
                        })

            except Exception as e:
                print(f"ERROR processing {filepath}: {str(e)}")
                continue

        # Generate dashboard if we have data
        if semester_data:
            stats = collect_stats()
            template = env.get_template('dashboard.html')
            html = template.render(
                semester_links=semester_data,
                stats=stats,
                semesters=[sem['name'] for sem in DATA['semesters']]
            )

            index_path = OUTPUT_DIR / 'index.html'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"✅ Successfully generated all HTML files in: {OUTPUT_DIR}")
            return True
        else:
            print("⚠️ WARNING: No semester data was generated")
            return False

    except Exception as e:
        print(f"❌ ERROR: Failed to generate HTML files: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    generate_html_files()