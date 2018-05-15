import React, { Component } from 'react';
import { LabeledArc } from './Arc.js';

class Piechart extends Component {
    constructor() {
        super();

        var d3 = require("d3");

        this.pie = d3.pie().value((d) => d.value);
        this.colors = d3.schemeCategory10;
        this.state = {x: 200, y: 100, outerRadius: 130, innerRadius: 50,
          data: [  {value: 92-34, label: 'Meeting'},
                   {value: 29, label: 'Weekend'},
                   {value: 54, label: 'Salary'},
                   {value: 34, label: 'Warning'},
                   {value: 34, label: 'Checking'}
                   ]};

    }

    arcGenerator(d, i) {
         return (
            <LabeledArc key={`arc-${i}`}
                        data={d}
                        innerRadius={this.state.innerRadius}
                        outerRadius={this.state.outerRadius}
                        color={this.colors[i]} />
        );
    }

    render() {
        let pie = this.pie(this.state.data),
            translate = `translate(${this.state.x}, ${this.state.y})`;

        return (
            <div id="svg2">
                <svg width="350" height="300" viewBox="100 -50 300 300">
                    <g transform={translate}>
                        {pie.map((d, i) => this.arcGenerator(d, i))}
                    </g>
                    <text x="90" y="245" fontFamily="sans-serif" fontSize="20px" fill="black">The most popular themes</text>
                </svg>
            </div>
        )
    }
}

export default Piechart;
