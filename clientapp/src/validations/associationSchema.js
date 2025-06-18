import * as yup from "yup";

const associationSchema = () => {
  return yup.object().shape({
    associationName: yup.string().required("Association Name is required"),
    associationCode: yup.string().nullable(),
    organisation: yup.object().required("Organisation Name is required"),
    parentAssociation: yup.object().nullable(),
    address1: yup.string().required("Address Line 1 is required"),
    address2: yup.string().required("Address Line 2 is required"),
    city: yup.string().required("City is required"),
    state: yup.object().required("State is required"),
    pinCode: yup.string().required("Pin Code is required"),
    country: yup.object().required("Country is required"),
    bank: yup.object().shape({
      bankName: yup.string().required("Bank Name is required"),
      branchName: yup.string().required("Branch Name is required"),
      accountName: yup.string().required("Account Name is required"),
      accountNumber: yup.string().required("Account Number is required"),
      ifscCode: yup.string().required("IFSC Code is required"),
      micrCode: yup.string().required("MICR Code is required"),
    }),
    associationContactDetails: yup
      .array()
      .of(
        yup.object().shape({
          firstName: yup.string().required("First Name is required"),
          lastName: yup.string().required("Last Name is required"),
          phone: yup.string().required("Phone Number is required"),
          email: yup
            .string()
            .email("Invalid email format")
            .required("Email is required"),
        })
      )
      .min(1, "At least one contact detail is required")
      .required("Contact details are required"),
    associationMessages: yup.array().of(
      yup.object().shape({
        name: yup.string().required("Name is required"),
        template: yup.string().required("Template is required"),
      })
    ),
   // mandateFile: yup.mixed().required("Mandate File is required"),
    qrCodeFile: yup.mixed().nullable(),
    acceptOnePayPayment: yup.boolean(),
    onePayId: yup.string().when("acceptOnePayPayment", {
      is: (val) => val === true,
      then: () => yup.string().required("Onepay ID is required"),
      otherwise: () => yup.string().nullable(),
    }),
  });
};

export default associationSchema;
