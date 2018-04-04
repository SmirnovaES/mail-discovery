import React, { Component } from 'react';
import InputRange from 'react-input-range';
import './RangeSlider.css'

class RangeSlider extends Component {
	constructor(props) {
		super(props);

		this.state = {
			value: { min: 2, max: 10 },
		}
	}
	
	render() {
		return (
			<InputRange maxValue={20} minValue={0} value={this.state.value} 
						onChange={value => this.setState({ value })} />
		)
	}
}

export default RangeSlider