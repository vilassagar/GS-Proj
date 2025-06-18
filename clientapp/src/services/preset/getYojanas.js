import { handleApiError, httpClient, Result } from "@/utils";

const getYojanas = async () => {
  try {
    const response = await httpClient.get(`/preset/getYojanas`);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getYojanas;
