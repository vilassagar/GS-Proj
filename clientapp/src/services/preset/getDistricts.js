import { handleApiError, httpClient, Result } from "@/utils";

const getDistricts = async () => {
  try {
    const response = await httpClient.get(`/preset/getDistricts`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getDistricts;
