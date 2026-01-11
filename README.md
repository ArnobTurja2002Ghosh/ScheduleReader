# Schedule Reader

<img src="docs/cd4.gif"/>
 
A web-based tool that converts schedule images (e.g., staff rosters) into structured tables using OCR, allows human review and tuning, and then syncs approved schedules to Google Calendar.

This project focuses on **correctness, human-in-the-loop review, and scalability**, not just raw OCR accuracy.

---

## What this project does

1. **Upload or paste a schedule image**
2. **Run OCR (Google Cloud Vision)** to extract text with bounding boxes
3. **Group text into a table** using geometric heuristics (row/column thresholds)
4. **Render the table in a web UI** for human review
5. **Allow live tuning** of thresholds (row/column spacing)
6. **Approve the table as a whole** (not per-event)
7. **Create calendar events** via Google Calendar API

---

## Why this exists

OCR is imperfect:
- `rn` ↔ `m`, `cl` ↔ `d`
- inconsistent spacing
- layout-dependent errors

This project assumes **humans are better reviewers than post-processing heuristics** and builds the system around that fact.

---

## Tech stack

### Backend
- **Python 3.10+**
- **Flask** – simple, explicit server-side rendering
- **Google Cloud Vision API** – OCR with bounding boxes
- **Google Calendar API** – event creation

### Frontend
- **HTML + Jinja** – server-rendered templates
- **Vanilla JavaScript** – GUI controls, live tuning
- **CSS (absolute + flex layout)** – deterministic placement

> No React / Streamlit by design — this app needs tight control over layout and state.

---

## Project structure

```
project_root/
├── src/                # Core business logic (no Flask)
│   ├── __init__.py
│   ├── date_time.py          # Vision API calls
│   ├── employee_name.py        
│   └── google_client_oauth.py     # Google Calendar integration
│
├── ui/                 # Web layer
│   ├── __init__.py
│   ├── app.py          # Flask app entry point
│   ├── allowed_files.py      # View helpers
│   └── templates/
│       └── review.html # OCR review UI
        └── index.html
        └──index.css
    │
    ├── static/
    │   ├── GUI.js
    │   └── project1GUI.js
│
├── data/
│   └── uploads/        # Temporary image storage
│
├── venv/               # Virtual environment (local only)
└── README.md
```

### Design rationale

- `src/` is framework-agnostic → testable and reusable
- `ui/` handles HTTP, HTML, and JS glue
- OCR results are **not persisted long-term**
- Filesystem storage is used deliberately to avoid premature infrastructure complexity

---

## Setup
<img src="docs/e889.gif"/>
### 1. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Google Cloud setup

- Create a Google Cloud project (no organization required)
- Enable:
  - **Cloud Vision API**
  - **Google Calendar API**
- Create a **service account**
- Download the JSON key

Set environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

---

## Running the app

From the project root:

```bash
python -m ui.app
```

Then open:

```
http://127.0.0.1:5000/
```

---

## How OCR review works

- OCR output is grouped into rows and columns using configurable thresholds
- Thresholds are exposed as GUI sliders
- Users tune until the table looks correct
- Approval applies to **the entire table**, not individual cells

This avoids micromanaging noisy OCR output.

---

## Why Flask (and not FastAPI / React / Streamlit)

- Flask is explicit and predictable
- Server-rendered HTML avoids state duplication
- Vanilla JS gives full layout control
- No hidden abstractions during early iteration


---

## Known limitations

- OCR quality depends on image clarity
- Native browser sliders have intrinsic height constraints
- Time parsing assumes consistent schedule formats

These are accepted trade-offs at this stage.

---

## Future directions

- Calendar preview before commit
- Multi-user support with auth
- Replace filesystem storage with object storage (optional)

---

## Philosophy

This project optimizes for:

- Correctness over automation
- Human review over heuristics
- Clear boundaries between layers

If OCR were perfect, this project wouldn’t be needed.

---

## License

GPL




