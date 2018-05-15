import React, { Component } from 'react'
import MenuRight from './MenuRight.js'

class ContainerRight extends Component {
	constructor(props){
		super(props);
		this.state = {
			isClicked: false,
			topics: [],
			isDataLoading: false,
		};

		this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
		this.setState( {isClicked: true, isDataLoading: true });
		

		fetch('http://localhost:8000/letters/?get_topics=1')
			.then(response => 
			{
				if (!response.ok) {
					throw Error(response.statusText);
				}
				return response.json();
			})
			.then(data => this.setState({ topics: data, isDataLoading: false }))
			.catch(function(error) {
				console.log(error);
			})

		this.props.update(this.state.topics)
	}

	render() {
		const { topics, isDataLoading, isClicked } = this.state;

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
					<button onClick={this.handleClick} type="button" class="btn btn-light">
							Start Topic Modeling
					</button>
				</div>

				<MenuRight topics={topics}/>
			</div>
		);
	}
}

export default ContainerRight