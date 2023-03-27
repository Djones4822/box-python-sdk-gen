from typing import Union

from box_sdk.base_object import BaseObject

import json

from box_sdk.schemas import FileRequest

from box_sdk.schemas import ClientError

from box_sdk.schemas import FileRequestUpdateRequest

from box_sdk.schemas import FileRequestCopyRequest

from box_sdk.developer_token_auth import DeveloperTokenAuth

from box_sdk.ccg_auth import CCGAuth

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class PutFileRequestsIdOptionsArg(BaseObject):
    def __init__(self, if_match: Union[None, str] = None, **kwargs):
        """
        :param if_match: Ensures this item hasn't recently changed before
            making changes.
            Pass in the item's last observed `etag` value
            into this header and the endpoint will fail
            with a `412 Precondition Failed` if it
            has changed since.
        :type if_match: Union[None, str], optional
        """
        super().__init__(**kwargs)
        self.if_match = if_match

class FileRequestsManager(BaseObject):
    def __init__(self, auth: Union[DeveloperTokenAuth, CCGAuth], **kwargs):
        super().__init__(**kwargs)
        self.auth = auth
    def get_file_requests_id(self, file_request_id: str) -> FileRequest:
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
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='GET', auth=self.auth))
        return FileRequest.from_dict(json.loads(response.text))
    def put_file_requests_id(self, file_request_id: str, request_body: FileRequestUpdateRequest, options: PutFileRequestsIdOptionsArg = None) -> FileRequest:
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
        """
        if options is None:
            options = PutFileRequestsIdOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='PUT', headers={'if-match': options.if_match}, body=json.dumps(request_body.to_dict()), auth=self.auth))
        return FileRequest.from_dict(json.loads(response.text))
    def delete_file_requests_id(self, file_request_id: str):
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
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id]), FetchOptions(method='DELETE', auth=self.auth))
        return response.content
    def post_file_requests_id_copy(self, file_request_id: str, request_body: FileRequestCopyRequest) -> FileRequest:
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
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/file_requests/', file_request_id, '/copy']), FetchOptions(method='POST', body=json.dumps(request_body.to_dict()), auth=self.auth))
        return FileRequest.from_dict(json.loads(response.text))