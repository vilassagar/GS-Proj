import * as yup from "yup";

const beneficarySchema = () => {
  return yup.object().shape({
    spouse: yup.object().shape({
      name: yup
        .string()
        .when(
          [
            "$isSpousePremiumSelected",
            "$isSelfSpousePremiumSelected",
            "$isTopUpSelfSpousePremiumSelected",
          ],
          {
            is: (
              isSpousePremiumSelected,
              isSelfSpousePremiumSelected,
              isTopUpSelfSpousePremiumSelected
            ) =>
              isSpousePremiumSelected === true ||
              isSelfSpousePremiumSelected === true ||
              isTopUpSelfSpousePremiumSelected === true,
            then: () => yup.string().required("Name is required"),
            otherwise: () => yup.string().notRequired().nullable(),
          }
        ),
      gender: yup
        .object()
        .when(
          [
            "$isSpousePremiumSelected",
            "$isSelfSpousePremiumSelected",
            "$isTopUpSelfSpousePremiumSelected",
          ],
          {
            is: (
              isSpousePremiumSelected,
              isSelfSpousePremiumSelected,
              isTopUpSelfSpousePremiumSelected
            ) =>
              isSpousePremiumSelected === true ||
              isSelfSpousePremiumSelected === true ||
              isTopUpSelfSpousePremiumSelected === true,
            then: () => yup.object().required("Gender is required"),
            otherwise: () => yup.object().notRequired().nullable(),
          }
        ),
      dateOfBirth: yup
        .string()
        .when(
          [
            "$isSpousePremiumSelected",
            "$isSelfSpousePremiumSelected",
            "$isTopUpSelfSpousePremiumSelected",
          ],
          {
            is: (
              isSpousePremiumSelected,
              isSelfSpousePremiumSelected,
              isTopUpSelfSpousePremiumSelected
            ) =>
              isSpousePremiumSelected === true ||
              isSelfSpousePremiumSelected === true ||
              isTopUpSelfSpousePremiumSelected === true,
            then: () => yup.string().required("Date of birth is required"),
            otherwise: () => yup.string().notRequired().nullable(),
          }
        ),
    }),
    child1: yup.object().shape({
      name: yup.string().when("$isChild1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isChild1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isChild1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      disabilityCertificate: yup.object().when("$isChild1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Disablity certificate is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
    }),
    child2: yup.object().shape({
      name: yup.string().when("$isChild2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isChild2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isChild2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      disabilityCertificate: yup.object().when("$isChild2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Disablity certificate is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
    }),
    parent1: yup.object().shape({
      name: yup.string().when("$isParent1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isParent1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isParent1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
    }),
    parent2: yup.object().shape({
      name: yup.string().when("$isParent2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isParent2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isParent2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
    }),
    inLaw1: yup.object().shape({
      name: yup.string().when("$isInLaw1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isInLaw1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isInLaw1PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
    }),
    inLaw2: yup.object().shape({
      name: yup.string().when("$isInLaw2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Name is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
      gender: yup.object().when("$isInLaw2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.object().required("Gender is required"),
        otherwise: () => yup.object().notRequired().nullable(),
      }),
      dateOfBirth: yup.string().when("$isInLaw2PremiumSelected", {
        is: (val) => val === true,
        then: () => yup.string().required("Date of birth is required"),
        otherwise: () => yup.string().notRequired().nullable(),
      }),
    }),
  });
};

export default beneficarySchema;
