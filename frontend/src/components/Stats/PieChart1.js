import React, { Component } from 'react';
import { LabeledArc } from './Arc.js';

class Piechart extends Component {
    constructor() {
        super();

        var d3 = require("d3");

        this.state = {isReady: false, dateFrom: '2001-04-04,13:10', dateTo: '2001-04-04,14:10' };
        fetch("http://localhost:8000/letters/?get_personal_top=1&dateFrom=" +
			dateToJSON(this.state.dateFrom) +'&dateTo=' +
			dateToJSON(this.state.dateTo))
			.then(response => response.json())
			.then(top => {
			    console.log('ups');

        this.pie = d3.pie().value((d) => d.value);
        this.colors = d3.schemeCategory10;
        this.setState( {isReady: true, x: 200, y: 100, outerRadius: 130, innerRadius: 50,
          data: top/*: [  {value: 12, label: 'John'},
                   {value: 13, label: 'Peter'},
                   {value: 21, label: 'Anna'},
                   {value: 11, label: 'Maria'},
                   {value: 27, label: 'Vlad'}
                   ]*/});

    });
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
        if (this.state.isReady) {
            let pie = this.pie(this.state.data),
                translate = `translate(${this.state.x}, ${this.state.y})`;

            return (
                <div id="svg2">
                    <svg width="350" height="300" viewBox="100 -50 300 300">
                        <g transform={translate}>
                            {pie.map((d, i) => this.arcGenerator(d, i))}
                        </g>
                        <text x="100" y="250" font-family="sans-serif" font-size="20px" fill="black">The most active
                            users
                        </text>
                    </svg>
                </div>
            )
        }
        else {
            return ('ups')
        }
    }
}

function dateToJSON(value) {
    var d = new Date(value);
    return d.toJSON().slice(0,10) + ',' + d.toTimeString().slice(0, 5)
}

export default Piechart;
