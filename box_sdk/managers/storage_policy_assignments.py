from enum import Enum

from box_sdk.base_object import BaseObject

from typing import Optional

from typing import Dict

import json

from box_sdk.base_object import BaseObject

from box_sdk.schemas import StoragePolicyAssignments

from box_sdk.schemas import ClientError

from box_sdk.schemas import StoragePolicyAssignment

from box_sdk.auth import Authentication

from box_sdk.network import NetworkSession

from box_sdk.utils import prepare_params

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class GetStoragePolicyAssignmentsResolvedForTypeArg(str, Enum):
    USER = 'user'
    ENTERPRISE = 'enterprise'

class CreateStoragePolicyAssignmentStoragePolicyArgTypeField(str, Enum):
    STORAGE_POLICY = 'storage_policy'

class CreateStoragePolicyAssignmentStoragePolicyArg(BaseObject):
    def __init__(self, type: CreateStoragePolicyAssignmentStoragePolicyArgTypeField, id: str, **kwargs):
        """
        :param type: The type to assign.
        :type type: CreateStoragePolicyAssignmentStoragePolicyArgTypeField
        :param id: The ID of the storage policy to assign.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id

class CreateStoragePolicyAssignmentAssignedToArgTypeField(str, Enum):
    USER = 'user'
    ENTERPRISE = 'enterprise'

class CreateStoragePolicyAssignmentAssignedToArg(BaseObject):
    def __init__(self, type: CreateStoragePolicyAssignmentAssignedToArgTypeField, id: str, **kwargs):
        """
        :param type: The type to assign the policy to.
        :type type: CreateStoragePolicyAssignmentAssignedToArgTypeField
        :param id: The ID of the user or enterprise
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id

class UpdateStoragePolicyAssignmentByIdStoragePolicyArgTypeField(str, Enum):
    STORAGE_POLICY = 'storage_policy'

class UpdateStoragePolicyAssignmentByIdStoragePolicyArg(BaseObject):
    def __init__(self, type: UpdateStoragePolicyAssignmentByIdStoragePolicyArgTypeField, id: str, **kwargs):
        """
        :param type: The type to assign.
        :type type: UpdateStoragePolicyAssignmentByIdStoragePolicyArgTypeField
        :param id: The ID of the storage policy to assign.
        :type id: str
        """
        super().__init__(**kwargs)
        self.type = type
        self.id = id

class StoragePolicyAssignmentsManager:
    def __init__(self, auth: Optional[Authentication] = None, network_session: Optional[NetworkSession] = None):
        self.auth = auth
        self.network_session = network_session
    def get_storage_policy_assignments(self, resolved_for_type: GetStoragePolicyAssignmentsResolvedForTypeArg, resolved_for_id: str, marker: Optional[str] = None) -> StoragePolicyAssignments:
        """
        Fetches all the storage policy assignment for an enterprise or user.
        :param resolved_for_type: The target type to return assignments for
        :type resolved_for_type: GetStoragePolicyAssignmentsResolvedForTypeArg
        :param resolved_for_id: The ID of the user or enterprise to return assignments for
        :type resolved_for_id: str
        :param marker: Defines the position marker at which to begin returning results. This is
            used when paginating using marker-based pagination.
            This requires `usemarker` to be set to `true`.
        :type marker: Optional[str], optional
        """
        query_params: Dict = {'marker': marker, 'resolved_for_type': resolved_for_type, 'resolved_for_id': resolved_for_id}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/storage_policy_assignments']), FetchOptions(method='GET', params=prepare_params(query_params), auth=self.auth, network_session=self.network_session))
        return StoragePolicyAssignments.from_dict(json.loads(response.text))
    def create_storage_policy_assignment(self, storage_policy: CreateStoragePolicyAssignmentStoragePolicyArg, assigned_to: CreateStoragePolicyAssignmentAssignedToArg) -> StoragePolicyAssignment:
        """
        Creates a storage policy assignment for an enterprise or user.
        :param storage_policy: The storage policy to assign to the user or
            enterprise
        :type storage_policy: CreateStoragePolicyAssignmentStoragePolicyArg
        :param assigned_to: The user or enterprise to assign the storage
            policy to.
        :type assigned_to: CreateStoragePolicyAssignmentAssignedToArg
        """
        request_body: BaseObject = BaseObject(storage_policy=storage_policy, assigned_to=assigned_to)
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/storage_policy_assignments']), FetchOptions(method='POST', body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return StoragePolicyAssignment.from_dict(json.loads(response.text))
    def get_storage_policy_assignment_by_id(self, storage_policy_assignment_id: str) -> StoragePolicyAssignment:
        """
        Fetches a specific storage policy assignment.
        :param storage_policy_assignment_id: The ID of the storage policy assignment.
            Example: "932483"
        :type storage_policy_assignment_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/storage_policy_assignments/', storage_policy_assignment_id]), FetchOptions(method='GET', auth=self.auth, network_session=self.network_session))
        return StoragePolicyAssignment.from_dict(json.loads(response.text))
    def update_storage_policy_assignment_by_id(self, storage_policy_assignment_id: str, storage_policy: UpdateStoragePolicyAssignmentByIdStoragePolicyArg) -> StoragePolicyAssignment:
        """
        Updates a specific storage policy assignment.
        :param storage_policy_assignment_id: The ID of the storage policy assignment.
            Example: "932483"
        :type storage_policy_assignment_id: str
        :param storage_policy: The storage policy to assign to the user or
            enterprise
        :type storage_policy: UpdateStoragePolicyAssignmentByIdStoragePolicyArg
        """
        request_body: BaseObject = BaseObject(storage_policy=storage_policy)
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/storage_policy_assignments/', storage_policy_assignment_id]), FetchOptions(method='PUT', body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return StoragePolicyAssignment.from_dict(json.loads(response.text))
    def delete_storage_policy_assignment_by_id(self, storage_policy_assignment_id: str):
        """
        Delete a storage policy assignment.
        
        Deleting a storage policy assignment on a user

        
        will have the user inherit the enterprise's default

        
        storage policy.

        
        There is a rate limit for calling this endpoint of only

        
        twice per user in a 24 hour time frame.

        :param storage_policy_assignment_id: The ID of the storage policy assignment.
            Example: "932483"
        :type storage_policy_assignment_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/storage_policy_assignments/', storage_policy_assignment_id]), FetchOptions(method='DELETE', auth=self.auth, network_session=self.network_session))
        return response.content