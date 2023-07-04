from enum import Enum

from box_sdk.base_object import BaseObject

from typing import Optional

from typing import Dict

import json

from box_sdk.base_object import BaseObject

from box_sdk.schemas import Comments

from box_sdk.schemas import ClientError

from box_sdk.schemas import CommentFull

from box_sdk.schemas import Comment

from box_sdk.auth import Authentication

from box_sdk.network import NetworkSession

from box_sdk.utils import to_map

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class CreateCommentItemArgTypeField(str, Enum):
    FILE = 'file'
    COMMENT = 'comment'

class CreateCommentItemArg(BaseObject):
    def __init__(self, id: str, type: CreateCommentItemArgTypeField, **kwargs):
        """
        :param id: The ID of the item
        :type id: str
        :param type: The type of the item that this comment will be placed on.
        :type type: CreateCommentItemArgTypeField
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type

class CommentsManager:
    def __init__(self, auth: Optional[Authentication] = None, network_session: Optional[NetworkSession] = None):
        self.auth = auth
        self.network_session = network_session
    def get_file_comments(self, file_id: str, fields: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> Comments:
        """
        Retrieves a list of comments for a file.
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
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/files/', file_id, '/comments']), FetchOptions(method='GET', params=to_map(query_params), auth=self.auth, network_session=self.network_session))
        return Comments.from_dict(json.loads(response.text))
    def get_comment_by_id(self, comment_id: str, fields: Optional[str] = None) -> CommentFull:
        """
        Retrieves the message and metadata for a specific comment, as well
        
        as information on the user who created the comment.

        :param comment_id: The ID of the comment.
            Example: "12345"
        :type comment_id: str
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
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/comments/', comment_id]), FetchOptions(method='GET', params=to_map(query_params), auth=self.auth, network_session=self.network_session))
        return CommentFull.from_dict(json.loads(response.text))
    def update_comment_by_id(self, comment_id: str, message: Optional[str] = None, fields: Optional[str] = None) -> CommentFull:
        """
        Update the message of a comment.
        :param comment_id: The ID of the comment.
            Example: "12345"
        :type comment_id: str
        :param message: The text of the comment to update
        :type message: Optional[str], optional
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
        request_body: BaseObject = BaseObject(message=message)
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/comments/', comment_id]), FetchOptions(method='PUT', params=to_map(query_params), body=json.dumps(to_map(request_body)), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return CommentFull.from_dict(json.loads(response.text))
    def delete_comment_by_id(self, comment_id: str):
        """
        Permanently deletes a comment.
        :param comment_id: The ID of the comment.
            Example: "12345"
        :type comment_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/comments/', comment_id]), FetchOptions(method='DELETE', auth=self.auth, network_session=self.network_session))
        return response.content
    def create_comment(self, message: str, tagged_message: Optional[str] = None, item: Optional[CreateCommentItemArg] = None, fields: Optional[str] = None) -> Comment:
        """
        Adds a comment by the user to a specific file, or
        
        as a reply to an other comment.

        :param message: The text of the comment.
            To mention a user, use the `tagged_message`
            parameter instead.
        :type message: str
        :param tagged_message: The text of the comment, including `@[user_id:name]`
            somewhere in the message to mention another user, which
            will send them an email notification, letting them know
            they have been mentioned.
            The `user_id` is the target user's ID, where the `name`
            can be any custom phrase. In the Box UI this name will
            link to the user's profile.
            If you are not mentioning another user, use `message`
            instead.
        :type tagged_message: Optional[str], optional
        :param item: The item to attach the comment to.
        :type item: Optional[CreateCommentItemArg], optional
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
        request_body: BaseObject = BaseObject(message=message, tagged_message=tagged_message, item=item)
        query_params: Dict = {'fields': fields}
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/comments']), FetchOptions(method='POST', params=to_map(query_params), body=json.dumps(to_map(request_body)), content_type='application/json', auth=self.auth, network_session=self.network_session))
        return Comment.from_dict(json.loads(response.text))