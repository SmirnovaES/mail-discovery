import React from 'react'
import './GraphViz.css'
import GraphV from './Graph'

class GraphViz extends React.Component {

    static propTypes = {}

    componentDidMount() {
        // D3 Code to create the chart
        this._chart = GraphV.create(
            this._rootNode,
            this.props.loadData,
            this.props.readyToLoad,
            this.props.onChangeLoading
        );
    }

    componentDidUpdate() {
        // D3 Code to update the chart
        GraphV.update(
           this._rootNode,
           this.props.loadData,
           this.props.readyToLoad,
           this.props.onChangeLoading,
           this._chart
        );
    }

    componentWillUnmount() {
        GraphV.destroy(this._rootNode);
    }

    _setRef(componentNode) {
        this._rootNode = componentNode;
    }

    render() {
        return <svg height="500"  viewBox="-300 -300 665 665" ref={this._setRef.bind(this)} />
    }
}

export default GraphViz
