import React, { Component } from 'react';
import Search from './Search.js';
import PieChart1 from './PieChart1.js';
import PieChart2 from './PieChart2.js';

import RangeSlider from '../Graph/RangeSlider.js'
import MenuLeft from '../Graph/MenuLeft.js'
import ContainerRight from '../Graph/ContainerRight.js'

import './index.css';

class Stats extends Component {

	constructor(props) {
		super(props);
		this.state = {
			timeRange : {min : new Date('2001-04-04,13:10').getTime(), 
						max : new Date('2001-04-04,14:10').getTime()},
			users : [],
			topics : [],
			searchAis : '',
			readyToLoad : 
				{'graph' : false,
				'user' : false,
				'date' : true} 
		};
		
		this.handleUserInputTimeRange = this.handleUserInputTimeRange.bind(this);
		this.handleUserInputUsers = this.handleUserInputUsers.bind(this);

		this.handleUserInputSearchText = this.handleUserInputSearchText.bind(this);
		this.handleComponentLoading = this.handleComponentLoading.bind(this);
		this.loadUsers = this.loadUsers.bind(this);
		this.loadDate = this.loadDate.bind(this);

		this.handleUserInputTopics = this.handleUserInputTopics.bind(this);
	}

	handleComponentLoading(readyToLoad) {
		this.setState({
			readyToLoad : readyToLoad
		});
	}

	handleUserInputTimeRange(timeRange) {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.user = true;
		this.setState({
			timeRange : timeRange,
			readyToLoad : readyToLoad
		});
		this.props.updateTimeRange(timeRange);
	}

	handleUserInputUsers(users) {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.graph = true;
		this.setState({
			users : users,
			readyToLoad : readyToLoad
		});
		this.props.updateUsers(users);
	}


	handleUserInputSearchText(newText) {
		this.setState({searchAis: newText});
		this.props.updateSearchText(newText);
	}

	loadDate() {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.date = false;
		this.setState({readyToLoad : readyToLoad});
		var dataDate = fetch("http://localhost:8000/letters/?get_date=1")
        .then(response => {
			if (!response.ok) {
				throw Error(response.statusText);
			}
			return response.json();
		});
		return dataDate;
	}

	loadUsers() {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.user = false;
		this.setState({readyToLoad : readyToLoad});
		var dataUsers = fetch("http://localhost:8000/letters/?get_departments=1&dateFrom=" + 
			dateToJSON(this.state.timeRange.min) +'&dateTo=' + 
			dateToJSON(this.state.timeRange.max))
			.then(response => {
				if (!response.ok) {
					throw Error(response.statusText);
				} 
				return response.json();
			});
		return dataUsers;
	}
	
	loadTopics() {
		var dataTopics = fetch('http://localhost:8000/letters/?get_topics=1')
			.then(response => 
			{
				if (!response.ok) {
					throw Error(response.statusText);
				}
				return response.json();
			});
		return dataTopics;
	}

	handleUserInputTopics(newTopics) {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.graph = true;
		this.setState({
			topics : newTopics,
			readyToLoad : readyToLoad
		});
		this.props.updateTopics(newTopics);
	}

	componentWillMount() {
        this.setState({
			timeRange : this.props.timeRange,
			users : this.props.users,
			topics : this.props.topics,
			searchAis : this.props.searchAis
		})
	}

	
	render() {	
		return (
			<div className="container">
				<div className='row'>
					<div className='col-md-3 order-0'>
						<MenuLeft 
								timeRange={this.state.timeRange}
								users={this.state.users}
								onUserInput={this.handleUserInputUsers}
								readyToLoad={this.state.readyToLoad}
								onChangeLoading={this.handleComponentLoading}
								loadData={this.loadUsers}
							/>
						
						<ContainerRight  
							update={this.handleUserInputTopics}
							loadData={this.loadTopics}/>
					</div>

					<div className='col-md-3 order-9'>
						<Search update={this.handleUserInputSearchText}/>
					</div>

					<div className='col-md-6 order-3'>
						<PieChart1/>
					</div>	
				</div>
				
				<div className='row'>
					<div className='col-md-6 offset-3'>
						<RangeSlider 
							timeRange={this.state.timeRange}
							onUserInput={this.handleUserInputTimeRange}
							readyToLoad={this.state.readyToLoad}
							onChangeLoading={this.handleComponentLoading}
							loadData={this.loadDate}
						/>
					</div>
				</div>
			</div>
		);
	}
}

export default Stats;

function dateToJSON(value) {
    var d = new Date(value);
    return d.toJSON().slice(0,10) + ',' + d.toTimeString().slice(0, 5)
}
