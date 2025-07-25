import { handleApiError, httpClient, Result } from "@/utils";

export const getUserDocuments = async () => {
  try {
    const response = await httpClient.get("profile/me");
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};
