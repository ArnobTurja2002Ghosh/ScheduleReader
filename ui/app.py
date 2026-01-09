from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import uuid
import os
from src.main import build_block, image_to_words, week_blocks_to_schedule
from ui.allowed_files import allowed_file
import hashlib
from src.employee_name import load_employee_names, match_employee_name
from src.google_client_oauth import shift_in_schedule

def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

app = Flask(__name__)
UPLOAD_DIR = "data/uploads"
@app.route("/rebuild/<job_id>", methods=["POST"])
def rebuild(job_id):
    data = request.json
    table=None
    row_thresh = int(data["row_thresh"])
    col_thresh = int(data["col_thresh"])
    print(f"data/uploads/{job_id}.jpg")
    img_path = f"data/uploads/{job_id}.jpg"
    words_sorted = image_to_words(img_path)
    blocks = build_block(row_thresh, col_thresh, words_sorted)
    if request.method == "POST":
        
        table= [uniform_list(i) for i in blocks]
    return jsonify({
        "table": table,
        "overlay_url": f"/overlay/{job_id}?v={row_thresh}-{col_thresh}"
    })
@app.route("/verify/<job_id>", methods=["POST"])
def verify(job_id):
    data = request.json
    row_thresh = int(data["row_thresh"])
    col_thresh = int(data["col_thresh"])
    print(f"data/uploads/{job_id}.jpg")
    img_path = f"data/uploads/{job_id}.jpg"
    words_sorted = image_to_words(img_path)
    blocks = build_block(row_thresh, col_thresh, words_sorted)
    print(blocks)
    schedule = week_blocks_to_schedule(blocks)
    print(schedule)
    shift_in_schedule("Arnob", schedule)
    return "done"
@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        file = request.files["image"]
        if file and allowed_file(file.filename):
            image_bytes = file.read()
            job_id = hash_bytes(image_bytes)[:10]


            path = os.path.join(UPLOAD_DIR, f"{job_id}.jpg")
            if not os.path.exists(path):
                with open(path, "wb") as f:
                    f.write(image_bytes)
            

            return redirect(url_for("review1", job_id=job_id))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=image>
      <input type=submit value=Upload>
    </form>
    '''
@app.route("/review/<job_id>", methods=["GET", "POST"])
def review1(job_id):
    table=None
    row_thresh = int(request.form.get("row_thresh", 15))
    col_thresh = int(request.form.get("col_thresh", 40))

    ocr_path = f"data/ocr/{job_id}.json"
    img_path = f"data/uploads/{job_id}.jpg"
    words_sorted = image_to_words(img_path)
    blocks = build_block(21, 51, words_sorted)
    if request.method == "POST":
        row_thresh = int(request.form["row_thresh"])
        col_thresh = int(request.form["col_thresh"])
        table= [uniform_list(i) for i in blocks]
    return render_template(
        "review.html",
        table=table,
        job_id=job_id,
        row_thresh=row_thresh,
        col_thresh=col_thresh,
        image_path=img_path
    )
@app.route('/')
def index():
    # Render the index.html file from the 'templates' folder
    return render_template('index.html')

@app.route("/uploads/<job_id>")
def serve_image(job_id):
    path = f"../data/uploads/{job_id}.jpg"#os.path.join("data", "uploads", f"{image_id}.jpg")
    return send_file(path, mimetype="image/jpeg")


def uniform_list(block):
    header = block[1]
    result=[]
    result.append([""]+list(map(lambda x: x["text"],block[0])))
    result.append([""]+list(map(lambda x: x["text"],header)))
    employees = load_employee_names()
    for row in block[2:]:
        name_raw = row[0]["text"].strip()
        name = match_employee_name(name_raw, employees)['matched']
        if not name:
            continue
        result.append([name]+["" for i in header])
        for col_index in range(1, len(row)):
            cell_text = row[col_index]["text"].strip()
            if cell_text:
                date_dist = [abs(i['x_center']-row[col_index]['x_center']) for i in header]
                result[-1][date_dist.index(min(date_dist)) +1] = cell_text
    return result           
            
if __name__ == "__main__":
    app.run(debug=True)
