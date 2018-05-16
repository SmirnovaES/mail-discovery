import React, { Component } from 'react'

var selectedTopics = [];

class MenuRight extends Component {
	constructor(props) {
		super(props);

		selectedTopics = this.props.selectedTopics;
		this.handleChecked = this.handleChecked.bind(this);
		this.isChecked = this.isChecked.bind(this)
	}

	handleChecked(e, topic) {
		if (e.target.checked === true) {
			selectedTopics.push(topic)
		} else {
			selectedTopics = selectedTopics.filter(item => item !== topic)
		}

		this.props.update(selectedTopics)
	}

	isChecked(topic) {
		return selectedTopics.some(item => item === topic)
	}

	render() {
		return (
			<div className="container">
				<div id="scrollbox" >
						{this.props.topics.map((topic, key) => (
							<div className="form-check" key={"topic" + key}>
								<input type="checkbox" className="form-check-input" id={"topic" + key} 
									checked={this.isChecked(topic)} onChange={(e) => this.handleChecked(e, topic)} />
								<label className="form-check-label" htmlFor={"topic" + key}> {topic} </label>
							</div>
						))}
					</div>
				</div>
		);
	}
}

export default MenuRight