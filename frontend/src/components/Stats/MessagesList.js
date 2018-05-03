import React, { Component } from 'react'

import './MessagesList.css'

class MessagesList extends Component {
	render() {
		if (this.props.isDataLoading) {
			return (
				<p>Loading...</p>
			);
		}

		if (this.props.messages.length === 0) {
			return (
				<p>Nothing has found...</p>
			);
		}

		return (
			<div className="container">
				<div id="scrolling">
					{this.props.messages.map((message, index) => (
						<MessageItem key={index} value={message}/>
					))}
				</div>
			</div>
		);
	}
}

export default MessagesList

class MessageItem extends Component {
	onMessageClick() {
		alert("You click on" + this.props.value["source"] + "email. Soon there will be full text window")
	}


	render() {
		var dateFormat = require('dateformat');
		var date = this.props.value["date"]

		return (
		<div className="card" onClick={this.onMessageClick.bind(this)}>
			<div className="card-body">
				<div className="pull-left">
					<h6>{ this.props.value["source"].slice(0, 10) }</h6>
				</div>
				
				<div className="pull-right">
					<h6 className="text-right">{ dateFormat(date, "shortDate") }</h6>
				</div>
				
				<div className="clearfix"></div>

				<p className="card-text"  fontSize="5">
					{this.props.value["summary"].slice(0, 100) }
				</p>
			</div>
		</div>
		);
	}
}