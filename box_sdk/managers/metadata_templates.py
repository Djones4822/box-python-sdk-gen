from enum import Enum

from typing import Union

from box_sdk.base_object import BaseObject

from typing import List

import json

from box_sdk.schemas import MetadataTemplates

from box_sdk.schemas import ClientError

from box_sdk.schemas import MetadataTemplate

from box_sdk.developer_token_auth import DeveloperTokenAuth

from box_sdk.ccg_auth import CCGAuth

from box_sdk.fetch import fetch

from box_sdk.fetch import FetchOptions

from box_sdk.fetch import FetchResponse

class GetMetadataTemplatesIdIdSchemaScopeArg(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'

class DeleteMetadataTemplatesIdIdSchemaScopeArg(str, Enum):
    GLOBAL = 'global'
    ENTERPRISE = 'enterprise'

class GetMetadataTemplatesGlobalOptionsArg(BaseObject):
    def __init__(self, marker: Union[None, str] = None, limit: Union[None, int] = None, **kwargs):
        """
        :param marker: Defines the position marker at which to begin returning results. This is
            used when paginating using marker-based pagination.
            This requires `usemarker` to be set to `true`.
        :type marker: Union[None, str], optional
        :param limit: The maximum number of items to return per page.
        :type limit: Union[None, int], optional
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.limit = limit

class GetMetadataTemplatesEnterpriseOptionsArg(BaseObject):
    def __init__(self, marker: Union[None, str] = None, limit: Union[None, int] = None, **kwargs):
        """
        :param marker: Defines the position marker at which to begin returning results. This is
            used when paginating using marker-based pagination.
            This requires `usemarker` to be set to `true`.
        :type marker: Union[None, str], optional
        :param limit: The maximum number of items to return per page.
        :type limit: Union[None, int], optional
        """
        super().__init__(**kwargs)
        self.marker = marker
        self.limit = limit

class PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldTypeField(str, Enum):
    STRING = 'string'
    FLOAT = 'float'
    DATE = 'date'
    ENUM = 'enum'
    MULTISELECT = 'multiSelect'

class PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldOptionsField(BaseObject):
    def __init__(self, key: str, **kwargs):
        """
        :param key: The text value of the option. This represents both the display name of the
            option and the internal key used when updating templates.
        :type key: str
        """
        super().__init__(**kwargs)
        self.key = key

class PostMetadataTemplatesSchemaRequestBodyArgFieldsField(BaseObject):
    def __init__(self, type: PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldTypeField, key: str, display_name: str, description: Union[None, str] = None, hidden: Union[None, bool] = None, options: Union[None, List[PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldOptionsField]] = None, **kwargs):
        """
        :param type: The type of field. The basic fields are a `string` field for text, a
            `float` field for numbers, and a `date` fields to present the user with a
            date-time picker.
            Additionally, metadata templates support an `enum` field for a basic list
            of items, and ` multiSelect` field for a similar list of items where the
            user can select more than one value.
        :type type: PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldTypeField
        :param key: A unique identifier for the field. The identifier must
            be unique within the template to which it belongs.
        :type key: str
        :param display_name: The display name of the field as it is shown to the user in the web and
            mobile apps.
        :type display_name: str
        :param description: A description of the field. This is not shown to the user.
        :type description: Union[None, str], optional
        :param hidden: Whether this field is hidden in the UI for the user and can only be set
            through the API instead.
        :type hidden: Union[None, bool], optional
        :param options: A list of options for this field. This is used in combination with the
            `enum` and `multiSelect` field types.
        :type options: Union[None, List[PostMetadataTemplatesSchemaRequestBodyArgFieldsFieldOptionsField]], optional
        """
        super().__init__(**kwargs)
        self.type = type
        self.key = key
        self.display_name = display_name
        self.description = description
        self.hidden = hidden
        self.options = options

class PostMetadataTemplatesSchemaRequestBodyArg(BaseObject):
    def __init__(self, scope: str, display_name: str, template_key: Union[None, str] = None, hidden: Union[None, bool] = None, fields: Union[None, List[PostMetadataTemplatesSchemaRequestBodyArgFieldsField]] = None, copy_instance_on_item_copy: Union[None, bool] = None, **kwargs):
        """
        :param scope: The scope of the metadata template to create. Applications can
            only create templates for use within the authenticated user's
            enterprise.
            This value needs to be set to `enterprise`, as `global` scopes can
            not be created by applications.
        :type scope: str
        :param display_name: The display name of the template.
        :type display_name: str
        :param template_key: A unique identifier for the template. This identifier needs to be
            unique across the enterprise for which the metadata template is
            being created.
            When not provided, the API will create a unique `templateKey`
            based on the value of the `displayName`.
        :type template_key: Union[None, str], optional
        :param hidden: Defines if this template is visible in the Box web app UI, or if
            it is purely intended for usage through the API.
        :type hidden: Union[None, bool], optional
        :param fields: An ordered list of template fields which are part of the template.
            Each field can be a regular text field, date field, number field,
            as well as a single or multi-select list.
        :type fields: Union[None, List[PostMetadataTemplatesSchemaRequestBodyArgFieldsField]], optional
        :param copy_instance_on_item_copy: Whether or not to copy any metadata attached to a file or folder
            when it is copied. By default, metadata is not copied along with a
            file or folder when it is copied.
        :type copy_instance_on_item_copy: Union[None, bool], optional
        """
        super().__init__(**kwargs)
        self.scope = scope
        self.display_name = display_name
        self.template_key = template_key
        self.hidden = hidden
        self.fields = fields
        self.copy_instance_on_item_copy = copy_instance_on_item_copy

class MetadataTemplatesManager(BaseObject):
    def __init__(self, auth: Union[DeveloperTokenAuth, CCGAuth], **kwargs):
        super().__init__(**kwargs)
        self.auth = auth
    def get_metadata_templates(self, metadata_instance_id: str) -> MetadataTemplates:
        """
        Finds a metadata template by searching for the ID of an instance of the
        
        template.

        :param metadata_instance_id: The ID of an instance of the metadata template to find.
            Example: "01234500-12f1-1234-aa12-b1d234cb567e"
        :type metadata_instance_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates']), FetchOptions(method='GET', params={'metadata_instance_id': metadata_instance_id}, auth=self.auth))
        return MetadataTemplates.from_dict(json.loads(response.text))
    def get_metadata_templates_id_id_schema(self, scope: GetMetadataTemplatesIdIdSchemaScopeArg, template_key: str) -> MetadataTemplate:
        """
        Retrieves a metadata template by its `scope` and `templateKey` values.
        
        To find the `scope` and `templateKey` for a template, list all templates for

        
        an enterprise or globally, or list all templates applied to a file or folder.

        :param scope: The scope of the metadata template
            Example: "global"
        :type scope: GetMetadataTemplatesIdIdSchemaScopeArg
        :param template_key: The name of the metadata template
            Example: "properties"
        :type template_key: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/', scope, '/', template_key, '/schema']), FetchOptions(method='GET', auth=self.auth))
        return MetadataTemplate.from_dict(json.loads(response.text))
    def delete_metadata_templates_id_id_schema(self, scope: DeleteMetadataTemplatesIdIdSchemaScopeArg, template_key: str):
        """
        Delete a metadata template and its instances.
        
        This deletion is permanent and can not be reversed.

        :param scope: The scope of the metadata template
            Example: "global"
        :type scope: DeleteMetadataTemplatesIdIdSchemaScopeArg
        :param template_key: The name of the metadata template
            Example: "properties"
        :type template_key: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/', scope, '/', template_key, '/schema']), FetchOptions(method='DELETE', auth=self.auth))
        return response.content
    def get_metadata_templates_id(self, template_id: str) -> MetadataTemplate:
        """
        Retrieves a metadata template by its ID.
        :param template_id: The ID of the template
            Example: "f7a9891f"
        :type template_id: str
        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/', template_id]), FetchOptions(method='GET', auth=self.auth))
        return MetadataTemplate.from_dict(json.loads(response.text))
    def get_metadata_templates_global(self, options: GetMetadataTemplatesGlobalOptionsArg = None) -> MetadataTemplates:
        """
        Used to retrieve all generic, global metadata templates available to all
        
        enterprises using Box.

        """
        if options is None:
            options = GetMetadataTemplatesGlobalOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/global']), FetchOptions(method='GET', params={'marker': options.marker, 'limit': options.limit}, auth=self.auth))
        return MetadataTemplates.from_dict(json.loads(response.text))
    def get_metadata_templates_enterprise(self, options: GetMetadataTemplatesEnterpriseOptionsArg = None) -> MetadataTemplates:
        """
        Used to retrieve all metadata templates created to be used specifically within
        
        the user's enterprise

        """
        if options is None:
            options = GetMetadataTemplatesEnterpriseOptionsArg()
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/enterprise']), FetchOptions(method='GET', params={'marker': options.marker, 'limit': options.limit}, auth=self.auth))
        return MetadataTemplates.from_dict(json.loads(response.text))
    def post_metadata_templates_schema(self, request_body: PostMetadataTemplatesSchemaRequestBodyArg) -> MetadataTemplate:
        """
        Creates a new metadata template that can be applied to
        
        files and folders.

        """
        response: FetchResponse = fetch(''.join(['https://api.box.com/2.0/metadata_templates/schema']), FetchOptions(method='POST', body=json.dumps(request_body.to_dict()), auth=self.auth))
        return MetadataTemplate.from_dict(json.loads(response.text))