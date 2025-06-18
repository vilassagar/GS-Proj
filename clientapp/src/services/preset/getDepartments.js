import { handleApiError, httpClient, Result } from "@/utils";

const getDepartments = async () => {
  try {
    const response = await httpClient.get(`/preset/getDepartments`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getDepartments;
