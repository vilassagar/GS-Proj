import * as yup from "yup";

const userProfileSchema = () => {
  return yup.object().shape({
    roles: yup.array().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() !== "pensioner",
      then: () =>
        yup
          .array()
          .of(
            yup.object().shape({
              id: yup.number(),
              name: yup.string(),
            })
          )
          .min(1, "Role is required"),
      otherwise: () => yup.array(),
    }),
    firstName: yup.string().required("First Name is required"),
    lastName: yup.string().required("Last Name is required"),
    email: yup.string().email("Invalid Email").notRequired(),
    empId: yup.string().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() === "pensioner",
      then: () => yup.string().required("Emp ID is required"),
      otherwise: () => yup.string().notRequired(),
    }),
    mobileNumber: yup.string().required("Mobile Number is required"),
    organisation: yup.string().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() === "association",
      then: () => yup.object().required("Organisation is required"),
      otherwise: () => yup.object().notRequired().nullable(),
    }),
    association: yup.object().when("$userType", {
      is: (userType) =>
        (userType !== null && userType.toLowerCase().trim() === "pensioner") ||
        (userType !== null && userType.toLowerCase().trim() === "association"),
      then: () => yup.object().required("Association is required"),
      otherwise: () => yup.object().notRequired().nullable(),
    }),
    dateOfBirth: yup.string().required("Date Of Birth is required"),
    gender: yup.object().nullable(),
    state: yup.object().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() === "pensioner",
      then: () => yup.object().required("Sate is required"),
      otherwise: () => yup.object().notRequired().nullable(),
    }),
    pincode: yup.string().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() === "pensioner",
      then: () => yup.string().required("Pin code is required"),
      otherwise: () => yup.string().notRequired(),
    }),
    address: yup.string().when("$userType", {
      is: (userType) =>
        userType !== null && userType.toLowerCase().trim() === "pensioner",
      then: () => yup.string().required("Address is required"),
      otherwise: () => yup.string().notRequired(),
    }),
  });
};

export default userProfileSchema;
