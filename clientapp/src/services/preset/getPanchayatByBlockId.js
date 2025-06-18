import { handleApiError, httpClient, Result } from "@/utils";

const getPanchayatByBlockId = async (blockId) => {
  try {
    const response = await httpClient.get(
      `/preset/getGramPanchayatsByBlockId?blockId=${blockId}`
    );
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default getPanchayatByBlockId;
