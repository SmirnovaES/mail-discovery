import React, { Component } from 'react'
import { BrowserRouter, Route } from 'react-router-dom'

import routes from './routes.js'
import Header from './Header.js'

import 'bootstrap/dist/css/bootstrap.css'
import 'font-awesome/css/font-awesome.css'
import 'react-input-range/lib/css/index.css'

class App extends Component {
	render() {
		const routeComponents = routes.map(({path, component}, key) => 
			<Route exact path={path} component={component} key={key} />);
		
		return (
			<BrowserRouter> 
				<div>
					<Header />
					{routeComponents}
				</div>
			</BrowserRouter> 
		)
	}
}

export default App