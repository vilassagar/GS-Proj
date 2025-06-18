import * as React from "react";
import { Check, ChevronsUpDown } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import PropTypes from "prop-types";

export function Combobox({
  options,
  onChange,
  valueProperty,
  labelProperty,
  value,
  isDisabled,
  error,
  id,
  placeholder,
}) {
  const [open, setOpen] = React.useState(false);
  const [cOptions, setCOptions] = React.useState([]);

  React.useEffect(() => {
    if (Array.isArray(options)) {
      setCOptions(options);
    }
  }, [options]);

  const handleChange = (value) => (e) => {
    onChange(value);
    setOpen(false);
  };

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          disabled={isDisabled}
          className={
            error.length
              ? " ring-red-600 focus-visible:ring-offset-0 focus-visible:ring-red-600 ring-1 flex justify-between overflow-hidden text-ellipsis "
              : "focus-visible:ring-offset-0 focus-visible:ring-1 flex justify-between overflow-hidden text-ellipsis "
          }
          id={id}
          size="sm"
        >
          {value !== null
            ? cOptions.find(
                (option) => option[valueProperty] === value[valueProperty]
              )?.[labelProperty]
            : placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search option..." />
          <CommandList>
            <CommandEmpty>No option found.</CommandEmpty>
            <CommandGroup>
              {cOptions.map((option) => (
                <CommandItem
                  key={option[valueProperty]}
                  value={option[valueProperty]}
                  onSelect={handleChange(option)}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      value?.[valueProperty] === option?.[valueProperty]
                        ? "opacity-100"
                        : "opacity-0"
                    )}
                  />
                  {option[labelProperty]}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

Combobox.defaultProps = {
  options: [],
  onChange: () => {},
  valueProperty: "id",
  labelProperty: "name",
  value: null,
  isDisabled: false,
  error: "",
  id: "",
  placeholder: "Select option...",
};

Combobox.propTypes = {
  options: PropTypes.array,
  onChange: PropTypes.func,
  valueProperty: PropTypes.string,
  labelProperty: PropTypes.string,
  value: PropTypes.object,
  isDisabled: PropTypes.bool,
  error: PropTypes.string,
  id: PropTypes.string,
  placeholder: PropTypes.string,
};
