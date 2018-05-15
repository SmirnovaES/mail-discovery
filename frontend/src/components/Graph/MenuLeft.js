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
				data.forEach(
					function(element, i, arr) {
						departments[element.group] = element.users.map(
							function(element) {
								return element.id;
							});
						users = users.concat(departments[element.group]);
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
			<div id="container">
				<div id="scrollbox" >
					<div id="content">
						{elements.map((department, index) => (
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
				<div className="input-group mb-3">
					<div className="input-group-text">
						<label>
							<input type="checkbox"
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
									onChange={(e) => this.changeCheckedUser.bind(this)(e, element)}
									defaultChecked />
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