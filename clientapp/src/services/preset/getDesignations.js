import { handleApiError, httpClient, Result } from "@/utils";

const getDesignations = async () => {
  try {
    const response = await httpClient.get(`/preset/getdesignations`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getDesignations;
