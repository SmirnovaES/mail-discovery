import React, { Component } from 'react'
import './Messages.css'

class Messages extends Component {
    constructor(props){
        super(props);
        this.state = {
            elements: []
        };
        var i;
        for (i = 0; i < 15; i++) {
            this.state.elements.push('Предпоказ сообщений')
        }
    }

	render() {
		return (
            <div id="messageBox">
                <div id="scrolling" >
                    <div id="message">
                        {this.state.elements.map((message, index) => (
                            <Message key={index} value={message}/>
                        ))}
                    </div>
                </div>
            </div>
		);
	}
}
export default Messages

class Message extends Component {

	render() {
		return (
            <div>
                <div className="input-group mb-3">
                    <div className="input-group-text">
                        {this.props.value}
                    </div>     
                </div>
            </div>
		);
	}
}
