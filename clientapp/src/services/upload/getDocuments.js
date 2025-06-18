import { handleApiError, httpClient, Result } from "@/utils";

const getDocuments = async () => {
  try {
    const response = await httpClient.get(`/upload/getdocumenttype`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getDocuments;
