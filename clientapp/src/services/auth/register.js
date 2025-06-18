import { handleApiError, httpClient, Result } from "../../utils";

const register = async (credentials) => {
  try {
    const response = await httpClient.post(`/auth/register`, credentials);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default register;
