import { handleApiError, httpClient, Result } from "@/utils";

const getUserById = async (id) => {
  try {
    const response = await httpClient.get(
      `/profile/${id}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getUserById;
