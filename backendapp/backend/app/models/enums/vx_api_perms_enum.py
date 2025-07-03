# Enum for different permission for routers
import enum


class VxAPIPermsEnum(enum.Enum):
    """ Enums used for setting permissions for different routes """
    PUBLIC = 'PUBLIC'
    AUTHENTICATED = 'AUTHENTICATED'
    # tobe added later
    # ADMIN_READ = "ADMIN_READ"
