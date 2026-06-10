import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AccumulationContractsTest(unittest.TestCase):
    def test_rolling_windows_excludes_partial_windows_by_default(self):
        tree = ast.parse(
            (ROOT / "core" / "accumulations.py").read_text(encoding="utf-8")
        )
        rolling_windows = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "rolling_windows"
        )
        namespace = {}
        module = ast.fix_missing_locations(
            ast.Module(body=[rolling_windows], type_ignores=[])
        )
        exec(compile(module, "core/accumulations.py", "exec"), namespace)

        self.assertEqual(namespace["rolling_windows"](87, 6)[-1], (78, 84))
        self.assertEqual(
            namespace["rolling_windows"](87, 6, include_partial=True)[-1],
            (84, 87),
        )

        with self.assertRaises(ValueError):
            namespace["rolling_windows"](87, 0)

    def test_accumulation_panel_helpers_use_suffixes(self):
        source = (ROOT / "graphics" / "panels.py").read_text(encoding="utf-8")

        self.assertIn('suffix=f"_acc{accumulation_hours:02d}"', source)
        self.assertIn('suffix=f"_acc{hours}"', source)
        self.assertIn('suffix=f"_day{day}"', source)


if __name__ == "__main__":
    unittest.main()
