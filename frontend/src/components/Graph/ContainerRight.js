import React, { Component } from 'react'
import MenuRight from './MenuRight.js'

class ContainerRight extends Component {
	constructor(props){
		super(props);
		this.state = {
			topics: [],
			isClicked: false,
			isDataLoading: false
		};

		this.handleClick = this.handleClick.bind(this);
		this.updateSelectedTopics = this.updateSelectedTopics.bind(this)
	}

	handleClick() {
		this.setState( {isClicked: true, isDataLoading: true });
		
		this.props.loadData()
			.then(data => this.setState({ topics: data, isDataLoading: false }))
			.catch(function(error) {
				console.log(error);
			})
	}

	updateSelectedTopics(newSelectedTopics) {
		this.props.update(newSelectedTopics)	
	}

	render() {
		const { topics, isClicked, isDataLoading } = this.state;

		if (!isClicked) {
			return (
				<div className="container w-100">
					<button onClick={this.handleClick} type="button" className="btn btn-light">
							Start Topic Modeling
					</button>
				</div>
			);
		}

		if (isDataLoading) {
			return (
				<div className="container w-100">
					<div className="card">
						<div className="card-body">
							<div className="card-text text-center">Loading...</div>
						</div>
					</div>
				</div>
			);
		}

		return (
			<div className="container w-100">
				<div className="container">
					<button onClick={this.handleClick} type="button" className="btn btn-light">
							Start Topic Modeling
					</button>
				</div>

				<MenuRight topics={topics} update={this.updateSelectedTopics} />
			</div>
		);
	}
}

export default ContainerRight