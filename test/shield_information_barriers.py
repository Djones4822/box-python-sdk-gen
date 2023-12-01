from box_sdk_gen.utils import to_string

import pytest

from box_sdk_gen.client import BoxClient

from box_sdk_gen.schemas import ShieldInformationBarrier

from box_sdk_gen.schemas import ShieldInformationBarriers

from box_sdk_gen.managers.shield_information_barriers import (
    CreateShieldInformationBarrierChangeStatusStatusArg,
)

from box_sdk_gen.utils import get_env_var

from test.commons import get_default_client_as_user

from test.commons import get_or_create_shield_information_barrier


def testShieldInformationBarriers():
    client: BoxClient = get_default_client_as_user(get_env_var('USER_ID'))
    enterprise_id: str = get_env_var('ENTERPRISE_ID')
    barrier: ShieldInformationBarrier = get_or_create_shield_information_barrier(
        client, enterprise_id
    )
    assert to_string(barrier.status) == 'draft'
    assert to_string(barrier.type) == 'shield_information_barrier'
    assert barrier.enterprise.id == enterprise_id
    assert to_string(barrier.enterprise.type) == 'enterprise'
    barrier_id: str = barrier.id
    barrier_from_api: ShieldInformationBarrier = (
        client.shield_information_barriers.get_shield_information_barrier_by_id(
            shield_information_barrier_id=barrier_id
        )
    )
    assert barrier_from_api.id == barrier_id
    barriers: ShieldInformationBarriers = (
        client.shield_information_barriers.get_shield_information_barriers()
    )
    assert len(barriers.entries) == 1
    with pytest.raises(Exception):
        client.shield_information_barriers.create_shield_information_barrier_change_status(
            id=barrier_id,
            status=CreateShieldInformationBarrierChangeStatusStatusArg.DISABLED.value,
        )