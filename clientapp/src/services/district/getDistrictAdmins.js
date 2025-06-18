import { handleApiError, httpClient, Result } from "@/utils";

const getDistrictAdmins = async () => {
  try {
    const response = await httpClient.get(`/district/getdistrictadmins`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getDistrictAdmins;
