import * as yup from "yup";

const productValidation = () => {
  return yup.object().shape({
    productName: yup.string().required("Product Name is required"),
    providerName: yup.string().nullable(),
    policyType: yup.object().required("Policy type is required"),
    basePolicy: yup.object().when("policyType", {
      is: (val) =>
        val !== null && val.name.toLowerCase().trim() === "topuppolicy",
      then: () => yup.object().required("Base policy is required"),
      otherwise: () => yup.object().notRequired().nullable(),
    }),
    isSpouseCoverage: yup.boolean(),
    isHandicappedChildrenCoverage: yup.boolean(),
    isParentsCoverage: yup.boolean(),
    isInLawsCoverage: yup.boolean(),
    numberOfHandicappedChildren: yup
      .number()
      .when(["isHandicappedChildrenCoverage", "$policyType"], {
        is: (isHandicappedChildrenCoverage, policyType) =>
          policyType.toLowerCase().trim() === "basepolicy" &&
          isHandicappedChildrenCoverage === true,
        then: () =>
          yup
            .number()
            .min(1)
            .max(2)
            .required("Number Of Handicaped children is required"),
        otherwise: () => yup.number(),
      }),
    numberOfParents: yup.number().when(["isParentsCoverage", "$policyType"], {
      is: (isParentsCoverage, policyType) =>
        policyType.toLowerCase().trim() === "basepolicy" &&
        isParentsCoverage === true,
      then: () =>
        yup.number().min(1).max(2).required("Number Of parents is required"),
      otherwise: () => yup.number(),
    }),
    numberOfInLaws: yup.number().when(["isInLawsCoverage", "$policyType"], {
      is: (isInLawsCoverage, policyType) =>
        policyType.toLowerCase().trim() === "basepolicy" &&
        isInLawsCoverage === true,
      then: () =>
        yup.number().min(1).max(2).required("Number Of In-laws is required"),
      otherwise: () => yup.number(),
    }),
    productDocument: yup.mixed().nullable(),
    premiumChart: yup
      .array()
      .of(
        yup.object().shape({
          id: yup.string(),
          sumInsured: yup.number().min(1).required("Sum insured is required"),
          selfOnlyPremium: yup
            .number(),
           // .min(0),
           // .required("Self premium is required"),
          selfSpousePremium: yup
            .number(),
            //.min(0),
            //.required("Self + Spouse premium is required"),
          spousePremium: yup.number().when("$isSpouseCoverage", {
            is: (val) => val === true,
            then: () =>
              yup.number().min(1).required("Spouse premium is required"),
            otherwise: () => yup.number(),
          }),
          child1Premium: yup
            .number()
            .when(["$isHandicappedChildrenCoverage", "$policyType"], {
              is: (isHandicappedChildrenCoverage, policyType) =>
                isHandicappedChildrenCoverage === true &&
                policyType.toLowerCase().trim() === "basepolicy",
              then: () =>
                yup.number().min(1).required("Child 1 premium is required."),
              otherwise: () => yup.number(),
            }),
          child2Premium: yup
            .number()
            .when(
              [
                "$isHandicappedChildrenCoverage",
                "$numberOfHandicappedChildren",
                "$policyType",
              ],
              {
                is: (
                  isHandicappedChildrenCoverage,
                  numberOfHandicappedChildren,
                  policyType
                ) =>
                  isHandicappedChildrenCoverage &&
                  numberOfHandicappedChildren === 2 &&
                  policyType.toLowerCase().trim() === "basepolicy",
                then: () =>
                  yup.number().min(1).required("Child 2 premium is required."),
                otherwise: () => yup.number(),
              }
            ),
          parent1Premium: yup
            .number()
            .when(["$isParentsCoverage", "$policyType"], {
              is: (isParentsCoverage, policyType) =>
                isParentsCoverage === true &&
                policyType.toLowerCase().trim() === "basepolicy",
              then: () =>
                yup.number().min(1).required("Parent 1 premium is required."),
              otherwise: () => yup.number(),
            }),
          parent2Premium: yup
            .number()
            .when(["$isParentsCoverage", "$numberOfParents", "$policyType"], {
              is: (isParentsCoverage, numberOfParents, policyType) =>
                isParentsCoverage &&
                numberOfParents === 2 &&
                policyType.toLowerCase().trim() === "basepolicy",
              then: () =>
                yup.number().min(1).required("Parent 2 premium is required."),
              otherwise: () => yup.number(),
            }),
          inLaw1Premium: yup
            .number()
            .when(["$isInLawsCoverage", "$policyType"], {
              is: (isInLawsCoverage, policyType) =>
                isInLawsCoverage === true &&
                policyType.toLowerCase().trim() === "basepolicy",
              then: () =>
                yup.number().min(1).required("In law 1 premium is required."),
              otherwise: () => yup.number(),
            }),
          inLaw2Premium: yup
            .number()
            .when(["$isInLawsCoverage", "$numberOfInLaws", "$policyType"], {
              is: (isInLawsCoverage, numberOfInLaws, policyType) =>
                isInLawsCoverage &&
                numberOfInLaws === 2 &&
                policyType.toLowerCase().trim() === "basepolicy",
              then: () =>
                yup.number().min(1).required("In law 2 premium is required."),
              otherwise: () => yup.number(),
            }),
        })
      )
      .min(1, "Minimum one policy option is required"),
  });
};

export default productValidation;
