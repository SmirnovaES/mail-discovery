import React, { Component } from 'react';
import Search from './Search.js';
import PieChart1 from './PieChart1.js';
import PieChart2 from './PieChart2.js';

import './index.css';

class Stats extends Component {
	render() {
		return (
		<div>
			<div className='col-md-3 offset-1'>
				<Search/>
			</div>

			<div className="PieChart1">
				<div className='col-md-4 offset-4'>
					<PieChart1/>
				</div>
			</div>

			<div className="PieChart2">
				<div className='col-md-4 offset-8'>
					<PieChart2/>
				</div>
			</div>
		</div>
		);
	}
}

export default Stats;
