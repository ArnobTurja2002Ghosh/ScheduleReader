import os
from src.date_time import *
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "project1.json"
from src.employee_name import load_employee_names, match_employee_name
from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()

def image_to_words(filename):
    print(filename)
    with io.open(filename, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    words = []

    for t in response.text_annotations[1:]:
        box = t.bounding_poly.vertices
        x = [v.x for v in box]
        y = [v.y for v in box]

        words.append({
            "text": t.description,
            "x_center": sum(x) / 4,
            "y_center": sum(y) / 4
        })

    words_sorted = sorted(words, key=lambda w: w["y_center"])
    return words_sorted
def build_block(row_threshold, col_threshold, words_sorted):
    rows2= build_table(row_threshold, col_threshold, words_sorted)
    
    header_rows= header_indices(rows2)

    return week_blocks(header_rows, rows2)

def build_table(row_threshold , col_threshold, words_sorted):
  # tweak later
    rows = []
    current_row = []
    for w in words_sorted:
        if not current_row:
            current_row = [w]
            continue

        if abs(w["y_center"] - current_row[0]["y_center"]) < row_threshold:
            current_row.append(w)
        else:
            rows.append(current_row)
            current_row = [w]

    rows.append(current_row)
    rows1=[sorted(i, key=lambda w:w["x_center"]) for i in rows]

    rows2=[]
    current_dict=None

    for i in rows1:

        rows2.append([])
        for j in i:
            if not current_dict:
                current_dict=j.copy()
                continue
            if abs(j["x_center"]-current_dict["x_center"])<col_threshold:
                current_dict['text']+=j['text']
            else:
                rows2[len(rows2)-1].append(current_dict)
                current_dict=j.copy()

        if(current_dict):
            rows2[len(rows2)-1].append(current_dict)
            current_dict=None
    return rows2



def header_indices(rows2):
    header_rows = []

    for i, row in enumerate(rows2):
        date_like_cells = sum(is_date(cell["text"]) for cell in row)
        alpha_only_cells = sum(cell["text"].isalpha() for cell in row)
        #print(i, date_like_cells, alpha_only_cells)
        if date_like_cells <2 and alpha_only_cells >6:
            header_rows.append(i)
    return header_rows

def week_blocks(header_rows, rows2):
    week_blocks = []

    for idx, header_idx in enumerate(header_rows):
        start = header_idx
        end = header_rows[idx + 1] if idx + 1 < len(header_rows) else len(rows2)
        week_blocks.append(rows2[start:end])
    return week_blocks
#print(build_block(21, 51))
def week_blocks_to_schedule(week_blocks):
    schedule = {}
    employees = load_employee_names()
    for block in week_blocks:
        header = block[1]
        #print(block)
        for row in block[2:]:
            name_raw = row[0]["text"].strip()
            name = match_employee_name(name_raw, employees)['matched']
            print(name)
            if not name:
                continue

            for col_index in range(1, len(row)):
                cell_text = row[col_index]["text"].strip()
                if cell_text:
                    date_dist = [abs(i['x_center']-row[col_index]['x_center']) for i in header]
                    date = header[date_dist.index(min(date_dist))]["text"]
                    print(date, cell_text)
                    if(parse_day(date) and parse_shift(cell_text)):
                        schedule.setdefault(name, []).append(build_datetimes(parse_day(date), parse_shift(cell_text)))

    return schedule

TIMEZONE = "America/St_Johns"
def shift_to_event(shift):
    start_dt, end_dt = shift

    source_id = f"{start_dt.isoformat()}"

    return {
        "summary": f"Work Shift",
        "description": f"source_id:{source_id}",
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": TIMEZONE,
        },
    }
