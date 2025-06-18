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
