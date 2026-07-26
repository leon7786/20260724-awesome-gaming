# 封面图系统对比：games.json cover vs pics/poster

> 分析时间：2026-07-27

## 一、两个系统概述

| 维度 | games.json cover（当前在用） | pics/poster（本地备用） |
|------|--------------------------|----------------------|
| 用途 | 首页 + 详情页 hero 封面 | 本地静态海报文件（未接入前端） |
| 总数 | 375 | 93 张 |
| 分辨率 | Steam lib 300×450 / LB 281px | **600×900 高清** |
| 来源 | Steam CDN + LaunchBox | Steam CDN (library_600x900_2x.jpg) |
| 非Windows游戏 | 75款用LB（多数281px） | 0款（无Switch/怀旧游戏） |

## 二、pics/poster 已有覆盖（#205–#374）

- 总需覆盖：170 款（#205–#374）
- 已有海报：88 款 ✓
- 缺少海报：82 款 ✗

### 已有海报的游戏

- **#210** 堡垒 (`210_Bastion.jpg`)
- **#211** 使命召唤：黑色行动3 (`211_Call_of_Duty_Black_Ops_III.jpg`)
- **#212** 人类：一败涂地 (`212_Human_Fall_Flat.jpg`)
- **#213** 光环无限 (`Halo_Infinite_213.jpg`)
- **#214** 木卫四协议 (`214_The_Callisto_Protocol.jpg`)
- **#215** 植物大战僵尸 (`215_Plants_vs_Zombies.jpg`)
- **#216** 英雄无敌 III (`216_Heroes_of_Might_and_Magic_III.jpg`)
- **#217** 无人深空 (`217_No_Mans_Sky.jpg`)
- **#218** 绝地求生 (`218_PUBG_Battlegrounds.jpg`)
- **#219** 刺猬索尼克 (`219_Sonic_the_Hedgehog.jpg`)
- **#221** 怪物猎人：荒野 (`221_Monster_Hunter_Wilds.jpg`)
- **#222** 第一日程 (`222_Schedule_I.jpg`)
- **#224** 废品回收 (`224_REPO.jpg`)
- **#228** 绝地潜兵 2 (`228_Helldivers_2.jpg`)
- **#229** 最终幻想 VII：重生 (`229_Final_Fantasy_VII_Rebirth.jpg`)
- **#230** 流放之路 2 (EA) (`230_Path_of_Exile_2.jpg`)
- **#231** 第一后裔 (`231_The_First_Descendant.jpg`)
- **#232** 生化危机 4 重制版 (`232_Resident_Evil_4_2023.jpg`)
- **#233** 致命公司 (`233_Lethal_Company.jpg`)
- **#234** 披萨塔 (`234_Pizza_Tower.jpg`)
- **#236** 师父 (`236_Sifu.jpg`)
- **#238** 怪物猎人：崛起 曙光 (`238_Monster_Hunter_Rise_Sunbreak.jpg`)
- **#244** 糖豆人：终极淘汰赛 (`244_Fall_Guys.jpg`)
- **#245** 原神 (`Genshin_Impact_245.jpg`)
- **#247** 漫威蜘蛛侠 1 (`247_Marvels_Spider-Man.jpg`)
- **#248** 掠食 (2017) (`248_Prey.jpg`)
- **#249** 巫师 3：血与酒 (`249_The_Witcher_3_-_Blood_and_Wine.jpg`)
- **#250** 神秘海域 4：盗贼末路 (`250_Uncharted_4_A_Thiefs_End.jpg`)
- **#251** 毁灭战士 (2016) (`251_DOOM_2016.jpg`)
- **#252** 内部 (`252_Inside.jpg`)
- **#253** 女神异闻录 5 (日版) (`253_Persona_5_JP.jpg`)
- **#254** 文明 6 (`254_Civilization_VI.jpg`)
- **#255** 火箭联盟 (`255_Rocket_League.jpg`)
- **#257** 铲子骑士 (`257_Shovel_Knight.jpg`)
- **#259** 异形：隔离 (`259_Alien_Isolation.jpg`)
- **#260** 晶体管 (`260_Transistor.jpg`)
- **#261** 最后的生还者 1 (`261_The_Last_of_Us.jpg`)
- **#262** 流放之路 1 (`262_Path_of_Exile.jpg`)
- **#264** 雨中冒险 1 (`264_Risk_of_Rain_1.jpg`)
- **#265** 古墓丽影 9 (重启) (`265_Tomb_Raider_2013.jpg`)
- **#266** 反恐精英：全球攻势 (`266_CSGO.jpg`)
- **#267** 激战 2 (`267_Guild_Wars_2.jpg`)
- **#270** 星际争霸 II：自由之翼 (`270_StarCraft_II_Wings_of_Liberty.jpg`)
- **#273** 死亡空间 1 (`273_Dead_Space_1.jpg`)
- **#274** 求生之路 1 (`274_Left_4_Dead_1.jpg`)
- **#275** 传送门 1 (`275_Portal_1.jpg`)
- **#276** 使命召唤 4：现代战争 (`276_Call_of_Duty_4_Modern_Warfare.jpg`)
- **#277** 巫师 1 (`277_The_Witcher_1.jpg`)
- **#278** 孤岛危机 1 (`278_Crysis_1.jpg`)
- **#280** 大神 (`280_Okami.jpg`)
- **#281** 生化危机 4 (原版) (`281_Resident_Evil_4_Original.jpg`)
- **#284** 文明 4 (`284_Civilization_IV.jpg`)
- **#286** 潜龙谍影 3：食蛇者 (`286_Metal_Gear_Solid_3_Snake_Eater.jpg`)
- **#289** 侠盗猎车手 III (`289_Grand_Theft_Auto_III.jpg`)
- **#290** 寂静岭 2 (`290_Silent_Hill_2.jpg`)
- **#291** 杀出重围 1 (`291_Deus_Ex_1.jpg`)
- **#293** 反恐精英 1.6 (`293_Counter-Strike_16.jpg`)
- **#295** 博德之门 II：安姆的阴影 (`295_Baldurs_Gate_II_Shadows_of_Amn.jpg`)
- **#298** 帝国时代 II：帝王世纪 (`298_Age_of_Empires_II_The_Age_of_Kings.jpg`)
- **#299** 半条命 1 (`299_Half-Life.jpg`)
- **#300** 潜龙谍影 1 (`300_Metal_Gear_Solid_1.jpg`)
- **#301** 星际争霸 1 (`301_StarCraft.jpg`)
- **#307** 最终幻想 VII (原版) (`307_Final_Fantasy_VII_Original.jpg`)
- **#311** 时空之轮 (`311_Chrono_Trigger.jpg`)
- **#313** 毁灭战士 (1993) (`313_DOOM_1993.jpg`)
- **#314** 街头霸王 II (`314_Street_Fighter_II.jpg`)
- **#317** 巫师2：国王刺客 (`317_The_Witcher_2_Assassins_of_Kings.jpg`)
- **#318** 双影奇境 (`318_Split_Fiction.jpg`)
- **#319** 刺客信条：起源 (`319_Assassins_Creed_Origins.jpg`)
- **#320** 刺客信条：英灵殿 (`320_Assassins_Creed_Valhalla.jpg`)
- **#321** 刺客信条：幻景 (`321_Assassins_Creed_Mirage.jpg`)
- **#322** 刺客信条：枭雄 (`322_Assassins_Creed_Syndicate.jpg`)
- **#323** 刺客信条：大革命 (`323_Assassins_Creed_Unity.jpg`)
- **#324** 孤岛惊魂 4 (`324_Far_Cry_4.jpg`)
- **#325** 孤岛惊魂 5 (`325_Far_Cry_5.jpg`)
- **#326** 孤岛惊魂 6 (`326_Far_Cry_6.jpg`)
- **#328** 刺客信条2 (`328_Assassins_Creed_II.jpg`)
- **#330** 刺客信条4：黑旗 (`330_Assassins_Creed_IV_Black_Flag.jpg`)
- **#332** 使命召唤：现代战争 II 2022 (`332_Call_of_Duty_Modern_Warfare_II.jpg`)
- **#333** 使命召唤：先锋 (`333_Call_of_Duty_Vanguard.jpg`)
- **#335** 使命召唤：二战 (`335_Call_of_Duty_WWII.jpg`)
- **#336** 使命召唤：无限战争 (`336_Call_of_Duty_Infinite_Warfare.jpg`)
- **#337** 使命召唤：高级战争 (`337_Call_of_Duty_Advanced_Warfare.jpg`)
- **#338** 使命召唤：幽灵 (`338_Call_of_Duty_Ghosts.jpg`)
- **#339** 使命召唤：现代战争 2 (`339_Call_of_Duty_Modern_Warfare_2.jpg`)
- **#340** 使命召唤：战争世界 (`340_Call_of_Duty_World_at_War.jpg`)
- **#341** 使命召唤 2 (`341_Call_of_Duty_2.jpg`)
- **#342** 使命召唤 1 (`342_Call_of_Duty.jpg`)

### 缺少海报的游戏

- **#205** 小小大星球 | LittleBigPlanet
- **#206** 密特罗德Prime 重制版 | Metroid Prime Remastered
- **#207** 恶魔之魂 重制版 | Demon's Souls
- **#208** 旺达与巨像 | Shadow of the Colossus
- **#209** 暗黑破坏神3 | Diablo III
- **#220** 使命召唤：现代战争3 | Call of Duty: Modern Warfare 3
- **#223** 山巅 | PEAK
- **#225** ARC 袭兵 | ARC Raiders
- **#226** 寂静岭 f | Silent Hill f
- **#227** 宇宙机器人 | Astro Bot
- **#235** 蚕茧 | Cocoon
- **#237** 漫威瞬战超能 | Marvel Snap
- **#239** 猎天使魔女 3 | Bayonetta 3
- **#240** 银河战士：生存恐惧 | Metroid Dread
- **#241** 永劫无间 | NARAKA: BLADEPOINT
- **#242** 最后的生还者 第二部 | The Last of Us Part II
- **#243** 恶魔之魂 重制版 | Demon's Souls Remake
- **#246** 路易吉洋馆 3 | Luigi's Mansion 3
- **#256** 猎天使魔女 2 | Bayonetta 2
- **#258** 炉石传说 | Hearthstone
- **#263** 雷曼：传奇 | Rayman Legends
- **#268** 神秘海域 3：德雷克的诡计 | Uncharted 3: Drake's Deception
- **#269** 荒野大镖客：救赎 1 | Red Dead Redemption 1
- **#271** 神秘海域 2：纵横四海 | Uncharted 2: Among Thieves
- **#272** 潜龙谍影 4 | Metal Gear Solid 4: Guns of the Patriots
- **#279** 上古卷轴 4：湮没 | The Elder Scrolls IV: Oblivion
- **#282** 战神 1 | God of War 1
- **#283** 鬼泣 3 | Devil May Cry 3
- **#285** 魔兽世界 | World of Warcraft
- **#287** 光环 2 | Halo 2
- **#288** 暗爆破坏神 II：毁灭之王 | Diablo II: Lord of Destruction
- **#292** 模拟人生 1 | The Sims 1
- **#294** 暗黑破坏神 II | Diablo II
- **#296** 放浪冒险谭 | Vagrant Story
- **#297** 刀魂 / 剑魂 1 | Soulcalibur
- **#302** 辐射 2 | Fallout 2
- **#303** 异度装甲 | Xenogears
- **#304** 生化危机 2 (原版) | Resident Evil 2 (1998)
- **#305** 侠盗猎车手 1 | Grand Theft Auto 1
- **#306** 恶魔城：月下夜想曲 | Castlevania: Symphony of the Night
- **#308** 007 黄金眼 | GoldenEye 007
- **#309** 暗黑破坏神 1 | Diablo 1
- **#310** 生化危机 1 (原版) | Resident Evil 1 (1996)
- **#312** 超级银河战士 | Super Metroid
- **#315** 俄罗斯方块 (FC/GB版) | Tetris (1984/1989)
- **#316** 吃豆人 | Pac-Man
- **#327** 刺客信条1 | Assassin's Creed
- **#329** 刺客信条3：高清重制版 | Assassin's Creed III Remastered
- **#331** 使命召唤：黑色行动 6 | Call of Duty: Black Ops 6
- **#334** 使命召唤：黑色行动 冷战 | Call of Duty: Black Ops Cold War
- **#343** 超级马力欧：奥德赛 | Super Mario Odyssey
- **#344** 塞尔达传说：旷野之息 | The Legend of Zelda: Breath of the Wild
- **#345** 塞尔达传说：王国之泪 | The Legend of Zelda: Tears of the Kingdom
- **#346** 任天堂明星大乱斗 特别版 | Super Smash Bros. Ultimate
- **#347** 超级马力欧3D世界 | Super Mario 3D World
- **#348** 马力欧赛车8豪华版 | Mario Kart 8 Deluxe
- **#349** 集合啦！动物森友会 | Animal Crossing: New Horizons
- **#350** Wii运动 | Wii Sports
- **#351** 超级马力欧兄弟 | Super Mario Bros.
- **#352** 宝可梦 红/蓝 | Pokémon Red/Blue
- **#353** 纸片马力欧：千年之门 重制版 | Paper Mario: The Thousand-Year Door (Remake)
- **#354** 超级马力欧兄弟 惊奇 | Super Mario Bros. Wonder
- **#355** GT赛车 7 | Gran Turismo 7
- **#356** 异度神剑 3 | Xenoblade Chronicles 3
- **#357** 火焰之纹章：风花雪月 | Fire Emblem: Three Houses
- **#358** 血源诅咒 | Bloodborne
- **#359** 超级马力欧创作家 | Super Mario Maker
- **#360** 马力欧赛车 8 (原版) | Mario Kart 8 (Wii U)
- **#361** 超级马力欧银河 2 | Super Mario Galaxy 2
- **#362** 战神 3 | God of War III
- **#363** 超级马力欧银河 1 | Super Mario Galaxy 1
- **#364** 任天堂明星大乱斗DX | Super Smash Bros. Melee
- **#365** 塞尔达传说：姆吉拉的假面 | The Legend of Zelda: Majora's Mask
- **#366** 塞尔达传说：时之笛 | The Legend of Zelda: Ocarina of Time
- **#367** 超级马力欧 64 | Super Mario 64
- **#368** 宝可梦 红/蓝 | Pokémon Red / Blue
- **#369** 超级马力欧耀西岛 | Super Mario World 2: Yoshi's Island
- **#370** 超级马力欧赛车 (初代) | Super Mario Kart
- **#371** 超级马力欧世界 | Super Mario World
- **#372** 塞尔达传说：众神的三角力量 | The Legend of Zelda: A Link to the Past
- **#373** 超级马力欧兄弟 3 | Super Mario Bros. 3
- **#374** 超级马力欧兄弟 1 | Super Mario Bros. 1

## 三、取长补短方案

### 短处 → 长处对应

| 问题 | 现状 | 解决方案 |
|------|------|---------|
| LB 281px 模糊 | 75款非Windows游戏封面模糊 | 用 poster 替换 LB 低清封面 |
| 海报覆盖率低 | 82款缺 poster | 从 Steam CDN/library 批量补全 |
| 两套数据不同步 | games.json 用远程URL，poster 是本地文件 | 统一用一个 600×900 高清源 |
| 非Windows游戏无 Steam 图 | 32款纯主机游戏无 600×900 | 用 LB 高清图替代（目前只有4款高清） |

### 建议优先级

1. **立即**：用现有 93 张 poster 替换 games.json 中的低清 LB 封面（7款已可替换）
2. **短期**：批量下载 82 款缺失海报（优先 #205–#342 的 Steam 游戏）
3. **中期**：非Windows游戏（#343–#374）用 LB 高清图批量替换 281px 缩略图
4. **长期**：统一封面源为 600×900，废弃 281px LB 缩略图