class Project1GUI extends GUI{
    constructor(container, job_id){
        super(container);
        this.job_id = job_id;
        this.setHTML();
        this.reset();
    }
    reset(){
        fetch(`/rebuild/${this.job_id}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
            row_thresh: document.getElementById('rowslider').value,
            col_thresh: document.getElementById('colslider').value
            })
        })
        .then(res => res.json())
        .then(data => {

            // update table
            console.log("updating table");
            const container = document.getElementById("TableDiv");
            container.innerHTML = this.buildTableHTML(data.table);
        });
        this.imageDiv.innerHTML = `<img src="/uploads/${this.job_id}" style="width:100%;">`;
    }
    verify(){
        fetch(`/verify/${this.job_id}`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                row_thresh: document.getElementById('rowslider').value,
                col_thresh: document.getElementById('colslider').value
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log("verify response:", data);
            });
        
    }
    buildTableHTML(table) {
        let html = "<div>";
        for (const block of table) {
            html += "<table border='2' >";
            for (const row of block) {
                html += "<tr>";
                for (const cell of row) {
                    html += `<td style='padding:0.1rem; font-size:1.3rem; text-align:center;'>${cell}</td>`;
                }
                html += "</tr>";
            }
            html += "</table>";
        }
        html += "</div>";
        return html;
    }
    setHTML(){
        let top = 0, skip = 35, s=1, c1 = 0, c2 = 200, c3 = 325, tWidth = 200, cWidth = 100, cHeight = 25;
        this.controlDiv = this.create('div', 'ControlDiv', 1, 2, 30, 6);
        this.addText(this.controlDiv, 'rowlabel', c1, top + s*skip, tWidth, cHeight, "Row Threshold:");
		this.addSlider(this.controlDiv, 'rowslider', c2, top + s*skip, cWidth, cHeight-10, 21, 14, 28, function() { this.gui.setRowThreshold(); });
		this.addText(this.controlDiv, 'rowvalue', c3, top + s++*skip, cWidth, cHeight, document.getElementById("rowslider").value);

        this.addText(this.controlDiv, 'collabel', c1, top + s*skip, tWidth, cHeight, "Column Threshold:");
		this.addSlider(this.controlDiv, 'colslider', c2, top + s*skip, cWidth, cHeight-10, 51, 34, 68, function() { this.gui.setColumnThreshold(); });
		this.addText(this.controlDiv, 'colvalue', c3, top + s++*skip, cWidth, cHeight, document.getElementById("colslider").value);

        this.addButton(this.controlDiv, 'verifybtn', c1, top + s*skip, cWidth*1.5, cHeight, "Add to Calendar", function() { this.gui.verify(); });
        this.tableDiv = this.create('div', 'TableDiv', 1, 20, 46, 25);
        this.imageDiv = this.create('div', 'ImageDiv', 47, 20, 46, 25);
    }
    setRowThreshold() {
		let sliderValue = document.getElementById('rowslider').value;
		document.getElementById('rowvalue').innerHTML = sliderValue;
		//this.settings.rowThreshold = sliderValue;
        this.reset();
	}

	setColumnThreshold() {
		let sliderValue = document.getElementById('colslider').value;
		document.getElementById('colvalue').innerHTML = sliderValue;
		//this.settings.columnThreshold = sliderValue;
        this.reset();
	}
}