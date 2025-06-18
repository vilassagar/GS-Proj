import { handleApiError, httpClient, Result } from "@/utils";

const getBlockAdmins = async (districtId) => {
  try {
    const response = await httpClient.get(
      `/block/getBlockAdmins?districtId=${districtId}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getBlockAdmins;
