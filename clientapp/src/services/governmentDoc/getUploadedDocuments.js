import { handleApiError, httpClient, Result } from "@/utils";

const getUploadedDocuments = async (filter, search) => {
  try {
    const response = await httpClient.get(
      `/GovernmentDoc/getDocs?type=${filter}&search=${search}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getUploadedDocuments;
