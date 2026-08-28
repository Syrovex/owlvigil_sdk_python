import os

import pytest

from owlvigil import OwlVigil


@pytest.mark.skipif(os.getenv("OWLVIGIL_LIVE_TEST") != "1", reason="set OWLVIGIL_LIVE_TEST=1")
def test_live_read_only_gateway_and_management_flow():
    with OwlVigil() as client:
        models = client.gateway.list_models()
        assert models.data["data"]
        workspaces = client.management.list_workspaces()
        assert workspaces.data["items"]
        usage = client.management.get_usage_summary(workspaces.data["items"][0]["id"])
        assert usage.data["requests"] >= 0
