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
		this.dateFrom = '1999-04-04,14:10';
		this.dateTo = '2002-04-04,14:10';
	}

	loadData() {
		if (!this.props.readyToLoad.date) {
			return false;
		}
		this.props.loadData()
			.then(data => {
				this.dateFrom = data[0];
				this.dateTo = data[1];
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
				minValue={new Date(this.dateFrom).getTime()} 
				maxValue={new Date(this.dateTo).getTime()} 
				value={this.state.value} 
				onChange={val => this.setState({value : val})}
				onChangeComplete={this.handleChange} />
		)
	}
}

export default RangeSlider