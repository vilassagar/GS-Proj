import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import PropTypes from "prop-types";

export function ConfirmDialog({
  dialogTrigger,
  onCancel,
  onConfirm,
  dialogTitle,
  dialogDescription,
}) {
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>{dialogTrigger}</AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{dialogTitle}</AlertDialogTitle>
          <AlertDialogDescription>{dialogDescription}</AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={onCancel}>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={onConfirm}>Continue</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

ConfirmDialog.defaultProps = {
  dialogTrigger: <></>,
  onCancel: () => {},
  onConfirm: () => {},
  dialogTitle: "",
  dialogDescription: "",
};

ConfirmDialog.propTypes = {
  dialogTrigger: PropTypes.element,
  onCancel: PropTypes.func,
  onConfirm: PropTypes.func,
  dialogTitle: PropTypes.string,
  dialogDescription: PropTypes.string,
};
