import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas import ShieldInformationBarrier

from box_sdk_gen.schemas import ShieldInformationBarrierSegment

from box_sdk_gen.schemas import ShieldInformationBarrierBase

from box_sdk_gen.schemas import ShieldInformationBarrierBaseTypeField

from box_sdk_gen.schemas import ShieldInformationBarrierSegmentRestriction

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionTypeArg,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentArg,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentArgTypeField,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentArg,
)

from box_sdk_gen.managers.shield_information_barrier_segment_restrictions import (
    CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentArgTypeField,
)

from box_sdk_gen.schemas import ShieldInformationBarrierSegmentRestrictions

from box_sdk_gen.utils import get_env_var

from box_sdk_gen.utils import get_uuid

from test.commons import get_default_client_as_user

from test.commons import get_or_create_shield_information_barrier


def testShieldInformationBarrierSegmentRestrictions():
    client: BoxClient = get_default_client_as_user(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    barrier_id: str = barrier.id
    segment: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            shield_information_barrier=ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER.value,
            ),
            name=get_uuid(),
            description='barrier segment description',
        )
    )
    segment_id: str = segment.id
    segment_to_restrict: ShieldInformationBarrierSegment = (
        client.shield_information_barrier_segments.create_shield_information_barrier_segment(
            shield_information_barrier=ShieldInformationBarrierBase(
                id=barrier_id,
                type=ShieldInformationBarrierBaseTypeField.SHIELD_INFORMATION_BARRIER.value,
            ),
            name=get_uuid(),
            description='barrier segment description',
        )
    )
    segment_to_restrict_id: str = segment_to_restrict.id
    segment_restriction: ShieldInformationBarrierSegmentRestriction = (
        client.shield_information_barrier_segment_restrictions.create_shield_information_barrier_segment_restriction(
            type=CreateShieldInformationBarrierSegmentRestrictionTypeArg.SHIELD_INFORMATION_BARRIER_SEGMENT_RESTRICTION.value,
            shield_information_barrier_segment=CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentArg(
                id=segment_id,
                type=CreateShieldInformationBarrierSegmentRestrictionShieldInformationBarrierSegmentArgTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT.value,
            ),
            restricted_segment=CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentArg(
                id=segment_to_restrict_id,
                type=CreateShieldInformationBarrierSegmentRestrictionRestrictedSegmentArgTypeField.SHIELD_INFORMATION_BARRIER_SEGMENT.value,
            ),
        )
    )
    segment_restriction_id: str = segment_restriction.id
    assert segment_restriction.shield_information_barrier_segment.id == segment_id
    segment_restrictions: ShieldInformationBarrierSegmentRestrictions = (
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restrictions(
            shield_information_barrier_segment_id=segment_id
        )
    )
    assert len(segment_restrictions.entries) > 0
    segment_restriction_from_api: ShieldInformationBarrierSegmentRestriction = (
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restriction_by_id(
            shield_information_barrier_segment_restriction_id=segment_restriction_id
        )
    )
    assert segment_restriction_from_api.id == segment_restriction_id
    assert (
        segment_restriction_from_api.shield_information_barrier_segment.id == segment_id
    )
    assert segment_restriction_from_api.restricted_segment.id == segment_to_restrict_id
    assert segment_restriction_from_api.shield_information_barrier.id == barrier_id
    client.shield_information_barrier_segment_restrictions.delete_shield_information_barrier_segment_restriction_by_id(
        shield_information_barrier_segment_restriction_id=segment_restriction_id
    )
    with pytest.raises(Exception):
        client.shield_information_barrier_segment_restrictions.get_shield_information_barrier_segment_restriction_by_id(
            shield_information_barrier_segment_restriction_id=segment_restriction_id
        )
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        shield_information_barrier_segment_id=segment_id
    )
    client.shield_information_barrier_segments.delete_shield_information_barrier_segment_by_id(
        shield_information_barrier_segment_id=segment_to_restrict_id
    )