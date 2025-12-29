import os
from date_time import *
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../project1.json"

from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()

with io.open("../n.jpg", "rb") as image_file:
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

rows = []
current_row = []
row_threshold = 21  # tweak later

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
col_threshold=51
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



header_rows = []

for i, row in enumerate(rows2):
    date_like_cells = sum(is_date(cell["text"]) for cell in row)
    alpha_only_cells = sum(cell["text"].isalpha() for cell in row)
    #print(i, date_like_cells, alpha_only_cells)
    if date_like_cells <2 and alpha_only_cells >6:
        header_rows.append(i)

week_blocks = []

for idx, header_idx in enumerate(header_rows):
    start = header_idx
    end = header_rows[idx + 1] if idx + 1 < len(header_rows) else len(rows2)
    week_blocks.append(rows2[start:end])

