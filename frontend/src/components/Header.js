import React, { Component } from 'react'
import { Link } from 'react-router-dom'

class Header extends Component {
	render() {
		return (
			<div>
				<nav className="navbar navbar-expand-lg navbar-light bg-light">
					<div className='container'>
						<Link className="navbar-brand" to="/">
							<img src={require("../images/logo.png")} className="d-inline-block vertical-align-middle" alt="">
							</img>
							<span align="right">More than e-mail</span>
						</Link>
						
						<div className="collapse navbar-collapse">
							<ul className="navbar-nav ml-auto">
								<li className="nav-item">
									<Link className="nav-link" to="/">Main</Link>
								</li>
								<li className="nav-item">
									<Link className="nav-link" to="/graph">Graph</Link>
								</li>
								<li className="nav-item">
									<Link className="nav-link" to="/stats">Statistics</Link>
								</li>
							</ul>
						</div>
					</div>
				</nav>
			</div>
		)
	}
}

export default Header