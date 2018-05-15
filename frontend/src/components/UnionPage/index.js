import React from 'react'
import Graph from '../Graph'
import Stats from '../Stats'

var _timeRange = {min : new Date('2001-04-04,13:10').getTime(), 
						max : new Date('2001-04-04,14:10').getTime()};
var _users = [];
var _topics = [];
var _searchAis = '';

class UnionPage extends React.Component {
    constructor(props) {
        super(props);
		
		this.updateTimeRange = this.updateTimeRange.bind(this);
		this.updateUsers = this.updateUsers.bind(this);
		this.updateSearchText = this.updateSearchText.bind(this);
		this.updateTopics = this.updateTopics.bind(this);
    }
	
	updateTimeRange(newTimeRange) {
		_timeRange = newTimeRange;
	}

	updateUsers(newUsers) {
		_users = newUsers;
    }

    updateSearchText(newSearchAis) {
		_searchAis = newSearchAis;
    }

    updateTopics(newTopics) {
		_topics = newTopics;
	}

    render() {
        if (this.props.flag === 1) {
            return <Graph 
                timeRange={_timeRange}
                users={_users}
                topics={_topics}
                searchAis={_searchAis}
                updateTimeRange={this.updateTimeRange}
                updateUsers={this.updateUsers}
                updateSearchText={this.updateSearchText}
                updateTopics={this.updateTopics}
                />
        } else {
            return <Stats 
                timeRange={_timeRange}
                users={_users}
                topics={_topics}
                searchAis={_searchAis}
                updateTimeRange={this.updateTimeRange}
                updateUsers={this.updateUsers}
                updateSearchText={this.updateSearchText}
                updateTopics={this.updateTopics}/>
        }
    }
}

export default UnionPage
