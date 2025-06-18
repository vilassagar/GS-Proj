import { handleApiError, httpClient, Result } from "../../utils";

const updateDistrictAdmin = async (districtId, admin) => {
  try {
    const response = await httpClient.post(`/district/updateDistrictAdmin`, {
      districtId,
      admin,
    });
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default updateDistrictAdmin;
