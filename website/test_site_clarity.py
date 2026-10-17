"""Regression checks for the homepage's first-use path and evidence labels."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"


class SiteClarityTests(unittest.TestCase):
    def test_homepage_states_owner_tested_grok_bot_route_without_crowding(self):
        hero = (SITE / "home-scene.html").read_text()
        self.assertIn("Your Grok Bot.", hero)
        self.assertIn("In the real world.", hero)
        self.assertIn("Connect the hardware around you to your Grok Bot.", hero)
        self.assertIn("Set it up from your phone, then just ask.", hero)
        self.assertEqual(hero.count('<div class="scene-intro">'), 1)
        self.assertNotIn('class="scene-status"', hero)
        self.assertNotIn("Alpha · one kit verified · native Grok Bot calls next", hero)
        self.assertNotIn("Today: approved local commands on Mac.", hero)
        self.assertIn(
            'class="status-link" href="doc-docs-public-support-matrix.html"',
            (SITE / "build.py").read_text(),
        )
        self.assertIn('id="scene-demo"', hero)
        self.assertIn('href="start.html"', hero)

    def test_today_next_later_and_distinct_reader_paths(self):
        builder = (SITE / "build.py").read_text()
        roadmap = (SITE / "roadmap-scene.js").read_text()
        nav = (SITE / "docs_navigation.py").read_text()
        self.assertIn("<h2>Today, next, later.</h2>", builder)
        self.assertIn(
            "Two people tested this on the owner’s relay and kit with their own iPhones (Phase 11).",
            builder,
        )
        self.assertIn("Tested from the guide on a fresh host (Phase 12a).", builder)
        self.assertNotIn("This is Phase 12; it has not started.", builder)
        self.assertIn(
            "a bad image reverts by itself. Tested on the owner’s kit (Phase 12b).",
            builder,
        )
        self.assertIn("The project hosts no relay.", builder)
        self.assertNotIn("optional hosted relay", builder)
        self.assertIn('"Use your gadget with Grok Bot"', builder)
        self.assertIn('"Build the tested OLED kit"', builder)
        self.assertIn('"Use a gadget"', nav)
        self.assertIn('"Status and roadmap"', nav)
        self.assertIn("name: 'Mac-free route'", roadmap)
        self.assertIn("status: 'Owner tested'", roadmap)
        self.assertNotIn("Daily use", roadmap)

    def test_newcomer_entry_points_continue_from_setup_to_claim(self):
        builder = (SITE / "build.py").read_text()
        start = builder.split('"start.html",\n    "Get started",', 1)[1].split(
            '"simulator.html",\n    "Simulator",', 1
        )[0]
        self.assertIn('"doc-docs-getting-started-claim-your-gadget.html"', start)
        self.assertIn('"Claim guide"', start)
        self.assertNotIn('"Connect guide"', start)
        entry = builder.split('aria-label="Choose a path"', 1)[1].split("</nav>", 1)[0]
        self.assertIn('href="doc-docs-getting-started-claim-your-gadget.html"', entry)
        self.assertIn("Claim in Grok Bot", entry)

    def test_three_build_paths_and_legacy_component_anchor_are_preserved(self):
        builder = (SITE / "build.py").read_text()
        for title in ['"No hardware"', '"Raspberry Pi / Linux"', '"OLED starter kit"']:
            self.assertIn(title, builder)
        self.assertIn("Run Home Assistant?", builder)
        for target in ["esp32.html", "linux.html", "home-assistant.html"]:
            self.assertIn(target, builder)
        self.assertIn('id="components"', builder)
        self.assertIn('href="components.html"', builder)
        self.assertIn('"components.html"', builder)
        self.assertIn(
            'class="header-actions"><a id="donate-open" href="donate.html"', builder
        )
        self.assertIn('(R / "website/donate.html").read_text()', builder)
        self.assertIn('<script src="donate.js" defer></script>', builder)
        self.assertIn('page("donate.html", "Donate", home_body)', builder)
        self.assertIn('"playground.html",\n    "Playground",', builder)
        self.assertIn('scene_markup.replace("{{PLAYGROUND_DETAILS}}", "")', builder)

    def test_component_inventory_is_rendered_on_docs_page(self):
        builder = (SITE / "build.py").read_text()
        self.assertIn('"components.html",\n    "Project components"', builder)
        home_page = builder.split("home_body =", 1)[1].split('page("index.html",', 1)[0]
        self.assertNotIn("website/components.html", home_page)
        inventory = (SITE / "components.html").read_text()
        self.assertEqual(len(re.findall(r'<details class="component', inventory)), 10)
        self.assertIn('href="playground.html"', inventory)

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

    def test_roadmap_hides_closed_and_completed_issues(self):
        builder = (SITE / "build.py").read_text()
        self.assertIn('issue.get("state", "open") == "open"', builder)
        self.assertIn('issue.get("stage", "ready") != "done"', builder)
        self.assertIn("for i in roadmap_issues", builder)

    def test_projected_nodes_stay_inside_scene_vertical_bounds(self):
        scene = (SITE / "scene.js").read_text()
        self.assertIn(
            "const halfY = button.getBoundingClientRect().height / 2 + 8;", scene
        )
        self.assertIn("const centerY = dy + (p[1] + offset) * scale;", scene)
        self.assertIn("Math.max(halfY, Math.min(rect.height - halfY, centerY))", scene)


if __name__ == "__main__":
    unittest.main()
