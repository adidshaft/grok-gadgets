"""Regression checks for the homepage's first-use path and evidence labels."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"


class SiteClarityTests(unittest.TestCase):
    def test_homepage_states_existing_grok_bot_and_pending_verification(self):
        hero = (SITE / "home-scene.html").read_text()
        self.assertIn(
            "Open-source SDKs for building hardware that your existing Grok Bot can use.",
            hero,
        )
        self.assertIn(
            "Grok Bot connection and physical hardware tests are still pending.", hero
        )
        self.assertIn('href="#scene-demo"', hero)

    def test_three_build_paths_and_legacy_component_anchor_are_preserved(self):
        builder = (SITE / "build.py").read_text()
        for target in ["esp32.html", "linux.html", "home-assistant.html"]:
            self.assertIn(target, builder)
        self.assertIn('id="components"', builder)
        self.assertIn('href="components.html"', builder)
        self.assertIn('"components.html"', builder)

    def test_component_inventory_is_rendered_on_docs_page(self):
        builder = (SITE / "build.py").read_text()
        self.assertIn('"components.html",\n    "Project components"', builder)
        home_page = builder.split('page(\n    "index.html",', 1)[1].split(
            'page(\n    "start.html",', 1
        )[0]
        self.assertNotIn("website/components.html", home_page)
        inventory = (SITE / "components.html").read_text()
        self.assertEqual(len(re.findall(r'<details class="component', inventory)), 10)
        self.assertIn('href="index.html#playground"', inventory)

    def test_finite_concept_stories_and_static_no_script_fallback_exist(self):
        hero = (SITE / "home-scene.html").read_text()
        stories = re.findall(r'data-story="([a-z]+)"', hero)
        self.assertEqual(stories, ["light", "sensor", "display", "home"])
        self.assertIn('id="scene-replay"', hero)
        self.assertIn("Static conceptual routes are shown above.", hero)
        self.assertIn('href="simulator.html"', hero)

    def test_motion_state_has_one_controller_and_offline_copy_is_uncertain(self):
        scene = (SITE / "scene.js").read_text()
        motion = (SITE / "motion.js").read_text()
        self.assertNotIn("matchMedia", scene)
        self.assertIn("grok:motion-change", motion)
        self.assertIn("document.hidden", motion)
        self.assertIn("current output unknown", scene)
        self.assertIn("error.code", scene)


if __name__ == "__main__":
    unittest.main()
