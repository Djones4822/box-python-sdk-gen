from enum import Enum

from typing import Optional

from box_sdk.base_object import BaseObject

import json

from typing import Dict

from box_sdk.base_object import BaseObject

from box_sdk.schemas import FileRequest

from box_sdk.schemas import ClientError

from box_sdk.schemas import FileRequestUpdateRequest

from box_sdk.schemas import FileRequestCopyRequest

from box_sdk.auth import Authentication

from box_sdk.network import NetworkSession

from box_sdk.utils import prepare_params

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class UpdateFileRequestByIdStatusArg(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class CreateFileRequestCopyFolderArgTypeField(str, Enum):
    FOLDER = 'folder'

class CreateFileRequestCopyFolderArg(BaseObject):
    def __init__(self, id: str, type: Optional[CreateFileRequestCopyFolderArgTypeField] = None, **kwargs):
        """
        :param id: The ID of the folder to associate the new
            file request to.
        :type id: str
        :param type: `folder`
        :type type: Optional[CreateFileRequestCopyFolderArgTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type

class CreateFileRequestCopyStatusArg(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class FileRequestsManager:
    def __init__(self, auth: Optional[Authentication] = None, network_session: Optional[NetworkSession] = None):
        self.auth = auth
        self.network_session = network_session
    def get_file_request_by_id(self, file_request_id: str) -> FileRequest:
        """
        Retrieves the information about a file request.
        :param file_request_id: The unique identifier that represent a file request.
            The ID for any file request can be determined
            by visiting a file request builder in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/filerequest/123`
            the `file_request_id` is `123`.
            Example: "123"
        :type file_request_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='GET', auth=self.auth, network_session=self.network_session))
        return FileRequest.from_dict(json.loads(response.text))
    def update_file_request_by_id(self, file_request_id: str, title: Optional[str] = None, description: Optional[str] = None, status: Optional[UpdateFileRequestByIdStatusArg] = None, is_email_required: Optional[bool] = None, is_description_required: Optional[bool] = None, expires_at: Optional[str] = None, if_match: Optional[str] = None) -> FileRequest:
        """
        Updates a file request. This can be used to activate or
        
        deactivate a file request.

        :param file_request_id: The unique identifier that represent a file request.
            The ID for any file request can be determined
            by visiting a file request builder in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/filerequest/123`
            the `file_request_id` is `123`.
            Example: "123"
        :type file_request_id: str
        :param title: An optional new title for the file request. This can be
            used to change the title of the file request.
            This will default to the value on the existing file request.
        :type title: Optional[str], optional
        :param description: An optional new description for the file request. This can be
            used to change the description of the file request.
            This will default to the value on the existing file request.
        :type description: Optional[str], optional
        :param status: An optional new status of the file request.
            When the status is set to `inactive`, the file request
            will no longer accept new submissions, and any visitor
            to the file request URL will receive a `HTTP 404` status
            code.
            This will default to the value on the existing file request.
        :type status: Optional[UpdateFileRequestByIdStatusArg], optional
        :param is_email_required: Whether a file request submitter is required to provide
            their email address.
            When this setting is set to true, the Box UI will show
            an email field on the file request form.
            This will default to the value on the existing file request.
        :type is_email_required: Optional[bool], optional
        :param is_description_required: Whether a file request submitter is required to provide
            a description of the files they are submitting.
            When this setting is set to true, the Box UI will show
            a description field on the file request form.
            This will default to the value on the existing file request.
        :type is_description_required: Optional[bool], optional
        :param expires_at: The date after which a file request will no longer accept new
            submissions.
            After this date, the `status` will automatically be set to
            `inactive`.
            This will default to the value on the existing file request.
        :type expires_at: Optional[str], optional
        :param if_match: Ensures this item hasn't recently changed before
            making changes.
            Pass in the item's last observed `etag` value
            into this header and the endpoint will fail
            with a `412 Precondition Failed` if it
            has changed since.
        :type if_match: Optional[str], optional
        """
        request_body: BaseObject = BaseObject(title=title, description=description, status=status, is_email_required=is_email_required, is_description_required=is_description_required, expires_at=expires_at)
        headers: Dict = {'if_match': if_match}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='PUT', headers=prepare_params(headers), body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return FileRequest.from_dict(json.loads(response.text))
    def delete_file_request_by_id(self, file_request_id: str):
        """
        Deletes a file request permanently.
        :param file_request_id: The unique identifier that represent a file request.
            The ID for any file request can be determined
            by visiting a file request builder in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/filerequest/123`
            the `file_request_id` is `123`.
            Example: "123"
        :type file_request_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='DELETE', auth=self.auth, network_session=self.network_session))
        return response.content
    def create_file_request_copy(self, file_request_id: str, folder: CreateFileRequestCopyFolderArg, title: Optional[str] = None, description: Optional[str] = None, status: Optional[CreateFileRequestCopyStatusArg] = None, is_email_required: Optional[bool] = None, is_description_required: Optional[bool] = None, expires_at: Optional[str] = None) -> FileRequest:
        """
        Copies an existing file request that is already present on one folder,
        
        and applies it to another folder.

        :param file_request_id: The unique identifier that represent a file request.
            The ID for any file request can be determined
            by visiting a file request builder in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/filerequest/123`
            the `file_request_id` is `123`.
            Example: "123"
        :type file_request_id: str
        :param folder: The folder to associate the new file request to.
        :type folder: CreateFileRequestCopyFolderArg
        :param title: An optional new title for the file request. This can be
            used to change the title of the file request.
            This will default to the value on the existing file request.
        :type title: Optional[str], optional
        :param description: An optional new description for the file request. This can be
            used to change the description of the file request.
            This will default to the value on the existing file request.
        :type description: Optional[str], optional
        :param status: An optional new status of the file request.
            When the status is set to `inactive`, the file request
            will no longer accept new submissions, and any visitor
            to the file request URL will receive a `HTTP 404` status
            code.
            This will default to the value on the existing file request.
        :type status: Optional[CreateFileRequestCopyStatusArg], optional
        :param is_email_required: Whether a file request submitter is required to provide
            their email address.
            When this setting is set to true, the Box UI will show
            an email field on the file request form.
            This will default to the value on the existing file request.
        :type is_email_required: Optional[bool], optional
        :param is_description_required: Whether a file request submitter is required to provide
            a description of the files they are submitting.
            When this setting is set to true, the Box UI will show
            a description field on the file request form.
            This will default to the value on the existing file request.
        :type is_description_required: Optional[bool], optional
        :param expires_at: The date after which a file request will no longer accept new
            submissions.
            After this date, the `status` will automatically be set to
            `inactive`.
            This will default to the value on the existing file request.
        :type expires_at: Optional[str], optional
        """
        request_body: BaseObject = BaseObject(folder=folder, title=title, description=description, status=status, is_email_required=is_email_required, is_description_required=is_description_required, expires_at=expires_at)
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id, '/copy']), FetchOptions(method='POST', body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return FileRequest.from_dict(json.loads(response.text))