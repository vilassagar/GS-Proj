export const YesNoQuestion = ({ label, name, value, onChange }) => {
  return (
    <div>
      <span className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </span>
      <div className="flex space-x-4">
        <label className="inline-flex items-center">
          <input
            type="radio"
            name={name}
            value="yes"
            checked={value === true}
            onChange={() => onChange(true)}
            className="form-radio h-4 w-4 text-indigo-600"
          />
          <span className="ml-2">Yes</span>
        </label>
        <label className="inline-flex items-center">
          <input
            type="radio"
            name={name}
            value="no"
            checked={value === false}
            onChange={() => onChange(false)}
            className="form-radio h-4 w-4 text-indigo-600"
          />
          <span className="ml-2">No</span>
        </label>
      </div>
    </div>
  );
};

export default YesNoQuestion;
