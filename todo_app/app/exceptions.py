from fastapi import HTTPException, status


# Base exception — all our custom exceptions inherit from this
class TodoException(HTTPException):
    def __init__(self, status_code: int, message: str, error_type: str):
        self.status_code = status_code
        self.detail = {
            "success": False,
            "status_code": status_code,
            "message": message,
            "error_type": error_type
        }
        super().__init__(status_code=status_code, detail=self.detail)


# When something is NOT FOUND
class NotFoundException(TodoException):
    def __init__(self, item: str = "Item", item_id: int = None):
        message = f"{item} not found"
        if item_id is not None:
            message = f"{item} with id {item_id} not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_type="not_found"
        )


# When trying to create DUPLICATE
class DuplicateException(TodoException):
    def __init__(self, item: str = "Item"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"{item} already exists",
            error_type="duplicate"
        )


# When client sends BAD data
class BadRequestException(TodoException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_type="bad_request"
        )


# When something goes wrong on SERVER
class ServerException(TodoException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_type="server_error"
        )