import React, { Component } from 'react';

class SearchForms extends Component {
	render() {
		return (
			<div>
				<div className='container'>
						<form>
						<div className='input-group'>
							<input className='form-control' type="text" placeholder='Search' box-shadow="none"/>
							
							<div className='input-group-btn'>
							<button className='btn btn-default' type='button'>
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

export default SearchForms
