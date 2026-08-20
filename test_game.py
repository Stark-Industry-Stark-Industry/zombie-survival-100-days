import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import game
from content import (
    COMPANIONS, DIFFICULTIES, EASTER_EGGS, JOBS, MARKET_NAMES, SHELTERS,
    WEAPONS, ZOMBIE_TYPES,
)


def sample_state(shelter="社区学校"):
    state = game.State(
        shelter=shelter, job="搜救队员", difficulty="标准",
        story_id="cold_chain",
        skills={k: 0 for k in ["搜刮", "战斗", "射击", "医疗", "建造",
                               "种植", "谈判", "守卫", "侦察", "研究"]},
    )
    state.skills.update(JOBS["搜救队员"]["skills"])
    return state


class FullGameTests(unittest.TestCase):
    def test_easter_egg_catalog_is_large_and_unique(self):
        self.assertGreaterEqual(len(EASTER_EGGS), 50)
        self.assertEqual(len(EASTER_EGGS), len({x["id"] for x in EASTER_EGGS}))
        self.assertGreaterEqual(len({x["source"] for x in EASTER_EGGS}), 10)

    def test_collected_egg_is_not_selected_again(self):
        state = sample_state()
        saved = {"version": 1, "found": [EASTER_EGGS[0]["id"]]}
        with patch.object(game, "load_collection",
                          side_effect=lambda: {"version": 1, "found": list(saved["found"])}), \
             patch.object(game, "save_collection",
                          side_effect=lambda value: saved.update(value)):
            game.maybe_easter_egg(
                state, random.Random(2), EASTER_EGGS[0]["source"], True, 1.0
            )
        self.assertEqual(len(saved["found"]), 2)
        self.assertNotEqual(saved["found"][0], saved["found"][1])

    def test_content_catalogs(self):
        self.assertEqual(len(DIFFICULTIES), 3)
        self.assertGreaterEqual(len(JOBS), 6)
        self.assertGreaterEqual(len(SHELTERS), 6)
        self.assertGreaterEqual(len(COMPANIONS), 10)

    def test_population_and_food_include_companions(self):
        state = sample_state()
        game.recruit(state, "林乔")
        game.recruit(state, "周野")
        before = state.food
        game.morning(state)
        self.assertEqual(state.population, 3)
        self.assertEqual(before - state.food, 3)

    def test_companion_skill_is_used(self):
        state = sample_state()
        state.survivors["程墨"] = game.survivor_from_catalog("程墨")
        self.assertEqual(game.best_skill(state, [state.survivors["程墨"]], "侦察"), 3)

    def test_recruit_respects_capacity(self):
        state = sample_state("山中别墅")
        for name in list(COMPANIONS)[:7]:
            game.recruit(state, name)
        self.assertEqual(state.population, SHELTERS["山中别墅"]["capacity"])
        result = game.recruit(state, list(COMPANIONS)[8])
        self.assertIn("容量上限", result)

    def test_loot_respects_carry_capacity(self):
        state = sample_state()
        loot = game.random_loot(state, [], random.Random(1), "商业")
        self.assertLessEqual(sum(loot.values()), 7)

    def test_save_round_trip(self):
        state = sample_state()
        game.recruit(state, "林乔")
        state.tag("trace_1")
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(game, "SAVE_DIR", Path(tmp)):
                game.save(state, "test")
                loaded = game.load("test")
        self.assertEqual(loaded.shelter, state.shelter)
        self.assertTrue(loaded.has("trace_1"))
        self.assertIn("林乔", loaded.survivors)

    def test_combat_auto_finishes(self):
        state = sample_state()
        state.ammo = 20
        result = game.auto_combat(state, [], random.Random(3), 2, 2)
        self.assertIsInstance(result, bool)
        self.assertGreaterEqual(state.hp, 0)

    def test_story_beats_are_ordered_and_reachable(self):
        state = sample_state()
        state.day = 90
        state.intel = 99
        rng = random.Random(2)
        for beat in game.STORY_BEATS:
            game.story_event(state, rng, random.Random(2))
            self.assertTrue(state.has(beat["id"]))

    def test_all_milestones_resolve(self):
        state = sample_state()
        state.food = state.materials = state.medicine = state.ammo = state.trade_goods = 50
        for day in [10, 20, 30, 40, 50, 60, 70, 80, 90, 95]:
            state.day = day
            game.milestone_event(state, random.Random(day), random.Random(day))
            self.assertTrue(state.has(f"milestone:{day}"))

    def test_healing_changes_actual_hp_and_charges_once(self):
        state = sample_state()
        state.hp = 2
        state.medicine = 3
        with patch.object(game, "choose", return_value=0):
            game.base_action(state, random.Random(1))
        self.assertEqual(state.hp, 3)
        self.assertEqual(state.medicine, 2)

    def test_full_hp_healing_does_not_consume_medicine(self):
        state = sample_state()
        state.hp = state.max_hp
        state.medicine = 3
        with patch.object(game, "choose", return_value=0):
            game.base_action(state, random.Random(1))
        self.assertEqual(state.hp, state.max_hp)
        self.assertEqual(state.medicine, 3)

    def test_custom_team_input_13(self):
        state = sample_state()
        for name in ["林乔", "周野", "程墨"]:
            state.survivors[name] = game.survivor_from_catalog(name)
        with patch("builtins.input", return_value="13"):
            team = game.select_team(state, None)
        self.assertEqual([p.name for p in team], ["林乔", "程墨"])

    def test_kicking_companion_has_strong_cost(self):
        state = sample_state()
        game.recruit(state, "林乔")
        before_morale = state.morale
        with patch.object(game, "choose", side_effect=[5, 0, 2, 0]):
            game.base_action(state, random.Random(1))
        self.assertNotIn("林乔", state.survivors)
        self.assertLessEqual(state.morale, before_morale - 10)

    def test_unaffordable_market_trade_cannot_create_resources(self):
        state = sample_state()
        state.discovered_markets = ["桥洞赌市"]
        state.trade_goods = 0
        before = (state.trade_goods, state.food, state.materials)
        with patch.object(game, "choose", side_effect=[0, 3]):
            game.market_visit(state, random.Random(1))
        self.assertEqual((state.trade_goods, state.food, state.materials), before)

    def test_weapon_and_zombie_catalogs(self):
        self.assertGreaterEqual(len(MARKET_NAMES), 6)
        self.assertGreaterEqual(len(WEAPONS), 8)
        self.assertGreaterEqual(len(ZOMBIE_TYPES), 5)
        self.assertGreater(WEAPONS["手枪"]["damage"], WEAPONS["撬棍"]["damage"])
        self.assertGreater(WEAPONS["猎枪"]["damage"], WEAPONS["消防斧"]["damage"])


if __name__ == "__main__":
    unittest.main()
