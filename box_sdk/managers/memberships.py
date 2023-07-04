from box_sdk.base_object import BaseObject

from enum import Enum

from typing import Optional

from typing import Dict

import json

from box_sdk.base_object import BaseObject

from box_sdk.schemas import GroupMemberships

from box_sdk.schemas import ClientError

from box_sdk.schemas import GroupMembership

from box_sdk.auth import Authentication

from box_sdk.network import NetworkSession

from box_sdk.utils import to_map

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class CreateGroupMembershipUserArg(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of the user to add to the group
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id

class CreateGroupMembershipGroupArg(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of the group to add the user to
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id

class CreateGroupMembershipRoleArg(str, Enum):
    MEMBER = 'member'
    ADMIN = 'admin'

class CreateGroupMembershipConfigurablePermissionsArg(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class UpdateGroupMembershipByIdRoleArg(str, Enum):
    MEMBER = 'member'
    ADMIN = 'admin'

class UpdateGroupMembershipByIdConfigurablePermissionsArg(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MembershipsManager:
    def __init__(self, auth: Optional[Authentication] = None, network_session: Optional[NetworkSession] = None):
        self.auth = auth
        self.network_session = network_session
    def get_user_memberships(self, user_id: str, limit: Optional[int] = None, offset: Optional[int] = None) -> GroupMemberships:
        """
        Retrieves all the groups for a user. Only members of this
        
        group or users with admin-level permissions will be able to

        
        use this API.

        :param user_id: The ID of the user.
            Example: "12345"
        :type user_id: str
        :param limit: The maximum number of items to return per page.
        :type limit: Optional[int], optional
        :param offset: The offset of the item at which to begin the response.
            Queries with offset parameter value
            exceeding 10000 will be rejected
            with a 400 response.
        :type offset: Optional[int], optional
        """
        query_params: Dict = {'limit': limit, 'offset': offset}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/users/', user_id, '/memberships']), FetchOptions(method='GET', params=to_map(query_params), auth=self.auth, network_session=self.network_session))
        return GroupMemberships.from_dict(json.loads(response.text))
    def get_group_memberships(self, group_id: str, limit: Optional[int] = None, offset: Optional[int] = None) -> GroupMemberships:
        """
        Retrieves all the members for a group. Only members of this
        
        group or users with admin-level permissions will be able to

        
        use this API.

        :param group_id: The ID of the group.
            Example: "57645"
        :type group_id: str
        :param limit: The maximum number of items to return per page.
        :type limit: Optional[int], optional
        :param offset: The offset of the item at which to begin the response.
            Queries with offset parameter value
            exceeding 10000 will be rejected
            with a 400 response.
        :type offset: Optional[int], optional
        """
        query_params: Dict = {'limit': limit, 'offset': offset}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/groups/', group_id, '/memberships']), FetchOptions(method='GET', params=to_map(query_params), auth=self.auth, network_session=self.network_session))
        return GroupMemberships.from_dict(json.loads(response.text))
    def create_group_membership(self, user: CreateGroupMembershipUserArg, group: CreateGroupMembershipGroupArg, role: Optional[CreateGroupMembershipRoleArg] = None, configurable_permissions: Optional[CreateGroupMembershipConfigurablePermissionsArg] = None, fields: Optional[str] = None) -> GroupMembership:
        """
        Creates a group membership. Only users with
        
        admin-level permissions will be able to use this API.

        :param user: The user to add to the group.
        :type user: CreateGroupMembershipUserArg
        :param group: The group to add the user to.
        :type group: CreateGroupMembershipGroupArg
        :param role: The role of the user in the group.
        :type role: Optional[CreateGroupMembershipRoleArg], optional
        :param configurable_permissions: Custom configuration for the permissions an admin
            if a group will receive. This option has no effect
            on members with a role of `member`.
            Setting these permissions overwrites the default
            access levels of an admin.
            Specifying a value of "null" for this object will disable
            all configurable permissions. Specifying permissions will set
            them accordingly, omitted permissions will be enabled by default.
        :type configurable_permissions: Optional[CreateGroupMembershipConfigurablePermissionsArg], optional
        :param fields: A comma-separated list of attributes to include in the
            response. This can be used to request fields that are
            not normally returned in a standard response.
            Be aware that specifying this parameter will have the
            effect that none of the standard fields are returned in
            the response unless explicitly specified, instead only
            fields for the mini representation are returned, additional
            to the fields requested.
        :type fields: Optional[str], optional
        """
        request_body: BaseObject = BaseObject(user=user, group=group, role=role, configurable_permissions=configurable_permissions)
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/group_memberships']), FetchOptions(method='POST', params=to_map(query_params), body=json.dumps(to_map(request_body)), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return GroupMembership.from_dict(json.loads(response.text))
    def get_group_membership_by_id(self, group_membership_id: str, fields: Optional[str] = None) -> GroupMembership:
        """
        Retrieves a specific group membership. Only admins of this
        
        group or users with admin-level permissions will be able to

        
        use this API.

        :param group_membership_id: The ID of the group membership.
            Example: "434534"
        :type group_membership_id: str
        :param fields: A comma-separated list of attributes to include in the
            response. This can be used to request fields that are
            not normally returned in a standard response.
            Be aware that specifying this parameter will have the
            effect that none of the standard fields are returned in
            the response unless explicitly specified, instead only
            fields for the mini representation are returned, additional
            to the fields requested.
        :type fields: Optional[str], optional
        """
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/group_memberships/', group_membership_id]), FetchOptions(method='GET', params=to_map(query_params), auth=self.auth, network_session=self.network_session))
        return GroupMembership.from_dict(json.loads(response.text))
    def update_group_membership_by_id(self, group_membership_id: str, role: Optional[UpdateGroupMembershipByIdRoleArg] = None, configurable_permissions: Optional[UpdateGroupMembershipByIdConfigurablePermissionsArg] = None, fields: Optional[str] = None) -> GroupMembership:
        """
        Updates a user's group membership. Only admins of this
        
        group or users with admin-level permissions will be able to

        
        use this API.

        :param group_membership_id: The ID of the group membership.
            Example: "434534"
        :type group_membership_id: str
        :param role: The role of the user in the group.
        :type role: Optional[UpdateGroupMembershipByIdRoleArg], optional
        :param configurable_permissions: Custom configuration for the permissions an admin
            if a group will receive. This option has no effect
            on members with a role of `member`.
            Setting these permissions overwrites the default
            access levels of an admin.
            Specifying a value of "null" for this object will disable
            all configurable permissions. Specifying permissions will set
            them accordingly, omitted permissions will be enabled by default.
        :type configurable_permissions: Optional[UpdateGroupMembershipByIdConfigurablePermissionsArg], optional
        :param fields: A comma-separated list of attributes to include in the
            response. This can be used to request fields that are
            not normally returned in a standard response.
            Be aware that specifying this parameter will have the
            effect that none of the standard fields are returned in
            the response unless explicitly specified, instead only
            fields for the mini representation are returned, additional
            to the fields requested.
        :type fields: Optional[str], optional
        """
        request_body: BaseObject = BaseObject(role=role, configurable_permissions=configurable_permissions)
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/group_memberships/', group_membership_id]), FetchOptions(method='PUT', params=to_map(query_params), body=json.dumps(to_map(request_body)), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return GroupMembership.from_dict(json.loads(response.text))
    def delete_group_membership_by_id(self, group_membership_id: str):
        """
        Deletes a specific group membership. Only admins of this
        
        group or users with admin-level permissions will be able to

        
        use this API.

        :param group_membership_id: The ID of the group membership.
            Example: "434534"
        :type group_membership_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/group_memberships/', group_membership_id]), FetchOptions(method='DELETE', auth=self.auth, network_session=self.network_session))
        return response.content