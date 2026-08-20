from __future__ import annotations

import argparse
import json
import os
import random
import textwrap
from dataclasses import asdict, dataclass, field
from pathlib import Path

from content import (
    ARMOR, COMPANIONS, DIFFICULTIES, EASTER_EGGS, EXPLORATION_ROUTES, FACTIONS, GEAR, JOBS,
    MARKET_NAMES, PETS, SCENE_TEXT, SHELTERS, SITE_NAMES, STORY_BEATS, STORYLINES, WEAPONS, ZOMBIE_TYPES,
)

VERSION = 3
ROOT = Path(__file__).resolve().parent
SAVE_DIR = ROOT / "saves"
COLLECTION_PATH = SAVE_DIR / "collection.json"
WIDTH = 78
COLOR = True


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


def paint(text: str, code: str) -> str:
    return f"{code}{text}{C.RESET}" if COLOR else text


@dataclass
class Survivor:
    name: str
    role: str
    skills: dict[str, int]
    hp: int = 4
    max_hp: int = 4
    trust: int = 0
    tired: int = 0
    alive: bool = True
    unique: str = ""
    mood: int = 55
    job: str = "待命"
    personality: str = ""
    notes: list[str] = field(default_factory=list)


@dataclass
class State:
    version: int = VERSION
    day: int = 1
    difficulty: str = "标准"
    job: str = ""
    shelter: str = ""
    skills: dict[str, int] = field(default_factory=dict)
    hp: int = 5
    max_hp: int = 5
    tired: int = 0
    food: int = 18
    medicine: int = 4
    ammo: int = 8
    materials: int = 8
    trade_goods: int = 3
    seeds: int = 0
    defense: int = 8
    threat: int = 8
    morale: int = 55
    farm: int = 0
    infirmary: int = 0
    workshop: int = 0
    intel: int = 0
    sample: int = 0
    weapons: dict[str, int] = field(default_factory=lambda: {"撬棍": 1})
    equipped: str = "撬棍"
    armor: str = "便服"
    armors: list[str] = field(default_factory=lambda: ["便服"])
    gear: list[str] = field(default_factory=list)
    pets: dict[str, dict] = field(default_factory=dict)
    faction_relations: dict[str, int] = field(default_factory=lambda: {name: 0 for name in FACTIONS})
    story_id: str = ""
    story_progress: int = 0
    survivors: dict[str, Survivor] = field(default_factory=dict)
    discovered_markets: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    clues: list[str] = field(default_factory=list)
    visited: list[str] = field(default_factory=list)
    journal: list[str] = field(default_factory=list)
    seed: int = 0
    ended: bool = False
    victory: bool = False

    def has(self, tag: str) -> bool:
        return tag in self.tags

    def tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    @property
    def living(self) -> list[Survivor]:
        return [x for x in self.survivors.values() if x.alive]

    @property
    def population(self) -> int:
        return 1 + len(self.living)


def wrap(text: str) -> str:
    return "\n".join(textwrap.fill(x, WIDTH, replace_whitespace=False)
                     if x.strip() else "" for x in text.splitlines())


def clear() -> None:
    if os.environ.get("NO_CLEAR") != "1":
        os.system("cls" if os.name == "nt" else "clear")


def bar(value: int, maximum: int, width: int = 12) -> str:
    filled = round(width * max(0, value) / max(1, maximum))
    return "[" + "#" * filled + "." * (width - filled) + "]"


def choose(prompt: str, options: list[str], auto: random.Random | None = None) -> int:
    if prompt:
        print(wrap(prompt))
    print()
    for i, option in enumerate(options, 1):
        print(wrap(f"{paint(f'[{i}]', C.CYAN)} {option}"))
    if auto:
        pick = auto.randrange(len(options))
        print(f"\n> {pick + 1}")
        return pick
    while True:
        raw = input("\n> ").strip().lower()
        digits = "".join(x for x in raw if x.isdigit())
        if digits and 1 <= int(digits) <= len(options):
            return int(digits) - 1
        if raw in {"status", "状态"}:
            print("请完成当前选择；状态栏会在每天开始时显示。")
        elif raw in {"quit", "q", "退出"}:
            raise KeyboardInterrupt
        else:
            print(f"请输入 1-{len(options)}。")


def delta(state: State, **changes: int) -> str:
    labels = {
        "food": "食物", "medicine": "药品", "ammo": "弹药",
        "materials": "材料", "trade_goods": "交易品", "seeds": "种子",
        "defense": "防御", "threat": "威胁", "morale": "士气",
        "intel": "调查线索", "sample": "样本", "hp": "生命",
    }
    limits = {
        "food": (0, 999), "medicine": (0, 99), "ammo": (0, 999),
        "materials": (0, 999), "trade_goods": (0, 99), "seeds": (0, 99),
        "defense": (0, 100), "threat": (0, 100), "morale": (0, 100),
        "intel": (0, 99), "sample": (0, 20), "hp": (0, state.max_hp),
    }
    shown = []
    for key, amount in changes.items():
        old = getattr(state, key)
        low, high = limits[key]
        new = max(low, min(high, old + amount))
        setattr(state, key, new)
        actual = new - old
        if actual:
            text = f"[{labels[key]} {'+' if actual > 0 else ''}{actual}]"
            shown.append(paint(text, C.GREEN if actual > 0 else C.RED))
    return " ".join(shown)


def load_collection() -> dict:
    """收藏是安装目录级元进度，不属于任何单局存档。"""
    if not COLLECTION_PATH.exists():
        return {"version": 1, "found": []}
    try:
        raw = json.loads(COLLECTION_PATH.read_text(encoding="utf-8"))
        found = [x for x in raw.get("found", []) if any(e["id"] == x for e in EASTER_EGGS)]
        return {"version": 1, "found": found}
    except (OSError, ValueError, TypeError):
        return {"version": 1, "found": []}


def save_collection(collection: dict) -> None:
    SAVE_DIR.mkdir(exist_ok=True)
    tmp = COLLECTION_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(COLLECTION_PATH)


def show_collection() -> None:
    collection = load_collection()
    found_ids = set(collection["found"])
    print("\n" + paint("【彩蛋收藏库】", C.BOLD))
    print(f"已收集 {len(found_ids)}/{len(EASTER_EGGS)}；彩蛋一经收集，后续周目不再重复出现。")
    groups = {}
    for egg in EASTER_EGGS:
        groups.setdefault(egg["source"], []).append(egg)
    source_names = {
        "weapon": "武器", "armor": "防具", "gear": "装备", "market": "集市",
        "zombie": "僵尸", "pet": "宠物", "explore": "探索", "survivor": "人物",
        "base": "基地", "story": "剧情", "night": "夜晚",
    }
    for source, eggs in groups.items():
        collected = [e for e in eggs if e["id"] in found_ids]
        print(f"\n{source_names.get(source, source)} {len(collected)}/{len(eggs)}")
        for egg in eggs:
            if egg["id"] in found_ids:
                print(wrap(f"  ◆ [{egg['rarity']}] {egg['name']}：{egg['text']}"))
            else:
                print("  ◇ ？？？")


def maybe_easter_egg(state: State, rng: random.Random, source: str,
                     persistent: bool = True, chance: float = 0.035) -> bool:
    """极低概率抽取未收藏彩蛋；自动平衡模拟不会污染玩家收藏。"""
    if rng.random() >= chance:
        return False
    collection = load_collection() if persistent else {"found": []}
    found = set(collection["found"])
    eligible = [e for e in EASTER_EGGS if e["source"] == source and e["id"] not in found]
    if not eligible:
        return False
    egg = rng.choice(eligible)
    if persistent:
        collection["found"].append(egg["id"])
        save_collection(collection)
    reward_text = delta(state, **egg.get("reward", {}))
    print("\n" + paint("★ 发现小概率彩蛋！", C.YELLOW))
    print(wrap(f"【{egg['rarity']}收藏：{egg['name']}】{egg['text']}"))
    if reward_text:
        print(reward_text)
    progress = len(collection["found"]) if persistent else 1
    print(f"[已收入收藏库：{progress}/{len(EASTER_EGGS)}；后续新游戏不再重复出现此彩蛋]")
    return True


def survivor_from_catalog(name: str) -> Survivor:
    raw = COMPANIONS[name]
    personalities = ["利他", "谨慎", "强硬", "幽默", "多疑", "理想主义"]
    return Survivor(name=name, role=raw["role"], skills=dict(raw["skills"]),
                    unique=raw["unique"], notes=[raw["intro"]],
                    personality=personalities[sum(ord(c) for c in name) % len(personalities)])


def recruit(state: State, name: str) -> str:
    if name in state.survivors:
        return f"{name}已经在基地。"
    if state.population >= SHELTERS[state.shelter]["capacity"]:
        return f"基地已达容量上限，{name}无法留下。"
    state.survivors[name] = survivor_from_catalog(name)
    state.tag(f"recruited:{name}")
    if name == "程墨":
        state.tag("radio_route")
    if name == "段黎":
        state.tag("advanced_building")
    if name == "白术":
        state.tag("sample_analysis")
    return f"{name}加入基地。\n[{name}｜{state.survivors[name].role}｜{state.survivors[name].unique}]"


def new_game(auto: random.Random | None = None) -> State:
    clear()
    print("《百日之后》\n")
    print(wrap(
        "一种来源不明的急性感染在十天内摧毁了城市秩序。通信中断，救援广播相互矛盾，"
        "城区只剩零散幸存者和不断扩大的尸群。没有列车，也没有保证会来的军队。"
    ))
    print()
    if not auto:
        collection = load_collection()
        print(paint(f"跨周目彩蛋收藏：{len(collection['found'])}/{len(EASTER_EGGS)}（已收藏内容不会再次出现）", C.YELLOW))
        print()
    print(wrap(
        "你的目标很朴素：建立基地，寻找同伴，活过一百天。"
        "但城市里散落的记录暗示，这场灾难并非完全没有答案。"
        "是否追查、相信谁、最终怎样处理发现，由你决定。"
    ))
    difficulty_names = list(DIFFICULTIES)
    d = choose("选择难度：", [
        f"{name}｜{DIFFICULTIES[name]['desc']}" for name in difficulty_names
    ], auto)
    job_names = list(JOBS)
    j = choose("选择灾难前的职业。所有技能都会直接参与玩法：", [
        f"{name}｜{JOBS[name]['desc']}" for name in job_names
    ], auto)
    shelter_names = list(SHELTERS)
    s = choose("选择最初的基地：", [
        f"{name}｜{SHELTERS[name]['desc']} 特性：{SHELTERS[name]['special']}"
        for name in shelter_names
    ], auto)
    difficulty, job, shelter = difficulty_names[d], job_names[j], shelter_names[s]
    spec = SHELTERS[shelter]
    bonus = DIFFICULTIES[difficulty]["start_bonus"]
    state = State(
        difficulty=difficulty, job=job, shelter=shelter,
        skills={k: 0 for k in ["搜刮", "战斗", "射击", "医疗", "建造", "种植", "谈判", "守卫", "侦察", "研究"]},
        food=max(8, spec["food"] + bonus), medicine=spec.get("medicine", 4),
        materials=max(3, spec["materials"] + bonus), defense=spec["defense"],
        farm=1 if shelter == "郊外农场" else 0,
        seed=auto.randrange(1_000_000) if auto else random.randrange(1_000_000),
        story_id=(auto.choice(list(STORYLINES)) if auto else random.choice(list(STORYLINES))),
    )
    state.skills.update(JOBS[job]["skills"])
    # A single starting companion keeps the opening readable.
    starter = "林乔" if job != "急诊护士" else "周野"
    state.survivors[starter] = survivor_from_catalog(starter)
    state.journal.append(f"第1天：我和{starter}在{state.shelter}建立基地。")
    print()
    print(wrap(
        f"你和{starter}在逃离居民安置点时互相救过一次。你只知道"
        f"{COMPANIONS[starter]['intro']} 现在基地只有你们两人。"
    ))
    print("\n" + paint("【资源与数值说明】", C.BOLD))
    tutorials = [
        "食物：人和宠物每天消耗；归零会降低心情、士气并增加疲劳。",
        "药品：治疗玩家、队友和宠物；样本分析与疾病事件也会消耗。",
        "弹药：枪械、弩、链锯和投掷武器的通用战斗消耗。",
        "材料：加固基地、升级设施、农田、制作与派系事件使用。",
        "交易品：各集市的通用支付单位；不同市场库存完全不同。",
        "种子：升级农田，换取长期稳定食物。",
        "防御：抵消夜间尸群与人类袭击；威胁越高，袭击越频繁。",
        "士气：基地整体稳定；队友另有个人心情与信任。",
        "调查线索/样本：推进本局随机主线；需要对应角色、岗位或设施。",
        "防具/装备/宠物：分别提供减伤、探索工具和可指挥的协同能力。",
    ]
    for item in tutorials:
        print("  · " + item)
    print(wrap(f"本局故事开端：{STORYLINES[state.story_id]['hook']} 这只是第一条异常记录，后续伏笔会在探索、对话和派系事件中逐步出现。"))
    if not auto:
        input("\n按 Enter 开始第一天……")
    return state


def show_status(state: State) -> None:
    clear()
    print(paint("╔" + "═" * (WIDTH - 2) + "╗", C.BLUE))
    title = f"  DAY {state.day:03d}/100  ·  {state.shelter}  ·  {state.difficulty}  "
    print(paint("║", C.BLUE) + paint(title.ljust(WIDTH - 2), C.BOLD) + paint("║", C.BLUE))
    print(paint("╠" + "═" * (WIDTH - 2) + "╣", C.BLUE))
    print(f"  你｜{state.job}  HP {state.hp}/{state.max_hp} {bar(state.hp, state.max_hp)}  "
          f"疲劳 {state.tired}/4  装备 {state.equipped}")
    player_skills = "、".join(f"{k}{v}" for k, v in state.skills.items() if v)
    print(f"  技能｜{player_skills or '无专长'}")
    print(f"  食物 {state.food:>3}（约 {state.food // max(1, state.population):>2} 天）"
          f"  药品 {state.medicine:>2}  弹药 {state.ammo:>3}  材料 {state.materials:>3}"
          f"  交易品 {state.trade_goods:>2}")
    threat_text = paint(str(state.threat), C.RED if state.threat >= 60 else C.YELLOW)
    print(f"  防御 {state.defense:>3}/100  威胁 {threat_text}/100  士气 {state.morale:>3}/100"
          f"  农田 {state.farm}  人口 {state.population}/{SHELTERS[state.shelter]['capacity']}")
    print(f"  调查 {'?' if state.intel < 2 else state.intel}  集市 {len(state.discovered_markets)}"
          f"  武器 {', '.join(state.weapons)}  防具 {state.armor}"
          + (f"  宠物：{', '.join(state.pets)}" if state.pets else ""))
    print(f"  彩蛋收藏 {len(load_collection()['found'])}/{len(EASTER_EGGS)}（主菜单可查看）")
    print(paint("╠" + "─" * (WIDTH - 2) + "╣", C.BLUE))
    print(paint("  基地人员", C.BOLD))
    for s in state.living:
        skills = "、".join(f"{k}{v}" for k, v in s.skills.items())
        print(f"   {s.name:<4} {s.role:<8} HP {s.hp}/{s.max_hp}  心情 {s.mood:>3}  "
              f"信任 {s.trust:+d}  岗位 {s.job}  {skills}")
    print(paint("╚" + "═" * (WIDTH - 2) + "╝", C.BLUE))


def best_skill(state: State, team: list[Survivor], skill: str) -> int:
    values = [state.skills.get(skill, 0)] + [x.skills.get(skill, 0) for x in team]
    return max(values)


def select_team(state: State, auto: random.Random | None) -> list[Survivor]:
    available = [x for x in state.living if x.hp > 1 and x.tired < 4]
    if not available:
        return []
    if auto:
        count = auto.randint(0, min(3, len(available)))
        return auto.sample(available, count)
    print("\n" + paint("【探索队编成】", C.BOLD))
    print("输入队友编号组合，例如输入 13 表示带第 1 和第 3 人；输入 0 独自外出。最多带 3 人。")
    for i, person in enumerate(available, 1):
        skills = "、".join(f"{k}{v}" for k, v in person.skills.items())
        print(wrap(f"[{i}] {person.name}｜{person.role}｜{skills}｜{person.unique}"))
    while True:
        raw = input("\n队伍 > ").strip()
        if raw == "0":
            return []
        indexes = []
        valid = True
        if raw.isdigit() and int(raw) >= 10 and int(raw) <= len(available):
            tokens = [raw]
        elif any(sep in raw for sep in [",", "，", " "]):
            tokens = raw.replace("，", ",").replace(" ", ",").split(",")
        else:
            tokens = list(raw)
        for token in tokens:
            if not token.isdigit() or int(token) == 0:
                valid = False
                break
            idx = int(token) - 1
            if idx < 0 or idx >= len(available) or idx in indexes:
                valid = False
                break
            indexes.append(idx)
        if valid and 1 <= len(indexes) <= 3:
            return [available[i] for i in indexes]
        print(f"请输入 1-{len(available)} 的不重复编号，最多 3 人；编号 10 以上请用逗号分隔。")


def enemy_group(state: State, rng: random.Random, risk: int) -> list[dict]:
    mult = DIFFICULTIES[state.difficulty]["enemy"]
    count = max(1, round((rng.randint(1, 2 + risk) + state.day // 32) * mult))
    available = ["游荡者"]
    if state.day >= 15:
        available.append("奔跑者")
    if state.day >= 30:
        available.append("尖啸者")
    if state.day >= 45:
        available.append("防暴感染者")
    if state.day >= 60:
        available.append("肿胀者")
    if state.day >= 35:
        available += ["爬行者", "消防员感染者"]
    if state.day >= 55:
        available += ["黏液者", "猎犬感染体", "菌毯宿主"]
    if state.day >= 70:
        available += ["寄生群", "镜面感染者"]
    if state.day >= 85:
        available += ["铁皮巨汉", "夜行者"]
    if state.day >= 95 and risk >= 4:
        available.append("巢母")
    weights = ([50, 18, 10, 10, 7] + [10] * max(0, len(available) - 5))[:len(available)]
    enemies = []
    for _ in range(count):
        kind = rng.choices(available, weights=weights, k=1)[0]
        data = ZOMBIE_TYPES[kind]
        enemies.append({"kind": kind, "hp": data["hp"], "max_hp": data["hp"]})
    return enemies


def auto_combat(state: State, team: list[Survivor], rng: random.Random,
                count: int, zombie_hp: int) -> bool:
    arsenal = max(WEAPONS[name]["damage"] for name in state.weapons)
    power = state.skills["战斗"] + state.skills["射击"] + arsenal // 2 + sum(
        p.skills.get("战斗", 0) + p.skills.get("射击", 0) for p in team
    )
    ammo_used = min(state.ammo, max(0, count - power // 3))
    state.ammo -= ammo_used
    chance = max(20, min(95, 58 + power * 6 + ammo_used * 8 - count * zombie_hp * 3))
    if rng.randint(1, 100) <= chance:
        if rng.random() < 0.18 and team:
            rng.choice(team).hp -= 1
        return True
    state.hp -= 1
    if team and rng.random() < 0.55:
        rng.choice(team).hp -= 1
    return False


def combat(state: State, team: list[Survivor], rng: random.Random,
           risk: int, auto: random.Random | None = None) -> bool:
    enemies = enemy_group(state, rng, risk)
    if auto:
        avg_hp = max(1, round(sum(x["hp"] for x in enemies) / len(enemies)))
        return auto_combat(state, team, rng, len(enemies), avg_hp)
    stamina = 4
    print("\n" + paint("╔═【遭遇战】" + "═" * 63 + "╗", C.RED))
    print("不同武器有独立伤害、命中、弹药、噪声和特殊效果。枪械伤害显著高于近战。")
    while enemies and state.hp > 0:
        ally_power = sum(x.skills.get("战斗", 0) for x in team if x.alive)
        print(f"\n你 HP {state.hp}/{state.max_hp}｜体力 {stamina}/4｜弹药 {state.ammo}｜装备 {state.equipped}")
        for i, enemy in enumerate(enemies, 1):
            spec = ZOMBIE_TYPES[enemy["kind"]]
            print(f"  ({i}) {enemy['kind']} HP {enemy['hp']}/{enemy['max_hp']}｜{spec['trait']}")
        weapon = WEAPONS[state.equipped]
        can_attack = (stamina >= weapon["stamina"] and state.ammo >= weapon["ammo"])
        attack_status = "" if can_attack else "【不可用：体力或弹药不足】"
        actions = [
            f"使用{state.equipped}攻击｜伤害 {weapon['damage']}，命中 {weapon['accuracy']}%，"
            f"耗弹 {weapon['ammo']}，噪声 {weapon['noise']} {attack_status}",
            "切换武器｜查看持有武器及特性，本回合不受攻击",
            "防守后退｜恢复 2 体力，降低本回合受伤率",
        ]
        if state.pets:
            actions.append("指挥宠物｜攻击、牵制或警戒；宠物可能受伤")
        actions.append("尝试逃跑｜成功率受侦察、宠物和敌人数影响")
        pick = choose("选择战斗动作：", actions, None)
        guarded = False
        skip_enemy_turn = False
        if pick == 0:
            if not can_attack:
                print("当前武器无法使用，请切换武器或防守。")
                continue
            target_options = [f"{e['kind']} HP {e['hp']}" for e in enemies]
            target_idx = choose("选择目标：", target_options, None) if len(enemies) > 1 else 0
            target = enemies[target_idx]
            zspec = ZOMBIE_TYPES[target["kind"]]
            skill = state.skills["射击"] if weapon["kind"] == "枪械" else state.skills["战斗"]
            accuracy = min(97, weapon["accuracy"] + skill * 6 - zspec["evasion"])
            stamina -= weapon["stamina"]
            state.ammo -= weapon["ammo"]
            state.threat = min(100, state.threat + weapon["noise"])
            if rng.randint(1, 100) <= accuracy:
                damage = weapon["damage"] + (skill if weapon["kind"] == "枪械" else skill // 2)
                armor = zspec["armor"]
                if state.equipped in {"消防斧", "猎枪"}:
                    armor = 0
                damage = max(1, damage - armor)
                affected = [target]
                if state.equipped in {"霰弹枪", "冲锋枪"}:
                    affected = enemies[target_idx:target_idx + 3]
                killed_bloater_melee = False
                for victim in affected:
                    victim["hp"] -= damage
                    if victim["kind"] == "肿胀者" and victim["hp"] <= 0 and weapon["kind"] == "近战":
                        killed_bloater_melee = True
                print(f"{state.equipped}命中，造成 {damage} 点伤害"
                      + (f"，波及 {len(affected)} 个目标" if len(affected) > 1 else "") + "。")
                if killed_bloater_melee and rng.random() < 0.45:
                    state.hp -= 1
                    print("肿胀者近距离破裂，你受到喷溅伤害。[生命 -1]")
            else:
                print(f"{state.equipped}攻击落空。")
            if state.equipped == "弩" and weapon["ammo"] and rng.random() < 0.5:
                state.ammo += 1
                print("你回收了一支弩箭。[弹药 +1]")
        elif pick == 1:
            names = list(state.weapons)
            wi = choose("选择装备：", [
                f"{name}｜{WEAPONS[name]['kind']}｜伤害 {WEAPONS[name]['damage']}｜"
                f"命中 {WEAPONS[name]['accuracy']}%｜{WEAPONS[name]['trait']}"
                for name in names
            ], None)
            state.equipped = names[wi]
            print(f"已装备{state.equipped}。")
            skip_enemy_turn = True
        elif pick == 2:
            guarded = True
            stamina = min(4, stamina + 2)
            print("你们收紧阵形。")
        elif state.pets and pick == 3:
            pet_names = list(state.pets)
            pi = choose("选择宠物：", [
                f"{n}｜{state.pets[n]['species']}｜HP {state.pets[n]['hp']}｜技能 {state.pets[n]['skill']}"
                for n in pet_names
            ], None)
            pet_name = pet_names[pi]
            pet = state.pets[pet_name]
            cmd = choose("下达指令：", [
                "攻击｜造成宠物攻击伤害，可能受反击",
                "牵制｜本回合敌方命中率降低",
                "警戒退路｜本回合逃跑率提高，但不攻击",
            ], None)
            if cmd == 0 and enemies:
                enemies[0]["hp"] -= pet.get("attack", 1)
                print(f"{pet_name}扑向{enemies[0]['kind']}，造成 {pet.get('attack', 1)} 点伤害。")
                if rng.random() < 0.18:
                    pet["hp"] -= 1
                    print(f"{pet_name}受伤。[宠物生命 -1]")
            elif cmd == 1:
                guarded = True
                print(f"{pet_name}不断骚扰敌人，敌方攻击被打乱。")
            else:
                state.tag("pet_escape_ready")
                print(f"{pet_name}守住退路；下一次逃跑获得额外加成。")
        else:
            scout = best_skill(state, team, "侦察")
            pet_scout = max([p.get("scout", 0) for p in state.pets.values()] or [0])
            chance = max(20, min(95, 55 + scout * 8 + pet_scout * 4
                                 + (18 if state.has("pet_escape_ready") else 0) - len(enemies) * 6))
            state.tags = [t for t in state.tags if t != "pet_escape_ready"]
            if rng.randint(1, 100) <= chance:
                print("你们甩开尸群，放弃了尚未带走的战利品。")
                return False
            print("退路被堵住了！")
        enemies = [x for x in enemies if x["hp"] > 0]
        if not enemies:
            break
        if skip_enemy_turn:
            continue
        # Companions contribute every round; this is where their combat skills matter.
        if ally_power and enemies:
            ally_damage = max(1, ally_power // 2)
            enemies[0]["hp"] -= ally_damage
            print(f"队友协同造成 {ally_damage} 点伤害。")
            enemies = [x for x in enemies if x["hp"] > 0]
            if not enemies:
                break
        screamers = sum(1 for x in enemies if x["kind"] == "尖啸者")
        if screamers and rng.random() < 0.18 * screamers:
            enemies.append({"kind": "游荡者", "hp": 3, "max_hp": 3})
            print("尖啸声引来一个新的游荡者！")
        armor_spec = ARMOR[state.armor]
        hit_chance = 40 + len(enemies) * 5 - (25 if guarded else 0) - ally_power * 2 - armor_spec["evasion"]
        if rng.randint(1, 100) <= hit_chance:
            target_pool = ["player"] + [p.name for p in team if p.alive]
            target = rng.choice(target_pool)
            damage = max(ZOMBIE_TYPES[x["kind"]]["damage"] for x in enemies)
            if target == "player":
                reduced = max(0, damage - armor_spec["armor"])
                state.hp -= reduced
                print(f"感染者击中了你。{state.armor}吸收 {damage - reduced} 点。[生命 -{reduced}]")
            else:
                state.survivors[target].hp -= damage
                print(f"{target}受伤了。[生命 -{damage}]")
        stamina = min(4, stamina + 1)
        for name in list(state.pets):
            if state.pets[name]["hp"] <= 0:
                print(f"{name}在战斗中死亡。")
                del state.pets[name]
                state.morale = max(0, state.morale - 10)
    print(paint("╚" + "═" * (WIDTH - 2) + "╝", C.RED))
    return not enemies


def cleanup_casualties(state: State) -> list[str]:
    messages = []
    for person in state.survivors.values():
        if person.alive and person.hp <= 0:
            person.alive = False
            messages.append(f"{person.name}没能从伤势中活下来。")
            state.morale = max(0, state.morale - 12)
    if state.hp <= 0:
        state.ended = True
        messages.append("你死了。基地的故事由留下的人继续，但你的游戏到此结束。")
    return messages


def random_loot(state: State, team: list[Survivor], rng: random.Random,
                profile: str) -> dict[str, int]:
    scale = DIFFICULTIES[state.difficulty]["loot"]
    scav = best_skill(state, team, "搜刮")
    carry = 5 + scav + (2 if "周野" in [x.name for x in team] else 0)
    if state.shelter == "河边物流仓":
        carry += 1
    tables = {
        "商业": {"food": rng.randint(2, 7), "trade_goods": rng.randint(0, 3)},
        "医疗": {"medicine": rng.randint(1, 5), "food": rng.randint(0, 2)},
        "住宅": {"food": rng.randint(1, 5), "materials": rng.randint(1, 4)},
        "工坊": {"materials": rng.randint(3, 8), "ammo": rng.randint(0, 3)},
        "隐藏": {"trade_goods": rng.randint(1, 4), "ammo": rng.randint(0, 5)},
        "自然": {"food": rng.randint(1, 5), "seeds": rng.randint(0, 2)},
        "农场": {"food": rng.randint(3, 8), "seeds": rng.randint(1, 3)},
        "废车": {"materials": rng.randint(2, 7), "food": rng.randint(0, 3)},
        "线索": {"intel": rng.randint(1, 3), "materials": rng.randint(0, 2)},
    }
    raw = tables.get(profile, {"food": 2, "materials": 2})
    output, used = {}, 0
    for key, amount in raw.items():
        amount = max(0, round(amount * scale))
        take = min(amount, max(0, carry - used))
        if take:
            output[key] = take
            used += take
    return output


def maybe_find_weapon(state: State, rng: random.Random, profile: str) -> str:
    chance = 0.025
    if profile in {"工坊", "隐藏", "废车"}:
        chance = 0.09
    if profile == "线索":
        chance = 0.05
    if rng.random() > chance:
        return ""
    pool = ["消防斧", "手枪", "左轮手枪", "霰弹枪", "猎枪", "冲锋枪", "弩"]
    weights = [24, 24, 13, 13, 8, 5, 13]
    weapon = rng.choices(pool, weights=weights, k=1)[0]
    if weapon not in state.weapons:
        state.weapons[weapon] = 1
        state.equipped = weapon
        return f"你在隐蔽处找到一件可用武器：[新武器：{weapon}] {WEAPONS[weapon]['trait']} 已自动装备。"
    state.trade_goods += 1
    return f"你找到一件重复的{weapon}，拆取零件后整理成交易品。[交易品 +1]"


def maybe_find_equipment(state: State, rng: random.Random, profile: str) -> str:
    if rng.random() > (0.08 if profile in {"工坊", "隐藏", "废车", "医疗"} else 0.025):
        return ""
    if rng.random() < 0.55:
        item = rng.choice(list(ARMOR)[1:])
        if item not in state.armors:
            state.armors.append(item)
            state.armor = item
            return f"[新防具：{item}] {ARMOR[item]['trait']} 已自动穿戴。"
    item = rng.choice(list(GEAR))
    if item not in state.gear:
        state.gear.append(item)
        return f"[新装备：{item}] {GEAR[item]['trait']}"
    state.trade_goods += 1
    return "[重复装备拆件：交易品 +1]"


def can_pay(state: State, cost: dict[str, int]) -> bool:
    return all(getattr(state, key) >= amount for key, amount in cost.items())


def pay(state: State, cost: dict[str, int]) -> str:
    if not can_pay(state, cost):
        return ""
    return delta(state, **{key: -value for key, value in cost.items()})


def faction_conflict(state: State, rng: random.Random,
                     auto: random.Random | None = None) -> bool:
    power = state.skills["战斗"] + state.skills["射击"] + len(state.weapons)
    options = [
        "伪造命令引开守卫｜谈判与管理相关，失败会暴露",
        "夜间潜入打开围栏｜侦察相关，失败会受伤",
        "正面袭击武装守卫｜消耗弹药，战斗能力相关",
        "放弃行动",
    ]
    pick = choose("市场由人类武装守卫控制，不会出现僵尸战斗。选择方案：", options, auto)
    if pick == 3:
        return False
    if pick == 0:
        chance = 35 + state.skills["谈判"] * 12 + sum(p.skills.get("管理", 0) for p in state.living) * 5
    elif pick == 1:
        chance = 40 + state.skills["侦察"] * 12
    else:
        cost = min(6, state.ammo)
        if cost < 3:
            print("弹药不足，无法正面袭击。")
            return False
        state.ammo -= cost
        chance = 35 + power * 6 + cost * 3
    if rng.randint(1, 100) <= min(90, chance):
        return True
    state.hp = max(1, state.hp - 2)
    state.threat = min(100, state.threat + 8)
    state.faction_relations["白塔治安队"] -= 20
    print("行动失败，你在撤退中受伤。[生命 -2] [白塔治安队关系 -20]")
    return False


def market_visit(state: State, rng: random.Random,
                 auto: random.Random | None = None) -> None:
    market = rng.choice(state.discovered_markets)
    bargaining = state.skills["谈判"] + (2 if "马会" in state.survivors and state.survivors["马会"].alive else 0)
    premium = max(0, 2 - bargaining // 2)
    print("\n" + paint(f"╔═【{market}】" + "═" * max(1, 64 - len(market) * 2) + "╗", C.YELLOW))
    print(f"库存：交易品 {state.trade_goods}｜食物 {state.food}｜材料 {state.materials}｜弹药 {state.ammo}")

    if market == "桥洞赌市":
        deals = [
            ("押 1 交易品猜单双｜50% 赢 2，50% 损失赌注", {"trade_goods": 1}, "dice"),
            ("押 2 交易品玩三杯球｜谈判技能可识破作弊", {"trade_goods": 2}, "cups"),
            ("下注地下搏斗｜风险极高，胜者得 5 交易品", {}, "fight"),
            ("离开", {}, "leave"),
        ]
    elif market == "北环犬舍":
        deals = [
            ("购买训练犬“灰耳”｜6 交易品；侦察与逃跑 +12%，每天多耗 1 食物",
             {"trade_goods": 6}, "dog"),
            ("购买犬粮换普通食物｜2 交易品换 4 食物", {"trade_goods": 2}, "food"),
            ("请训犬师训练守卫犬｜3 交易品；基地防御 +6", {"trade_goods": 3}, "dog_guard"),
            ("离开", {}, "leave"),
        ]
    elif market == "河滩夜市":
        deals = [
            (f"购买食物｜{3 + premium} 交易品换 6 食物", {"trade_goods": 3 + premium}, "food6"),
            (f"购买种子｜{2 + premium} 交易品换 2 种子", {"trade_goods": 2 + premium}, "seeds"),
            ("买一条未经证实的消息｜2 交易品，可能获得调查线索", {"trade_goods": 2}, "rumor"),
            ("卖出 5 食物换 1 交易品", {"food": 5}, "sell_food"),
            ("离开", {}, "leave"),
        ]
    elif market == "旧货场军需站":
        weapon = rng.choice(["手枪", "左轮手枪", "霰弹枪", "猎枪", "冲锋枪", "弩"])
        price = 4 + WEAPONS[weapon]["damage"] // 2 + premium
        deals = [
            (f"购买{weapon}｜{price} 交易品｜{WEAPONS[weapon]['trait']}", {"trade_goods": price}, "weapon"),
            (f"购买弹药｜{3 + premium} 交易品换 8 弹药", {"trade_goods": 3 + premium}, "ammo"),
            ("维修并改装当前武器｜4 材料；获得 2 交易品（重复零件）", {"materials": 4}, "salvage"),
            ("离开", {}, "leave"),
        ]
    elif market == "白塔劳工市场":
        deals = [
            ("替一名被强迫劳动者赎身｜8 交易品；可能成为队友，士气大幅上升",
             {"trade_goods": 8}, "free_captive"),
            ("雇用强迫劳工一天｜3 交易品；获得大量材料，基地士气和队友信任重挫",
             {"trade_goods": 3}, "exploit"),
            ("暗中破坏市场并帮助被关押者逃跑｜高风险战斗；成功后永久关闭此地",
             {}, "sabotage"),
            ("离开", {}, "leave"),
        ]
    elif market == "圣心诊所黑市":
        deals = [
            (f"购买药品｜{4 + premium} 交易品换 3 药品", {"trade_goods": 4 + premium}, "medicine"),
            ("接受手术治疗｜3 交易品；完全恢复生命", {"trade_goods": 3}, "surgery"),
            ("请黑市检验员分析样本｜2 交易品 + 1 样本；获得调查进展",
             {"trade_goods": 2, "sample": 1}, "analysis"),
            ("离开", {}, "leave"),
        ]
    elif market == "钟楼铸甲铺":
        armor_item = rng.choice(list(ARMOR)[1:])
        deals = [
            (f"购买{armor_item}｜6 交易品｜{ARMOR[armor_item]['trait']}", {"trade_goods": 6}, "armor"),
            ("定制轻量化护甲｜4 交易品；当前防具闪避惩罚减轻（换成摩托护具）", {"trade_goods": 4}, "light_armor"),
            ("用废金属换甲片｜5 材料换 1 交易品", {"materials": 5}, "sell_metal"),
            ("离开", {}, "leave"),
        ]
    elif market == "十三号奇物摊":
        odd = rng.choice(list(GEAR))
        deals = [
            (f"购买密封纸袋里的“奇物”｜4 交易品；本次是：{odd}", {"trade_goods": 4}, "odd_gear"),
            ("交换一段真正的怪谈｜1 交易品；可能是线索，也可能只是让人睡不着", {"trade_goods": 1}, "weird_story"),
            ("购买罐装笑声｜2 交易品；基地心情上升但威胁增加", {"trade_goods": 2}, "canned_laugh"),
            ("离开", {}, "leave"),
        ]
    elif market == "长波拍卖场":
        auction_weapon = rng.choice(list(WEAPONS)[4:])
        deals = [
            (f"竞拍{auction_weapon}｜7 交易品", {"trade_goods": 7}, "auction_weapon"),
            ("竞拍一份未公开坐标｜4 交易品；获得调查线索并改善广播联盟关系", {"trade_goods": 4}, "auction_coord"),
            ("寄售 8 弹药｜换 2 交易品", {"ammo": 8}, "sell_ammo"),
            ("离开", {}, "leave"),
        ]
    elif market == "地下种子银行":
        deals = [
            ("购买耐旱种子｜3 交易品换 4 种子", {"trade_goods": 3}, "seed_bank"),
            ("购买菌菇培养箱｜5 交易品；农田 +1，但偶尔触发奇怪蘑菇事件", {"trade_goods": 5}, "mushroom"),
            ("交换农业记录｜2 交易品；河湾互助会关系 +5", {"trade_goods": 2}, "farm_record"),
            ("离开", {}, "leave"),
        ]
    elif market == "移动酒馆":
        deals = [
            ("请全队喝一轮｜3 交易品；全员心情 +10，次日疲劳 +1", {"trade_goods": 3}, "round"),
            ("参加末日冷笑话比赛｜免费；获胜得到 2 交易品，失败只会尴尬", {}, "joke"),
            ("在吧台打听失踪者｜2 交易品；可能发现新角色或派系消息", {"trade_goods": 2}, "bar_rumor"),
            ("离开", {}, "leave"),
        ]
    else:  # 宠物驿站
        pet_name = rng.choice(list(PETS))
        deals = [
            (f"领养{pet_name}（{PETS[pet_name]['species']}）｜5 交易品｜技能：{PETS[pet_name]['skill']}",
             {"trade_goods": 5}, "adopt_pet"),
            ("治疗所有宠物｜2 药品", {"medicine": 2}, "heal_pets"),
            ("宠物战术训练｜3 交易品；所有宠物攻击 +1", {"trade_goods": 3}, "train_pets"),
            ("离开", {}, "leave"),
        ]

    while True:
        labels = []
        for text, cost, action in deals:
            locked = ""
            if action == "dog" and len(state.pets) >= 3:
                locked = "【不可用：宠物栏已满】"
            elif action in {"surgery"} and state.hp >= state.max_hp:
                locked = "【不可用：生命已满】"
            elif action == "sabotage" and state.has("labor_market_closed"):
                locked = "【不可用：市场已关闭】"
            elif action in {"heal_pets", "train_pets"} and not state.pets:
                locked = "【不可用：没有宠物】"
            elif action == "adopt_pet" and len(state.pets) >= 3:
                locked = "【不可用：宠物栏已满】"
            elif not can_pay(state, cost):
                locked = "【不可用：物资不足】"
            labels.append(f"{text} {locked}".strip())
        pick = choose("选择交易或事件：", labels, auto)
        text, cost, action = deals[pick]
        locked = (action == "dog" and len(state.pets) >= 3) or (
            action == "surgery" and state.hp >= state.max_hp
        ) or (action == "sabotage" and state.has("labor_market_closed")) or (
            action in {"heal_pets", "train_pets"} and not state.pets
        ) or (action == "adopt_pet" and len(state.pets) >= 3) or not can_pay(state, cost)
        if locked:
            print("该选项当前不可执行，不会扣除任何物资。")
            if auto:
                return
            continue
        if action == "leave":
            return
        paid = pay(state, cost)
        if paid:
            print(paid)
        if action == "dice":
            print(delta(state, trade_goods=2) if rng.random() < 0.5 else "骰子输了，赌注已经归庄家。")
        elif action == "cups":
            chance = min(85, 32 + bargaining * 12)
            print(delta(state, trade_goods=5) if rng.randint(1, 100) <= chance else "你没找到球。马会皱眉说杯底做了手脚。")
        elif action == "fight":
            won = combat(state, [], rng, 4, auto)
            print(delta(state, trade_goods=5, morale=-2) if won else "你被拖出场地，没有获得奖金。")
        elif action == "dog":
            state.pets["灰耳"] = dict(PETS["灰耳"])
            print("灰耳加入基地。它会参与侦察、逃跑和夜间警戒，但每天消耗 1 食物。")
        elif action == "food":
            print(delta(state, food=4))
        elif action == "dog_guard":
            print(delta(state, defense=6))
        elif action == "food6":
            print(delta(state, food=6))
        elif action == "seeds":
            print(delta(state, seeds=2))
        elif action == "rumor":
            if rng.random() < 0.65 + bargaining * 0.04:
                print(delta(state, intel=1))
            else:
                print("消息只是把几段旧广播拼在一起。")
        elif action == "sell_food":
            print(delta(state, trade_goods=1))
        elif action == "weapon":
            if weapon not in state.weapons:
                state.weapons[weapon] = 1
                state.equipped = weapon
                print(f"获得并装备{weapon}。")
            else:
                print(delta(state, trade_goods=2))
                print("这件武器与你已有的重复，拆件后换回部分交易品。")
        elif action == "ammo":
            print(delta(state, ammo=8))
        elif action == "salvage":
            print(delta(state, trade_goods=2))
        elif action == "free_captive":
            name = possible_recruit(state, rng)
            print(delta(state, morale=8))
            if name:
                print(recruit(state, name))
            else:
                print("获救者选择前往别处，并留下一个安全路线标记。")
                state.tag("freed_captive_route")
        elif action == "exploit":
            print(delta(state, materials=12, morale=-18))
            for person in state.living:
                person.trust = max(-5, person.trust - 2)
            state.tag("used_forced_labor")
            print("基地获得材料，但所有队友信任 -2。部分后续合作选项将被关闭。")
        elif action == "sabotage":
            won = faction_conflict(state, rng, auto)
            if won:
                state.tag("labor_market_closed")
                state.morale = min(100, state.morale + 12)
                state.discovered_markets = [m for m in state.discovered_markets if m != market]
                print("被关押的人趁混乱逃离。白塔劳工市场永久关闭。[士气 +12]")
        elif action == "medicine":
            print(delta(state, medicine=3))
        elif action == "surgery":
            restored = state.max_hp - state.hp
            state.hp = state.max_hp
            print(f"手术完成。[生命 +{restored}]")
        elif action == "analysis":
            print(delta(state, intel=2))
            state.tag("black_market_analysis")
        elif action == "armor":
            if armor_item not in state.armors:
                state.armors.append(armor_item)
            state.armor = armor_item
            print(f"已穿戴{armor_item}。")
        elif action == "light_armor":
            if "摩托护具" not in state.armors:
                state.armors.append("摩托护具")
            state.armor = "摩托护具"
        elif action == "sell_metal":
            print(delta(state, trade_goods=1))
        elif action == "odd_gear":
            if odd not in state.gear:
                state.gear.append(odd)
            print(f"获得{odd}：{GEAR[odd]['trait']}")
        elif action == "weird_story":
            if rng.random() < 0.45:
                print(delta(state, intel=1))
            else:
                for p in state.living:
                    p.mood = max(0, p.mood - 2)
                print("故事没有线索价值，但今晚没人愿意单独守厕所。")
        elif action == "canned_laugh":
            print(delta(state, morale=8, threat=3))
        elif action == "auction_weapon":
            state.weapons[auction_weapon] = 1
            state.equipped = auction_weapon
        elif action == "auction_coord":
            print(delta(state, intel=2))
            state.faction_relations["旧城广播联盟"] += 5
        elif action == "sell_ammo":
            print(delta(state, trade_goods=2))
        elif action == "seed_bank":
            print(delta(state, seeds=4))
        elif action == "mushroom":
            state.farm = min(8, state.farm + 1)
            state.tag("mushroom_box")
        elif action == "farm_record":
            state.faction_relations["河湾互助会"] += 5
        elif action == "round":
            for p in state.living:
                p.mood = min(100, p.mood + 10)
                p.tired = min(4, p.tired + 1)
        elif action == "joke":
            if rng.random() < 0.5:
                print(delta(state, trade_goods=2, morale=3))
            else:
                print(delta(state, morale=1))
        elif action == "bar_rumor":
            name = possible_recruit(state, rng)
            if name:
                print(recruit(state, name))
            else:
                faction = rng.choice(list(state.faction_relations))
                state.faction_relations[faction] += 3
        elif action == "adopt_pet":
            if len(state.pets) >= 3:
                print("宠物栏已满，本次领养取消并退还交易品。")
                state.trade_goods += 5
            else:
                state.pets[pet_name] = dict(PETS[pet_name])
                print(f"{pet_name}加入基地。")
        elif action == "heal_pets":
            for pet in state.pets.values():
                pet["hp"] = min(PETS[next(n for n in PETS if PETS[n]["species"] == pet["species"])]["hp"], pet["hp"] + 3)
        elif action == "train_pets":
            for pet in state.pets.values():
                pet["attack"] += 1
        if auto:
            return


def possible_recruit(state: State, rng: random.Random) -> str | None:
    remaining = [x for x in COMPANIONS if x not in state.survivors]
    if not remaining:
        return None
    # Later survivors are rarer and some need story progress.
    allowed = [x for x in remaining if x not in {"白术"} or state.intel >= 8]
    return rng.choice(allowed) if allowed else None


def exploration(state: State, rng: random.Random,
                auto: random.Random | None = None) -> None:
    team = select_team(state, auto)
    route_names = list(EXPLORATION_ROUTES)
    if not state.has("radio_route"):
        route_names.remove("监听无线电坐标后前往")
    options = [f"{name}｜{EXPLORATION_ROUTES[name]['desc']} 风险等级 {EXPLORATION_ROUTES[name]['risk']}/5"
               for name in route_names]
    route = route_names[choose("选择探索方向。你只能看到线索和风险，无法预知具体收获：", options, auto)]
    spec = EXPLORATION_ROUTES[route]
    profile = rng.choice(spec["profiles"])
    site = rng.choice(SITE_NAMES[profile])
    print(f"\n你们发现了：{site}。")
    print(rng.choice(SCENE_TEXT[profile]))
    if site not in state.visited:
        state.visited.append(site)
    risk = spec["risk"]
    scout = best_skill(state, team, "侦察")
    roll = rng.randint(1, 100)
    combat_threshold = max(6, 14 + risk * 5 - scout * 5)
    if profile == "市场":
        undiscovered = [m for m in MARKET_NAMES if m not in state.discovered_markets]
        market = rng.choice(undiscovered) if undiscovered else rng.choice(state.discovered_markets)
        if market not in state.discovered_markets:
            state.discovered_markets.append(market)
            print(f"这里是一处幸存者集市。你记住了安全进入的暗号。[解锁集市：{market}]")
        market_visit(state, rng, auto)
    elif profile == "幸存者":
        name = possible_recruit(state, rng)
        if name and rng.random() < 0.58:
            print(wrap(COMPANIONS[name]["intro"]))
            options = [
                f"邀请{name}加入基地｜人口增加，每天多消耗食物",
                "交换少量物资后离开｜不会增加人口",
            ]
            if choose("对方愿意同行，但会成为基地长期成员：", options, auto) == 0:
                print(recruit(state, name))
            else:
                print(delta(state, food=2, trade_goods=-1 if state.trade_goods else 0))
        else:
            print("营地已经空了，只留下几处尚有余温的火堆。")
            print(delta(state, food=2, materials=1))
    elif profile == "陷阱":
        chance = min(85, 35 + scout * 12)
        pick = choose(
            "物资摆得过于显眼。你要如何处理？",
            [f"检查周围后靠近｜识破陷阱概率 {chance}%",
             "不碰物资，立即离开｜放弃潜在收益",
             "从远处制造动静试探｜消耗 1 弹药" if state.ammo else "绕远观察｜会增加疲劳"],
            auto,
        )
        if pick == 0 and rng.randint(1, 100) <= chance:
            print("你发现了藏在二楼窗口后的枪口。对方见骗局暴露，先撤了。")
            print(delta(state, trade_goods=2, intel=1))
        elif pick == 1:
            print("你们安全离开。那只箱子在身后一直没有人碰。")
        elif pick == 2 and state.ammo:
            print(delta(state, ammo=-1, threat=2))
            print("枪声逼出两名埋伏者。他们逃跑时丢下一袋物资。")
            print(delta(state, food=3, materials=2))
        else:
            print("埋伏者从侧面冲出来！")
            combat(state, team, rng, risk + 1, auto)
    else:
        if roll <= combat_threshold:
            print("搜刮刚开始，阴影里就响起拖行脚步。")
            won = combat(state, team, rng, risk, auto)
            if not won:
                print("你们撤退了，没能带走主要物资。")
                state.threat = min(100, state.threat + 2)
                return
        loot = random_loot(state, team, rng, profile)
        print("你们检查了能安全到达的区域。")
        print(delta(state, **loot))
        weapon_found = maybe_find_weapon(state, rng, profile)
        if weapon_found:
            print(weapon_found)
        equipment_found = maybe_find_equipment(state, rng, profile)
        if equipment_found:
            print(equipment_found)
        if profile == "线索" or (rng.random() < 0.15 + 0.03 * best_skill(state, team, "研究")):
            found = rng.choice(["异常封锁记录", "互相矛盾的病历", "未公开的运输清单", "损坏的数据存储器"])
            state.clues.append(found)
            print(f"[发现调查材料：{found}]")
            print(delta(state, intel=1))
        if rng.random() < 0.08 and profile in {"医疗", "线索"}:
            print(delta(state, sample=1))
            print("你找到一份保存状况未知的生物样本。需要合适的人和设施才能分析。")
    for person in team:
        person.tired = min(4, person.tired + 1)
    state.tired = min(4, state.tired + 1)


DIALOGUE = {
    "闲聊": [
        "灾难前我最烦的是排队。现在我会为能排一次队付出不少东西。",
        "如果以后真有人写历史，最好别把我们写得太英勇。",
        "昨晚有人说梦话，点了三份外卖。没人笑，但我记住了。",
        "我在想，僵尸会不会也讨厌下雨。至少鞋里进水这点大家平等。",
        "要是能开一家末日餐馆，我只卖一道菜：今天找到什么就是什么。",
        "我给那只鹅起外号叫警报器。它显然觉得这是晋升。",
        "有人把防暴甲晾在厨房，锅里的汤现在有一股橡胶味。",
        "我不怀念上班，但我居然开始怀念周一早上的抱怨。",
    ],
    "抱怨": [
        "岗位总落在同几个人身上。这样下去不是基地，是慢性处刑。",
        "食物账对不上。也许不是有人偷，只是没人愿意承认算错。",
        "你每次带人出去都说风险可控。可控的是数字，受伤的是人。",
        "基地规则越来越多，可写规则的人从来不用排夜班。",
        "宠物吃得比伤员好，这不是动物的问题，是分配的问题。",
        "你又把同一个人安排去搜刮。他不是工具，也会怕。",
        "有些集市只欢迎有枪的人。我们是不是也正在变成那样？",
        "大家都说为了长远，可每一次长远都由今天的人挨饿。",
    ],
    "线索": [
        "我见过那个标记，在灾难前的封锁车上也有。",
        "有段广播每隔十七分钟重复一次，但背景里的钟声每次不同。",
        "那份名单不是病人名单，更像是运输优先级。",
        "有人在刻意收购同一种冷藏箱，价格高得不像为了药。",
        "白塔的人用两套口令，一套给商人，一套给运送劳工的车。",
        "气象站的电早断了，可昨晚仍有人上传新数据。",
        "那只乌鸦总在同一栋楼盘旋，楼顶可能藏着发射器。",
        "旧货场卖出的枪，有几支序列号来自封锁部队。",
    ],
    "秘密": [
        "我有一件事一直没写进登记表。现在告诉你，是因为我还想留在这里。",
        "我认识另一个团体的人。我们没有敌对，但也绝不是朋友。",
        "那天我本可以多救一个人。我选择了更容易救的那个。",
        "我并不相信所有真相都该公开，但我相信你应该先知道。",
        "我曾替另一个团体传过消息。如果他们来找我，你会知道原因。",
        "我藏了一件私人物品。不是武器，但可能让大家怀疑我。",
        "我知道一条能离城的路，只是那条路要经过我不想再见的人。",
        "我第一次见到感染者时没有救人。我关了门，现在还记得敲门声。",
    ],
}


def talk_to_survivor(state: State, person: Survivor, rng: random.Random) -> None:
    if person.mood < 30:
        category = "抱怨"
    elif person.trust >= 3 and rng.random() < 0.45:
        category = "秘密"
    elif state.intel and rng.random() < 0.35:
        category = "线索"
    else:
        category = "闲聊"
    print(f"\n【{person.name}｜{category}】{rng.choice(DIALOGUE[category])}")
    if category == "抱怨":
        person.mood = min(100, person.mood + 8)
        person.trust = min(5, person.trust + 1)
        print(f"[{person.name}心情 +8] [信任 +1]")
    elif category == "线索":
        state.intel += 1
        person.trust = min(5, person.trust + 1)
        print("[调查线索 +1] [信任 +1]")
    elif category == "秘密":
        person.trust = min(5, person.trust + 1)
        state.tag(f"secret:{person.name}")
        print(f"[解锁{person.name}秘密事件] [信任 +1]")
    else:
        person.mood = min(100, person.mood + 4)
        print(f"[{person.name}心情 +4]")


def base_action(state: State, rng: random.Random,
                auto: random.Random | None = None) -> None:
    options = [
        "休息和治疗｜恢复生命与疲劳，可能消耗药品",
        "加固基地｜消耗材料，建造技能提高收益",
        "开垦或照料农田｜消耗种子/材料，提高长期食物产量",
        "整理物资制作交易品｜用多种零散物资换取可交易货物",
        "建设功能设施｜升级医务室或工作间",
        "人员管理｜查看技能或驱逐一名队友（强烈负面影响）",
        "训练基地人员｜提高士气与夜间守卫",
    ]
    fortify_cost = max(2, 5 - state.skills["建造"] - (
        1 if "段黎" in state.survivors and state.survivors["段黎"].alive else 0
    ))
    facility_build = state.skills["建造"] + (
        2 if "段黎" in state.survivors and state.survivors["段黎"].alive else 0
    )
    facility_cost = max(4, 9 - facility_build)
    if state.materials < fortify_cost:
        options[1] += f"【不可用：需要 {fortify_cost} 材料】"
    if state.seeds < 1 or state.materials < 2:
        options[2] += "【不可用：需要 1 种子和 2 材料】"
    if state.food < 3 or state.materials < 2:
        options[3] += "【不可用：需要 3 食物和 2 材料】"
    if state.infirmary >= 3 and state.workshop >= 3:
        options[4] += "【不可用：所有设施已满级】"
    elif state.materials < facility_cost:
        options[4] += f"【不可用：需要 {facility_cost} 材料】"
    if not state.living:
        options[5] += "【不可用：没有队友】"
    if state.discovered_markets:
        options.append("前往已发现的幸存者集市｜进行交易")
    pick = choose("今天留出一次基地行动：", options, auto)
    if pick == 0:
        heal = 1 + state.skills["医疗"] // 2 + state.infirmary
        med_cost = 0 if state.skills["医疗"] >= 3 or state.shelter == "社区医院" else 1
        before_hp = state.hp
        if state.hp >= state.max_hp:
            print("你的生命已经全满；休息仍会恢复疲劳，但不会虚假显示生命增加。")
        elif med_cost and state.medicine < med_cost:
            print("药品不足，无法处理伤口；本次行动只恢复疲劳，不扣除药品。")
        else:
            actual = min(heal, state.max_hp - state.hp)
            state.hp += actual
            if med_cost:
                state.medicine -= med_cost
            print(f"[生命 +{actual}]" + (f" [药品 -{med_cost}]" if med_cost else ""))
        assert state.hp >= before_hp
        state.tired = max(0, state.tired - 3)
        treated = []
        for p in state.living:
            p.tired = max(0, p.tired - 1)
            if p.hp < p.max_hp and state.medicine > 0:
                restored = min(1 + (1 if state.infirmary >= 2 else 0), p.max_hp - p.hp)
                p.hp += restored
                state.medicine -= 1
                treated.append(f"{p.name}+{restored}")
        print("疲劳已经恢复。" + (f" 队友治疗：{', '.join(treated)}。" if treated else ""))
    elif pick == 1:
        cost = fortify_cost
        if state.materials >= cost:
            gain = 5 + state.skills["建造"] * 2
            print(delta(state, materials=-cost, defense=gain, threat=-2))
        else:
            print("材料不足，今天只完成了测量。")
    elif pick == 2:
        if state.seeds > 0 and state.materials >= 2:
            gain = 1 + state.skills["种植"] // 2 + (1 if "许穗" in state.survivors and state.survivors["许穗"].alive else 0)
            state.seeds -= 1
            state.materials -= 2
            state.farm = min(8, state.farm + gain)
            print(f"农田提升到 {state.farm} 级。[种子 -1] [材料 -2]")
        else:
            print("需要至少 1 份种子和 2 份材料。")
    elif pick == 3:
        if state.food >= 3 and state.materials >= 2:
            print(delta(state, food=-3, materials=-2, trade_goods=2 + state.workshop))
        else:
            print("缺少可整理成套的多余物资。")
    elif pick == 4:
        facility = choose("选择设施：", [
            f"升级医务室（当前 {state.infirmary}/3）｜提高治疗效果",
            f"升级工作间（当前 {state.workshop}/3）｜制作更多交易品",
        ], auto)
        build = state.skills["建造"] + (2 if "段黎" in state.survivors and state.survivors["段黎"].alive else 0)
        cost = max(4, 9 - build)
        if state.materials < cost:
            print(f"需要 {cost} 材料，当前不足。")
        elif facility == 0 and state.infirmary < 3:
            state.materials -= cost
            state.infirmary += 1
            print(f"[材料 -{cost}] [医务室升至 {state.infirmary} 级]")
        elif facility == 1 and state.workshop < 3:
            state.materials -= cost
            state.workshop += 1
            print(f"[材料 -{cost}] [工作间升至 {state.workshop} 级]")
        else:
            print("该设施已经达到最高等级。")
    elif pick == 5:
        if not state.living:
            print("基地没有可以管理的队友。")
            return
        names = [p.name for p in state.living]
        choice = choose("选择人员：", [
            f"{p.name}｜{p.role}｜{p.unique}｜信任 {p.trust:+d}" for p in state.living
        ] + ["取消"], auto)
        if choice == len(names):
            print("没有进行人员变动。")
            return
        name = names[choice]
        action = choose(f"管理{name}：", [
            "安排岗位｜岗位每天产生实际效果",
            "谈话｜根据性格、心情与信任触发对话",
            "驱逐｜强烈负面效果",
            "取消",
        ], auto)
        if action == 0:
            jobs = ["搜刮员", "守卫", "农夫", "医护", "工匠", "厨师", "研究员", "调解员", "无线电员", "待命"]
            ji = choose("选择岗位：", jobs, auto)
            state.survivors[name].job = jobs[ji]
            print(f"{name}被安排为{jobs[ji]}。岗位效果将在每日结算中生效。")
            return
        if action == 1:
            talk_to_survivor(state, state.survivors[name], rng)
            return
        if action == 3:
            print("没有进行人员变动。")
            return
        confirm = choose(
            f"确定驱逐{name}？后果：人口 -1、士气 -12、威胁 +4、其他队友信任 -1，"
            "并永久失去其技能和专属事件。",
            ["确定驱逐", "取消"],
            auto,
        )
        if confirm == 0:
            del state.survivors[name]
            state.tag(f"exiled:{name}")
            print(delta(state, morale=-12, threat=4))
            for person in state.living:
                person.trust = max(-5, person.trust - 1)
            print(f"{name}带走个人物品离开基地。其他队友信任 -1。")
        else:
            print("驱逐已取消。")
    elif pick == 6:
        guard = state.skills["守卫"] + sum(p.skills.get("守卫", 0) for p in state.living) + sum(1 for p in state.pets.values() if p.get("skill") in {"夜间警报", "牵制"})
        print(delta(state, morale=3, defense=min(5, 1 + guard // 2)))
    else:
        market_visit(state, rng, auto)


def story_event(state: State, rng: random.Random,
                auto: random.Random | None = None) -> bool:
    for beat in STORY_BEATS:
        if state.has(beat["id"]) or state.day < beat["min_day"] or state.intel < beat["intel"]:
            continue
        if any(not state.has(req) for req in beat["requires"]):
            continue
        state.tag(beat["id"])
        scenario = STORYLINES[state.story_id]
        beat_index = next(i for i, b in enumerate(STORY_BEATS) if b["id"] == beat["id"])
        story_title = scenario["beats"][beat_index]
        print(f"\n【主线事件：{story_title}】")
        texts = {
            "trace_1": "你把几份撤离记录按日期排开，发现官方公布的首例之前，已有一支封闭运输队穿过城区。",
            "trace_2": "同一家医院留下两套不同病历。一套记录症状，另一套只记录编号和转运时间。",
            "trace_3": "样本在低温下表现出与街头感染者不同的反应。问题不只是“它从哪里来”，还包括它后来被改变过什么。",
            "trace_4": "一份残缺命令证明，封锁并非单纯为了阻止感染向外扩散。有人在封锁圈内寻找某样东西。",
            "trace_5": "所有记录终于能连成一条完整路径。城市里仍存在一种可执行的处理方案，但启动它需要人员、样本和一处守得住的基地。",
        }
        prefixes = {
            "cold_chain": "冷藏运输记录中又出现一个不该存在的交接点。",
            "echo": "无线电底噪里恢复出一段新的重复结构。",
            "white_rain": "环境样本与官方气象记录再次冲突。",
            "convoy": "十四号车队留下的路线出现新的矛盾。",
        }
        print(wrap(prefixes[state.story_id] + texts[beat["id"]]))
        cast = {
            "cold_chain": ["林乔", "白术"],
            "echo": ["程墨", "唐七"],
            "white_rain": ["叶芝", "乌木"],
            "convoy": ["罗宁", "费诚", "周野"],
        }[state.story_id]
        present = [name for name in cast if name in state.survivors and state.survivors[name].alive]
        if present:
            witness = rng.choice(present)
            state.intel += 1
            state.survivors[witness].trust = min(5, state.survivors[witness].trust + 1)
            print(f"{witness}认出了记录中的细节，并补上一段个人经历。[角色伏笔回收] [调查 +1] [信任 +1]")
        if beat["id"] == "trace_2" and "林乔" in state.survivors and state.survivors["林乔"].alive:
            print("林乔指出病历中的用药顺序不可能出自普通急诊流程。[林乔专属]")
            state.intel += 2
        if beat["id"] == "trace_3":
            if "白术" in state.survivors and state.survivors["白术"].alive and state.sample >= 2:
                print("白术使用两份样本完成对照分析。[白术专属] [样本 -2]")
                state.sample -= 2
                state.tag("analysis_complete")
            else:
                print("缺少研究人员或对照样本，分析只能停在推测阶段。")
                state.tag("analysis_incomplete")
        if beat["id"] == "trace_4" and "程墨" in state.survivors and state.survivors["程墨"].alive:
            print("程墨从旧频率中恢复了命令的后半段。[程墨专属]")
            state.tag("radio_decoded")
        state.story_progress += 1
        state.journal.append(f"第{state.day}天：主线推进——{story_title}。")
        if not auto:
            input("\n按 Enter 继续……")
        return True
    return False


def milestone_event(state: State, rng: random.Random,
                    auto: random.Random | None = None) -> None:
    events = {
        10: ("第一次大迁徙",
             "城北的尸群开始整体向南移动。它们不是冲着基地来的，但会经过附近。",
             [("彻底熄灯两天，等待尸群通过。", {"food": -2, "threat": -8, "morale": -2}, "dark_days"),
              ("设置声源把尸群引向无人区。", {"materials": -3, "threat": -12, "morale": 2}, "decoy_horde"),
              ("趁道路被清空，冒险搜刮。", {"food": 7, "materials": 5, "threat": 8}, "horde_scavenge")]),
        20: ("断水",
             "基地原有水源开始发臭。即使还有食物，没有可靠水源也撑不过下一个月。",
             [("消耗材料建立过滤和储水系统。", {"materials": -7, "defense": 2, "morale": 5}, "water_system"),
              ("限制每日用水，等待降雨。", {"morale": -8, "threat": -2}, "water_ration"),
              ("和附近据点交换水源使用权。", {"trade_goods": -3, "morale": 3}, "water_deal")]),
        30: ("画在门上的记号",
             "外墙出现一个新画的白色圆圈。没人承认见过画记号的人。",
             [("改变岗哨和入口布置。", {"materials": -3, "defense": 7, "threat": -4}, "changed_watch"),
              ("保留记号，设伏等对方回来。", {"ammo": -2, "trade_goods": 3, "threat": 5}, "ambushed_scout"),
              ("擦掉记号，不让恐慌扩散。", {"morale": 2, "threat": 2}, "erased_mark")]),
        40: ("一小时广播",
             "一个陌生频率连续播报幸存者姓名和物资需求，恰好持续一小时。",
             [("回应并交换基地需求。", {"trade_goods": 2, "threat": 5, "intel": 1}, "answered_broadcast"),
              ("只监听并记录发射方位。", {"intel": 2, "morale": 1}, "tracked_broadcast"),
              ("干扰频率，避免基地成员被诱惑。", {"threat": -3, "morale": -3}, "jammed_broadcast")]),
        50: ("半数日",
             "这是第一百天目标的一半。有人提议庆祝，有人认为清点死者更重要。",
             [("拿出食物，让所有人吃一顿完整晚餐。", {"food": -8, "morale": 12}, "half_feast"),
              ("举行纪念，不额外消耗物资。", {"morale": 6, "intel": 1}, "half_memorial"),
              ("照常工作。活着本身不值得浪费。", {"materials": 3, "morale": -6}, "half_work")]),
        60: ("带枪的车队",
             "一支十二人的家庭车队请求在基地附近建立附属营地。他们有武器和孩子，也需要一批启动物资。",
             [("提供物资并结盟，让他们驻扎在外围。", {"food": -8, "ammo": 8, "morale": 8, "threat": 4}, "family_allied"),
              ("只救治伤者，不建立长期关系。", {"food": -2, "morale": 1, "medicine": -2}, "family_treated"),
              ("拒绝，但提供附近安全地点。", {"food": -2, "threat": -2}, "family_redirected")]),
        70: ("灰色高烧",
             "三名基地成员同时高烧。症状像感染，也像污染水源引起的疾病。",
             [("集中使用药品，按普通感染治疗。", {"medicine": -5, "morale": 4}, "fever_treated"),
              ("严格隔离，等待症状变化。", {"morale": -6, "threat": -2}, "fever_isolated"),
              ("使用保存的样本作对照。", {"sample": -1, "intel": 2, "medicine": -2}, "fever_compared")]),
        80: ("红色夜空",
             "城区方向连续发生爆炸，火光照亮云层。无线电称有一处大型仓库正在失守。",
             [("组织车队抢救仓库物资。", {"food": 10, "materials": 10, "ammo": -5, "threat": 12}, "red_sky_raid"),
              ("救援逃出仓库的人。", {"food": -4, "morale": 9, "intel": 2}, "red_sky_rescue"),
              ("封锁基地，任何人不得外出。", {"threat": -8, "morale": -4}, "red_sky_closed")]),
        90: ("最后十天",
             "基地里每个人都知道第一百天将至。这个数字本没有意义，却成了所有人的共同目标。",
             [("把剩余工作和食物公开，让所有人投票。", {"morale": 8, "defense": 3}, "open_plan"),
              ("集中权力，优先完成防御与调查。", {"morale": -5, "defense": 7, "intel": 2}, "central_plan"),
              ("不宣布任何特殊安排。", {"morale": -1, "threat": -2}, "quiet_plan")]),
        95: ("突然的寂静",
             "整整一天，附近没有枪声、广播，也没有感染者撞击围栏。寂静比噪声更让人不安。",
             [("派侦察队确认外围。", {"intel": 2, "threat": 4}, "scouted_silence"),
              ("利用安静全力加固。", {"materials": -5, "defense": 9}, "fortified_silence"),
              ("让所有人休息。", {"morale": 8, "threat": 2}, "rested_silence")]),
    }
    if state.day not in events or state.has(f"milestone:{state.day}"):
        return
    title, text, choices = events[state.day]
    print(f"\n【阶段事件：{title}】")
    labels = {
        "food": "食物", "materials": "材料", "threat": "威胁",
        "morale": "士气", "defense": "防御", "trade_goods": "交易品",
        "ammo": "弹药", "medicine": "药品", "intel": "调查线索",
        "sample": "样本",
    }
    spendable = {"food", "materials", "trade_goods", "ammo", "medicine", "sample", "seeds"}
    def affordable(effects):
        return all(key not in spendable or value >= 0 or getattr(state, key) >= -value
                   for key, value in effects.items())
    shown = [
        f"{label}｜可能影响：" + "、".join(
            f"{labels.get(key, key)}{'+' if value > 0 else ''}{value}" for key, value in effects.items()
        ) + ("" if affordable(effects) else "【不可用：物资不足】")
        for label, effects, _ in choices
    ]
    if auto:
        valid = [i for i, (_, effects, _) in enumerate(choices) if affordable(effects)]
        pick = auto.choice(valid) if valid else 0
        print(wrap(text))
        print(f"\n> {pick + 1}")
    else:
        while True:
            pick = choose(text, shown, None)
            if affordable(choices[pick][1]):
                break
            print("该选项物资不足，不会执行，也不会扣除任何物资。")
    label, effects, tag = choices[pick]
    # Population effects are intentionally represented through narrative/recruitment,
    # while all numeric effects go through the clamped state updater.
    valid = {k: v for k, v in effects.items() if hasattr(state, k)}
    print(label)
    print(delta(state, **valid))
    state.tag(f"milestone:{state.day}")
    state.tag(tag)
    state.journal.append(f"第{state.day}天·{title}：{label}")


def random_base_event(state: State, rng: random.Random,
                      auto: random.Random | None = None) -> None:
    roll = rng.random()
    if roll < 0.12 and state.population < SHELTERS[state.shelter]["capacity"]:
        name = possible_recruit(state, rng)
        if name:
            print(f"\n【敲门声】{COMPANIONS[name]['intro']}")
            pick = choose("是否让对方留下？", [
                f"接纳{name}｜每天增加一人食物消耗，并获得其实际技能",
                "给少量补给，让对方离开｜食物 -1",
            ], auto)
            if pick == 0:
                print(recruit(state, name))
            else:
                print(delta(state, food=-1, morale=-1))
    elif roll < 0.22:
        print("\n【夜间骚动】围墙外出现试探性的脚步。")
        guard = state.skills["守卫"] + sum(p.skills.get("守卫", 0) for p in state.living) + sum(1 for p in state.pets.values() if p.get("skill") in {"夜间警报", "牵制"})
        chance = min(90, 35 + state.defense + guard * 5 - state.threat // 2)
        if rng.randint(1, 100) <= chance:
            print("守夜者及时发现了缺口，没有开枪就逼退了来者。")
            print(delta(state, threat=-4))
        else:
            lost = min(state.food, rng.randint(2, 6))
            print(f"有人趁乱偷走食物。[食物 -{lost}]")
            state.food -= lost
            state.morale = max(0, state.morale - 3)
    elif roll < 0.28 and state.day > 12:
        print("\n【陌生商队】一支蒙着车牌的商队在基地外停了十分钟。")
        if rng.random() < 0.55:
            market = rng.choice(MARKET_NAMES)
            if market not in state.discovered_markets:
                state.discovered_markets.append(market)
                print(f"他们留下了一处交换点的暗号。[解锁集市：{market}]")
        else:
            print("他们只愿用一盒罐头换两份材料。")
            if choose("接受这笔明显不划算的交易？", ["接受", "拒绝"], auto) == 0 and state.materials >= 2:
                print(delta(state, materials=-2, food=1))
    elif roll < 0.36 and state.day > 15:
        faction = rng.choice(list(FACTIONS))
        print(f"\n【其他团体：{faction}】{FACTIONS[faction]}")
        pick = choose("他们提出一次合作：", [
            "提供 3 食物建立联系｜关系 +6",
            "交换情报｜消耗 1 调查线索，关系 +4、交易品 +2",
            "拒绝接触｜无直接消耗，关系 -2",
        ], auto)
        if pick == 0 and state.food >= 3:
            print(delta(state, food=-3))
            state.faction_relations[faction] += 6
        elif pick == 1 and state.intel >= 1:
            print(delta(state, intel=-1, trade_goods=2))
            state.faction_relations[faction] += 4
        else:
            state.faction_relations[faction] -= 2


def morning(state: State) -> None:
    pet_food = sum(p.get("food", 1) for p in state.pets.values())
    cooks = sum(1 for p in state.living if p.job == "厨师")
    use = max(1, round(state.population * DIFFICULTIES[state.difficulty]["food_use"]) - cooks) + pet_food
    farmers = sum(1 for p in state.living if p.job == "农夫")
    farm_yield = state.farm + farmers + (2 if "许穗" in state.survivors and state.survivors["许穗"].alive and state.farm else 0)
    if farm_yield:
        state.food += farm_yield
    eaten = min(use, state.food)
    state.food -= eaten
    print(f"\n晨间结算：人口 {state.population}，消耗食物 {eaten}/{use}，农田产出 {farm_yield}。")
    if eaten < use:
        shortage = use - eaten
        state.morale = max(0, state.morale - shortage * 4)
        state.tired = min(4, state.tired + 1)
        print("食物不足。饥饿使所有行动变得更危险。")
    # Passive recovery and practical companion effects.
    if "林乔" in state.survivors and state.survivors["林乔"].alive and state.medicine > 0:
        injured = [p for p in state.living if p.hp < p.max_hp]
        if injured:
            target = injured[0]
            target.hp = min(target.max_hp, target.hp + 2)
            state.medicine -= 1
            print(f"林乔治疗了{target.name}。[药品 -1] [{target.name}生命 +2]")
        elif state.hp < state.max_hp:
            state.hp = min(state.max_hp, state.hp + 1)
            state.medicine -= 1
            print("林乔替你处理了伤口。[药品 -1] [生命 +1]")
    elif state.skills.get("医疗", 0) >= 2 and state.hp < state.max_hp and state.medicine > 0:
        state.hp = min(state.max_hp, state.hp + 1)
        state.medicine -= 1
        print("你处理了自己的伤口。[药品 -1] [生命 +1]")
    if state.shelter == "山中别墅":
        state.threat = max(0, state.threat - 2)
    if state.shelter == "社区医院":
        state.threat = min(100, state.threat + 2)
    # Assigned jobs are practical passive production, not flavor labels.
    guards = sum(1 for p in state.living if p.job == "守卫")
    crafters = sum(1 for p in state.living if p.job == "工匠")
    scavengers = sum(1 for p in state.living if p.job == "搜刮员")
    mediators = sum(1 for p in state.living if p.job == "调解员")
    researchers = sum(1 for p in state.living if p.job == "研究员")
    radios = sum(1 for p in state.living if p.job == "无线电员")
    state.defense = min(100, state.defense + guards)
    state.materials += crafters // 2 + scavengers // 2
    state.morale = min(100, state.morale + mediators)
    if researchers and state.day % 5 == 0:
        state.intel += 1
        print("[研究岗位：调查线索 +1]")
    if radios and state.day % 7 == 0:
        faction = min(state.faction_relations, key=state.faction_relations.get)
        state.faction_relations[faction] += 2
        print(f"[无线电岗位：{faction}关系 +2]")
    for person in state.living:
        if person.job == "待命":
            person.mood = min(100, person.mood + 1)
        elif state.food == 0:
            person.mood = max(0, person.mood - 5)


def night(state: State, rng: random.Random,
          auto: random.Random | None = None) -> None:
    state.threat = min(100, state.threat + 1 + state.population // 4)
    if state.threat > state.defense + 25 and rng.random() < 0.35:
        print("\n【基地袭击】积累的威胁引来了尸群。")
        defenders = [p for p in state.living if p.tired < 4]
        won = combat(state, defenders[:2], rng, 4, auto)
        if won:
            print("基地守住了。")
            state.threat = max(0, state.threat - 15)
        else:
            print("尸群冲入储藏区。")
            print(delta(state, food=-min(8, state.food), materials=-min(5, state.materials),
                        defense=-6, morale=-8))
    random_base_event(state, rng, auto)
    unhappy = [p for p in state.living if p.mood < 25 or p.trust <= -3]
    mediation = sum(p.skills.get("调解", 0) for p in state.living)
    if unhappy and rng.random() < max(0.03, 0.18 - mediation * 0.025):
        leader = rng.choice(unhappy)
        print(f"\n【内部冲突】{leader.name}拒绝继续执行当前分工，几名队友在仓库门口争吵。")
        pick = choose("如何处理？", [
            "公开物资和岗位记录，重新投票｜士气恢复，可能削弱你的权威",
            "让调解员分别谈话｜需要调解岗位或相应技能",
            "强制执行原分工｜防御不受影响，但信任和心情恶化",
            f"允许{leader.name}带个人物品离开｜永久失去该队友",
        ], auto)
        if pick == 0:
            state.morale = min(100, state.morale + 5)
            for p in state.living:
                p.mood = min(100, p.mood + 4)
        elif pick == 1 and mediation:
            leader.mood = min(100, leader.mood + 15)
            leader.trust = min(5, leader.trust + 1)
        elif pick == 3:
            del state.survivors[leader.name]
            state.tag(f"deserted:{leader.name}")
            state.morale = max(0, state.morale - 8)
        else:
            leader.mood = max(0, leader.mood - 12)
            leader.trust = max(-5, leader.trust - 2)
            state.defense = min(100, state.defense + 2)
    for p in state.living:
        p.tired = max(0, p.tired - 1)
    state.tired = max(0, state.tired - 1)
    for message in cleanup_casualties(state):
        print(message)


def final_event(state: State, rng: random.Random,
                auto: random.Random | None = None) -> None:
    print("\n【第一百天】")
    solved = state.has("trace_5")
    ready = state.has("analysis_complete") and state.has("radio_decoded")
    if solved:
        options = [
            "执行调查所得的处理方案｜需要样本、研究能力和足够防御",
            "公开全部资料，让各幸存者据点自行决定",
            "封存资料，继续维持基地",
        ]
        pick = choose("你已经知道足够多。现在必须决定怎样使用这些发现：", options, auto)
        if pick == 0:
            research = state.skills["研究"] + sum(p.skills.get("研究", 0) for p in state.living)
            chance = min(95, 30 + state.defense // 3 + research * 8 + state.sample * 5)
            if ready:
                chance += 15
            print(f"最终行动成功率：{min(95, chance)}%。")
            if rng.randint(1, 100) <= min(95, chance):
                state.victory = True
                print(wrap("基地整夜没有熄灯。天亮时，城市没有恢复正常，但某种持续了一百天的趋势第一次被逆转。你们证明末日不是只能被忍受。"))
            else:
                print(wrap("行动启动了，却没能完整运行。你们保住基地和资料，下一次尝试仍有可能，但这一百天没有迎来确定答案。"))
        elif pick == 1:
            state.victory = state.intel >= 26 and state.population >= 5
            print(wrap("无线电把资料送向所有仍在监听的人。没有统一命令，只有一个又一个据点确认收到。真正的结果也许需要更久才能看见。"))
        else:
            print(wrap("资料被锁进最深的储藏室。基地仍然活着，而秘密也仍然属于少数人。"))
    else:
        print(wrap("你们活过了一百天，却没能拼出灾难的完整真相。城里还有未探索的地方，但今天本身就是一个答案。"))
    state.ended = True


def save(state: State, slot: str = "autosave") -> Path:
    SAVE_DIR.mkdir(exist_ok=True)
    path = SAVE_DIR / f"{slot}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)
    return path


def load(slot: str = "autosave") -> State:
    raw = json.loads((SAVE_DIR / f"{slot}.json").read_text(encoding="utf-8"))
    if raw.get("version") != VERSION:
        raise ValueError("存档版本不兼容")
    survivors = {k: Survivor(**v) for k, v in raw.pop("survivors").items()}
    return State(**raw, survivors=survivors)


def play(state: State, auto: random.Random | None = None) -> State:
    rng = random.Random(state.seed + state.day * 997)
    try:
        while state.day <= 100 and not state.ended:
            show_status(state)
            morning(state)
            if state.day == 100:
                final_event(state, rng, auto)
                break
            actions = 1 if state.day <= 2 else 2
            for action_no in range(actions):
                if state.ended:
                    break
                options = [
                    "外出探索｜选择方向和队友；具体发现未知",
                    "留在基地行动｜建设、治疗、种植、训练或交易",
                ]
                if state.discovered_markets:
                    options.append("直接前往集市｜不会触发普通探索事件")
                pick = choose(f"今日行动 {action_no + 1}/{actions}：", options, auto)
                if pick == 0:
                    exploration(state, rng, auto)
                    maybe_easter_egg(state, rng, "explore", auto is None)
                    secondary = ["weapon", "armor", "gear", "zombie"]
                    if state.pets:
                        secondary.append("pet")
                    if state.living:
                        secondary.append("survivor")
                    maybe_easter_egg(state, rng, rng.choice(secondary), auto is None, 0.018)
                elif pick == 1:
                    base_action(state, rng, auto)
                    maybe_easter_egg(state, rng, "base", auto is None)
                    if state.living:
                        maybe_easter_egg(state, rng, "survivor", auto is None, 0.015)
                else:
                    market_visit(state, rng, auto)
                    maybe_easter_egg(state, rng, "market", auto is None, 0.045)
                for message in cleanup_casualties(state):
                    print(message)
                if not auto and not state.ended:
                    input("\n按 Enter 继续……")
            if not state.ended:
                milestone_event(state, rng, auto)
                if story_event(state, rng, auto):
                    maybe_easter_egg(state, rng, "story", auto is None, 0.06)
                night(state, rng, auto)
                maybe_easter_egg(state, rng, "night", auto is None, 0.018)
                if state.pets:
                    maybe_easter_egg(state, rng, "pet", auto is None, 0.012)
            state.journal.append(
                f"第{state.day}天结束：人口{state.population}，食物{state.food}，防御{state.defense}，线索{state.intel}。"
            )
            state.day += 1
            if not auto:
                save(state)
                input("\n已自动存档。按 Enter 进入下一天……")
        show_status(state)
        print("\n" + ("真正胜利：你们不仅活了下来。" if state.victory else "本局结束。"))
        print(f"存活天数：{min(100, state.day)}  最终人口：{state.population}  调查线索：{state.intel}")
        return state
    except KeyboardInterrupt:
        if not auto:
            save(state)
            print("\n游戏已保存。")
        return state


def simulate(count: int) -> None:
    results = {"victory": 0, "survived_100": 0, "died": 0}
    populations, intel = [], []
    for i in range(count):
        auto = random.Random(10000 + i)
        state = new_game(auto)
        play(state, auto)
        if state.victory:
            results["victory"] += 1
        elif state.day >= 100 and state.hp > 0:
            results["survived_100"] += 1
        else:
            results["died"] += 1
        populations.append(state.population)
        intel.append(state.intel)
    results["avg_population"] = round(sum(populations) / count, 2)
    results["avg_intel"] = round(sum(intel) / count, 2)
    print(json.dumps(results, ensure_ascii=False))


def main() -> None:
    global COLOR
    parser = argparse.ArgumentParser(description="《百日之后》终端丧尸生存游戏")
    parser.add_argument("--new", action="store_true", help="开始新游戏")
    parser.add_argument("--simulate", type=int, metavar="N", help="自动模拟 N 局")
    parser.add_argument("--collection", action="store_true", help="查看跨周目彩蛋收藏库")
    parser.add_argument("--no-color", action="store_true", help="关闭 ANSI 彩色界面")
    args = parser.parse_args()
    COLOR = not args.no_color and os.environ.get("NO_COLOR") is None
    if os.name == "nt" and COLOR:
        os.system("")
    if args.simulate:
        simulate(args.simulate)
        return
    if args.collection:
        show_collection()
        return
    while choose("《百日之后》", [
        "进入游戏",
        f"查看彩蛋收藏库｜{len(load_collection()['found'])}/{len(EASTER_EGGS)}",
    ], None) == 1:
        show_collection()
        input("\n按 Enter 返回……")
    path = SAVE_DIR / "autosave.json"
    if path.exists() and not args.new:
        pick = choose("发现自动存档：", ["继续游戏", "开始新游戏"], None)
        if pick == 0:
            try:
                state = load()
            except Exception:
                print("存档损坏或版本不兼容，将开始新游戏。")
                state = new_game()
        else:
            state = new_game()
    else:
        state = new_game()
    play(state)


if __name__ == "__main__":
    main()
