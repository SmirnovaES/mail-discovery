import React from 'react';

const BarChart = (props) => {
  return (
    <rect
      className={props.className}
      {...props}
    />
  );
}

BarChart.propTypes = {
  fill: React.PropTypes.string,
  width: React.PropTypes.number,
  height: React.PropTypes.number,
  x: React.PropTypes.number,
  y: React.PropTypes.number,
  className: React.PropTypes.string
}

BarChart.defaultProps = { className: 'barchart-bar' };

export default BarChart;
