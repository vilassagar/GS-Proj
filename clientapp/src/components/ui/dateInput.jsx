import React from "react";
import PropTypes from "prop-types";

const DateInput = ({
  label,
  id,
  name,
  value,
  onChange,
  error,
  required,
  disabled,
  min,
  max,
  className = "",
}) => {
  return (
    <div className="space-y-1">
      {label && (
        <label
          htmlFor={id || name}
          className="block text-sm font-medium text-gray-700"
        >
          {label} {required && <span className="text-red-600">*</span>}
        </label>
      )}

      <input
        type="date"
        id={id || name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        disabled={disabled}
        min={min}
        max={max}
        className={`border rounded px-3 py-2 w-full ${
          error ? "border-red-500" : "border-gray-300"
        } ${className}`}
      />

      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
};

DateInput.defaultProps = {
  label: "",
  id: "",
  value: "",
  error: "",
  required: false,
  disabled: false,
  min: "",
  max: "",
  className: "",
};

DateInput.propTypes = {
  label: PropTypes.string,
  id: PropTypes.string,
  name: PropTypes.string.isRequired,
  value: PropTypes.string, // Format: 'YYYY-MM-DD'
  onChange: PropTypes.func.isRequired,
  error: PropTypes.string,
  required: PropTypes.bool,
  disabled: PropTypes.bool,
  min: PropTypes.string,
  max: PropTypes.string,
  className: PropTypes.string,
};

export default DateInput;
