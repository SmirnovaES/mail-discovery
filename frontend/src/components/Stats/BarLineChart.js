import * as d3 from 'd3'
import React from 'react'
import Chart from '../chart'
import Axis from '../axis'
import DataSeries from './DataSeries'

class BarLineChart extends React.Component {

  render () {
    return (
      <Chart
        width={this.props.width}
        height={this.props.height + this.props.margins.top + this.props.margins.bottom}>
          <g
            transform={`translate(${this.props.margins.left}, 	 ${this.props.margins.top})`}>
            <DataSeries
              height={this.props.height}
              width={this.props.height}
              lineData={this.props.linedata}
              barData={this.props.data}
            />
          </g>
      </Chart>
    )
  }
}

BarLineChart.propTypes = {
  margins: React.PropTypes.obj,
  barWidth: React.PropTypes.number,
  barMargin: React.PropTypes.number,
  width: React.PropTypes.number,
  height: React.PropTypes.number,
  className: React.PropTypes.string,
}

BarLineChart.defaultProps = {
  className: 'BarLineChart',
  margins: {top: 20, right: 20, bottom: 30, left: 40},
  barWidth: 15,
  barMargin: 15,
}

export default BarLineChart