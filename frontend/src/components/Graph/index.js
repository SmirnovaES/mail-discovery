import React, { Component } from 'react'
import GraphViz from './GraphViz';
import SearchForms from './SearchForms.js'
import RangeSlider from './RangeSlider.js'
import MenuLeft from './MenuLeft.js'
import ContainerRight from './ContainerRight.js'


class Graph extends Component {
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
		this.loadGraph = this.loadGraph.bind(this);
		this.loadUsers = this.loadUsers.bind(this);
		this.loadDate = this.loadDate.bind(this);

		this.handleUserInputTopics = this.handleUserInputTopics.bind(this);
	}

	componentWillMount() {
        this.setState({
			timeRange : this.props.timeRange,
			users : this.props.users,
			topics : this.props.topics,
			searchAis : this.props.searchAis
		})
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

	loadGraph() {
		var search = this.state.searchAis;
		if (search === '') {
			search = 'NULLVALUEMAILDISCOVERYAIS';
		}
		var topics = this.state.topics;
		if (topics.length === 0) {
			topics = 'gas';
		} else {
			topics = topics.join(',');
		}
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.graph = false;
		this.setState({readyToLoad : readyToLoad});
		var dataGraph = fetch("http://localhost:8000/letters/",{  
			method: 'post',  
			headers: {  
			"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"  
			},  
			body: 
				"datefrom="+dateToJSON(this.state.timeRange.min)+
				"&dateto="+dateToJSON(this.state.timeRange.max)+
				"&users="+this.state.users.toString()+
				"&topics="+topics+
				"&search="+search  
			})
			.then(response => 
				{
					if (!response.ok) {
						throw Error(response.statusText);
					}
					return response.json();
				});
		return dataGraph;
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

	render() {
		return (
			<div className='container'>
				<div className='row'>
					<div className='col-md-6 offset-3'>
						<SearchForms 
							searchAis={this.state.searchAis}
							onUserInput={this.handleUserInputSearchText}
						/>
					</div>
				</div>

				<div className='row'>
					<div className='col-md-6 order-3'>	
						<GraphViz 
							readyToLoad={this.state.readyToLoad}
							onChangeLoading={this.handleComponentLoading}
							loadData={this.loadGraph}
						/>
					</div>

					<div className='col-md-3 order-0'>
						<MenuLeft 
							timeRange={this.state.timeRange}
							users={this.state.users}
							onUserInput={this.handleUserInputUsers}
							readyToLoad={this.state.readyToLoad}
							onChangeLoading={this.handleComponentLoading}
							loadData={this.loadUsers}
						/>
					</div>

					<div className='col-md-3 order-9'>
						<ContainerRight  
							update={this.handleUserInputTopics}
							loadData={this.loadTopics}/>
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

export default Graph

function dateToJSON(value) {
    var d = new Date(value);
    return d.toJSON().slice(0,10) + ',' + d.toTimeString().slice(0, 5)
}