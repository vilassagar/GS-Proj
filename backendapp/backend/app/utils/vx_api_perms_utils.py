# File for setting permissions for routers
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
import contextvars
from typing import Dict, Tuple


class VxAPIPermsUtils:
    """
        This class will be used to set up the routers with the required permissions and some other necessary specs
    """

    # Setting up context vars for storing all the API router with its permissions needed for calling
    # Dict[Tuple[str, str], VxAPIPermsEnum] -> {(method, path): public/authenticated}
    _vx_perms_dict: contextvars.ContextVar[Dict[Tuple[str, str], VxAPIPermsEnum]] = contextvars.ContextVar(
        'vx_perms_list')

    # initial val an empty dict
    _vx_perms_dict.set({})

    @staticmethod
    def set_perm_for_route(method: str, path: str, perm: VxAPIPermsEnum):
        """"
            Saving the required permission/privileges for the routes
        """

        # Get the current permissions dictionary with all the updated routes
        current_perms = VxAPIPermsUtils._vx_perms_dict.get()

        # Add the new (method, path) and permission to the dictionary
        current_perms[(method, path)] = perm

        # Update the context variable with the new dictionary
        VxAPIPermsUtils._vx_perms_dict.set(current_perms)

    # -------------------- Methods for Setting Route Permissions -------------------- #

    @staticmethod
    def set_perm_get(path: str, perm: VxAPIPermsEnum):
        VxAPIPermsUtils.set_perm_for_route("GET", path, perm)

    @staticmethod
    def set_perm_post(path: str, perm: VxAPIPermsEnum):
        VxAPIPermsUtils.set_perm_for_route("POST", path, perm)

    @staticmethod
    def set_perm_put(path: str, perm: VxAPIPermsEnum):
        VxAPIPermsUtils.set_perm_for_route("PUT", path, perm)

    @staticmethod
    def set_perm_patch(path: str, perm: VxAPIPermsEnum):
        VxAPIPermsUtils.set_perm_for_route("PATCH", path, perm)

    @staticmethod
    def set_perm_delete(path: str, perm: VxAPIPermsEnum):
        VxAPIPermsUtils.set_perm_for_route("DELETE", path, perm)

    @staticmethod
    def get_all_routes_perms() -> Dict[(Tuple[str, str]), VxAPIPermsEnum]:
        return VxAPIPermsUtils._vx_perms_dict.get()

    # -------------------- Useful Functions -------------------- #

    @staticmethod
    def is_api_public(method: str, path: str) -> bool:
        """ Function to check whether the provided route with Path is public"""
        # print("RRoutes dictt: ")
        # from pprint import pprint
        # pprint(VxAPIPermsUtils._vx_perms_dict.__dict__)
        return VxAPIPermsUtils._vx_perms_dict.get().get((method, path)) == VxAPIPermsEnum.PUBLIC
