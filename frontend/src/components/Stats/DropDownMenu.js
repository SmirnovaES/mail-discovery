import React, { Component } from 'react';
import './DropDownMenu.css'

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
					<div id="dropdown_1">
						<div>
							<div className="input-group">
								<button className="btn btn-light btn-sm dropdown-item" type="button"
									onClick={(e) => this.updatePieChart(e, 1)}> 
									PieChart1
									{ this.state.index === 1 ?
										<span className="fa fa-check"></span>
										: null } 
								</button>
							</div>

							<button className="btn btn-light btn-sm dropdown-item" type="button" 
								onClick={(e) => this.updatePieChart(e, 2)}> 
								PieChart2
								{ this.state.index === 2 ?
									<span className="fa fa-check"></span>
									: null }
							</button>
						</div>
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