import React, { Component } from 'react';
import SearchForms from './SearchForms.js';
import Messages from './Messages.js';
import PieChart1 from './PieChart1.js';
import PieChart2 from './PieChart2.js';

import './index.css';

class Stats extends Component {
  render() {
    return (
      <div className="Stats">
        <div className='Search'>
			<div className='col-md-3 offset-1'>
				<SearchForms/>
			</div>
		</div>
 
        <div className="Messages">
            <div className='col-md-4 offset-1'>
			    <Messages/>
            </div>
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
