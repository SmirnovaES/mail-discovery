import React from 'react'
import Main from './Main.js'
import UnionPage from './UnionPage'

const routes = [{
	path: '/',
	component: Main,
}, {
	path: '/graph',
	component: () => <UnionPage flag={1}/>,
}, {
	path: '/stats',
	component: () => <UnionPage flag={0}/>,
},
];

export default routes