import React, { Component } from 'react'
import './MenuLeft.css'
var departments = {};
var users = [];
var elements = [];
class MenuLeft extends Component {
	constructor(props){
		super(props);
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
						if (this.props.users.length === 0) {
							users = users.concat(departments[element.group]);
						}
					}, this);
				elements = 
						data.map(
							function(element) {
								return element.group;
							});
				var readyToLoad = this.props.readyToLoad;
				readyToLoad.user = false;
				if (this.props.users.length === 0) {
					this.props.onUserInput(users);
				} else {
					readyToLoad.graph = true;
				}
				this.props.onChangeLoading(readyToLoad);
			})
			.catch(function(error) {
				console.log(error);
			});
	}
	
	componentWillMount() {
		users = this.props.users;
		this.loadData();
	}

    componentWillUpdate() {
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
			checked: [],
			pStyle : {
				display : 'none'
			  },
			value : 'false'
		};	
	};

	componentDidMount() {
		this.setState({
			elements : this.props.users,
			checked: this.props.users.map((value) => users.indexOf(value) > -1)
		});	
	}

	changeVisible(e) {
		var display = 'none'
		if (e.target.checked === true) {
			display = 'flex';
		}
		this.setState({
			pStyle: {display : display},
		});
	};

	changeCheckedDepartment(e) {
		var value = 'false'
		if (e.target.checked === true) {
			value = 'true';
		}
		this.setState({
			value: value
		});
	};

	changeCheckedUser(e, element, index) {
		if (e.target.checked === true) {
			users.push(element)
		} else {
			users = users.filter(item => item !== element)
		}
		var copyChecked = this.state.checked;
		copyChecked[index] = !copyChecked[index];
		this.setState({checked:copyChecked});
		this.props.handleChange(users);
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
					<div style={this.state.pStyle} key={"user" + element + index}>   
						<div className="form-check" key={"user"  + element + index}>
							<input type="checkbox" className="form-check-input" id={"user" + element + index} 
								checked={this.state.checked[index]} 
								onChange={(e) => this.changeCheckedUser.bind(this)(e, element, index)} />
							<label className="form-check-label" htmlFor={"user" + element + index}> {element} </label>
						</div>
					</div>
				))}
			</div>
		);
	}
}
