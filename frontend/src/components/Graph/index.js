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
			timeRange : {min : new Date('2001-04-04,13:10').getTime(), max : new Date('2001-04-04,14:10').getTime()},
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

		this.updateTopics = this.updateTopics.bind(this);
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
	}

	handleUserInputUsers(users) {
		var readyToLoad = this.state.readyToLoad;
		readyToLoad.graph = true;
		this.setState({
			users : users,
			readyToLoad : readyToLoad
		});
	}


	handleUserInputSearchText(newText) {
		this.setState({searchAis: newText});
	}

	loadDate() {
		var dataDate = fetch("http://localhost:8000/letters/?get_date=1")
        .then(response => {
			if (!response.ok) {
				throw Error(response.statusText);
			} else {
				var readyToLoad = this.state.readyToLoad;
				readyToLoad.date = false;
				this.setState({readyToLoad : readyToLoad});
			}
			return response.json();
		});
		return dataDate;
	}

	loadUsers() {
		var dataUsers = fetch("http://localhost:8000/letters/?get_departments=1&dateFrom=" + 
			dateToJSON(this.state.timeRange.min) +'&dateTo=' + 
			dateToJSON(this.state.timeRange.max))
			.then(response => {
				if (!response.ok) {
					throw Error(response.statusText);
				} else {
					var readyToLoad = this.state.readyToLoad;
					readyToLoad.user = false;
					this.setState({readyToLoad : readyToLoad});
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
		var dataGraph = fetch("http://localhost:8000/letters/",{  
			method: 'post',  
			headers: {  
			"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"  
			},  
			body: 
				"datefrom="+dateToJSON(this.state.timeRange.min)+
				"&dateto="+dateToJSON(this.state.timeRange.max)+
				"&users="+this.state.users.toString()+
				"&topics=gas"+
				"&search="+search  
			})
			.then(response => 
				{
					if (!response.ok) {
						throw Error(response.statusText);
					} else {
						var readyToLoad = this.state.readyToLoad;
						readyToLoad.graph = false;
						this.setState({readyToLoad : readyToLoad});
					}
					return response.json();
				});
		return dataGraph;
  }

	updateTopics(newTopics) {
		this.setState({ topics : newTopics })
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
						<ContainerRight  update={this.updateTopics}/>
					</div>
				</div>
				
				<div className='row'>
					<div className='col-md-8 offset-2'>
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