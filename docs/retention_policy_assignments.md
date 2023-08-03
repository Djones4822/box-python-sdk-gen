# RetentionPolicyAssignmentsManager


- [List retention policy assignments](#list-retention-policy-assignments)
- [Assign retention policy](#assign-retention-policy)
- [Get retention policy assignment](#get-retention-policy-assignment)
- [Remove retention policy assignment](#remove-retention-policy-assignment)
- [Get files under retention](#get-files-under-retention)
- [Get file versions under retention](#get-file-versions-under-retention)

## List retention policy assignments

Returns a list of all retention policy assignments associated with a specified
retention policy.

This operation is performed by calling function `get_retention_policy_assignments`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policies-id-assignments/).

*Currently we don't have an example for calling `get_retention_policy_assignments` in integration tests*

### Arguments

- retention_policy_id `str`
  - The ID of the retention policy. Example: "982312"
- type `Optional[GetRetentionPolicyAssignmentsTypeArg]`
  - The type of the retention policy assignment to retrieve.
- fields `Optional[str]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response.  Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `RetentionPolicyAssignments`.

Returns a list of the retention policy assignments associated with the
specified retention policy.


## Assign retention policy

Assigns a retention policy to an item.

This operation is performed by calling function `create_retention_policy_assignment`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-retention-policy-assignments/).

*Currently we don't have an example for calling `create_retention_policy_assignment` in integration tests*

### Arguments

- policy_id `str`
  - The ID of the retention policy to assign
- assign_to `CreateRetentionPolicyAssignmentAssignToArg`
  - The item to assign the policy to
- filter_fields `Optional[List]`
  - If the `assign_to` type is `metadata_template`, then optionally add the `filter_fields` parameter which will require an array of objects with a field entry and a value entry. Currently only one object of `field` and `value` is supported.
- start_date_field `Optional[str]`
  - The date the retention policy assignment begins.  If the `assigned_to` type is `metadata_template`, this field can be a date field's metadata attribute key id.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `RetentionPolicyAssignment`.

Returns a new retention policy assignment object.


## Get retention policy assignment

Retrieves a retention policy assignment

This operation is performed by calling function `get_retention_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policy-assignments-id/).

*Currently we don't have an example for calling `get_retention_policy_assignment_by_id` in integration tests*

### Arguments

- retention_policy_assignment_id `str`
  - The ID of the retention policy assignment. Example: "1233123"
- fields `Optional[str]`
  - A comma-separated list of attributes to include in the response. This can be used to request fields that are not normally returned in a standard response.  Be aware that specifying this parameter will have the effect that none of the standard fields are returned in the response unless explicitly specified, instead only fields for the mini representation are returned, additional to the fields requested.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `RetentionPolicyAssignment`.

Returns the retention policy assignment object.


## Remove retention policy assignment

Removes a retention policy assignment
applied to content.

This operation is performed by calling function `delete_retention_policy_assignment_by_id`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/delete-retention-policy-assignments-id/).

*Currently we don't have an example for calling `delete_retention_policy_assignment_by_id` in integration tests*

### Arguments

- retention_policy_assignment_id `str`
  - The ID of the retention policy assignment. Example: "1233123"
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `None`.

Returns an empty response when the policy assignment
is successfully deleted.


## Get files under retention

Returns a list of files under retention for a retention policy assignment.

This operation is performed by calling function `get_retention_policy_assignment_file_under_retention`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policy-assignments-id-files-under-retention/).

*Currently we don't have an example for calling `get_retention_policy_assignment_file_under_retention` in integration tests*

### Arguments

- retention_policy_assignment_id `str`
  - The ID of the retention policy assignment. Example: "1233123"
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.  This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `FilesUnderRetention`.

Returns a list of files under retention that are associated with the
specified retention policy assignment.


## Get file versions under retention

Returns a list of file versions under retention for a retention policy
assignment.

This operation is performed by calling function `get_retention_policy_assignment_file_version_under_retention`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/get-retention-policy-assignments-id-file-versions-under-retention/).

*Currently we don't have an example for calling `get_retention_policy_assignment_file_version_under_retention` in integration tests*

### Arguments

- retention_policy_assignment_id `str`
  - The ID of the retention policy assignment. Example: "1233123"
- marker `Optional[str]`
  - Defines the position marker at which to begin returning results. This is used when paginating using marker-based pagination.  This requires `usemarker` to be set to `true`.
- limit `Optional[int]`
  - The maximum number of items to return per page.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.


### Returns

This function returns a value of type `FilesUnderRetention`.

Returns a list of file versions under retention that are associated with
the specified retention policy assignment.

