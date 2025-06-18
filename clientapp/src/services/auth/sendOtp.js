import { handleApiError, httpClient, Result } from "../../utils";

const sendOtp = async (mobileNumber) => {
  try {
    const response = await httpClient.post(`/auth/sendOtp`, { mobileNumber });
    const { data } = response;
    return Result.success(data);
  } catch (e) {
    return handleApiError(e);
  }
};

export default sendOtp;
