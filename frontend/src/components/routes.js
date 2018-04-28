import Main from './Main.js'
import Graph from './Graph'
import Stats from './Stats'

const routes = [{
	path: '/',
	component: Main,
}, {
	path: '/graph',
	component: Graph,
}, {
	path: '/stats',
	component: Stats,
},
];

export default routes