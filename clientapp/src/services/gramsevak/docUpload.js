import { handleApiError, httpClient, Result } from "../../utils";

const docUpload = async (payload) => {
  try {
    const response = await httpClient.post(`/gramsevak/docUpload`, payload);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default docUpload;
