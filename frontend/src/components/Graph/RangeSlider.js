import React, { Component } from 'react';
import InputRange from 'react-input-range';
import './RangeSlider.css'

class RangeSlider extends Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
	}

	handleChange(timeRange) {
		this.props.onUserInput(
			timeRange
		);
	}
	
	render() {
		return (
			<InputRange maxValue={20} minValue={0} value={this.props.timeRange} 
						onChange={this.handleChange} />
		)
	}
}

export default RangeSlider