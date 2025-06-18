import { handleApiError, httpClient, Result } from "@/utils";

const getUsers = async (districtId) => {
  try {
    const response = await httpClient.get(
      `/user/getUsersByDistrictID?districtId=${districtId}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getUsers;
