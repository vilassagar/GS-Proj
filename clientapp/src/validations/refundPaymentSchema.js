import * as yup from "yup";

const refundPaymentSchema = (activeTab) =>
  yup.object().shape({
    chequeDetails: yup.object().shape({
      chequeNumber: yup.string().when("$activeTab", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Cheque Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      chequeBankName: yup.string().when("$activeTab", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Bank Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      chequeDate: yup.string().when("$activeTab", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("Date is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      inFavourOf: yup.string().when("$activeTab", {
        is: (val) => val === "cheque",
        then: () => yup.string().required("In Favour Of  Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      chequePhoto: yup.mixed().when("$activeTab", {
        is: (val) => val === "cheque",
        then: () => yup.object().required("Cheque photo is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
    }),
    neft: yup.object().shape({
      neftBankName: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Bank Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftBranchName: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Branch Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftAccountName: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Account Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftAccountNumber: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Account Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftIfscCode: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("IFSC Code is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftTransactionId: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Transaction Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftDate: yup.string().when("$activeTab", {
        is: (val) => val === "neft",
        then: () => yup.string().required("Date is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      neftPaymentReceipt: yup.mixed().when("$activeTab", {
        is: (val) => val === "neft",
        then: () =>
          yup.object().required("Neft payment receipt  photo is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
    }),
    upi: yup.object().shape({
      upiTransactionId: yup.string().when("$activeTab", {
        is: (val) => val === "upi",
        then: () => yup.string().required("Transaction Number is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      upiDate: yup.string().when("$activeTab", {
        is: (val) => val === "upi",
        then: () => yup.string().required("Date is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      upiPaymentReceipt: yup.mixed().when("$activeTab", {
        is: (val) => val === "upi",
        then: () =>
          yup.object().required("UPI payment receipt photo is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
    }),
  });

export default refundPaymentSchema;
