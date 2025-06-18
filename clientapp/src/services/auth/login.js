import { handleApiError, httpClient, Result } from "../../utils";

const login = async (credentials) => {
  try {
    const response = await httpClient.post(`/auth/login`, credentials);
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default login;
