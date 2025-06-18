import * as yup from "yup";

export const organisationSchema = () =>
  yup.object().shape({
    name: yup.string().required("Organisation name is required"),
    description: yup.string(),
  });

export default organisationSchema;
