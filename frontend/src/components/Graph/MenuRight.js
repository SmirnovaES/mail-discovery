import React, { Component } from 'react'
import './MenuRight.css'

class MenuRight extends Component {
    constructor(props){
        super(props);
        this.state = {
            elements: this.props.topics
        };
    }

	render() {
		return (
            <div id="container">
                <div id="scrollbox" >
                    <div id="content">
                        {this.state.elements.map((topic, index) => (
                            <Topic key={index} value={topic}/>
                        ))}
                    </div>
                </div>
            </div>
		);
	}
}
export default MenuRight

class Topic extends Component {

	render() {
		return (
            <div>
                <div className="input-group mb-3">
                    <div className="input-group-prepend">
                        <div className="input-group-text">
                            <input type="checkbox" aria-label="Checkbox for following text input"
                                onChange={function (e) {console.log(e.target.checked)}}/>
                        </div>
                    </div>
                    <div className="input-group-text">
                        {this.props.value}
                    </div>     
                </div>
            </div>
		);
	}
}