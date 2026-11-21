"""Offline guard: publish workflows must not bypass the release review event."""

from pathlib import Path
import unittest

# Keep dependency-free unittest CI, while marking collected tests for the
# repository's strict pytest gate when pytest is installed.
try:
    import pytest
except ImportError:
    pytest = None
if pytest is not None:
    pytestmark = pytest.mark.offline

ROOT = Path(__file__).resolve().parents[2]


class PublicationGuardTests(unittest.TestCase):
    def test_publishing_requires_release_event(self):
        for name in ("docker-publish.yml", "pypi-publish.yml"):
            text = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
            self.assertIn("  release:\n    types: [published]", text)
            self.assertNotIn("  workflow_dispatch:", text)
            self.assertNotRegex(text, r"(?m)^  push:\s*$")

    def test_manual_build_uses_test_sha_namespace(self):
        text = (ROOT / ".github/workflows/docker-build-manual.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("  workflow_dispatch:", text)
        self.assertIn(
            'TEST_IMAGE_TAG="test-sha-$(git rev-parse --short=12 HEAD)"', text
        )
        self.assertIn('echo "image_tag=$TEST_IMAGE_TAG" >> $GITHUB_OUTPUT', text)
        self.assertIn(
            "type=raw,value=${{ steps.get_tag.outputs.image_tag }}", text
        )
        self.assertNotIn("type=raw,value=${{ steps.get_tag.outputs.tag }}", text)
        self.assertIn(
            "ghcr.io/${{ github.repository }}:${{ steps.get_tag.outputs.image_tag }}",
            text,
        )


if __name__ == "__main__":
    unittest.main()
