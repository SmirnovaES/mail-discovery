import React, { Component } from 'react'
import GraphViz from './GraphViz';
import SearchForms from './SearchForms.js'
import RangeSlider from './RangeSlider.js'
import MenuLeft from './MenuLeft'
import MenuRight from './MenuRight'


class Graph extends Component {
	render() {
		return (
			<div className='container'>
				<div className='row'>
					<div className='col-md-8 offset-2'>
						<SearchForms />
					</div>
				</div>

				<div className='row'>
					<div className='col-md-7 order-3'>	
						<GraphViz />
					</div>

					<div className='col-md-3 order-0'>
						<MenuLeft />
					</div>

					<div className='col-md-2 order-10'>
						<MenuRight />
					</div>
				</div>
				
				<div className='row'>
					<div className='col-md-8 offset-2'>
						<RangeSlider />
					</div>
				</div>
			</div>
		);
	}
}

export default Graph