import warnings

import pytest

from tests.output_betterproto.deprecated_message_option import Bar, Foo


def test_deprecated_message_option_has_warnings_import():
    """Test that generated code with deprecated message option includes warnings import."""

    # Check that creating a deprecated message triggers a warning
    with pytest.warns(DeprecationWarning, match="Foo is deprecated"):
        foo = Foo(old_field="test")

    # Check that creating a normal message doesn't trigger a warning
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        bar = Bar(normal_field="test")


def test_generated_code_has_warnings_import():
    """Test that the generated code includes the warnings import."""

    # Check the actual generated file content
    with open(
        "tests/output_betterproto/deprecated_message_option/__init__.py", "r"
    ) as f:
        content = f.read()

    # Verify warnings import is present
    assert "import warnings" in content, (
        "warnings import should be present in generated code"
    )

    # Verify warnings.warn calls are present
    assert "warnings.warn" in content, (
        "warnings.warn calls should be present in generated code"
    )

    # Verify DeprecationWarning is used
    assert "DeprecationWarning" in content, (
        "DeprecationWarning should be used in generated code"
    )


def test_deprecated_message_works_correctly():
    """Test that the deprecated message works correctly."""

    # Test that the deprecated message can be instantiated
    foo = Foo(old_field="test")
    assert foo.old_field == "test"

    # Test that the normal message can be instantiated
    bar = Bar(normal_field="test")
    assert bar.normal_field == "test"


def test_warnings_import_is_available():
    """Test that the warnings module is available in the generated module."""

    import tests.output_betterproto.deprecated_message_option as module

    # Check that warnings is imported
    assert hasattr(module, "warnings"), "warnings module should be imported"

    # Verify the import statement exists in the source
    import inspect

    source = inspect.getsource(module)
    assert "import warnings" in source, "warnings import should be present in source"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
