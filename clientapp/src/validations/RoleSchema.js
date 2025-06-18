import * as yup from "yup";

export const roleSchema = yup.object().shape({
  name: yup.string().required("Role name is required"),
  description: yup.string().required("Description is required"),
  permissions: yup.array().of(
    yup.object().shape({
      type: yup.string(),
      name: yup.string(),
      actions: yup.object().shape({
        create: yup.boolean(),
        read: yup.boolean(),
        update: yup.boolean(),
        delete: yup.boolean(),
      }),
    })
  ),
});
