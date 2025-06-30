import { handleApiError, httpClient, Result } from "@/utils";

const getGramSevakById = async () => {
  try {
    const response = await httpClient.get(
      `/v1/profile/me`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getGramSevakById;
