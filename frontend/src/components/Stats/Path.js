import React from 'react';

const Path = (props) => {
  return (
    <path
      className={props.class}
      d={props.path}
      {...props} />
  );
}

Path.propTypes = {
  fill: React.PropTypes.string,
  path: React.PropTypes.string,
  stroke: React.PropTypes.string,
  strokeWidth: React.PropTypes.number,
  className: React.PropTypes.string
}

Path.defaultProps = { className: 'linechart-path' };

export default Path;