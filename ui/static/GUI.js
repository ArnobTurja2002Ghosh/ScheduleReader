///\/\/\\\/\/\//\\///\//\\\///////\/\/\\\/\/\//\\///\//\\\//////
//
//  Assignment       COMP3200 - Assignment 4
//  Professor:       David Churchill
//  Year / Term:     2023-09
//  File Name:       GUI.js
// 
//  Student Name:    Arnob Ghosh
//  Student User:    arnobg
//  Student Email:   arnobg@mun.ca
//  Student ID:      202136073
//  Group Member(s): [enter student name(s)]
//
///\/\/\\\/\/\//\\///\//\\\///////\/\/\\\/\/\//\\///\//\\\//////
       
// Basic JavaScript HTML5 GUI Helper Functions
//
// Author: David Churchill, Memorial University
//         dave.churchill@gmail.com

class GUI {

    constructor(container) {
        this.container = container;
    }

    create(type, id, left, top, width, height) {
        let elem = document.createElement(type);
        elem.id = id;
        elem.style.position = 'absolute';
        if (left != 0) { elem.style.left = left+"rem"; }
        if (top != 0) { elem.style.top = top+"rem"; }
        if (height != 0) {
            if (type === 'canvas') {
                elem.height = height+"rem";
            } else {
                elem.style.height = height+"rem";
            }
        }
        if (width != 0) {
            if (type === 'canvas') {
                elem.width = width+"rem";
            } else {
                elem.style.width = width+"rem";
            }
        }
        this.container.appendChild(elem);
        return elem;
    }

    createCanvas(width, height) {
        this.bg = this.create('canvas', 'bg', 0, 0, width, height);
        this.fg = this.create('canvas', 'fg', 0, 0, width, height);
        this.bg_ctx = this.bg.getContext("2d");
        this.fg_ctx = this.fg.getContext("2d");
        this.fg_ctx.font = '14px Arial';
    }

    getMousePos(canvas, evt) {
        let rect = canvas.getBoundingClientRect();
        return { x: evt.clientX - rect.left, y: evt.clientY - rect.top };
    }

    createElement(type, id, left, top, width, height) {
        let element = document.createElement(type);
        element.id = id;
        element.gui = this;

        element.style.position = "absolute";
        element.style.left = left +"px";
        element.style.top = top +"px";
        element.style.width = width +"px";
        element.style.height = height +"px";

        
        element.style.display = "block";
        element.style.whiteSpace = "nowrap";
        element.style.flexShrink = "0";

        return element;
    }


    addButton(container, id, left, top, width, height, label, onclick) {
        let button = this.createElement('button', id, left, top, width, height);
        button.innerHTML = label;
        button.onclick = onclick;
        container.appendChild(button);
    }
       
    addText(container, id, left, top, width, height, label) {
        let div = this.createElement('div', id, left, top, width, height);
        div.innerHTML = label;
        container.appendChild(div);
    }

    // adds a Select box to the given container
    // values: [[val1, desc1], [val2, desc2]]
    addSelectBox(container, id, left, top, width, height, onchange, values) {
        let select = this.createElement('select', id, left, top, width, height);
        select.onchange = onchange;
        for (let i = 0; i < values.length; i++) {
            let option = document.createElement("option");
            option.value = values[i][0];
            option.text = values[i][1];
            select.appendChild(option);
        }
        container.appendChild(select);
    }

    addSlider(container, id, left, top, width, height, value, min, max, onchange) {
        let slider = this.createElement('input', id, left, top, width, height);
        slider.type = 'range';
        slider.min = min;
        slider.max = max;
        slider.value = value;
        slider.oninput = onchange;
        container.appendChild(slider);
    }
       
    addNumberBox(container, id, left, top, width, height, value, min, max, step, onchange) {
        let slider = this.createElement('input', id, left, top, width, height);
        slider.type = 'number';
        slider.value = value;
        slider.style.textAlign = 'center';
        slider.min = min;
        slider.max = max;
        slider.step = step;
        slider.oninput = onchange;
        container.appendChild(slider);
    }

    showElements(ids) {
        for (let i = 0; i < ids.length; i++) {
            document.getElementById(ids[i]).style.display = 'inline';
        }
    }

    hideElements(ids) {
        for (let i = 0; i < ids.length; i++) {
            document.getElementById(ids[i]).style.display = 'none';
        }
    }
}


// Copyright (C) David Churchill - All Rights Reserved
// COMP3200 - 2023-09 - Assignment 4
// Written by David Churchill (dave.churchill@gmail.com)
// Unauthorized copying of these files are strictly prohibited
// Distributed only for course work at Memorial University
// If you see this file online please contact email above
