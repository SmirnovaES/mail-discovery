import React, { Component } from 'react';
import PieChart1 from './PieChart1.js'
import PieChart2 from './PieChart2.js'
import DropDownMenu from './DropDownMenu.js'

class PieChartContainer extends Component {
	constructor(props) {
		super(props);
		
		this.state = {
			index: 1,
		}

		this.updatePieChart = this.updatePieChart.bind(this);
		this.changePieChart = this.changePieChart.bind(this);
	}

	updatePieChart(ind) {
		this.setState( {index: ind } )
	}

  	changePieChart(ind) {
		if (this.state.indexShow !== ind) {
			this.setState( {indexShow : ind} )
		}
	}

	render() {
		return (
			<div>
				<DropDownMenu update={this.updatePieChart}/>
				
				{
					(this.state.index === 1) ? (
						<PieChart1 search={this.props.search} date={this.props.date}/>
					) : (
						<PieChart2 search={this.props.search}/>
					)
				}

			</div>
		)
	}
}

export default PieChartContainer