import React, { Component } from 'react';
import InputRange from 'react-input-range';
import 'react-input-range/lib/css/index.css';


class RangeSlider extends Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.state = {
			value: this.props.timeRange,
		};
		this.props.dateFrom = '1999-04-04,14:10';
		this.props.dateTo = '2002-04-04,14:10';
	}

	componentDidMount() {
        fetch("http://localhost:8000/letters/?get_date=1")
        .then(response => response.json())
        .then(data => {
			this.props.dateFrom = data[0];
			this.props.dateTo = data[1];
		});
    }

	handleChange(timeRange) {
		this.props.onUserInput(
			timeRange
		);
	}

	render() {
		var dateFormat = require('dateformat');
		var date = new Date(0);
		return (
			<InputRange 
				formatLabel={value => `${dateFormat(new Date(value), "mmmm dS, yyyy")}`}
				minValue={new Date(this.props.dateFrom).getTime()} 
				maxValue={new Date(this.props.dateTo).getTime()} 
				value={this.state.value} 
				onChange={val => this.setState({value : val})}
				onChangeComplete={this.handleChange} />
		)
	}
}

export default RangeSlider