import React, { Component } from 'react';
import ReactDOM from 'react-dom';

class SearchForm extends Component {
	onButtonClick() {
		this.props.update(ReactDOM.findDOMNode(this.refs.searchForm).value)
	}

	render() {
		return (
			<div>
				<div className='container'>
					<form>
						<div className='input-group'>
							<input ref="searchForm" className='form-control' type="text" placeholder='Search' box-shadow="none"/>
							
							<div className='input-group-btn'>
							<button onClick={this.onButtonClick.bind(this)} className='btn btn-default' type='button'>
								<span className='fa fa-search'></span>
							</button>
							</div>
						</div>
					</form>
				</div>
			</div>	
		)
	}
}

export default SearchForm
