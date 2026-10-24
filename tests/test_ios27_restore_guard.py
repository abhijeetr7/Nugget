"""Offline tests for Nugget's conservative restore-version gate.

These tests do not connect to or modify a device.
"""

from src.devicemanagement.constants import Device, MAX_VERSION


def make_device(version: str, build: str = "test-build") -> Device:
    return Device(
        udid="offline-test", usb=True, name="Test iPhone", version=version,
        build=build, model="iPhone99,1", hardware="test", cpu="test",
        locale="en_US", books_container_uuid="",
    )


def test_ios_27_is_not_restore_supported():
    device = make_device("27.0")
    assert device.supported() is False
    assert "Apple has patched" in (device.restore_support_reason() or "")
    assert "data loss" in (device.restore_support_reason() or "")


def test_ios_27_point_releases_remain_blocked():
    for version in ("27.0", "27.0.1", "27.1"):
        assert make_device(version).supported() is False


def test_known_range_stays_version_eligible():
    device = make_device(MAX_VERSION)
    assert device.supported() is True
    assert device.restore_support_reason() is None


def test_versions_below_minimum_are_blocked():
    device = make_device("16.7.9")
    assert device.supported() is False
    assert "minimum supported version" in (device.restore_support_reason() or "")
