import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ModuleContractsTest(unittest.TestCase):
    def test_panel_wrappers_accept_suffix(self):
        tree = ast.parse((ROOT / "graphics" / "panels.py").read_text(encoding="utf-8"))
        definitions = {
            node.name: [argument.arg for argument in node.args.args]
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }

        for wrapper in (
            "create_operational_panel",
            "create_uncertainty_panel",
            "create_probability_panel",
        ):
            self.assertIn("suffix", definitions[wrapper])

    def test_operational_launcher_runs_modular_entrypoint(self):
        launcher = (ROOT / "run_tlaloc.sh").read_text(encoding="utf-8")

        self.assertIn("python3 main.py", launcher)
        self.assertNotIn("python3 unico.py", launcher)


if __name__ == "__main__":
    unittest.main()
