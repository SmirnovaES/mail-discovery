import React, { Component } from 'react'
import './MenuLeft.css'
var departments = {};
var users = [];
var elements = [];
class MenuLeft extends Component {
	constructor(props){
		super(props);
		this.state = {
			// elements: [],
			// localTimeRange: this.props.timeRange
		};
		elements = [];
		users = [];
	}

	loadData() {
		if (!this.props.readyToLoad.user) {
			return false;
		}
        this.props.loadData()
			.then(data => {
				if (this.props.users.length !== 0) {
					users = this.props.users;
				}
				data.forEach(
					function(element, i, arr) {
						departments[element.group] = element.users.map(
							function(element) {
								return element.id;
							});
						// if (this.props.users.length !== 0) {
						// 	departments[element.group] = departments[element.group]
						// 	.filter((value) => users.indexOf(value) > -1);
						// }
							// в списке пользователей есть лишние пользователи, которых я убрал на статистике
						if (this.props.users.length === 0) {
							users = users.concat(departments[element.group]);
						}
					}, this);
				this.props.onUserInput(users);
				elements = 
						data.map(
							function(element) {
								return element.group;
							});
				

				var readyToLoad = this.props.readyToLoad;
				readyToLoad.user = false;
				//readyToLoad.graph = true; изменил в onUserInput
				this.props.onChangeLoading(readyToLoad);
			})
			.catch(function(error) {
				console.log(error);
			});
	}
	
	componentWillMount() {
		if (this.props.users.length === 0)
		this.loadData();
	}

    componentWillUpdate() {
		// if (this.state.localTimeRange !== this.props.timeRange) {
		// 	this.loadData();
		// 	this.setState({
		// 		localTimeRange: this.props.timeRange
		// 	});
		// }
		this.loadData();
    }

	render() {
		return (
			<div className="container">
				<div id="scrollbox" >
					{elements.map((department, index) => (
						<Department key={index}
							value={department}
							users={departments[department]}
							handleChange={this.props.onUserInput}
						/>
					))}
				</div>
			</div>
		);
	}
}
export default MenuLeft

class Department extends Component {
	constructor(props){
		super(props);
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

	changeCheckedUser(e, element) {
		if (e.target.checked === true) {
			users.push(element)
		} else {
			users = users.filter(item => item !== element)
		}
		this.props.handleChange(users);
		console.log(users);
	};

	render() {
		return (
			<div>
				
				<dt><label>
					<input type="checkbox"
						onChange={this.changeVisible.bind(this)}/>
						{this.props.value}
				</label></dt>
					
				{this.state.elements.map((element, index) => (
					<div style={this.state.pStyle} key={"user" + index}>   
						<div className="form-check" key={"user" + index}>
							<input type="checkbox" className="form-check-input" id={"user" + index} 
								defaultChecked onChange={(e) => this.changeCheckedUser.bind(this)(e, element)} />
							<label className="form-check-label" htmlFor={"user" + index}> {element} </label>
						</div>
					</div>
				))}
			</div>
		);
	}
}
