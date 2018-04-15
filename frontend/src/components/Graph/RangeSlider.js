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
				maxValue={new Date().getTime()} 
				minValue={new Date(0).getTime()} 
				value={this.state.value} 
				onChange={val => this.setState({value : val})}
				onChangeComplete={this.handleChange} />
		)
	}
}

export default RangeSlider