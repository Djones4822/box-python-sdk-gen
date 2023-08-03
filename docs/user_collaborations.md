# UserCollaborationsManager


- [Get collaboration](#get-collaboration)
- [Update collaboration](#update-collaboration)
- [Remove collaboration](#remove-collaboration)
- [Create collaboration](#create-collaboration)

## Get collaboration

Retrieves a single collaboration.

This operation is performed by calling function `get_collaboration_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-collaborations-id/).

*Currently we don't have an example for calling `get_collaboration_by_id` in integration tests*

### Arguments

- collaboration_id `str`
  - The ID of the collaboration Example: "1234"
- fields `Optional[str]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response.  Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `Collaboration`.

Returns a collaboration object.


## Update collaboration

Updates a collaboration.
Can be used to change the owner of an item, or to
accept collaboration invites.

This operation is performed by calling function `update_collaboration_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/put-collaborations-id/).

*Currently we don't have an example for calling `update_collaboration_by_id` in integration tests*

### Arguments

- collaboration_id `str`
  - The ID of the collaboration Example: "1234"
- role `UpdateCollaborationByIdRoleArg`
  - The level of access granted.
- status `Optional[UpdateCollaborationByIdStatusArg]`
  - <!--alex ignore reject--> Set the status of a `pending` collaboration invitation, effectively accepting, or rejecting the invite.
- expires_at `Optional[str]`
  - Update the expiration date for the collaboration. At this date, the collaboration will be automatically removed from the item.  This feature will only work if the **Automatically remove invited collaborators: Allow folder owners to extend the expiry date** setting has been enabled in the **Enterprise Settings** of the **Admin Console**. When the setting is not enabled, collaborations can not have an expiry date and a value for this field will be result in an error.  Additionally, a collaboration can only be given an expiration if it was created after the **Automatically remove invited collaborator** setting was enabled.
- can_view_path `Optional[bool]`
  - Determines if the invited users can see the entire parent path to the associated folder. The user will not gain privileges in any parent folder and therefore can not see content the user is not collaborated on.  Be aware that this meaningfully increases the time required to load the invitee's **All Files** page. We recommend you limit the number of collaborations with `can_view_path` enabled to 1,000 per user.  Only owner or co-owners can invite collaborators with a `can_view_path` of `true`.  `can_view_path` can only be used for folder collaborations.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `Collaboration`.

Returns an updated collaboration object unless the owner has changed.If the role is changed to `owner`, the collaboration is deleted
and a new collaboration is created. The previous `owner` of
the old collaboration will be a `co-owner` on the new collaboration.


## Remove collaboration

Deletes a single collaboration.

This operation is performed by calling function `delete_collaboration_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-collaborations-id/).

*Currently we don't have an example for calling `delete_collaboration_by_id` in integration tests*

### Arguments

- collaboration_id `str`
  - The ID of the collaboration Example: "1234"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `None`.

A blank response is returned if the collaboration was
successfully deleted.


## Create collaboration

Adds a collaboration for a single user or a single group to a file
or folder.

Collaborations can be created using email address, user IDs, or a
group IDs.

If a collaboration is being created with a group, access to
this endpoint is dependent on the group's ability to be invited.

If collaboration is in `pending` status, the following fields
are redacted:
- `login` and `name` are hidden if a collaboration was created
using `user_id`,
-  `name` is hidden if a collaboration was created using `login`.

This operation is performed by calling function `create_collaboration`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-collaborations/).

*Currently we don't have an example for calling `create_collaboration` in integration tests*

### Arguments

- item `CreateCollaborationItemArg`
  - The item to attach the comment to.
- accessible_by `CreateCollaborationAccessibleByArg`
  - The user or group to give access to the item.
- role `CreateCollaborationRoleArg`
  - The level of access granted.
- can_view_path `Optional[bool]`
  - Determines if the invited users can see the entire parent path to the associated folder. The user will not gain privileges in any parent folder and therefore can not see content the user is not collaborated on.  Be aware that this meaningfully increases the time required to load the invitee's **All Files** page. We recommend you limit the number of collaborations with `can_view_path` enabled to 1,000 per user.  Only owner or co-owners can invite collaborators with a `can_view_path` of `true`.  `can_view_path` can only be used for folder collaborations.
- expires_at `Optional[str]`
  - Set the expiration date for the collaboration. At this date, the collaboration will be automatically removed from the item.  This feature will only work if the **Automatically remove invited collaborators: Allow folder owners to extend the expiry date** setting has been enabled in the **Enterprise Settings** of the **Admin Console**. When the setting is not enabled, collaborations can not have an expiry date and a value for this field will be result in an error.
- fields `Optional[str]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response.  Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- notify `Optional[bool]`
  - Determines if users should receive email notification for the action performed.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `Collaboration`.

Returns a new collaboration object.

