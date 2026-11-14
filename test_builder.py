import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import asdk_agraph_plugin_builder as builder


class BuilderRegressionTests(unittest.TestCase):
    def setUp(self):
        self.verbose = patch.object(builder, '_verbose', False, create=True)
        self.verbose.start()
        self.addCleanup(self.verbose.stop)

    def test_resources_follow_script_when_working_directory_changes(self):
        script = Path(builder.__file__).resolve()
        with tempfile.TemporaryDirectory() as directory:
            previous = os.getcwd()
            try:
                os.chdir(directory)
                spec = importlib.util.spec_from_file_location('relocated_builder', script)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            finally:
                os.chdir(previous)
        self.assertEqual(Path(module._ASDK_PLUGIN_BUILDER_REPO), script.parent)
        self.assertTrue(Path(module._openapi_generator_jar_filepath).is_file())

    def test_nested_bundle_keeps_root_and_sibling_files(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / 'portfolio'
            expected = []
            for name in ('root.json', 'first/a.json', 'second/b.json'):
                path = bundle / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('{}')
                expected.append(str(path))
            with patch.object(builder, '_generate_api_client_using_swagger', side_effect=ValueError('fixture')) as generate:
                builder._create_plugin_content(str(bundle), directory, '1.0.0')
            self.assertCountEqual([call.args[1] for call in generate.call_args_list], expected)

    def test_trailing_separator_preserves_plugin_name(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / 'portfolio'
            bundle.mkdir()
            with patch.object(builder, '_print_run_summary') as summary:
                builder._create_plugin_content(str(bundle) + os.sep, directory, '1.0.0')
            self.assertEqual(summary.call_args.args[0], 'asdk_plugin_portfolio')

    def test_failed_generator_does_not_touch_existing_target_or_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            details = ('DemoAPI', 'v1', 'asdk_plugin_demo.agraph.demo.v1.DemoAPI')
            with patch.object(builder, '_fetch_api_details_from_agraph_swagger', return_value=details), \
                    patch.object(builder, '_run_command', return_value=False) as run, \
                    patch.object(builder, '_update_asdk_plugin_codegen_section') as registry:
                with self.assertRaisesRegex(RuntimeError, 'generation failed'):
                    builder._generate_api_client_using_swagger('asdk_plugin_demo', 'fixture.json', directory)
            self.assertEqual(run.call_count, 1)
            registry.assert_not_called()

    def test_failed_copy_does_not_update_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            details = ('DemoAPI', 'v1', 'asdk_plugin_demo.agraph.demo.v1.DemoAPI')
            with patch.object(builder, '_fetch_api_details_from_agraph_swagger', return_value=details), \
                    patch.object(builder, '_run_command', side_effect=lambda command, **kwargs: command[0] == 'java'), \
                    patch.object(builder, '_update_asdk_plugin_codegen_section') as registry:
                with self.assertRaisesRegex(RuntimeError, 'Copying'):
                    builder._generate_api_client_using_swagger('asdk_plugin_demo', 'fixture.json', directory)
            registry.assert_not_called()


if __name__ == '__main__':
    unittest.main()
