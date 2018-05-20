import React, { Component } from 'react';
import InputRange from 'react-input-range';
import 'react-input-range/lib/css/index.css';

var dateFrom = '1999-04-04 14:10';
var dateTo = '2002-04-04 14:10';

class RangeSlider extends Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.state = {
			value: this.props.timeRange,
		};
	}

	loadData() {
		if (!this.props.readyToLoad.date) {
			return false;
		}
		this.props.loadData()
			.then(data => {
				dateFrom = data[0].split(',').join(' ');
				dateTo = data[1].split(',').join(' ');
				var readyToLoad = this.props.readyToLoad;
				readyToLoad.date = false;
				readyToLoad.user = true;
				this.props.onChangeLoading(readyToLoad);
			})
			.catch(function(error) {
				console.log(error);
			});
	}

	componentDidMount() {
        this.loadData();
    }

	handleChange(timeRange) {
		this.props.onUserInput(
			timeRange
		);
	}

	render() {
		var dateFormat = require('dateformat');
		return (
			<InputRange 
				formatLabel={value => `${dateFormat(new Date(value), "mmmm dS, yyyy")}`}
				minValue={new Date(dateFrom).getTime()} 
				maxValue={new Date(dateTo).getTime()} 
				value={this.state.value} 
				onChange={val => this.setState({value : val})}
				onChangeComplete={this.handleChange} />
		)
	}
}

export default RangeSlider