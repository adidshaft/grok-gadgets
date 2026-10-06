"""Regression checks for the homepage's first-use path and evidence labels."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"


class SiteClarityTests(unittest.TestCase):
    def test_homepage_states_existing_grok_bot_and_pending_verification(self):
        hero = (SITE / "home-scene.html").read_text()
        self.assertIn("your Grok Bot.", hero)
        self.assertIn("Open-source tools and SDKs", hero)
        self.assertIn("Grok Bot and hardware connection tests are still ahead.", hero)
        self.assertIn('href="doc-docs-public-support-matrix.html"', hero)
        self.assertIn('id="scene-demo"', hero)
        self.assertIn('href="start.html"', hero)

    def test_three_build_paths_and_legacy_component_anchor_are_preserved(self):
        builder = (SITE / "build.py").read_text()
        for title in ['"No hardware"', '"Raspberry Pi / Linux"', '"ESP32"']:
            self.assertIn(title, builder)
        self.assertIn("Already use Home Assistant?", builder)
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

    def test_concept_stories_and_static_no_script_fallback_exist(self):
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

    def test_scene_gallery_and_author_credit_are_available(self):
        hero = (SITE / "home-scene.html").read_text()
        gallery = (SITE / "scene-gallery.js").read_text()
        builder = (SITE / "build.py").read_text()
        self.assertEqual(
            re.findall(r'data-scene="([a-z]+)"', hero),
            ["devices", "signal", "hardware", "roadmap"],
        )
        self.assertIn("grok:scene-change", gallery)
        self.assertIn("scene.setActive(key === name)", gallery)
        self.assertIn("stories.hidden = name !== 'devices'", gallery)
        self.assertEqual(builder.count('href="https://x.com/adidshaft"'), 2)
        for name in ["roadmap-scene", "signal-scene", "hardware-scene"]:
            self.assertIn(name + ".js", builder)
            self.assertIn(name + ".css", builder)

    def test_projected_nodes_stay_inside_scene_vertical_bounds(self):
        scene = (SITE / "scene.js").read_text()
        self.assertIn(
            "const halfY = button.getBoundingClientRect().height / 2 + 8;", scene
        )
        self.assertIn("const centerY = dy + (p[1] + offset) * scale;", scene)
        self.assertIn("Math.max(halfY, Math.min(rect.height - halfY, centerY))", scene)


if __name__ == "__main__":
    unittest.main()
