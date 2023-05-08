from typing import Optional

from box_sdk.base_object import BaseObject

from typing import Union

import json

from box_sdk.schemas import TrashFileRestored

from box_sdk.schemas import ClientError

from box_sdk.schemas import TrashFile

from box_sdk.developer_token_auth import DeveloperTokenAuth

from box_sdk.ccg_auth import CCGAuth

from box_sdk.jwt_auth import JWTAuth

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class RestoreFileFromTrashRequestBodyArgParentField(BaseObject):
    def __init__(self, id: Optional[str] = None, **kwargs):
        """
        :param id: The ID of parent item
        :type id: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id

class RestoreFileFromTrashRequestBodyArg(BaseObject):
    def __init__(self, name: Optional[str] = None, parent: Optional[RestoreFileFromTrashRequestBodyArgParentField] = None, **kwargs):
        """
        :param name: An optional new name for the file.
        :type name: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.name = name
        self.parent = parent

class RestoreFileFromTrashOptionsArg(BaseObject):
    def __init__(self, fields: Optional[str] = None, **kwargs):
        """
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
        super().__init__(**kwargs)
        self.fields = fields

class GetFileTrashOptionsArg(BaseObject):
    def __init__(self, fields: Optional[str] = None, **kwargs):
        """
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
        super().__init__(**kwargs)
        self.fields = fields

class TrashedFilesManager(BaseObject):
    def __init__(self, auth: Union[DeveloperTokenAuth, CCGAuth, JWTAuth], **kwargs):
        super().__init__(**kwargs)
        self.auth = auth
    def restore_file_from_trash(self, file_id: str, request_body: RestoreFileFromTrashRequestBodyArg, options: RestoreFileFromTrashOptionsArg = None) -> TrashFileRestored:
        """
        Restores a file that has been moved to the trash.
        
        An optional new parent ID can be provided to restore the file to in case the

        
        original folder has been deleted.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        """
        if options is None:
            options = RestoreFileFromTrashOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id]), FetchOptions(method='POST', params={'fields': options.fields}, body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth))
        return TrashFileRestored.from_dict(json.loads(response.text))
    def get_file_trash(self, file_id: str, options: GetFileTrashOptionsArg = None) -> TrashFile:
        """
        Retrieves a file that has been moved to the trash.
        
        Please note that only if the file itself has been moved to the

        
        trash can it be retrieved with this API call. If instead one of

        
        its parent folders was moved to the trash, only that folder

        
        can be inspected using the

        
        [`GET /folders/:id/trash`](e://get_folders_id_trash) API.

        
        To list all items that have been moved to the trash, please

        
        use the [`GET /folders/trash/items`](e://get-folders-trash-items/)

        
        API.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        """
        if options is None:
            options = GetFileTrashOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/trash']), FetchOptions(method='GET', params={'fields': options.fields}, auth=self.auth))
        return TrashFile.from_dict(json.loads(response.text))
    def delete_file_trash(self, file_id: str):
        """
        Permanently deletes a file that is in the trash.
        
        This action cannot be undone.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/trash']), FetchOptions(method='DELETE', auth=self.auth))
        return response.content