import React, { Component } from 'react'
import MenuRight from './MenuRight.js'

import './ContainerRight.css'

var topics = []

class ContainerRight extends Component {
	constructor(props){
		super(props);
		
		if (topics.length === 0) {
			topics = this.props.topics
		}

		this.state = {
			selectedTopics: this.props.topics,
			isDataLoading: false
		};


		this.handleClick = this.handleClick.bind(this);
		this.updateSelectedTopics = this.updateSelectedTopics.bind(this)
	}

	handleClick() {
		this.setState( { isDataLoading: true });
		
		this.props.loadData()
			.then(data => {
				this.setState({ selectedTopics: data, isDataLoading: false });
				topics = data;
				this.props.update(data);
			})
			.catch(function(error) {
				console.log(error);
			})
	}

	updateSelectedTopics(newSelectedTopics) {
		this.props.update(newSelectedTopics)	
	}

	render() {
		const { selectedTopics, isDataLoading } = this.state;

		if (isDataLoading) {
			return (
				<div className="container">
					<div className="card">
						<div className="card-body">
							<div className="card-text text-center">Loading...</div>
						</div>
					</div>
				</div>
			);
		}

		if (topics.length === 0) {
			return (
				<div className="container">
					<div className="text-center">
						<button onClick={this.handleClick} type="button" className="btn btn-light">
							Start Topic Modeling
						</button>
					</div>
				</div>
			);
		}

		return (
			<div className="container">
				<div className="container text-center">
					<button onClick={this.handleClick} type="button" className="btn btn-light">
							Start Topic Modeling
					</button>
				</div>

				<MenuRight topics={topics} selectedTopics={selectedTopics} 
					update={this.updateSelectedTopics} />
			</div>
		);
	}
}

export default ContainerRight