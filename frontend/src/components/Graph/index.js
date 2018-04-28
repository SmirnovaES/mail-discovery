import React, { Component } from 'react'
import GraphViz from './GraphViz';
import SearchForms from './SearchForms.js'
import RangeSlider from './RangeSlider.js'
import MenuLeft from './MenuLeft'
import MenuRight from './MenuRight'


class Graph extends Component {
	static configuration = {
		timeRange : this.state.timeRange,
		users : this.state.users,
		topics : this.state.topics,
		searchAis : this.state.searchAis
	}
	constructor(props) {
		super(props);
		this.state = {
			timeRange : {min : new Date('2001-04-04,13:10').getTime(), max : new Date('2001-04-04,14:10').getTime()},
			users : [],
			topics : [],
			searchAis : ''
		};
		
		this.handleUserInput = this.handleUserInput.bind(this);
	}

	handleUserInput(timeRange) {
		this.setState({
			timeRange : timeRange
		});
	}

	render() {
		return (
			<div className='container'>
				<div className='row'>
					<div className='col-md-8 offset-2'>
						<SearchForms 
							searchAis={this.state.searchAis}
						/>
					</div>
				</div>

				<div className='row'>
					<div className='col-md-7 order-3'>	
						<GraphViz 
							configuration={this.configuration}
						/>
					</div>

					<div className='col-md-3 order-0'>
						<MenuLeft 
							timeRange={this.state.timeRange}
							users={this.state.users}
						/>
					</div>

					<div className='col-md-2 order-10'>
						<MenuRight />
					</div>
				</div>
				
				<div className='row'>
					<div className='col-md-8 offset-2'>
						<RangeSlider 
							timeRange={this.state.timeRange}
							onUserInput={this.handleUserInput}
						/>
					</div>
				</div>
			</div>
		);
	}
}

export default Graph