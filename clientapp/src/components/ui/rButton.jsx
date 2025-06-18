import { Loader2 } from "lucide-react";
import PropTypes from "prop-types";
import { Button } from "./button";

export default function RButton({
  onClick,
  isLoading,
  isDisabled,
  children,
  className,
  type,
  variant,
}) {
  return (
    <Button
      type={type}
      className={className}
      onClick={onClick}
      disabled={isDisabled || isLoading}
      size="sm"
      variant={variant}
    >
      {isLoading ? (
        <span className="flex items-center">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Please wait
        </span>
      ) : (
        <span>{children}</span>
      )}
    </Button>
  );
}

RButton.defaultProps = {
  onClick: () => {},
  isLoading: false,
  isDisabled: false,
  children: <></>,
  className: "",
  type: "",
  variant: "",
};

RButton.propTypes = {
  onClick: PropTypes.func,
  isLoading: PropTypes.bool,
  isDisabled: PropTypes.bool,
  children: PropTypes.element,
  className: PropTypes.string,
  type: PropTypes.string,
  variant: PropTypes.string,
};
