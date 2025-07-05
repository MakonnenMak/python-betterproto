import warnings

import pytest

from tests.mocks import MockChannel
from tests.output_betterproto.deprecated import (
    Empty,
    Message,
    Test,
    TestServiceStub,
)


@pytest.fixture
def message():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return Message(value="hello")


def test_deprecated_message():
    with pytest.warns(DeprecationWarning) as record:
        Message(value="hello")

    assert len(record) == 1
    assert str(record[0].message) == f"{Message.__name__} is deprecated"


def test_message_with_deprecated_field(message):
    with pytest.warns(DeprecationWarning) as record:
        Test(message=message, value=10)

    assert len(record) == 1
    assert str(record[0].message) == f"{Test.__name__}.message is deprecated"


def test_message_with_deprecated_field_not_set(message):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        Test(value=10)


def test_message_with_deprecated_field_not_set_default(message):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        _ = Test(value=10).message


def test_generated_code_has_warnings_import():
    """Test that the generated code includes the warnings import statement.
    
    This test verifies the core fix for the NameError issue where generated code
    would call warnings.warn() but not include 'import warnings'.
    """
    # Check the actual generated file content
    with open('tests/output_betterproto/deprecated/__init__.py', 'r') as f:
        content = f.read()
    
    # Verify warnings import is present
    assert 'import warnings' in content, "warnings import should be present in generated code"
    
    # Verify warnings.warn calls are present
    assert 'warnings.warn' in content, "warnings.warn calls should be present in generated code"
    
    # Verify DeprecationWarning is used
    assert 'DeprecationWarning' in content, "DeprecationWarning should be used in generated code"


@pytest.mark.asyncio
async def test_service_with_deprecated_method():
    stub = TestServiceStub(MockChannel([Empty(), Empty()]))

    with pytest.warns(DeprecationWarning) as record:
        await stub.deprecated_func(Empty())

    assert len(record) == 1
    assert str(record[0].message) == f"TestService.deprecated_func is deprecated"

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        await stub.func(Empty())
