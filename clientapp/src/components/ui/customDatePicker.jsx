/* eslint-disable react/prop-types */
import React, { useState, useEffect, useRef } from "react";
import { format, isValid, parse } from "date-fns";

const CustomDatePicker = ({
  label,
  id,
  placeholder = "dd/mm/yyyy",
  onChange,
  isRequired = false,
  error,
  isDisabled = false,
  date,
  isFutureDateAllowed = true,
}) => {
  const [inputDate, setInputDate] = useState("");
  const [showCalendar, setShowCalendar] = useState(false);
  const calendarRef = useRef(null); // Ref to track calendar popover

  const minDate = "1930-01-01";
  const today = new Date().toISOString().split("T")[0];

  useEffect(() => {
    if (date) {
      const parsedDate = new Date(date);
      if (isValid(parsedDate) && parsedDate >= new Date(minDate)) {
        setInputDate(format(parsedDate, "dd/MM/yyyy"));
      } else {
        console.error("Invalid date provided or date before 1930:", date);
        setInputDate("");
      }
    } else {
      setInputDate("");
    }
  }, [date]);

  const handleDateChange = (e) => {
    const newDate = e.target.value;
    const parsedDate = parse(newDate, "yyyy-MM-dd", new Date());

    if (isValid(parsedDate)) {
      setInputDate(format(parsedDate, "dd/MM/yyyy"));

      if (onChange) {
        // Pass the date back in the "yyyy-MM-dd" format
        onChange(format(parsedDate, "yyyy-MM-dd"));
      }

      setShowCalendar(false); // Close popover only when selecting a date from the calendar
    }
  };

  const handleInputChange = (e) => {
    const userInput = e.target.value;
    setInputDate(userInput);

    const parsedDate = parse(userInput, "dd/MM/yyyy", new Date());
    if (isValid(parsedDate)) {
      if (onChange) {
        // Convert to "yyyy-MM-dd" for internal use
        onChange(format(parsedDate, "yyyy-MM-dd"));
      }
    }
    // Keep the calendar open while typing manually
    setShowCalendar(true);
  };

  const toggleCalendar = () => {
    if (!isDisabled) {
      setShowCalendar(!showCalendar);
    }
  };

  // Handle click outside of the calendar
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (calendarRef.current && !calendarRef.current.contains(event.target)) {
        setShowCalendar(false); // Close the calendar if clicked outside
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const getParsedDate = (dateStr) => {
    const parsedDate = parse(dateStr, "dd/MM/yyyy", new Date());
    return isValid(parsedDate) ? format(parsedDate, "yyyy-MM-dd") : ""; // Ensure only valid dates are used
  };

  return (
    <div className="relative">
      <label
        htmlFor={id}
        className="block text-sm font-medium text-gray-700 mb-1"
      >
        {label} {isRequired && <span className="text-red-500">*</span>}
      </label>
      <input
        type="text"
        id={id}
        name={id}
        value={inputDate}
        onChange={handleInputChange} // Allow manual date entry
        onClick={toggleCalendar} // Open calendar on click
        placeholder={placeholder}
        className={`w-full px-4 py-2 text-gray-700 bg-white border rounded-lg focus:outline-none ${
          isDisabled ? "bg-gray-100 cursor-not-allowed" : ""
        }`}
        disabled={isDisabled}
      />
      {showCalendar && (
        <div
          ref={calendarRef}
          className="absolute z-10 mt-1 bg-white border rounded-lg shadow-lg"
        >
          <input
            type="date"
            value={getParsedDate(inputDate) || ""} // Ensure valid date or pass empty string
            onChange={handleDateChange}
            min={minDate}
            max={isFutureDateAllowed ? undefined : today}
            className="p-2"
          />
        </div>
      )}
    </div>
  );
};

export default CustomDatePicker;
