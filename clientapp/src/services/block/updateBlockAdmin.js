import { handleApiError, httpClient, Result } from "../../utils";

const updateBlockAdmin = async (blockId, admin) => {
  try {
    const response = await httpClient.post(`/block/updateBlockAdmin`, {
      blockId,
      admin,
    });
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default updateBlockAdmin;
