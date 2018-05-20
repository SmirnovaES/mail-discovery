import React, { Component } from 'react';

class SearchForm extends Component {
	constructor(props) {
    	super(props);
    	this.state = {
    		value: this.props.searchAis
    	};

    	this.handleChange = this.handleChange.bind(this);
    	this.handleSubmit = this.handleSubmit.bind(this);
  	}

  	handleChange(event) {
    	this.setState({value: event.target.value});
  	}

  	handleSubmit(event) {
    	this.props.onUserInput(this.state.value)
    	event.preventDefault();
  	}

	render() {
		return (
			<div>
				<div className='container'>
					<form onSubmit={this.handleSubmit}>
						<div className='input-group'>
							<input type="text" className='form-control' placeholder='Search' value={this.state.value} onChange={this.handleChange} />
       						<button className='btn btn-default' type='submit'>
								<span className='fa fa-search'></span>
							</button>
       					</div>
      				</form>
				</div>
			</div>	
		)
	}
}

export default SearchForm