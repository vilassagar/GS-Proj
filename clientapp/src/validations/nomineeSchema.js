import * as yup from "yup";

const nomineeSchema = () => {
  return yup.object().shape({
    nominee: yup.object().shape({
      name: yup.string().required("Name is required"),
      gender: yup.object().required("Gender is required"),
      dateOfBirth: yup.string().required("Date of birth is required"),
      nomineeRelation: yup.object().required("Nominee relation is required"),
    }),
  });
};

export default nomineeSchema;
