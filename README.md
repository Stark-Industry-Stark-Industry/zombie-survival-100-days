# 《百日之后》v2.1

一款在 Windows 终端运行的 100 天文字丧尸生存游戏。探索未知地点、经营基地、招募队友、
与幸存者派系往来，并在四条随机主线中调查灾难真相。

## 下载与安装

你可以从仓库右侧的 **Releases** 下载 v2.1 完整压缩包，解压后双击 `开始游戏.bat`。
也可以直接克隆源码：

```powershell
git clone https://github.com/Stark-Industry-Stark-Industry/zombie-survival-100-days.git
cd zombie-survival-100-days
python game.py
```

## 运行

```powershell
python game.py
python game.py --new
python game.py --no-color
python game.py --collection
```

## v2.1 内容规模

- 完整 100 天，三种难度、六种职业、六种基地
- 22 种武器、11 种防具、12 种功能装备
- 15 类感染者，包括高生命、高护甲精英与首领
- 10 种可指挥宠物
- 12 个功能完全不同的集市
- 24 名候选队友；同一局不会保证全部出现
- 9 类基地岗位、个人心情/信任/性格、对话与内乱
- 5 个其他幸存者派系
- 4 条开局随机加载的主线，每条包含连续伏笔节点
- 50 个低概率彩蛋，覆盖武器、防具、装备、集市、僵尸、宠物、人物、基地、剧情与夜晚
- 独立的跨周目收藏库：首次发现后永久排除，不会在后续新游戏中重复出现
- 未知探索、队伍自由编成、战斗、交易、设施、农田与自动存档

彩蛋收藏保存在 `saves/collection.json`，与单局自动存档分离。删除单局存档不会
清空收藏；只有主动删除该收藏文件才会重置进度。主菜单和
`python game.py --collection` 都可以查看收藏库，未发现条目保持隐藏。

完整玩法、公开剧情背景和系统资料见
[`docs/百日之后_v2.1_剧情介绍与系统百科.docx`](docs/百日之后_v2.1_剧情介绍与系统百科.docx)。

## 测试

```powershell
python -m unittest -v
python game.py --simulate 20 --no-color
```

自动模拟不会修改玩家存档。v1.x 存档与 v2.0 不兼容。
