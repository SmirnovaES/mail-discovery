import React, { Component } from 'react'
import './MenuLeft.css'
var departments = {};
var users = [];
class MenuLeft extends Component {
	constructor(props){
		super(props);
		this.state = {
			elements: []
		};
		users = [];
	}

	loadData() {
        fetch("http://localhost:8000/letters/?get_departments=1&dateFrom=" + 
			dateToJSON(this.props.timeRange.min) +'&dateTo=' + 
			dateToJSON(this.props.timeRange.max))
			.then(response => response.json())
			.then(data => {
				data.forEach(
					function(element, i, arr) {
						departments[element.group] = element.users.map(
							function(element) {
								return element.id;
							});
						users.push(departments[element.group]);
					}, this);
				this.props.onUserInput(users);
				this.setState(
					{elements : 
						data.map(
							function(element) {
								return element.group;
							})
					}
				);
			});
	}
	
	componentWillMount() {
		this.loadData();
	}

    // componentWillUpdate() {
    //     this.loadData();
    // }

	render() {
		return (
			<div id="container">
				<div id="scrollbox" >
					<div id="content">
						{this.state.elements.map((department, index) => (
							<Department key={index}
								value={department}
								users={departments[department]}
								handleChange={this.props.onUserInput}
							/>
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
			  },
			value : 'false'
		};	
	};

	componentDidMount() {
		this.setState({
			elements : this.props.users
		});	
	}

	changeVisible(e) {
		var display = 'none'
		if (e.target.checked === true) {
			display = 'flex';
		}
		console.log(e.target.checked + " " + display);
		this.setState({
			pStyle: {display : display},
		});
	};

	changeCheckedDepartment(e) {
		var value = 'false'
		if (e.target.checked === true) {
			value = 'true';
		}
		console.log(e.target.checked + " " + value);
		this.setState({
			value: value
		});
	};

	render() {
		return (
			<div>
				<div className="input-group mb-3">
					<div className="input-group-prepend">
						<div className="input-group-text">
							<input type="checkbox" aria-label="Checkbox for following text input"
								onChange={this.changeCheckedDepartment.bind(this)}/>
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
								<input type="checkbox" value={this.state.value} aria-label="Checkbox for following text input"
									onChange={function (e, element) {console.log(e.target.checked, element)}}/>
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

function dateToJSON(value) {
    var d = new Date(value);
    return d.toJSON().slice(0,10) + ',' + d.toTimeString().slice(0, 5)
}

function unique(arr) {
	var obj = {};

	for (var i = 0; i < arr.length; i++) {
		var str = arr[i];
		obj[str] = true; // запомнить строку в виде свойства объекта
	}

	return Object.keys(obj); // или собрать ключи перебором для IE8-
}