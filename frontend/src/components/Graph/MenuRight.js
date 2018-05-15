import React, { Component } from 'react'
import './MenuRight.css'

var selectedTopics = [];

class MenuRight extends Component {
	constructor(props) {
		super(props);
		this.state = {
			topics: this.props.topics
		};

		selectedTopics = this.props.topics;
		this.handleChecked = this.handleChecked.bind(this);
	}

	handleChecked(e, topic) {
		if (e.target.checked === true) {
			selectedTopics.push(topic)
		} else {
			selectedTopics = selectedTopics.filter(item => item !== topic)
		}

		this.props.update(selectedTopics)
	}

	render() {
		return (
			<div id="container">
				<div id="scrollbox" >
					<div id="content">
						{this.state.topics.map((topic, key) => (
							<div className="form-check" key={key}>
								<input type="checkbox" className="form-check-input" id={key} defaultChecked="treu" 
										onChange={(e) => this.handleChecked.bind(this)(e, topic)} />
								<label className="form-check-label" htmlFor={key}> {topic} </label>
							</div>
						))}
					</div>
				</div>
			</div>
		);
	}
}

export default MenuRight