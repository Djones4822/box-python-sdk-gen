from enum import Enum

from typing import Optional

from typing import Dict

import json

from box_sdk.base_object import BaseObject

from box_sdk.schemas import FileVersions

from box_sdk.schemas import ClientError

from box_sdk.schemas import FileVersionFull

from box_sdk.auth import Authentication

from box_sdk.network import NetworkSession

from box_sdk.utils import prepare_params

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class PromoteFileVersionTypeArg(str, Enum):
    FILE_VERSION = 'file_version'

class FileVersionsManager:
    def __init__(self, auth: Optional[Authentication] = None, network_session: Optional[NetworkSession] = None):
        self.auth = auth
        self.network_session = network_session
    def get_file_versions(self, file_id: str, fields: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> FileVersions:
        """
        Retrieve a list of the past versions for a file.
        
        Versions are only tracked by Box users with premium accounts. To fetch the ID

        
        of the current version of a file, use the `GET /file/:id` API.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        :param fields: A comma-separated list of attributes to include in the
            response. This can be used to request fields that are
            not normally returned in a standard response.
            Be aware that specifying this parameter will have the
            effect that none of the standard fields are returned in
            the response unless explicitly specified, instead only
            fields for the mini representation are returned, additional
            to the fields requested.
        :type fields: Optional[str], optional
        :param limit: The maximum number of items to return per page.
        :type limit: Optional[int], optional
        :param offset: The offset of the item at which to begin the response.
            Queries with offset parameter value
            exceeding 10000 will be rejected
            with a 400 response.
        :type offset: Optional[int], optional
        """
        query_params: Dict = {'fields': fields, 'limit': limit, 'offset': offset}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/versions']), FetchOptions(method='GET', params=prepare_params(query_params), auth=self.auth, network_session=self.network_session))
        return FileVersions.from_dict(json.loads(response.text))
    def get_file_version_by_id(self, file_id: str, file_version_id: str, fields: Optional[str] = None) -> FileVersionFull:
        """
        Retrieve a specific version of a file.
        
        Versions are only tracked for Box users with premium accounts.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        :param file_version_id: The ID of the file version
            Example: "1234"
        :type file_version_id: str
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
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/versions/', file_version_id]), FetchOptions(method='GET', params=prepare_params(query_params), auth=self.auth, network_session=self.network_session))
        return FileVersionFull.from_dict(json.loads(response.text))
    def update_file_version_by_id(self, file_id: str, file_version_id: str, trashed_at: Optional[str] = None) -> FileVersionFull:
        """
        Restores a specific version of a file after it was deleted.
        
        Don't use this endpoint to restore Box Notes,

        
        as it works with file formats such as PDF, DOC,

        
        PPTX or similar.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        :param file_version_id: The ID of the file version
            Example: "1234"
        :type file_version_id: str
        :param trashed_at: Set this to `null` to clear
            the date and restore the file.
        :type trashed_at: Optional[str], optional
        """
        request_body: BaseObject = BaseObject(trashed_at=trashed_at)
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/versions/', file_version_id]), FetchOptions(method='PUT', body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return FileVersionFull.from_dict(json.loads(response.text))
    def delete_file_version_by_id(self, file_id: str, file_version_id: str, if_match: Optional[str] = None):
        """
        Move a file version to the trash.
        
        Versions are only tracked for Box users with premium accounts.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        :param file_version_id: The ID of the file version
            Example: "1234"
        :type file_version_id: str
        :param if_match: Ensures this item hasn't recently changed before
            making changes.
            Pass in the item's last observed `etag` value
            into this header and the endpoint will fail
            with a `412 Precondition Failed` if it
            has changed since.
        :type if_match: Optional[str], optional
        """
        headers: Dict = {'if_match': if_match}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/versions/', file_version_id]), FetchOptions(method='DELETE', headers=prepare_params(headers), auth=self.auth, network_session=self.network_session))
        return response.content
    def promote_file_version(self, file_id: str, id: Optional[str] = None, type: Optional[PromoteFileVersionTypeArg] = None, fields: Optional[str] = None) -> FileVersionFull:
        """
        Promote a specific version of a file.
        
        If previous versions exist, this method can be used to

        
        promote one of the older versions to the top of the version history.

        
        This creates a new copy of the old version and puts it at the

        
        top of the versions history. The file will have the exact same contents

        
        as the older version, with the the same hash digest, `etag`, and

        
        name as the original.

        
        Other properties such as comments do not get updated to their

        
        former values.

        
        Don't use this endpoint to restore Box Notes,

        
        as it works with file formats such as PDF, DOC,

        
        PPTX or similar.

        :param file_id: The unique identifier that represents a file.
            The ID for any file can be determined
            by visiting a file in the web application
            and copying the ID from the URL. For example,
            for the URL `https://*.app.box.com/files/123`
            the `file_id` is `123`.
            Example: "12345"
        :type file_id: str
        :param id: The file version ID
        :type id: Optional[str], optional
        :param type: The type to promote
        :type type: Optional[PromoteFileVersionTypeArg], optional
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
        request_body: BaseObject = BaseObject(id=id, type=type)
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/versions/current']), FetchOptions(method='POST', params=prepare_params(query_params), body=json.dumps(request_body.to_dict()), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return FileVersionFull.from_dict(json.loads(response.text))