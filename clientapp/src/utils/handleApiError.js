import Result from "./result";

export default function handleApiError(e) {
  if (e.response) {
    switch (e.response.status) {
      case 401:
        // unAuthorized
        return Result.unauthorized([
          e.response?.data?.message || "You are unauthorized!",
        ]);
      case 403:
        // Forbidden
        return Result.forbidden([
          "You don’t have permission to access this service.",
        ]);
      case 400:
        // Bad_request
        return Result.invalid(e.response.data.errors, ["Invalid Request."]);
      case 404:
        return Result.notFound([
          e?.response?.data?.message || "Page not found!",
        ]);
      case 409:
        return Result.conflict(e.response.data);
      case 500:
        // Internal_Server_Error
        return Result.internalServerError(["Internal Server Error."]);
      default:
        return Result.error([e.message]);
    }
  } else if (e.request) {
    return Result.noResponse(["Unable to connect to the server"]);
  } else {
    return Result.error([
      "Unable to make a request, please check your connection.",
    ]);
  }
}
