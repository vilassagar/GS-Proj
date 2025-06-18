import * as yup from "yup";

const signUpSchema = () => {
  return yup.object().shape({
    userType: yup.object().required("User type is required"),
    firstName: yup.string().required("First Name is required"),
    lastName: yup.string().required("Last Name is required"),
    email: yup
      .string()
      .nullable()
      .test("is-valid-email", "Invalid Email", (value) => {
        if (!value) return true; // Allow empty or null values
        return yup.string().email().isValidSync(value);
      }),
    countryCode: yup.number().required("Country Code is required"),
    mobileNumber: yup
      .string()
      .matches(/^\d{10}$/, "Mobile Number must be 10 digits")
      .required("Mobile Number is required"),
    organization: yup.object().nullable(),
    association: yup.object().required("Association is required"),
  });
};

export default signUpSchema;
