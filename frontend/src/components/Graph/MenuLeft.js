import React, { Component } from 'react'
import './MenuLeft.css'

class MenuLeft extends Component {
	constructor(props){
		super(props);
		this.state = {
			elements: []
		};
		var i;
		for (i = 0; i < 30; i++) {
			this.state.elements.push('Департамент номер ' + i)
		}
	}

	render() {
		return (
			<div id="container">
				<div id="scrollbox" >
					<div id="content">
						{this.state.elements.map((department, index) => (
							<Department key={index} value={department}/>
						))}
					</div>
				</div>
			</div>
		);
	}
}
export default MenuLeft

class Department extends Component {
	constructor(props){
		super(props);
		var i;
		this.state = {
			elements: [],
			pStyle : {
				display : 'none'
			  }
		};
		for (i = 0; i < 3; i++) {
			this.state.elements.push('Поддепартамент номер ' + i)
		}
	};

	changeVisible(e) {
		var display = 'none'
		if (e.target.checked === true) {
			display = 'flex';
		}
		console.log(e.target.checked + " " + display);
		this.setState({
			pStyle: {display : display}
		});
	};

	render() {
		return (
			<div>
				<div className="input-group mb-3">
					<div className="input-group-prepend">
						<div className="input-group-text">
							<input type="checkbox" aria-label="Checkbox for following text input"
								onChange={function (e) {console.log(e.target.checked)}}/>
						</div>
					</div>
					<div className="input-group-text">
						<label>
							<input type="checkbox" value="false"
								onChange={this.changeVisible.bind(this)}/>
								{this.props.value}
						</label>
					</div>     
				</div>
				{this.state.elements.map((element, index) => (
					<div className="input-group mb-3" style={this.state.pStyle} key={index}>    
						<div className="input-group-prepend">
							<div className="input-group-text">
								<input type="checkbox" aria-label="Checkbox for following text input"
									onChange={function (e) {console.log(e.target.checked)}}/>
							</div>
						</div>
						<div className="input-group-text">
							{element}
						</div>
					</div>
				))}
			</div>
		);
	}
}