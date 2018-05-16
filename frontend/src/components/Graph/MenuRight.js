import React, { Component } from 'react'

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
			<div className="container">
				<div id="scrollbox" >
						{this.state.topics.map((topic, key) => (
							<div className="form-check" key={"topic" + key}>
								<input type="checkbox" className="form-check-input" id={"topic" + key} 
									defaultChecked onChange={(e) => this.handleChecked.bind(this)(e, topic)} />
								<label className="form-check-label" htmlFor={"topic" + key}> {topic} </label>
							</div>
						))}
					</div>
				</div>
		);
	}
}

export default MenuRight