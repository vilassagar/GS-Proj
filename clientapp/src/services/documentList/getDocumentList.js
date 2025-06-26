import { handleApiError, httpClient, Result } from "@/utils";

export const getDocumentList = async () => {
  try {
    const res = await httpClient.get(`gramsevak/books`);
    const { data } = res;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};
// export  getDocumentList;
