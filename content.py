DIFFICULTIES = {
    "休闲": {
        "desc": "资源较多，战斗伤害较低，适合体验剧情。",
        "loot": 1.30, "enemy": 0.80, "food_use": 0.80, "start_bonus": 5,
    },
    "标准": {
        "desc": "资源与风险均衡，推荐首次游玩。",
        "loot": 1.00, "enemy": 1.00, "food_use": 1.00, "start_bonus": 0,
    },
    "残酷": {
        "desc": "资源稀少，尸群更危险，队友更容易永久死亡。",
        "loot": 0.78, "enemy": 1.25, "food_use": 1.15, "start_bonus": -3,
    },
}

JOBS = {
    "搜救队员": {
        "desc": "搜刮 2、战斗 2。外出携带量更高，撤退成功率更高。",
        "skills": {"搜刮": 2, "战斗": 2},
    },
    "急诊护士": {
        "desc": "医疗 3、搜刮 1。治疗消耗更少，可识别感染与药品。",
        "skills": {"医疗": 3, "搜刮": 1},
    },
    "猎户": {
        "desc": "射击 3、战斗 1。枪械命中率高，首次远程攻击更稳。",
        "skills": {"射击": 3, "战斗": 1},
    },
    "建筑工": {
        "desc": "建造 3、守卫 1。加固消耗较少，基地防御收益更高。",
        "skills": {"建造": 3, "守卫": 1},
    },
    "农技员": {
        "desc": "种植 3、医疗 1。农田产量高，能辨认可食植物。",
        "skills": {"种植": 3, "医疗": 1},
    },
    "商店经理": {
        "desc": "谈判 3、搜刮 1。交易价格更好，容易识别骗局。",
        "skills": {"谈判": 3, "搜刮": 1},
    },
}

SHELTERS = {
    "社区学校": {
        "desc": "房间多、可容纳很多人；出入口多，防守压力较大。",
        "capacity": 14, "defense": 8, "food": 12, "materials": 9,
        "special": "操场可改造成农田。",
    },
    "山中别墅": {
        "desc": "隐蔽且有水井；距离城区远，探索消耗更大。",
        "capacity": 8, "defense": 14, "food": 16, "materials": 5,
        "special": "夜间威胁增长较慢。",
    },
    "废弃地铁站": {
        "desc": "入口少、隧道可通往远处；潮湿黑暗，容易发生隐蔽袭击。",
        "capacity": 12, "defense": 16, "food": 9, "materials": 11,
        "special": "探索时更容易发现城区捷径。",
    },
    "河边物流仓": {
        "desc": "仓储空间和车辆丰富；开阔地带会放大枪声与灯光。",
        "capacity": 16, "defense": 10, "food": 15, "materials": 14,
        "special": "每次探索可多携带一份战利品。",
    },
    "社区医院": {
        "desc": "医疗设施完整；求救者与感染者都会不断靠近。",
        "capacity": 13, "defense": 7, "food": 8, "materials": 7,
        "medicine": 8, "special": "治疗效果更强，但夜间威胁较高。",
    },
    "郊外农场": {
        "desc": "拥有土地、牲畜棚和小型风机；建筑分散，防守需要人手。",
        "capacity": 11, "defense": 9, "food": 20, "materials": 8,
        "special": "农田起始等级为 1。",
    },
}

# 玩家只会在遇见他们时看到相应资料。unique 字段会直接影响系统。
COMPANIONS = {
    "林乔": {
        "role": "急诊护士", "skills": {"医疗": 3},
        "unique": "治疗时额外恢复 1 点生命；解锁医学调查。",
        "intro": "她背着从医院带出的急救包，不愿谈最后一班夜班发生了什么。",
    },
    "周野": {
        "role": "货运司机", "skills": {"搜刮": 2, "战斗": 1},
        "unique": "探索携带上限 +2；物流地点收益提高。",
        "intro": "他熟悉城区仓库和辅路，认为车比任何围墙都可靠。",
    },
    "程墨": {
        "role": "无线电爱好者", "skills": {"侦察": 3},
        "unique": "降低探索遇伏概率；解锁无线电线索。",
        "intro": "他随身带着改装收音机，能从噪声里分辨重复信号。",
    },
    "韩松": {
        "role": "退伍步兵", "skills": {"战斗": 3, "射击": 2, "守卫": 2},
        "unique": "同行时战斗先手；守夜显著降低袭击损失。",
        "intro": "他拒绝说自己从哪个检查站逃出来，只检查每个人的枪口方向。",
    },
    "许穗": {
        "role": "农技站职员", "skills": {"种植": 3, "医疗": 1},
        "unique": "农田产量 +2；探索自然地点可能找到种子。",
        "intro": "她带着一只装满种子的铁盒，要求先看基地有没有可用的土。",
    },
    "马会": {
        "role": "杂货店老板", "skills": {"谈判": 3, "搜刮": 1},
        "unique": "市场交易成本降低；每天可能识别一种高价货。",
        "intro": "他把每一次交换都写进小账本，包括别人欠你的命。",
    },
    "段黎": {
        "role": "土木工程师", "skills": {"建造": 3},
        "unique": "升级基地少消耗 1 材料；解锁高级设施。",
        "intro": "她看任何建筑的第一眼都在找承重墙和第二出口。",
    },
    "罗宁": {
        "role": "基层民警", "skills": {"守卫": 3, "谈判": 1},
        "unique": "基地人员越多时越能压低内乱概率。",
        "intro": "他保存着一本不完整的撤离登记册，里面有几页被撕掉。",
    },
    "白术": {
        "role": "检验科研究员", "skills": {"医疗": 2, "研究": 3},
        "unique": "解锁样本分析和核心调查选项。",
        "intro": "他手里的低温箱已经断电，却仍不允许任何人打开。",
    },
    "小满": {
        "role": "无家可归的孩子", "skills": {"侦察": 2},
        "unique": "不会参加正面战斗；能发现成年人忽略的藏匿点。",
        "intro": "她知道城里许多没有写在地图上的洞和门，但从不白带路。",
    },
    "顾临": {"role": "炊事班厨师", "skills": {"烹饪": 3}, "unique": "担任厨师时每日食物消耗 -1；低士气时能做安慰餐。", "intro": "他坚持盐比子弹更能阻止一群人互相仇恨。"},
    "殷桃": {"role": "兽医", "skills": {"医疗": 2, "驯兽": 3}, "unique": "治疗宠物，宠物战斗受伤概率降低。", "intro": "她的背包一半是药，一半是不同动物的零食。"},
    "老岑": {"role": "铁匠", "skills": {"建造": 2, "锻造": 3}, "unique": "可修复重甲和制作近战武器。", "intro": "他认为任何门都能变成盾，任何弹簧都能变成陷阱。"},
    "苏萤": {"role": "心理咨询师", "skills": {"调解": 3, "谈判": 1}, "unique": "降低内乱概率；谈话恢复更多心情。", "intro": "她从不问你怕不怕，只问这种恐惧让你做了什么。"},
    "费诚": {"role": "前记者", "skills": {"侦察": 2, "研究": 2}, "unique": "伏笔事件提供额外解释；公开真相会获得支持。", "intro": "他保存了灾难前最后七十二小时的采访录音。"},
    "姜饼": {"role": "街头魔术师", "skills": {"谈判": 2, "侦察": 1}, "unique": "集市赌博胜率提高；偶尔用把戏缓解心情。", "intro": "他声称自己能让硬币消失，但绝不让别人的口粮消失。"},
    "秦望": {"role": "电工", "skills": {"建造": 2, "电力": 3}, "unique": "发电设施更便宜；夜间照明降低潜入事件。", "intro": "他听电流声就像别人听雨。"},
    "温岚": {"role": "前法院书记员", "skills": {"谈判": 2, "管理": 3}, "unique": "担任管理员时岗位效率提高，处罚引发的信任损失降低。", "intro": "她带着一枚坏掉的印章，并坚持规则必须先写下来。"},
    "阿洛": {"role": "攀岩教练", "skills": {"搜刮": 2, "战斗": 1}, "unique": "高层探索额外战利品；撤退时可带回一件物资。", "intro": "他总在进入房间前先看天花板和窗外。"},
    "杜鹃": {"role": "酒吧歌手", "skills": {"调解": 2}, "unique": "担任文娱时全员心情缓慢恢复；噪声可能提高威胁。", "intro": "她只剩一把缺弦吉他，仍觉得沉默比歌声危险。"},
    "乌木": {"role": "化学教师", "skills": {"研究": 2, "医疗": 1}, "unique": "识别化学物资和毒性僵尸；可制作燃烧瓶。", "intro": "他用红笔给每一个危险容器重新写了标签。"},
    "石榴": {"role": "快递站长", "skills": {"搜刮": 3, "管理": 1}, "unique": "熟悉仓储编码；探索重复地点时仍可能找到夹层。", "intro": "她记得整座城区的仓库门朝哪边开。"},
    "唐七": {"role": "民间无线电台主", "skills": {"侦察": 2, "谈判": 2}, "unique": "可联络派系并刷新远程交易。", "intro": "他说每一段静电后面都可能有人等着回答。"},
    "叶芝": {"role": "植物园管理员", "skills": {"种植": 3, "研究": 1}, "unique": "发现药用植物；农田事件更丰富。", "intro": "她把植物称作不会说谎的幸存者。"},
}

EXPLORATION_ROUTES = {
    "沿主干道向城区推进": {
        "risk": 3, "profiles": ["商业", "医疗", "住宅"],
        "desc": "道路开阔，招牌和车辆能提供方向，也更容易遇到尸群或其他队伍。",
    },
    "沿小巷搜索陌生建筑": {
        "risk": 2, "profiles": ["住宅", "工坊", "隐藏"],
        "desc": "不知道门后是什么。风险较分散，常有被遗漏的小型物资点。",
    },
    "追踪远处的烟或灯光": {
        "risk": 4, "profiles": ["幸存者", "市场", "陷阱"],
        "desc": "可能是营地、集市、求救信号，也可能有人故意吸引访客。",
    },
    "搜索郊区和自然地带": {
        "risk": 2, "profiles": ["自然", "农场", "废车"],
        "desc": "食物与材料并不集中，但尸群较少，天气影响更大。",
    },
    "监听无线电坐标后前往": {
        "risk": 3, "profiles": ["线索", "幸存者", "市场"],
        "desc": "坐标可能过期，也可能是只广播给特定人的暗号。",
    },
}

SITE_NAMES = {
    "商业": ["停电超市", "街角便利店", "百货仓库", "被洗劫的餐馆"],
    "医疗": ["社区诊所", "宠物医院", "药品中转库", "废弃救护站"],
    "住宅": ["封闭公寓", "城中村小院", "养老公寓", "装修中的住宅楼"],
    "工坊": ["汽修厂", "家具作坊", "五金仓", "印刷车间"],
    "隐藏": ["广告牌后的暗门", "没有标记的地下室", "封死的防空洞", "排水渠检修室"],
    "幸存者": ["临时路障", "屋顶信号点", "废车组成的营地", "加油站哨塔"],
    "市场": ["桥洞集市", "旧车站交换点", "河滩夜市", "仓库黑市"],
    "陷阱": ["无人看守的补给箱", "敞开大门的仓库", "循环播放的求救车", "路中央的药箱"],
    "自然": ["河滩芦苇地", "废弃果园", "林间水塔", "公路防护林"],
    "农场": ["温室大棚", "种子仓", "养鸡场", "农机站"],
    "废车": ["连环事故现场", "长途客车", "快递货车", "工程抢险车"],
    "线索": ["疾控临时办公室", "被封锁的实验楼", "新闻转播车", "军方观察点"],
}

SCENE_TEXT = {
    "商业": ["卷帘门只升起半米，里面有购物车自己缓慢滑动。", "收银台上摆着一张写有“拿走可以，别开冷柜”的纸。", "货架被搬成迷宫，显然有人故意改变过路线。"],
    "医疗": ["候诊屏仍显示一个永远不会被叫到的号码。", "药柜贴着两套互相矛盾的隔离标签。", "手术室门从里面用输液架顶住，地面却没有血。"],
    "住宅": ["餐桌上摆着四副碗筷，其中一碗还是温的。", "整栋楼只有一扇窗户每天晚上亮十分钟。", "住户把每个门把手都缠上了不同颜色的毛线。"],
    "工坊": ["空气里有新鲜机油味，工具却按尺寸整齐排列。", "一台自制机器正用自行车链条给电池充电。", "墙上画满失败陷阱的改进图，最后一张还没完成。"],
    "隐藏": ["入口后不是房间，而是一条写满日期的窄廊。", "有人把罐头藏在假墙里，也把一封道歉信藏在最上面。", "门锁完好，通风口却传出断断续续的口琴声。"],
    "幸存者": ["守门人要求每个访客讲一个灾难前的笑话。", "营地把姓名写在鞋底，声称尸体翻过来才能认人。", "这里的人从不问你来自哪里，只问有没有跟踪者。"],
    "市场": ["入口没有招牌，只有三种不同颜色的瓶盖挂在电线上。", "所有摊主同时停下说话，直到你放下武器。", "市场用一首走调童谣作为当天暗号。"],
    "陷阱": ["补给箱太干净，周围灰尘里却没有送来它的脚印。", "求救广播很真实，直到它第三次用完全相同的咳嗽收尾。", "门口尸体的鞋带全被人重新系过。"],
    "自然": ["鸟群突然从一片没有风的芦苇里飞起。", "果树下埋着密封玻璃瓶，每个瓶里有一张天气记录。", "水塔上有人画了一张夸张的怪物地图。"],
    "农场": ["温室里长着一排被起了人名的番茄。", "鸡舍门上写着“鸡比人可信，但不会开锁”。", "拖拉机油箱里装的不是柴油，而是晒干的豆子。"],
    "废车": ["客车每个座位都系着安全带，司机位却放着一束塑料花。", "快递单上的收件地址全部被改成同一个仓库。", "工程车吊臂上挂着一只会随风敲击车门的饭盒。"],
    "线索": ["碎纸机旁堆着来不及销毁的最后一批文件。", "白板上所有名字都被擦掉，只有箭头和时间还在。", "录音设备没有电，磁带却还在缓慢转动。"],
}

MARKET_NAMES = [
    "桥洞赌市", "北环犬舍", "河滩夜市", "旧货场军需站", "白塔劳工市场", "圣心诊所黑市",
    "钟楼铸甲铺", "十三号奇物摊", "长波拍卖场", "地下种子银行", "移动酒馆", "宠物驿站",
]

WEAPONS = {
    "撬棍": {
        "kind": "近战", "damage": 2, "accuracy": 88, "ammo": 0, "noise": 0,
        "stamina": 1, "trait": "稳定，不消耗弹药。",
    },
    "消防斧": {
        "kind": "近战", "damage": 4, "accuracy": 72, "ammo": 0, "noise": 0,
        "stamina": 2, "trait": "重击；对防护感染者额外有效。",
    },
    "手枪": {
        "kind": "枪械", "damage": 5, "accuracy": 72, "ammo": 1, "noise": 2,
        "stamina": 0, "trait": "可靠、弹药消耗低。",
    },
    "左轮手枪": {
        "kind": "枪械", "damage": 7, "accuracy": 68, "ammo": 1, "noise": 3,
        "stamina": 0, "trait": "高单发伤害；对精英感染者有效。",
    },
    "霰弹枪": {
        "kind": "枪械", "damage": 5, "accuracy": 82, "ammo": 2, "noise": 5,
        "stamina": 0, "trait": "命中后同时伤害最多三个目标。",
    },
    "猎枪": {
        "kind": "枪械", "damage": 9, "accuracy": 62, "ammo": 1, "noise": 4,
        "stamina": 0, "trait": "高伤害、穿透护甲；射击技能影响显著。",
    },
    "冲锋枪": {
        "kind": "枪械", "damage": 4, "accuracy": 66, "ammo": 3, "noise": 5,
        "stamina": 0, "trait": "三连发，可分配给多个目标。",
    },
    "弩": {
        "kind": "枪械", "damage": 6, "accuracy": 70, "ammo": 1, "noise": 0,
        "stamina": 1, "trait": "安静；战斗结束有概率回收弹药。",
    },
    "棒球棍": {"kind": "近战", "damage": 3, "accuracy": 84, "ammo": 0, "noise": 0, "stamina": 1, "trait": "击退率高。"},
    "长矛": {"kind": "近战", "damage": 4, "accuracy": 78, "ammo": 0, "noise": 0, "stamina": 1, "trait": "可安全攻击肿胀者。"},
    "砍刀": {"kind": "近战", "damage": 5, "accuracy": 76, "ammo": 0, "noise": 0, "stamina": 2, "trait": "对无甲目标暴击率高。"},
    "电击棍": {"kind": "近战", "damage": 3, "accuracy": 86, "ammo": 1, "noise": 1, "stamina": 1, "trait": "命中可使奔跑者失去一回合。"},
    "链锯": {"kind": "近战", "damage": 8, "accuracy": 74, "ammo": 1, "noise": 6, "stamina": 1, "trait": "高伤害但极吵，使用燃料弹药。"},
    "钉枪": {"kind": "枪械", "damage": 4, "accuracy": 74, "ammo": 1, "noise": 1, "stamina": 0, "trait": "低噪声，工坊常见。"},
    "消音手枪": {"kind": "枪械", "damage": 5, "accuracy": 76, "ammo": 1, "noise": 0, "stamina": 0, "trait": "不增加威胁，稀有。"},
    "双管霰弹枪": {"kind": "枪械", "damage": 8, "accuracy": 78, "ammo": 2, "noise": 6, "stamina": 0, "trait": "同时重创两个目标。"},
    "突击步枪": {"kind": "枪械", "damage": 6, "accuracy": 74, "ammo": 2, "noise": 5, "stamina": 0, "trait": "稳定两连发并穿轻甲。"},
    "轻机枪": {"kind": "枪械", "damage": 5, "accuracy": 62, "ammo": 5, "noise": 8, "stamina": 0, "trait": "压制全体敌人，消耗极大。"},
    "信号枪": {"kind": "枪械", "damage": 3, "accuracy": 80, "ammo": 1, "noise": 4, "stamina": 0, "trait": "点燃目标，也可能引来人类。"},
    "鱼叉枪": {"kind": "枪械", "damage": 7, "accuracy": 64, "ammo": 1, "noise": 0, "stamina": 1, "trait": "安静、可回收弹药、击退。"},
    "燃烧瓶": {"kind": "投掷", "damage": 6, "accuracy": 72, "ammo": 1, "noise": 3, "stamina": 0, "trait": "持续伤害一组敌人。"},
    "土制炸弹": {"kind": "投掷", "damage": 12, "accuracy": 68, "ammo": 1, "noise": 10, "stamina": 0, "trait": "一次性群体爆炸，可能伤到队伍。"},
}

ZOMBIE_TYPES = {
    "游荡者": {"hp": 3, "evasion": 0, "armor": 0, "damage": 1, "trait": "普通感染者。"},
    "奔跑者": {"hp": 2, "evasion": 15, "armor": 0, "damage": 1, "trait": "更难命中，优先攻击。"},
    "防暴感染者": {"hp": 5, "evasion": -5, "armor": 2, "damage": 1, "trait": "护甲减伤；斧和猎枪可穿透。"},
    "肿胀者": {"hp": 7, "evasion": -10, "armor": 0, "damage": 2, "trait": "死亡时可能喷溅，近战危险。"},
    "尖啸者": {"hp": 3, "evasion": 5, "armor": 0, "damage": 1, "trait": "若未优先击杀，可能呼来增援。"},
    "爬行者": {"hp": 2, "evasion": 12, "armor": 0, "damage": 1, "trait": "容易被忽略，攻击腿部。"},
    "消防员感染者": {"hp": 6, "evasion": -8, "armor": 3, "damage": 1, "trait": "厚重防护，怕穿甲和钝击。"},
    "黏液者": {"hp": 5, "evasion": 0, "armor": 0, "damage": 1, "trait": "命中会降低武器命中。"},
    "猎犬感染体": {"hp": 3, "evasion": 22, "armor": 0, "damage": 2, "trait": "高速扑击，可被宠物牵制。"},
    "菌毯宿主": {"hp": 8, "evasion": -12, "armor": 1, "damage": 1, "trait": "缓慢恢复生命，火焰克制。"},
    "寄生群": {"hp": 4, "evasion": 18, "armor": 0, "damage": 1, "trait": "分散小型目标，霰弹和火焰有效。"},
    "铁皮巨汉": {"hp": 15, "evasion": -15, "armor": 4, "damage": 3, "trait": "重装精英，需要穿甲、爆炸或协同控制。"},
    "巢母": {"hp": 22, "evasion": -20, "armor": 2, "damage": 3, "trait": "首领，会孵化寄生群；猎枪伤害不再溢出。"},
    "镜面感染者": {"hp": 9, "evasion": 10, "armor": 1, "damage": 2, "trait": "会模仿人声，干扰队友心情。"},
    "夜行者": {"hp": 10, "evasion": 25, "armor": 0, "damage": 3, "trait": "只在高威胁夜晚出现，强光可克制。"},
}

ARMOR = {
    "便服": {"armor": 0, "evasion": 0, "noise": 0, "trait": "无额外效果。"},
    "厚外套": {"armor": 1, "evasion": -2, "noise": 0, "trait": "轻度防护。"},
    "摩托护具": {"armor": 2, "evasion": 0, "noise": 1, "trait": "均衡轻甲。"},
    "防刺背心": {"armor": 2, "evasion": -2, "noise": 0, "trait": "减少抓咬伤害。"},
    "消防服": {"armor": 3, "evasion": -8, "noise": 1, "trait": "抗火与喷溅。"},
    "防暴甲": {"armor": 4, "evasion": -12, "noise": 2, "trait": "重甲，降低逃跑率。"},
    "军用插板甲": {"armor": 5, "evasion": -10, "noise": 2, "trait": "高防御，稀有。"},
    "铁片拼装甲": {"armor": 4, "evasion": -18, "noise": 4, "trait": "可制作但非常吵。"},
    "轻型隔离服": {"armor": 1, "evasion": 2, "noise": 0, "trait": "减少毒雾与样本事件风险。"},
    "蜂农面罩": {"armor": 1, "evasion": -1, "noise": 0, "trait": "克制寄生群和喷溅。"},
    "吉祥物玩偶服": {"armor": 2, "evasion": -15, "noise": 1, "trait": "僵尸较难咬透，但队友心情莫名上升。"},
}

GEAR = {
    "登山包": {"trait": "探索携带 +3。"},
    "夜视仪": {"trait": "夜间侦察与命中提高。"},
    "强光手电": {"trait": "克制夜行者，消耗电池弹药。"},
    "撬锁工具": {"trait": "隐藏地点额外战利品。"},
    "急救腰包": {"trait": "战斗后可立即治疗一次。"},
    "无线电测向器": {"trait": "更容易找到派系与主线坐标。"},
    "折叠推车": {"trait": "携带 +5，但逃跑率降低。"},
    "诱饵音箱": {"trait": "可改变尸群目标，增加远处威胁。"},
    "净水滤芯": {"trait": "断水与疾病事件更安全。"},
    "便携太阳能板": {"trait": "设施无需额外燃料。"},
    "拍立得": {"trait": "对话库增加照片话题，改善心情。"},
    "坏掉的测谎仪": {"trait": "谈判时偶尔给出完全不可靠的提示。"},
}

PETS = {
    "灰耳": {"species": "德国牧羊犬", "hp": 5, "attack": 3, "scout": 3, "food": 1, "skill": "牵制"},
    "算盘": {"species": "边境牧羊犬", "hp": 4, "attack": 2, "scout": 4, "food": 1, "skill": "搜索"},
    "罐头": {"species": "橘猫", "hp": 3, "attack": 1, "scout": 2, "food": 1, "skill": "发现藏匿点"},
    "将军": {"species": "鹅", "hp": 3, "attack": 2, "scout": 2, "food": 1, "skill": "夜间警报"},
    "扳手": {"species": "山羊", "hp": 5, "attack": 3, "scout": 1, "food": 1, "skill": "撞击"},
    "邮票": {"species": "信鸽群", "hp": 2, "attack": 0, "scout": 4, "food": 1, "skill": "派系通信"},
    "静电": {"species": "乌鸦", "hp": 2, "attack": 1, "scout": 4, "food": 1, "skill": "标记尸群"},
    "拖拉机": {"species": "迷你猪", "hp": 4, "attack": 1, "scout": 2, "food": 2, "skill": "嗅出食物"},
    "皇后": {"species": "巨蜥", "hp": 4, "attack": 3, "scout": 1, "food": 1, "skill": "恐吓人类"},
    "收据": {"species": "浣熊", "hp": 3, "attack": 1, "scout": 3, "food": 1, "skill": "偷取小物"},
}

FACTIONS = {
    "自由商队": "重视契约与利润，控制多数公开集市。",
    "白塔治安队": "以秩序为名征用劳力，拥有武装检查站。",
    "河湾互助会": "由多个小型基地组成，愿意共享水和农作物。",
    "拾荒圣徒": "把危险物品视为启示，经营奇物与仪式。",
    "旧城广播联盟": "控制无线电中继，重视消息真实性。",
}

# 不在说明中展示。玩家必须通过探索和特定队友逐步触发。
STORY_BEATS = [
    {"id": "trace_1", "min_day": 8, "intel": 2, "requires": [], "title": "被删掉的日期"},
    {"id": "trace_2", "min_day": 22, "intel": 6, "requires": ["trace_1"], "title": "两种病历"},
    {"id": "trace_3", "min_day": 40, "intel": 11, "requires": ["trace_2"], "title": "静默样本"},
    {"id": "trace_4", "min_day": 61, "intel": 17, "requires": ["trace_3"], "title": "封锁前的命令"},
    {"id": "trace_5", "min_day": 80, "intel": 24, "requires": ["trace_4"], "title": "仍然有效的方法"},
]

STORYLINES = {
    "cold_chain": {
        "name": "冷链断点",
        "hook": "灾难前夜，多辆无牌冷藏车同时驶入城区。",
        "beats": ["错误温度", "空白收货人", "活着的样本", "第三座冷库", "逆向运输", "零下四度的选择"],
    },
    "echo": {
        "name": "回声协议",
        "hook": "所有救援广播里都藏着同一段听不见的低频脉冲。",
        "beats": ["第十七分钟", "没有播音员", "模仿者", "中继塔名单", "沉默区", "最后一次广播"],
    },
    "white_rain": {
        "name": "白雨",
        "hook": "第一次感染潮之前，城南曾下过一场只持续十一分钟的白色细雨。",
        "beats": ["屋檐残留", "被改写的气象表", "植物园病斑", "净水厂夜班", "云层下的航线", "无雨的预报"],
    },
    "convoy": {
        "name": "十四号车队",
        "hook": "封锁记录中存在一支从未抵达、也从未宣布失踪的车队。",
        "beats": ["少一辆车", "重复的驾驶员", "公路边的儿童画", "封死的服务区", "返程燃料", "没有终点的路线"],
    },
}

# 跨周目彩蛋。触发后写入 saves/collection.json，同一安装目录中不再重复出现。
# source 决定它可能在哪类行动中出现；chance 是在“本次命中彩蛋判定”后的相对权重。
EASTER_EGGS = [
    {"id": "weapon_spoon", "source": "weapon", "name": "末日餐具学", "rarity": "稀有", "text": "你找到一把被磨成刺刀的长柄汤勺，柄上刻着：文明从不用手抓罐头开始。", "reward": {"materials": 1}},
    {"id": "weapon_confetti", "source": "weapon", "name": "庆典模式", "rarity": "珍奇", "text": "信号枪射出的不是照明弹，而是一团受潮彩纸。附近的僵尸和你都愣了半秒。", "reward": {"morale": 4}},
    {"id": "weapon_duck", "source": "weapon", "name": "战术橡皮鸭", "rarity": "罕见", "text": "枪托夹层里塞着一只橡皮鸭。捏响后，远处传来另一只鸭子的回应。", "reward": {"ammo": 1}},
    {"id": "weapon_manual", "source": "weapon", "name": "反向说明书", "rarity": "稀有", "text": "一本武器说明书把“不要对准自己”印了七遍，唯一的操作说明却被撕走了。", "reward": {"intel": 1}},
    {"id": "weapon_baguette", "source": "weapon", "name": "昨日法棍", "rarity": "普通", "text": "一根硬到能当棍棒的法棍奇迹般没有发霉。你决定不测试它的伤害。", "reward": {"food": 1}},
    {"id": "armor_tie", "source": "armor", "name": "最后的着装规范", "rarity": "稀有", "text": "防暴甲里面端正系着一条领带，标签写着“周五可穿休闲装”。", "reward": {"morale": 3}},
    {"id": "armor_bell", "source": "armor", "name": "潜行克星", "rarity": "普通", "text": "一套重甲脚踝上绑着猫铃。没人承认这是自己的改装。", "reward": {"materials": 1}},
    {"id": "armor_glitter", "source": "armor", "name": "闪耀生还者", "rarity": "珍奇", "text": "你掀开披风，亮片反射出一整面彩虹。防护一般，自信极强。", "reward": {"morale": 5}},
    {"id": "armor_receipt", "source": "armor", "name": "七日无理由", "rarity": "罕见", "text": "插板甲口袋里有张末日前一天的退货小票，退货理由是“可能用不上”。", "reward": {"trade_goods": 1}},
    {"id": "gear_tamagotchi", "source": "gear", "name": "电子生命", "rarity": "稀有", "text": "一只电子宠物还活着，而且对你连续一百天没喂它这件事非常生气。", "reward": {"morale": 4}},
    {"id": "gear_printer", "source": "gear", "name": "世界最后一页", "rarity": "珍奇", "text": "便携打印机吐出一页纸：请更换青色墨盒。它拒绝打印任何更重要的东西。", "reward": {"materials": 2}},
    {"id": "gear_compass", "source": "gear", "name": "指向午饭", "rarity": "罕见", "text": "坏指南针不指北，只坚定地指向最近的一罐午餐肉。", "reward": {"food": 2}},
    {"id": "gear_camera", "source": "gear", "name": "多出来的人", "rarity": "传说", "text": "拍立得合影里，队伍最后多站着一个戴纸袋的人。回头时那里只有墙。", "reward": {"intel": 2}},
    {"id": "gear_usb", "source": "gear", "name": "重要资料.zip", "rarity": "稀有", "text": "U盘里只有三百张猫图和一个名为“真的重要资料”的空文件夹。", "reward": {"morale": 3}},
    {"id": "market_coupon", "source": "market", "name": "过期优惠券", "rarity": "普通", "text": "摊主郑重收下过期十年的第二杯半价券，并找给你一颗薄荷糖。", "reward": {"food": 1}},
    {"id": "market_oracle", "source": "market", "name": "罐头占卜", "rarity": "罕见", "text": "占卜师摇晃罐头听未来：你的命运含盐量偏高。", "reward": {"morale": 3}},
    {"id": "market_tax", "source": "market", "name": "末日税务局", "rarity": "稀有", "text": "一个戴袖章的人要征收“活着附加税”。摊主们把他连桌子一起抬了出去。", "reward": {"trade_goods": 1}},
    {"id": "market_vending", "source": "market", "name": "自动售货机之王", "rarity": "珍奇", "text": "集市中央供着一台仍能制冷的售货机。它只接受游戏代币，并被尊称为陛下。", "reward": {"food": 2}},
    {"id": "market_insurance", "source": "market", "name": "僵尸险", "rarity": "稀有", "text": "保险摊承诺被咬后赔两罐豆子，前提是投保人亲自来签收。", "reward": {"morale": 2}},
    {"id": "zombie_helmet", "source": "zombie", "name": "安全第一", "rarity": "普通", "text": "感染者戴着安全帽，帽上贴着“连续零天无事故”。", "reward": {"materials": 1}},
    {"id": "zombie_delivery", "source": "zombie", "name": "超时配送", "rarity": "罕见", "text": "感染者背包里的外卖仍然温热，备注是“放门口，不要敲门”。", "reward": {"food": 2}},
    {"id": "zombie_dancer", "source": "zombie", "name": "节拍感染", "rarity": "珍奇", "text": "尖啸者的叫声恰好卡在音乐节拍上，尸群短暂完成了一段整齐舞步。", "reward": {"morale": 4}},
    {"id": "zombie_badge", "source": "zombie", "name": "本月员工", "rarity": "稀有", "text": "铁皮巨汉胸前别着“本月最佳员工”，背面写着奖励：带薪休假一天。", "reward": {"trade_goods": 1}},
    {"id": "zombie_apology", "source": "zombie", "name": "非常抱歉", "rarity": "传说", "text": "镜面感染者模仿人声说出一句完整的“对不起”，随后再也没有开口。", "reward": {"intel": 2}},
    {"id": "pet_goose", "source": "pet", "name": "基地真正的首领", "rarity": "普通", "text": "将军叼走你的值班表，重新安排了所有人的巡逻。没人敢反对。", "reward": {"defense": 2}},
    {"id": "pet_cat", "source": "pet", "name": "罐头的罐头", "rarity": "罕见", "text": "橘猫罐头从墙洞拖回一个猫罐头，并拒绝解释供应链。", "reward": {"food": 2}},
    {"id": "pet_pigeon", "source": "pet", "name": "已读不回", "rarity": "稀有", "text": "信鸽带回一张纸条，上面只有一个潦草的“收到”。", "reward": {"intel": 1}},
    {"id": "pet_raccoon", "source": "pet", "name": "职业采购员", "rarity": "珍奇", "text": "浣熊收据带回三颗螺丝、一只袜子和完整购物小票。总价为零。", "reward": {"materials": 2}},
    {"id": "pet_lizard", "source": "pet", "name": "微型龙骑士", "rarity": "传说", "text": "有人给巨蜥做了纸板翅膀。它站在弹药箱上接受了全基地的效忠。", "reward": {"morale": 6}},
    {"id": "explore_wifi", "source": "explore", "name": "最后的 Wi-Fi", "rarity": "稀有", "text": "手机突然连上名为“世界末日也不给密码”的网络，信号满格，没有互联网。", "reward": {"intel": 1}},
    {"id": "explore_skeleton", "source": "explore", "name": "教程骷髅", "rarity": "普通", "text": "路边骷髅怀里抱着纸牌：按任意键翻滚。你在终端里找不到翻滚键。", "reward": {"morale": 2}},
    {"id": "explore_fridge", "source": "explore", "name": "冰箱之光", "rarity": "罕见", "text": "整栋楼断电，唯独一台空冰箱开门时还会亮灯。", "reward": {"materials": 1}},
    {"id": "explore_mannequin", "source": "explore", "name": "橱窗换班", "rarity": "珍奇", "text": "你第二次经过橱窗时，模特换了姿势，手里还多了一张写着“别紧张”的纸。", "reward": {"intel": 1}},
    {"id": "explore_phone", "source": "explore", "name": "未接来电", "rarity": "传说", "text": "没有电池的座机响了一声。听筒里，一个声音准确叫出你的名字。", "reward": {"intel": 2}},
    {"id": "explore_movie", "source": "explore", "name": "片尾之后", "rarity": "稀有", "text": "电影院仍循环播放灾难片片尾，保洁名单里有你一名队友的名字。", "reward": {"intel": 1}},
    {"id": "survivor_birthday", "source": "survivor", "name": "末日生日歌", "rarity": "普通", "text": "没人知道今天是谁生日，于是大家给基地的门唱了生日歌。", "reward": {"morale": 5}},
    {"id": "survivor_chess", "source": "survivor", "name": "缺失的棋子", "rarity": "罕见", "text": "两名队友用药瓶下棋，输了的人坚持说自己玩的是围棋。", "reward": {"morale": 3}},
    {"id": "survivor_radio", "source": "survivor", "name": "点歌台", "rarity": "稀有", "text": "无线电收到点歌请求，署名竟是基地里一只宠物。", "reward": {"morale": 4}},
    {"id": "survivor_clone", "source": "survivor", "name": "同名同姓", "rarity": "珍奇", "text": "陌生广播完整念出一名队友的姓名和履历，最后说：冒牌货就在你们中间。", "reward": {"intel": 2}},
    {"id": "survivor_vote", "source": "survivor", "name": "严肃表决", "rarity": "普通", "text": "基地用半小时投票决定最后一卷卫生纸横着挂还是竖着挂。弃权票获胜。", "reward": {"morale": 2}},
    {"id": "base_coffee", "source": "base", "name": "文明复兴", "rarity": "罕见", "text": "你们修好一台咖啡机。它只会出热水，但所有人仍排队鼓掌。", "reward": {"morale": 4}},
    {"id": "base_door", "source": "base", "name": "禁止僵尸入内", "rarity": "普通", "text": "有人在基地门口挂上“禁止僵尸入内”。当晚袭击次数没有变化。", "reward": {"defense": 1}},
    {"id": "base_socks", "source": "base", "name": "失踪袜子案", "rarity": "稀有", "text": "仓库盘点发现所有左脚袜子消失。浣熊有重大嫌疑，但拒绝配合调查。", "reward": {"intel": 1}},
    {"id": "base_trophy", "source": "base", "name": "优秀基地奖", "rarity": "珍奇", "text": "围墙外出现一座昨夜还不存在的奖杯：年度最不容易被吃掉基地。", "reward": {"morale": 5}},
    {"id": "story_redacted", "source": "story", "name": "删节者", "rarity": "稀有", "text": "档案里所有机密都被涂黑，唯独涂黑笔的采购发票完整保留。", "reward": {"intel": 1}},
    {"id": "story_wrongcity", "source": "story", "name": "寄错城市", "rarity": "珍奇", "text": "绝密命令最后一页写着另一座城市的名字。有人在旁边批注：将错就错。", "reward": {"intel": 2}},
    {"id": "story_devnote", "source": "story", "name": "不该存在的批注", "rarity": "传说", "text": "一份旧记录边缘写着：如果玩家看到这里，说明概率系统又坏了。", "reward": {"morale": 4, "intel": 1}},
    {"id": "night_knock", "source": "night", "name": "三短一长", "rarity": "稀有", "text": "夜里有人敲出三短一长。守卫开门后，外面只有一份热腾腾的菜单。", "reward": {"food": 1}},
    {"id": "night_moon", "source": "night", "name": "备用月亮", "rarity": "传说", "text": "云层裂开时，所有人都看见两个月亮。眨眼后只剩一个，但照片里仍有两个。", "reward": {"intel": 2}},
    {"id": "night_lullaby", "source": "night", "name": "尸群摇篮曲", "rarity": "珍奇", "text": "远处尸群发出有规律的低鸣，一名队友听着它睡了灾难后最安稳的一觉。", "reward": {"morale": 5}},
]
