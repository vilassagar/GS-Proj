import { handleApiError, httpClient, Result } from "@/utils";

const getGramSevakById = async (id) => {
  try {
    const response = await httpClient.get(
      `/gramsevak/getGramsevakById?id=${id}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getGramSevakById;
