import { handleApiError, httpClient, Result } from "@/utils";

const getUsers = async (blockId) => {
  try {
    const response = await httpClient.get(
      `/user/getUsersByBlockID?blockId=${blockId}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getUsers;
