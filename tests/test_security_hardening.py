import io
import os
import tempfile
import unittest
import zipfile
from types import SimpleNamespace

from security_engine.handlers.rule.rule_load_handler import GithubRepoRuleLoadHandler
from security_engine.utils.safe_eval import UnsafeExpressionError, safe_eval


class SafeExpressionEvaluatorTests(unittest.TestCase):
    def test_supported_rule_expression_is_evaluated(self):
        context = {
            'token_transfer': SimpleNamespace(to='0xrecipient'),
            'get_token': lambda address: address == '0xrecipient',
        }

        result = safe_eval(
            'bool(token_transfer) and bool(get_token(token_transfer.to))',
            context,
        )

        self.assertTrue(result)

    def test_comprehension_and_membership_are_supported(self):
        contracts = [
            SimpleNamespace(is_multisig=False),
            SimpleNamespace(is_multisig=True),
        ]

        self.assertTrue(
            safe_eval('any([item.is_multisig for item in contracts])', {
                'contracts': contracts,
            })
        )

    def test_import_and_private_attribute_access_are_rejected(self):
        with self.assertRaises(UnsafeExpressionError):
            safe_eval("__import__('os').system('echo unsafe')", {})

        with self.assertRaises(UnsafeExpressionError):
            safe_eval('value.__class__', {'value': object()})


class ArchiveExtractionTests(unittest.TestCase):
    def test_path_traversal_archive_entry_is_rejected(self):
        with tempfile.TemporaryDirectory() as destination:
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w') as zip_ref:
                zip_ref.writestr('../escaped.txt', 'must not be written')
            archive.seek(0)

            with zipfile.ZipFile(archive) as zip_ref:
                with self.assertRaises(ValueError):
                    GithubRepoRuleLoadHandler._extract_archive(zip_ref, destination)

            self.assertFalse(os.path.exists(os.path.join(destination, '..', 'escaped.txt')))

    def test_valid_archive_is_extracted(self):
        with tempfile.TemporaryDirectory() as destination:
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, 'w') as zip_ref:
                zip_ref.writestr('repo/ruleset/text/common.yaml', '[]')
            archive.seek(0)

            with zipfile.ZipFile(archive) as zip_ref:
                GithubRepoRuleLoadHandler._extract_archive(zip_ref, destination)

            extracted = os.path.join(destination, 'repo', 'ruleset', 'text', 'common.yaml')
            self.assertTrue(os.path.isfile(extracted))


if __name__ == '__main__':
    unittest.main()
