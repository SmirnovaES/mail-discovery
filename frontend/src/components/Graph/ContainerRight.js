import React, { Component } from 'react'
import MenuRight from './MenuRight.js'

const API = 'http://localhost:8000/letters/?get_topics=';
const DEFAULT_QUERY = '1';

//FOR DEBUG
const QUERY = 'http://localhost:8001/topics.json'

class ContainerRight extends Component {
    constructor(props){
        super(props);
        this.state = {
            isClicked: false,
            topics: [],
            isDataLoading: false,
        };

        this.handleClick = this.handleClick.bind(this);
    }


    handleClick() {
        this.setState( {isClicked: true, isDataLoading: true });
        

        fetch(API + DEFAULT_QUERY)
            .then(response => 
            {
                if (!response.ok) {
                    throw Error(response.statusText);
                }
                return response.json();
            })            
            .then(data => this.setState({ topics: data, isDataLoading: false }))
            .catch(function(error) {
                console.log(error);
            })
    }

	render() {
        const { topics, isDataLoading, isClicked } = this.state;

        if (!isClicked) {
            return (
                <div>
                    <button onClick={this.handleClick} type="button" class="btn btn-light">
                            Start Topic Modeling
                    </button>
                </div>
            );
        }

        if (isDataLoading) {
            return (
                <div>
                    Loading ... 
                </div>
            );
        }

        return (
            <MenuRight topics={topics}/>
        );
    }
}

export default ContainerRight