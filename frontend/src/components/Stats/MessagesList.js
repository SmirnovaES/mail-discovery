import React, { Component } from 'react'
import Modal from 'react-modal'

import './MessagesList.css'

class MessagesList extends Component {
	render() {
		if (this.props.isDataLoading) {
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

		if (this.props.messages.length === 0) {
			return (
				<div className="container">
					<div className="card">
						<div className="card-body">
							<div className="card-text text-center">Nothing has been found...</div>
						</div>
					</div>
				</div>
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

export default MessagesList;

Modal.setAppElement('body');

class MessageItem extends Component {
	constructor (props) {
		super(props);
		this.state = {
			showModal: false,
			isDataLoaded: false,
			data: { "text" : this.props.value["summary"]}
		};
	
		this.handleOpenModal = this.handleOpenModal.bind(this);
		this.handleCloseModal = this.handleCloseModal.bind(this);
	}

	loadData() {
		var query = this.props.value

		fetch('http://localhost:8000/letters/?get_text=1&source=' 
				+ query["source"] + '&target=' + query["target"] 
				+ '&date=' + query["date"] + '&topic=' + query["topic"])
			.then(response => response.json())
			.then(data => this.setState({ data: data["0"]}));
	}

	handleOpenModal () {
		if (!this.state.isDataLoaded) {
			this.loadData();
			this.setState( {isDataLoaded : true} );
		}

		this.setState({ showModal: true });
	}

	handleCloseModal () {
		this.setState({ showModal: false });
	}

	render() {
		var dateFormat = require('dateformat');
		var date = this.props.value["date"]

		return (
		<div>
		
		<div className="card" onClick={this.handleOpenModal}>
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

		<Modal isOpen={this.state.showModal} onRequestClose={this.handleCloseModal} style={customStyles}>
			
			<button onClick={this.handleCloseModal} type="button" class="close" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			</button>
					
			<dl className="row">
				<dt className="col-sm-2">
					<p className="font-italic"> From </p>
				</dt>

				<dd className="col-sm-10">
					{this.props.value["source"]}
				</dd>
				
				<dt className="col-sm-2">
					<p className="font-italic">To</p>
				</dt>
				<dd className="col-sm-10">{this.props.value["target"]}</dd>

				<dd className="col-sm-10"> 
					<p className="font-weight-bold">
						{dateFormat(date, "default")}
					</p> 
				</dd>
			</dl>

			<p className="font-weight-light">
				{this.state.data["text"]}
			</p>
		</Modal>
		</div>
		);
	}
}

const customStyles = {
	content : {
		top : '10%',
		left : '20%',
		right : '20%',
		bottom : '10%'
	}
};