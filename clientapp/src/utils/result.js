export default class Result {
  constructor(status, data, errors, validationErrors) {
    return {
      status: status,
      data: data,
      errors: errors,
      validationErrors: validationErrors,
    };
  }
  static success(data) {
    return new Result("success", data, undefined, undefined);
  }

  static NoContent(data) {
    return new Result("noContent", data, undefined, undefined);
  }

  static error(errors) {
    return new Result("error", undefined, errors, undefined);
  }

  static invalid(validationErrors, errors) {
    return new Result("invalid", undefined, errors, validationErrors);
  }

  static notFound(errors) {
    return new Result("notFound", undefined, errors, undefined);
  }

  static internalServerError(errors) {
    return new Result("serverError", undefined, errors, undefined);
  }

  static unauthorized(errors) {
    return new Result("unauthorized", undefined, errors, undefined);
  }

  static noResponse(errors) {
    return new Result("noResponse", undefined, errors, undefined);
  }

  static forbidden(errors) {
    return new Result("forbidden", undefined, errors, undefined);
  }

  static conflict(errors) {
    return new Result("conflict", undefined, errors, undefined);
  }
}
