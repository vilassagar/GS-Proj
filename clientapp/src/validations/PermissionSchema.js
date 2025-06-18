import * as yup from "yup";

export const permissionSchema = yup.object().shape({
  type: yup.mixed().required("Permission type is required"),
  name: yup.string().required("Permission name is required"),
  actions: yup.object({
    create: yup.boolean(),
    read: yup.boolean(),
    update: yup.boolean(),
    delete: yup.boolean(),
  }),
});
