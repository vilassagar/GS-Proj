import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { getYears, months } from "@/lib/data";
import { useDateStore } from "@/lib/store";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { Combobox } from "./comboBox";

export function DatePicker({
  date,
  onChange,
  error,
  isDisabled,
  isRequired,
  label,
  id,
  size,
  fromDate,
  isFutureDateAllowed,
}) {
  const monthInfo = useDateStore((state) => state.months);
  const yearInfo = useDateStore((state) => state.years);

  const [selectedDate, setSelectedDate] = useState(null);
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const [month, setMonth] = useState(null);
  const [year, setYear] = useState(null);

  const parseDate = (dateInput) => {
    if (!dateInput) return null;

    // Handle both string and Date object inputs
    const parsedDate =
      typeof dateInput === "string" ? new Date(dateInput) : dateInput;

    // Ensure the date is at the start of the day in local time zone
    return new Date(
      parsedDate.getFullYear(),
      parsedDate.getMonth(),
      parsedDate.getDate()
    );
  };

  useEffect(() => {
    const parsedDate = parseDate(date);

    if (parsedDate) {
      setSelectedDate(parsedDate);

      const dateMonth = parsedDate.getMonth();
      const dateYear = parsedDate.getFullYear();

      setMonth(monthInfo[dateMonth]);
      setYear(yearInfo[dateYear]);
    } else {
      const currentDate = new Date();

      let currentMonth = currentDate.getMonth();
      let info = monthInfo[currentMonth];
      setMonth(monthInfo[currentDate.getMonth()]);
      setYear(yearInfo[currentDate.getFullYear()]);
    }
  }, [date, monthInfo, yearInfo]);

  const handleSelectDate = (selectedDate) => {
    // Create a new date with time set to midnight in local timezone
    const localDate = new Date(
      selectedDate.getFullYear(),
      selectedDate.getMonth(),
      selectedDate.getDate(),
      0,
      0,
      0,
      0
    );

    // Explicitly format the date to avoid timezone conversion issues
    const formattedDate = `${localDate.getFullYear()}-${String(
      localDate.getMonth() + 1
    ).padStart(2, "0")}-${String(localDate.getDate()).padStart(2, "0")}`;

    setSelectedDate(localDate);
    onChange(formattedDate);
    setIsDatePickerOpen(false);
  };

  const handleChangeMonth = (event) => {
    debugger;
    setMonth(event);

    const currentDate = selectedDate || new Date();
    const newDate = new Date(
      currentDate.getFullYear(),
      event.id - 1,
      currentDate.getDate()
    );

    setSelectedDate(newDate);
    onChange(newDate.toISOString().split("T")[0]);
  };

  const handleChangeYear = (event) => {
    setYear(event);

    const currentDate = selectedDate || new Date();
    const newDate = new Date(
      event.id,
      currentDate.getMonth(),
      currentDate.getDate()
    );

    setSelectedDate(newDate);
    onChange(newDate.toISOString().split("T")[0]);
  };

  const handleArrowIconClick = (date) => {
    const dateMonth = date.getMonth();
    const dateYear = date.getFullYear();

    setMonth(monthInfo[dateMonth]);
    setYear(yearInfo[dateYear]);
    setSelectedDate(date);
  };

  const disabledDays = {
    before: fromDate ? new Date(fromDate) : undefined,
    after: !isFutureDateAllowed ? new Date() : undefined,
  };

  return (
    <div className="grid gap-1.5">
      {label.length ? (
        <Label htmlFor={id}>
          <span>{label}</span>
          {isRequired ? <span className="text-red-600 ml-1">*</span> : null}
        </Label>
      ) : null}
      <Popover open={isDatePickerOpen} onOpenChange={setIsDatePickerOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={`${
              error?.length
                ? "ring-red-600 focus-visible:ring-offset-0 focus-visible:ring-red-600 ring-1"
                : "focus-visible:ring-offset-0 focus-visible:ring-1"
            } justify-start text-left font-normal`}
            disabled={isDisabled}
            size={size}
            onClick={() => {
              setIsDatePickerOpen(true);
            }}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {selectedDate ? (
              format(selectedDate, "PPP")
            ) : (
              <span>Pick a date</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <div className="flex justify-between p-3">
            <Combobox
              placeholder="Month"
              options={months}
              value={month}
              onChange={handleChangeMonth}
            />
            <Combobox
              placeholder="Year"
              options={getYears()}
              value={year}
              onChange={handleChangeYear}
            />
          </div>
          <Calendar
            mode="single"
            onSelect={handleSelectDate}
            selected={selectedDate}
            onChange={handleChangeYear}
            month={selectedDate || new Date()}
            onMonthChange={handleArrowIconClick}
            disabled={disabledDays}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}

DatePicker.defaultProps = {
  id: "",
  name: "",
  date: "",
  onChange: () => {},
  error: "",
  isRequired: false,
  isDisabled: false,
  label: "",
  placeholder: "",
  size: "sm",
  fromDate: "",
  isFutureDateAllowed: true,
};

DatePicker.propTypes = {
  id: PropTypes.string,
  name: PropTypes.string,
  date: PropTypes.oneOfType([PropTypes.string, PropTypes.instanceOf(Date)]),
  onChange: PropTypes.func,
  error: PropTypes.string,
  isRequired: PropTypes.bool,
  isDisabled: PropTypes.bool,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  size: PropTypes.string,
  fromDate: PropTypes.string,
  isFutureDateAllowed: PropTypes.bool,
};

export default DatePicker;
