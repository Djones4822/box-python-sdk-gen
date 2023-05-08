from typing import Optional

from box_sdk.base_object import BaseObject

from typing import Union

import json

from box_sdk.schemas import CollaborationAllowlistExemptTargets

from box_sdk.schemas import ClientError

from box_sdk.schemas import CollaborationAllowlistExemptTarget

from box_sdk.developer_token_auth import DeveloperTokenAuth

from box_sdk.ccg_auth import CCGAuth

from box_sdk.jwt_auth import JWTAuth

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class GetCollaborationWhitelistExemptTargetsOptionsArg(BaseObject):
    def __init__(self, marker: Optional[str] = None, limit: Optional[int] = None, **kwargs):
        """
        :param marker: Defines the position marker at which to begin returning results. This is
            used when paginating using marker-based pagination.
            This requires `usemarker` to be set to `true`.
        :type marker: Optional[str], optional
        :param limit: The maximum number of items to return per page.
        :type limit: Optional[int], optional
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.limit = limit

class CreateCollaborationWhitelistExemptTargetRequestBodyArgUserField(BaseObject):
    def __init__(self, id: str, **kwargs):
        """
        :param id: The ID of the user to exempt.
        :type id: str
        """
        super().__init__(**kwargs)
        self.id = id

class CreateCollaborationWhitelistExemptTargetRequestBodyArg(BaseObject):
    def __init__(self, user: CreateCollaborationWhitelistExemptTargetRequestBodyArgUserField, **kwargs):
        """
        :param user: The user to exempt.
        :type user: CreateCollaborationWhitelistExemptTargetRequestBodyArgUserField
        """
        super().__init__(**kwargs)
        self.user = user

class CollaborationAllowlistExemptTargetsManager(BaseObject):
    def __init__(self, auth: Union[DeveloperTokenAuth, CCGAuth, JWTAuth], **kwargs):
        super().__init__(**kwargs)
        self.auth = auth
    def get_collaboration_whitelist_exempt_targets(self, options: GetCollaborationWhitelistExemptTargetsOptionsArg = None) -> CollaborationAllowlistExemptTargets:
        """
        Returns a list of users who have been exempt from the collaboration
        
        domain restrictions.

        """
        if options is None:
            options = GetCollaborationWhitelistExemptTargetsOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/collaboration_whitelist_exempt_targets']), FetchOptions(method='GET', params={'marker': options.marker, 'limit': options.limit}, auth=self.auth))
        return CollaborationAllowlistExemptTargets.from_dict(json.loads(response.text))
    def create_collaboration_whitelist_exempt_target(self, request_body: CreateCollaborationWhitelistExemptTargetRequestBodyArg) -> CollaborationAllowlistExemptTarget:
        """
        Exempts a user from the restrictions set out by the allowed list of domains
        
        for collaborations.

        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/collaboration_whitelist_exempt_targets']), FetchOptions(method='POST', body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth))
        return CollaborationAllowlistExemptTarget.from_dict(json.loads(response.text))
    def get_collaboration_whitelist_exempt_target_by_id(self, collaboration_whitelist_exempt_target_id: str) -> CollaborationAllowlistExemptTarget:
        """
        Returns a users who has been exempt from the collaboration
        
        domain restrictions.

        :param collaboration_whitelist_exempt_target_id: The ID of the exemption to the list.
            Example: "984923"
        :type collaboration_whitelist_exempt_target_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/collaboration_whitelist_exempt_targets/', collaboration_whitelist_exempt_target_id]), FetchOptions(method='GET', auth=self.auth))
        return CollaborationAllowlistExemptTarget.from_dict(json.loads(response.text))
    def delete_collaboration_whitelist_exempt_target_by_id(self, collaboration_whitelist_exempt_target_id: str):
        """
        Removes a user's exemption from the restrictions set out by the allowed list
        
        of domains for collaborations.

        :param collaboration_whitelist_exempt_target_id: The ID of the exemption to the list.
            Example: "984923"
        :type collaboration_whitelist_exempt_target_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/collaboration_whitelist_exempt_targets/', collaboration_whitelist_exempt_target_id]), FetchOptions(method='DELETE', auth=self.auth))
        return response.content