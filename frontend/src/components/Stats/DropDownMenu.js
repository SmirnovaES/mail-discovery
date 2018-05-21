import React, { Component } from 'react';

class DropDownMenu extends Component {
	constructor() {
		  super();
		  this.state = {
			showMenu: false,
			index: 1
		};

		this.showMenu = this.showMenu.bind(this);
		this.updatePieChart = this.updatePieChart.bind(this);
	}
	
	updatePieChart(e, ind) {
		if (ind !== this.state.index) {
			this.setState( {index : ind} )
			this.props.update(ind)
		}
	}

	showMenu(event) {
		this.setState( prevState => ( {showMenu: !prevState.showMenu} ))
	}

	render() {
		return (
			<div>
				<button className="btn btn-light btn-sm dropdown-toggle" type="button" data-toggle="dropdown"
					aria-haspopup="true" aria-expanded="false" onClick={this.showMenu}>
					Choose PieChart
				</button>
				
				{ this.state.showMenu ? (
						<div>
							<button className="btn btn-light btn-sm dropdown-item" type="button"
								onClick={(e) => this.updatePieChart(e, 1)}> 
								PieChart1 
							</button>

							<button className="btn btn-light btn-sm dropdown-item" type="button" 
								onClick={(e) => this.updatePieChart(e, 2)}> 
								PieChart2
							</button>
						</div>
					) : (
					   null
					)
				}
			</div>
		);
	}
}

export default DropDownMenu;