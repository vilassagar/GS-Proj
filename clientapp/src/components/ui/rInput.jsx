import PropTypes from "prop-types";
import { Input } from "./input";
import { Label } from "./label";

const RInput = ({
  id,
  name,
  value,
  onChange,
  error,
  isRequired,
  isDisabled,
  label,
  placeholder,
  type,
  min,
  max,
}) => {
  return (
    <>
      {label.length ? (
        <Label htmlFor={id}>
          <span>{label}</span>
          {isRequired ? <span className="text-red-600	ml-1">*</span> : null}
        </Label>
      ) : null}
      <Input
        id={id}
        name={name}
        onChange={onChange}
        placeholder={placeholder}        
        className={
          error?.length
            ? " ring-red-600 focus-visible:ring-offset-0 focus-visible:ring-red-600 ring-1 "
            : "focus-visible:ring-offset-0 focus-visible:ring-1"
        }
        disabled={isDisabled}
        value={value === 0 ? "" : value}
        type={type}
        min={min}
        max={max}
      />
    </>
  );
};

RInput.defaultProps = {
  id: "",
  name: "",
  value: "",
  onChange: () => {},
  error: "",
  isRequired: false,
  isDisabled: false,
  label: "",
  placeholder: "",
  type: "number",
  min: "",
  max: "",
};

RInput.propTypes = {
  id: PropTypes.string,
  name: PropTypes.string,
  value: PropTypes.string,
  onChange: PropTypes.func,
  error: PropTypes.string,
  isRequired: PropTypes.bool,
  isDisabled: PropTypes.bool,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  type: PropTypes.string,
  min: PropTypes.string,
  max: PropTypes.string,
};

export default RInput;
