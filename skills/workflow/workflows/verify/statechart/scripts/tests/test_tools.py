"""Check dependency preparation's filesystem and network boundaries."""
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('tlc_tool', Path(__file__).resolve().parents[1] / 'tlc-tool.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class ToolCacheTests(unittest.TestCase):
    def test_check_missing_does_not_download_or_create_directories(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(tool, 'urlopen') as network:
            target = Path(temp) / 'absent'
            with self.assertRaises(FileNotFoundError):
                tool.prepare(target, check=True)
            network.assert_not_called()
            self.assertFalse(target.exists())

    def test_invalid_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(tool, 'urlopen') as network:
            target = Path(temp) / tool.FILENAME
            target.write_bytes(b'user data')
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                tool.prepare(Path(temp))
            self.assertEqual(target.read_bytes(), b'user data')
            network.assert_not_called()

    def test_download_hash_is_checked_before_publishing(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(tool, 'urlopen', return_value=io.BytesIO(b'bad')):
            target = Path(temp) / 'cache'
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                tool.prepare(target)
            self.assertFalse(target.exists())

    def test_valid_download_and_second_check_are_repeatable(self):
        data = b'purpose-generated dependency fixture'
        with tempfile.TemporaryDirectory() as temp, patch.object(tool, 'SHA256', hashlib.sha256(data).hexdigest()), \
                patch.object(tool, 'urlopen', return_value=io.BytesIO(data)) as network:
            target = tool.prepare(Path(temp))
            self.assertEqual(target.read_bytes(), data)
            self.assertEqual(tool.prepare(Path(temp), check=True), target)
            self.assertEqual(network.call_count, 1)
            self.assertEqual(list(Path(temp).iterdir()), [target])

    def test_cache_inside_package_is_refused(self):
        with patch.object(tool, 'urlopen') as network:
            with self.assertRaisesRegex(ValueError, 'outside the immutable'):
                tool.prepare(tool.package_root() / 'tools')
            network.assert_not_called()


if __name__ == '__main__':
    unittest.main()
