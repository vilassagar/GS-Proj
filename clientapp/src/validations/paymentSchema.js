import * as yup from "yup";

const paymentSchema = () => {
  return yup.object().shape({
    paymentMode: yup.object().nullable(),
    chequeDetails: yup.object().shape({
      chequeNumber: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Cheque Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      amount: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("amount is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      bankName: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Bank name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      date: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Date name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      inFavourOf: yup.object().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.object().required("Association name is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      micrCode: yup.object().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().notRequired().nullable(),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      ifscCode: yup.object().when("$offlinePaymentMode", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("IFSC Code is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),

      chequeDepositLocation: yup.string().notRequired().nullable(),
      chequePhoto: yup.object().notRequired().nullable(),
    }),
    neft: yup.object().shape({
      bankName: yup.string().notRequired().nullable(),
      branchName: yup.string().notRequired().nullable(),
      accountName: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Account Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      accountNumber: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Account Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      ifscCode: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("IFSC code is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      transactionId: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Transaction ID is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      amount: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("amount is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      date: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Date name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftPaymentReceipt: yup.object().notRequired().nullable(),
    }),
    upi: yup.object().shape({
      transactionId: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "upi",
        then: () => yup.string().required("Transaction ID is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      amount: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "upi",
        then: () => yup.string().required("amount is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      date: yup.string().when("$offlinePaymentMode", {
        is: (val) => val === "upi",
        then: () => yup.string().required("Date name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      upiPaymentReceipt: yup.object().notRequired().nullable(),
    }),
  });
};

export default paymentSchema;
