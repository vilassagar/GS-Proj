import * as React from "react";
import { addDays, format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import PropTypes from "prop-types";
import { Label } from "./label";

export function DateRangePicker({
  className,
  dates,
  onChange,
  error,
  isDisabled,
  isRequired,
  label,
  id,
  size,
}) {
  const [selectedDates, setSelectedDates] = React.useState(null);
  const [isDatePickerOpen, setIsDatePickerOpen] = React.useState(false);

  React.useEffect(() => {
    (() => {
      if (!dates?.from?.length && !dates?.to?.length) {
        setSelectedDates(null);
      }
      if (dates?.from?.length && dates?.to?.length) {
        setSelectedDates({
          from: new Date(dates?.from),
          to: new Date(dates?.to),
        });
      }
    })();
  }, [dates]);

  const handleChange = (e) => {
    setSelectedDates(e);
    onChange({
      from: e?.from?.toISOString() || "",
      to: e?.to?.toISOString() || "",
    });

    if (e?.to) {
      setIsDatePickerOpen(false);
    }
  };

  return (
    <div className={cn("grid gap-2", className)}>
      {label.length ? (
        <Label htmlFor={id}>
          <span>{label}</span>
          {isRequired ? <span className="text-red-600	ml-1">*</span> : null}
        </Label>
      ) : null}
      <Popover open={isDatePickerOpen} onOpenChange={setIsDatePickerOpen}>
        <PopoverTrigger asChild>
          <Button
            id="date"
            variant={"outline"}
            className={cn(
              "w-[300px] justify-start text-left font-normal",
              !selectedDates && "text-muted-foreground",
              error?.length &&
                "ring-red-600 focus-visible:ring-offset-0 focus-visible:ring-red-600 ring-1"
            )}
            disabled={isDisabled}
            size={size}
            onClick={() => {
              setIsDatePickerOpen(true);
            }}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {selectedDates?.from ? (
              selectedDates.to ? (
                <>
                  {format(selectedDates.from, "LLL dd, y")} -{" "}
                  {format(selectedDates.to, "LLL dd, y")}
                </>
              ) : (
                format(selectedDates.from, "LLL dd, y")
              )
            ) : (
              <span>Pick a date</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            initialFocus
            mode="range"
            defaultMonth={selectedDates?.from}
            selected={selectedDates}
            onSelect={handleChange}
            numberOfMonths={2}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}

DateRangePicker.defaultProps = {
  id: "",
  className: "",
  dates: null,
  onChange: () => {},
  error: "",
  isRequired: false,
  isDisabled: false,
  label: "",
  placeholder: "",
  size: "sm",
};

DateRangePicker.propTypes = {
  id: PropTypes.string,
  className: PropTypes.string,
  dates: PropTypes.object,
  onChange: PropTypes.func,
  error: PropTypes.string,
  isRequired: PropTypes.bool,
  isDisabled: PropTypes.bool,
  label: PropTypes.string,
  placeholder: PropTypes.string,
  size: PropTypes.string,
};
