# Steam 商店页面布局分析 - 黑神话：悟空 (appid: 2358720)

## 页面整体结构

Steam 商店页面采用经典的左右分栏布局，主要分为以下几个区域：

---

## 1. 顶部导航栏 (Header)

**位置**: 页面最顶部，固定显示

**内容**:
- Steam Logo
- 主导航菜单：商店、社区、关于、客服
- 右侧操作区：安装 Steam、登录、语言选择

**功能**: 全局导航，用户可以在不同区域间切换

---

## 2. 面包屑导航 (Breadcrumb)

**位置**: 导航栏下方

**内容**: 
```
所有游戏 > 动作游戏 > Black Myth: Wukong
```

**功能**: 显示当前页面在游戏分类中的位置

---

## 3. 游戏标题区 (Title Area)

**位置**: 页面主体顶部

**内容**:
- 游戏名称：Black Myth: Wukong
- 社区中心链接

**样式**: 大字号标题，醒目显示

---

## 4. 左侧主内容区 (Left Column - 约65%宽度)

### 4.1 媒体展示区 (Media Section)

**位置**: 标题下方，左侧主区域

**内容**:
- 视频播放器（支持多个视频切换）
- 截图轮播（横向滚动）
- 媒体缩略图选择器

**功能**: 展示游戏视觉内容，支持视频和截图切换

### 4.2 购买区域 (Purchase Area)

**位置**: 媒体区下方

**内容**:
```
Buy Black Myth: Wukong
$59.99 USD
[Add to Cart]

Buy Black Myth: Wukong Digital Deluxe Edition
$69.99 USD
[Add to Cart]

Content For This Game
- Black Myth: Wukong Deluxe Edition Upgrade ($9.99)
- Black Myth: Wukong Soundtrack Selection ($9.99)
[Add all DLC to Cart]
```

**功能**: 展示游戏价格、版本、DLC，提供购买按钮

### 4.3 关于此游戏 (About This Game)

**位置**: 购买区域下方

**内容**:
- 游戏简介（支持富文本、图片、视频）
- 游戏特色介绍
- 系统要求概览

**样式**: 长文本区域，支持图文混排

### 4.4 系统需求 (System Requirements)

**位置**: 关于此游戏下方

**内容**:
- 最低配置要求
- 推荐配置要求
- 分平台显示（Windows/Mac/Linux）

**格式**: 表格形式，清晰对比

### 4.5 用户评测 (Customer Reviews)

**位置**: 页面底部

**内容**:
```
ENGLISH REVIEWS:
Very Positive (69,794 reviews)

Total reviews in all languages:
875,116 - Overwhelmingly Positive

Recent Reviews in all languages:
1,727 - Very Positive
```

**功能**: 
- 显示总体评价
- 分语言评价统计
- 评测筛选器（按语言、游玩时间等）
- 用户评论列表

### 4.6 类似游戏推荐 (Recommended)

**位置**: 评测区域附近

**内容**: 
- 横向滚动的相似游戏卡片
- 包含游戏封面、名称、价格

**功能**: 推荐相似游戏，增加用户停留时间

---

## 5. 右侧信息面板 (Right Column - 约35%宽度)

**位置**: 页面右侧，粘性定位

**内容**:

### 5.1 游戏封面 (Header Image)
- 游戏宣传图
- 宽度固定，高度自适应

### 5.2 游戏简介 (Short Description)
```
Black Myth: Wukong is an action RPG rooted in Chinese mythology. 
You shall set out as the Destined One to venture into the challenges 
and marvels ahead, to uncover the obscured truth beneath the veil 
of a glorious legend from the past.
```

### 5.3 评测摘要 (Review Summary)
```
RECENT REVIEWS:
Very Positive (1,727)

ENGLISH REVIEWS:
Very Positive (69,794)
```

### 5.4 发行信息 (Release Info)
```
RELEASE DATE:
20 Aug, 2024
```

### 5.5 开发商/发行商 (Developer/Publisher)
```
DEVELOPER:
Game Science

PUBLISHER:
Game Science
```

### 5.6 用户标签 (Tags)
```
Popular user-defined tags for this product:
Mythology | Action RPG | Action | Souls-like | RPG | 3D | +
```

### 5.7 成就展示 (Achievements)
- 成就图标网格
- 显示已解锁/总成就数

### 5.8 语言支持 (Language Support)
- 表格形式显示
- 界面、字幕、音频支持情况

### 5.9 年龄分级 (Age Rating)
- PEGI/ESRB 分级图标
- 内容警告

---

## 6. 页面底部 (Footer)

**内容**:
- Valve 版权信息
- 隐私政策、服务条款链接
- 社交媒体链接

---

## 布局特点总结

### 视觉层次
1. **第一层**: 媒体展示区（视频/截图）- 吸引注意力
2. **第二层**: 购买区域 - 转化用户
3. **第三层**: 游戏详情 - 提供信息
4. **第四层**: 用户评测 - 社会证明

### 信息密度
- 左侧：详细内容（媒体、购买、描述、评测）
- 右侧：快速参考（关键信息、标签、成就）

### 交互设计
- 粘性右侧栏：滚动时保持可见
- 媒体轮播：支持键盘/鼠标操作
- 评测筛选：多维度过滤

### 响应式设计
- 桌面端：左右分栏
- 移动端：单栏堆叠
- 断点：约 900px

---

## 关键数据指标（黑神话：悟空）

- 总评测数：875,116
- 好评率：Overwhelmingly Positive（压倒性好评）
- 近期评测：1,727 条
- 语言支持：15+ 种语言
- 成就数量：显示在右侧面板

---

## 技术实现要点

1. **HTML 结构**: 语义化标签，清晰的层级关系
2. **CSS 布局**: Flexbox/Grid 混合使用
3. **JavaScript**: 媒体轮播、评测筛选、动态加载
4. **性能优化**: 图片懒加载、CDN 加速
5. **可访问性**: ARIA 标签、键盘导航支持
