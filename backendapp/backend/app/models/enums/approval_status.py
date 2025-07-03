from enum import Enum


class ApprovalStatus(Enum):
    """
        These statuses enums we can use for USER Approval status
        And DOCUMENT status
    """
    APPROVED = 'APPROVED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'


class ApprovalStatusRequest(Enum):
    APPROVED = 'APPROVED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    ALL = 'ALL'
    
    """
        These statuses enums we can use for USER Approval status
        And DOCUMENT status
        This is used in request to filter the data
    """
class ApprovalStatusResponse(Enum):
    APPROVED = 'APPROVED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    ALL = 'ALL'

    @classmethod
    def from_request(cls, request_status: ApprovalStatusRequest):
        if request_status == ApprovalStatusRequest.ALL:
            return [cls.APPROVED, cls.PENDING, cls.REJECTED]
        return [getattr(cls, request_status.name)]