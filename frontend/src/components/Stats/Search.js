import React, { Component } from 'react';
import SearchForm from './SearchForm.js'
import MessagesList from './MessagesList.js'


class Search extends Component {
	constructor() {
		super();
		
		this.state = {
			searchText: '',
			searchResults: null,
			isDataLoading: false
		}
	}

	updateSearchText(newText) {
		this.props.update(newText);
		this.setState({searchText: newText});
	}

	loadData() {
		this.setState({isDataLoading: true})
		var words = this.state.searchText.split(' ').join(',')

		fetch('http://localhost:8000/letters/?search_ais=1&words=' + words)
			.then(response => response.json())
			.then(data => this.setState({ searchResults: data, isDataLoading: false }));
	}

	componentWillMount() {
		this.loadData()
	}

	componentDidUpdate(prevProps, prevState) {
		if (prevState.searchText !== this.state.searchText) {
			this.loadData()
		}
	}

	render() {
		return (
			<div>
				<SearchForm update={this.updateSearchText.bind(this)}
							searchAis={this.props.searchAis}/>

				<MessagesList messages={this.state.searchResults} isDataLoading={this.state.isDataLoading}/>				
			</div>	
		)
	}
}

export default Search