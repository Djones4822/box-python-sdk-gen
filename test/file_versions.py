from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas.files import Files

from box_sdk_gen.managers.uploads import UploadFileAttributes

from box_sdk_gen.managers.uploads import UploadFileAttributesParentField

from box_sdk_gen.schemas.file_full import FileFull

from box_sdk_gen.managers.uploads import UploadFileVersionAttributes

from box_sdk_gen.schemas.file_versions import FileVersions

from box_sdk_gen.schemas.file_version_full import FileVersionFull

from box_sdk_gen.managers.file_versions import PromoteFileVersionType

from box_sdk_gen.internal.utils import get_uuid

from box_sdk_gen.internal.utils import generate_byte_stream

from test.commons import get_default_client

client: BoxClient = get_default_client()


def testCreateListGetRestoreDeleteFileVersion():
    old_name: str = get_uuid()
    new_name: str = get_uuid()
    files: Files = client.uploads.upload_file(
        UploadFileAttributes(
            name=old_name, parent=UploadFileAttributesParentField(id='0')
        ),
        generate_byte_stream(10),
    )
    file: FileFull = files.entries[0]
    assert file.name == old_name
    assert file.size == 10
    new_files: Files = client.uploads.upload_file_version(
        file.id, UploadFileVersionAttributes(name=new_name), generate_byte_stream(20)
    )
    new_file: FileFull = new_files.entries[0]
    assert new_file.name == new_name
    assert new_file.size == 20
    file_versions: FileVersions = client.file_versions.get_file_versions(file.id)
    assert file_versions.total_count == 1
    file_version: FileVersionFull = client.file_versions.get_file_version_by_id(
        file.id, file_versions.entries[0].id
    )
    assert file_version.id == file_versions.entries[0].id
    client.file_versions.promote_file_version(
        file.id,
        id=file_versions.entries[0].id,
        type=PromoteFileVersionType.FILE_VERSION.value,
    )
    file_restored: FileFull = client.files.get_file_by_id(file.id)
    assert file_restored.name == old_name
    assert file_restored.size == 10
    file_versions_restored: FileVersions = client.file_versions.get_file_versions(
        file.id
    )
    client.file_versions.delete_file_version_by_id(
        file.id, file_versions_restored.entries[0].id
    )
    client.file_versions.get_file_versions(file.id)
    client.files.delete_file_by_id(file.id)
