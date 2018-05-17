import React, { Component } from 'react';
import { LabeledArc } from './Arc.js';
import './index.css'


class Piechart extends Component {
    constructor(props) {
        super();
        this.request(props);

        var d3 = require("d3");



    }

    request(props){
        var d3 = require("d3");
        this.state = {isReady: false, dateRange: props.date, search: props.search} ;

        fetch("http://35.202.93.3:8000/letters/?get_personal_top=1&dateFrom=" +
			dateToJSON(this.state.dateRange.min) +'&dateTo=' +
			dateToJSON(this.state.dateRange.max) +
            '&words=' + this.state.search.split(" ").join(","))
			.then(response => response.json())
			.then(top => {
			    console.log('ups');

			    var sum = 0;
                var users = [];
                var i;

                for(i=0; i < 5; i++){
                    sum += top[i].value;
                    users.push(top[i].label) ;
                }

                for(i=0; i < 5; i++){
                    top[i].label = Math.round(100 * (top[i].value / sum))  + '%';
                }

        this.pie = d3.pie().value((d) => d.value);
        this.colors = d3.schemeCategory10;
        this.setState( {isReady: true, x: 200, y: 100, outerRadius: 130, innerRadius: 50,
          data: top, users: users});

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

    componentWillReceiveProps/*: function*/(nextProps) {
    this.setState({
        /*date: nextProps.date > this.props.date,*/
        search: nextProps.search > this.props.search
        });
    this.request(nextProps);
    console.log('rrr');
    }

    render() {
        console.log('zzz')
        if (this.state.isReady) {
            let pie = this.pie(this.state.data),
                translate = `translate(${this.state.x}, ${this.state.y})`;
            let legend = this.state.users.map((entry, i)=>{return <div><td className={"color_box"} style={{background:this.colors[i]}}></td><td>{entry}</td></div>})


            return (
                <div>
                    <svg height="400" viewBox="50 -100 300 400">
                        <text x="100" y="-50" fontFamily="sans-serif" fontSize="20px" fill="black">The most active
                            users
                        </text>

                        <g transform={translate}>
                            {pie.map((d, i) => this.arcGenerator(d, i))}
                        </g>
                    </svg>
                    {legend}
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

