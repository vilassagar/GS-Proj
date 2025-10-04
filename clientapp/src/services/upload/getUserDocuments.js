import { handleApiError, httpClient, Result } from "@/utils";

const getUserDocuments = async () => {
  try {
    const response = await httpClient.get(`/profile/documents`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getUserDocuments;
