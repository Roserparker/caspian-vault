# Caspian v4 官网重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 按已批准 spec（`docs/superpowers/specs/2026-07-08-caspian-v4-design.md`）把 `index.html` 从 v3 重构为 v4「钢青精密/深海图录」——真实地理 HERO、B1 等深归心 logo、中文 slogan、五章换装、全站简笔画清除。

**Architecture:** 零构建单文件站（`index.html` 独占全部 HTML/CSS/JS，inline SVG）。重构 = 换 CSS 令牌层 + 重画 HERO/logo + 逐章换装 + 动画系统，v3 文案内容块全保留。每任务本地 commit，**最后一个任务统一验收后才 push**（push 即上线 caspianvault.com）。

**Tech Stack:** 原生 HTML/CSS/JS，inline SVG，思源宋 webfont（loli.net 镜像+回退），IntersectionObserver，无任何依赖。

## Global Constraints（每个任务默认继承）

- 单文件：所有改动只发生在 `index.html`（及最终任务的 `README.md`）；不新建 css/js 文件。
- 色彩令牌（:root 定义，唯一真源）：`--steel-black:#070B0E` `--deep-teal:#0E1A20` `--steel:#31586B` `--titan:#9FC6D4` `--silver:#D9DEE2` `--mist:#7D8894` `--btc:#E8813A` `--btc-dim:#8A5A34`。
- **唯一暖色铁律**：`--btc`/`--btc-dim` 只用于 ₿ 符号、BTC 供应阶梯、每股含币量数字、币阵光、回撤柱；按钮/链接/hover/装饰一律冷色。
- 字体三层：标题 `"Noto Serif SC","Songti SC","STSong",serif` 600；正文 `-apple-system,"PingFang SC","HarmonyOS Sans SC","Microsoft YaHei",sans-serif`；数据 `"SF Mono",Menlo,Consolas,monospace`。₿ 字符一律 `Georgia,serif`。
- 中文为主：界面文字/图注/标注全中文；英文全站仅三处（CASPIAN VAULT 字标、页脚一行铭文、徽记缩微文字）。HERO 无英文。
- 禁词（全文 grep 必须为零）：`升值` `增值` `回报` `保证收益` `保本`。
- 禁形：任何箭头（SVG marker、`→` 在图形语境、三角箭头 path）；任何简笔画式示意图。文案里的「→」链接指示符允许保留在纯文本链接中（如「进入胡侃比特 →」），但 SVG 图形内零箭头。
- 逐字保留（不得改动）：①眉标「品牌展示 · 非要约邀请 · 筹建中」②tag「Delaware C-Corp · 筹建中 · Caspian Vault 为暂定名」③Ch04 中性法务行整段（含「（措辞待持牌律师终审）」）④页脚 `.fine` 免责整段 ⑤analytics 行 `<script src="analytics.js?v=20260708" data-endpoint="https://hukanbit-analytics.jpstone.workers.dev/collect" data-site="caspian" defer></script>` ⑥全部 og/meta 标签。
- 动画：只用 transform/opacity；统一缓动 `--ease-velvet:cubic-bezier(.22,.61,.2,1)`；`prefers-reduced-motion` 下全部静态终帧；新增 JS ≤ 4KB。
- 兼容承接：断点 960/768/520；`overflow-x:hidden`；定位写 top/right/bottom/left 不写 `inset`；固定高不用 `aspect-ratio`；保留 `renderer=webkit`、`format-detection`、safe-area。
- git：每任务结尾 `git add index.html && git commit`（本地），**除 Task 10 外禁止 `git push`**。
- 本地预览：`cd "/Users/garfield/Desktop/Caspian Vault/Reserve/03_Caspian_Vault" && python3 -m http.server 8437` 后开 `http://localhost:8437/`（analytics 在 localhost 自动静默，不污染数据）。

---

### Task 1: 设计令牌层与全局排版基座

**Files:**
- Modify: `index.html`（`<head>` 内 `<style>` 顶部 + 字体 link + body/nav/页基础样式）

**Interfaces:**
- Produces: `:root` 全部色彩令牌（见 Global Constraints）、`--ease-velvet`、`.serif`（标题字体族 helper）、`.mono`（数据字体族 helper）、`.plate`（图录铭牌卡：`background:var(--deep-teal);border:1px solid rgba(49,88,107,.3);border-radius:2px;padding:26px 28px`）、`.hairline`（`border-top:1px solid rgba(49,88,107,.35)`）、`.knum`（数据数字样式：mono+`--titan`）。后续所有任务只用这些令牌，不得硬编码新颜色。

- [ ] **Step 1: 加载思源宋（异步+回退）**

在 `<head>` 现有字体 link 位置替换为：

```html
<link rel="stylesheet" href="https://fonts.loli.net/css2?family=Noto+Serif+SC:wght@400;600&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.loli.net/css2?family=Noto+Serif+SC:wght@400;600&display=swap"></noscript>
```

若 v3 已有 loli.net link 则原位替换；确保只此一条 webfont 引用。

- [ ] **Step 2: 写入令牌层与基座样式**

`<style>` 最顶部（替换 v3 的 `:root` 与 body 基座）：

```css
:root{
  --steel-black:#070B0E;--deep-teal:#0E1A20;--steel:#31586B;--titan:#9FC6D4;
  --silver:#D9DEE2;--mist:#7D8894;--btc:#E8813A;--btc-dim:#8A5A34;
  --ease-velvet:cubic-bezier(.22,.61,.2,1);
  --serif:"Noto Serif SC","Songti SC","STSong",serif;
  --sans:-apple-system,"PingFang SC","HarmonyOS Sans SC","Microsoft YaHei",sans-serif;
  --mono:"SF Mono",Menlo,Consolas,monospace;
}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--steel-black);color:var(--silver);
  font:17px/1.9 var(--sans);overflow-x:hidden;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
h1,h2,h3,.serif{font-family:var(--serif);font-weight:600;color:#EAEDEF}
h2{font-size:clamp(1.5rem,3.4vw,2.05rem);letter-spacing:.08em;line-height:1.5;margin:0 0 18px}
.mono,.knum{font-family:var(--mono)}
.knum{color:var(--titan);font-weight:400}
.plate{background:var(--deep-teal);border:1px solid rgba(49,88,107,.3);border-radius:2px;padding:26px 28px}
.hairline{border-top:1px solid rgba(49,88,107,.35)}
a{color:var(--titan);text-decoration:none;border-bottom:1px solid rgba(159,198,212,.28)}
a:hover{border-bottom-color:var(--titan)}
::selection{background:#16303c;color:#fff}
```

沿用 v3 的 `.wrap/.wide` 容器宽度与断点结构（960/768/520），只改颜色引用为令牌。

- [ ] **Step 3: 导航基座换装**

v3 `nav.top` 保结构，样式改为：底 `rgba(7,11,14,.88)` + backdrop-filter 有则用无则回退纯色、下缘 `.hairline`、链接 `--mist` hover `--titan`（冷色，无暖色）。「教育馆 ↗」外链样式一致。（logo 图形 Task 2 换。）

- [ ] **Step 4: 预览验证**

启本地服务开首页：页面整体已是钢黑底/银字/宋体标题；控制台零错误；无横向滚动条。v3 的旧金色部件此刻会临时显得突兀——属预期，后续任务逐个换。

- [ ] **Step 5: Commit**

```bash
git add index.html && git commit -m "v4 T1：钢青令牌层+三层字体+图录基座（唯一暖色铁律入令牌）"
```

---

### Task 2: Logo「等深归心」四件套

**Files:**
- Modify: `index.html`（nav logo、favicon `<link rel="icon">`、页脚铭章；HERO 大图形本任务先做成独立 symbol，Task 3 摆位）

**Interfaces:**
- Produces: `<symbol id="lg-mark" viewBox="0 0 120 120">`（图形单标，`<use>` 复用）；`.lg-row`（横排组合标容器）；页脚 `.seal-v4`。
- Consumes: Task 1 令牌。

- [ ] **Step 1: 在 `<body>` 顶部写入共享 symbol**

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="lg-mark" viewBox="0 0 120 120">
  <g fill="none" stroke-linecap="round">
    <path d="M60,14 C81,13 97,22 101,38 C105,53 95,62 97,74 C99,88 103,96 100,106 C95,120 78,126 64,127 C50,126 37,118 35,105 C34,92 41,83 41,71 C39,59 31,51 34,37 C38,22 48,15 60,14 Z" stroke="#9FC6D4" stroke-width="1.7" opacity=".95"/>
    <path d="M60,25 C76,24 88,31 91,43 C94,54 87,62 89,72 C91,83 94,90 92,98 C88,109 75,114 64,115 C53,114 43,107 42,97 C41,87 47,79 47,69 C45,59 39,52 42,41 C45,30 51,26 60,25 Z" stroke="#9FC6D4" stroke-width="1" opacity=".62"/>
    <path d="M60,36 C71,35 80,40 82,49 C84,57 79,63 81,71 C82,79 85,84 83,90 C80,98 71,102 64,103 C56,102 49,97 48,90 C48,82 52,76 52,68 C51,60 46,54 48,47 C50,39 54,37 60,36 Z" stroke="#9FC6D4" stroke-width=".8" opacity=".38"/>
    <path d="M60,47 C67,46 73,50 74,56 C75,62 71,66 72,71 C73,77 75,80 74,84 C72,89 67,92 63,92 C58,92 54,88 53,84 C53,79 56,75 56,70 C55,64 52,60 53,55 C54,50 56,48 60,47 Z" stroke="#9FC6D4" stroke-width=".7" opacity=".2"/>
  </g>
  <text x="60" y="76" font-size="20" text-anchor="middle" fill="#E8813A" font-family="Georgia,serif" font-weight="bold">₿</text>
</symbol>
</defs></svg>
```

注：环线是「柔和闭合的等深曲线」，由外到内 4 环、透明度 .95→.2 渐隐、₿ 略低于几何中心（沉底感）。symbol 内用字面色值（symbol 不继承 var 时最稳）。

- [ ] **Step 2: 导航横排组合标**

替换 v3 `a.logo` 内容：

```html
<a class="logo lg-row" href="#sea" aria-label="里海金库 首页">
  <svg width="30" height="30" aria-hidden="true"><use href="#lg-mark"/></svg>
  <span class="lg-name"><span class="lg-en">CASPIAN VAULT</span><span class="lg-zh">里海金库</span></span>
</a>
```

```css
.lg-row{display:flex;align-items:center;gap:10px;border:none}
.lg-name{display:flex;flex-direction:column;line-height:1.25}
.lg-en{font:600 12.5px/1 var(--sans);letter-spacing:.34em;color:var(--silver)}
.lg-zh{font:400 10px/1 var(--sans);letter-spacing:.5em;color:var(--mist);margin-top:4px}
```

- [ ] **Step 3: favicon 换新（16px 减环版：双环+₿）**

替换 `<link rel="icon" ...>` 为（data URI，双环版）：

```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23070B0E'/%3E%3Cellipse cx='32' cy='32' rx='22' ry='26' fill='none' stroke='%239FC6D4' stroke-width='2.4'/%3E%3Cellipse cx='32' cy='33' rx='13' ry='16' fill='none' stroke='%239FC6D4' stroke-width='1.2' opacity='.55'/%3E%3Ctext x='32' y='41' font-size='22' text-anchor='middle' fill='%23E8813A' font-family='Georgia,serif' font-weight='bold'%3E%E2%82%BF%3C/text%3E%3C/svg%3E">
```

- [ ] **Step 4: 页脚铭章（含缩微文字，英文合法三处之一）**

页脚原 `.seal`（≋+₿ 旧印章）替换为：

```html
<div class="seal-v4" aria-hidden="true">
  <svg width="54" height="54"><use href="#lg-mark"/></svg>
  <div class="seal-micro">42°N 51°E · NOTHING FLOWS OUT</div>
</div>
```

```css
.seal-v4{margin-top:26px;display:flex;flex-direction:column;align-items:center;gap:8px;opacity:.8}
.seal-micro{font:400 8.5px/1 var(--mono);letter-spacing:.3em;color:var(--mist)}
```

- [ ] **Step 5: 预览验证 + Commit**

浏览器缩放导航到 50% 看小尺寸可读性；favicon 在标签页读得出 ₿。

```bash
git add index.html && git commit -m "v4 T2：等深归心 logo 四件套（symbol 复用/导航横排/favicon 双环/页脚铭章）"
```

---

### Task 3: HERO 重构——真实海盆 + 三段编排 + 中文 slogan

**Files:**
- Modify: `index.html`（`header#sea` 整体替换：`#basinMap` SVG、文案块、编排 CSS/JS）

**Interfaces:**
- Consumes: Task 1 令牌与缓动。
- Produces: `#basinMap`（海盆 SVG）、`.rv`（河流光丝 path 类）、CSS 变量 `--hero-t`（编排总时长基准 1.2s）；HERO 文案块类 `.hero-eyebrow/.hero-h1/.hero-slogan/.hero-thesis/.hero-tag`。

- [ ] **Step 1: 海盆 SVG（真实地理，艺术品级基底）**

替换 v3 `#basinMap` 全部内容。viewBox `0 0 460 640`。解剖检查点：宽北盆+伏尔加口三角洲（顶缘锯齿）、东北乌拉尔口、东侧**卡拉博加兹湾**（近闭潟湖+窄峡相连）、阿普歇伦半岛西岸东突收腰、浑圆南盆。主岸线 path（可在此基础上微调平滑，但检查点不得丢）：

```html
<svg id="basinMap" viewBox="0 0 460 640" role="img" aria-label="里海测深图：万川归之，无一外流">
  <defs>
    <linearGradient id="bathy" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#17384A"/>
      <stop offset=".38" stop-color="#0F2635"/>
      <stop offset=".72" stop-color="#0A1A26"/>
      <stop offset="1" stop-color="#071018"/>
    </linearGradient>
    <radialGradient id="deepGlow" cx=".5" cy=".82" r=".5">
      <stop offset="0" stop-color="#040A10"/><stop offset="1" stop-color="#040A10" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <!-- 主水体：北浅南深 -->
  <path id="coast" fill="url(#bathy)" stroke="#9FC6D4" stroke-width="1.1" stroke-opacity=".55" d="
    M150,42 C162,36 178,40 192,38 C204,36 214,42 226,40 C240,38 256,46 268,54
    C280,62 292,76 298,96 C305,118 302,140 292,158 C284,172 280,188 283,206
    C285,220 284,230 286,238 C287,244 286,250 282,254
    C276,262 274,272 278,284 C284,300 292,306 291,322
    C290,338 282,346 284,362 C287,384 298,398 302,420
    C308,452 306,492 292,524 C278,556 254,580 226,588
    C198,594 168,584 148,562 C130,542 122,514 124,486
    C126,462 136,446 132,424 C128,404 116,394 112,376
    C109,360 114,348 122,338 C130,328 142,322 156,320
    C166,318 176,320 184,316 C190,312 190,304 184,300
    C176,294 162,296 150,292 C136,288 124,278 118,262
    C112,246 112,228 108,210 C104,190 100,170 104,150
    C108,128 118,108 128,92 C136,76 140,54 150,42 Z"/>
  <!-- 卡拉博加兹湾（近闭潟湖，窄峡相连） -->
  <path id="kbg" fill="#0E2230" stroke="#9FC6D4" stroke-width=".9" stroke-opacity=".45" d="
    M291,236 C296,232 306,226 320,224 C340,221 362,228 372,244
    C382,260 380,282 368,294 C354,306 330,308 314,300
    C300,293 294,282 293,270 C292,260 290,248 288,242 C287,238 289,237 291,236 Z"/>
  <!-- 内等深线两圈（中盆/南盆各一，手绘柔和闭合曲线，线宽 .7/.55，opacity .3/.22） -->
  <path fill="none" stroke="#9FC6D4" stroke-width=".7" stroke-opacity=".3" d="M232,300 C258,296 276,312 278,338 C280,366 266,382 244,386 C220,390 200,376 198,352 C196,326 210,304 232,300 Z"/>
  <path fill="none" stroke="#9FC6D4" stroke-width=".55" stroke-opacity=".22" d="M236,428 C262,424 282,444 284,476 C286,508 268,534 240,538 C212,542 190,520 188,490 C186,458 208,432 236,428 Z"/>
  <ellipse cx="234" cy="490" rx="80" ry="90" fill="url(#deepGlow)"/>
  <!-- 水深标注（中文+数字，mono） -->
  <text x="200" y="120" class="depth-t">北盆 · 浅</text>
  <text x="244" y="356" class="depth-t">中盆 −788 米</text>
  <text x="238" y="492" class="depth-t" fill-opacity=".9">南盆 −1025 米</text>
  <!-- 河流光丝（Task 3 Step 3 编排）：伏尔加/乌拉尔/捷列克/库拉/阿特列克 -->
  <path class="rv" d="M150,6 C158,18 162,28 158,40" />
  <path class="rv" d="M320,26 C302,38 286,46 274,56" />
  <path class="rv" d="M52,150 C74,152 90,150 102,152" />
  <path class="rv" d="M50,332 C76,334 100,336 118,338" />
  <path class="rv" d="M404,430 C376,428 340,424 304,420" />
</svg>
```

```css
.depth-t{font-family:var(--mono);font-size:10px;fill:#9FC6D4;fill-opacity:.6;text-anchor:middle;letter-spacing:.18em}
```

**验收对照**：与站长提供的地图截图并排比对——北宽、东湾、腰细、南圆四特征肉眼可辨。

- [ ] **Step 2: HERO 文案块（中文 slogan 铸字，无英文）**

```html
<div class="inner">
  <div class="hero-eyebrow">品牌展示 · 非要约邀请 · 筹建中</div>
  <h1 class="hero-h1">里海金库</h1>
  <div class="hero-slogan serif">聚流成海，藏金于渊。</div>
  <p class="hero-thesis">里海是一片被大地环抱的海：一百多条河注入，却没有一个出海口。<br>我们把公司的资产负债表，建成这样一座里海——<b>价值存进来，就安放在最深处。</b></p>
  <div class="hero-tag">Delaware C-Corp · 筹建中 · Caspian Vault 为暂定名</div>
</div>
<div class="scrollhint">▼ 入 渊</div>
```

```css
.hero-eyebrow{font:400 11px/1 var(--sans);letter-spacing:.42em;color:var(--mist)}
.hero-h1{font-size:clamp(2.5rem,7vw,4rem);letter-spacing:.22em;margin:20px 0 10px}
.hero-slogan{font-size:clamp(1.15rem,3vw,1.6rem);letter-spacing:.3em;color:var(--titan);margin:0 0 26px}
.hero-thesis{max-width:34em;margin:0 auto;color:var(--silver);font-size:15.5px;line-height:2.1}
.hero-tag{margin-top:26px;font:400 11px/1 var(--mono);letter-spacing:.2em;color:var(--mist)}
```

注意：v3 原 `.slogan`（英文 Nothing flows out.）与 `.en`（Caspian Vault 英文行）**删除**；hero-mark 大徽记不放 HERO（徽记归导航与页脚，海图即主视觉）。

- [ ] **Step 3: 三段编排（水体先显 → 光丝河后至 → 常驻呼吸）**

```css
/* 帧1：水体显形 0–1.2s（无任何线条先动） */
#coast,#kbg{opacity:0;animation:seaIn 1.2s var(--ease-velvet) .1s forwards}
@keyframes seaIn{to{opacity:1}}
/* 帧2：河流光丝 1.2s 起错峰滑入，无箭头，端点微亮溶入 */
.rv{fill:none;stroke:#7FB6CC;stroke-width:1.1;stroke-linecap:round;opacity:0;
  stroke-dasharray:60;stroke-dashoffset:60}
.rv{animation:rvIn 1.5s var(--ease-velvet) forwards}
.rv:nth-of-type(1){animation-delay:1.25s}.rv:nth-of-type(2){animation-delay:1.45s}
.rv:nth-of-type(3){animation-delay:1.65s}.rv:nth-of-type(4){animation-delay:1.85s}
.rv:nth-of-type(5){animation-delay:2.05s}
@keyframes rvIn{0%{opacity:0;stroke-dashoffset:60}25%{opacity:.85}100%{opacity:.5;stroke-dashoffset:0}}
/* 常驻：水面光泽极缓呼吸（20s），只动 opacity */
#basinMap{will-change:opacity}
#coast{transform-origin:center}
@keyframes seaBreathe{0%,100%{stroke-opacity:.55}50%{stroke-opacity:.75}}
#coast{animation:seaIn 1.2s var(--ease-velvet) .1s forwards,seaBreathe 20s ease-in-out 3s infinite}
/* reduced-motion：全部终帧 */
@media(prefers-reduced-motion:reduce){
  #coast,#kbg{opacity:1;animation:none}
  .rv{opacity:.5;stroke-dashoffset:0;animation:none}
}
```

- [ ] **Step 4: 视觉验证（重点）**

刷新页面盯首帧：**0–1.2 秒内屏幕上除渐显的水体外没有任何线条**；河流从 1.25s 起依次滑入且**无箭头**；20 秒内观察岸线呼吸不突兀。开 DevTools 切 `prefers-reduced-motion: reduce`（渲染面板模拟）确认全静态。与地图截图并排对照海形。

- [ ] **Step 5: Commit**

```bash
git add index.html && git commit -m "v4 T3：真实地理海盆+三段编排（水先/光丝河/无箭头）+中文slogan铸字"
```

---

### Task 4: 海床 ₿ 阵列带 + 右缘深度刻度 + 滚动潜深

**Files:**
- Modify: `index.html`（HERO 之后插入 `<section id="seabed">`；`<body>` 末尾 JS 块加深度刻度与滚动联动）

**Interfaces:**
- Consumes: Task 1 令牌、Task 3 的 HERO 结构。
- Produces: `#seabed`（币阵带）、`#depthRail`（右缘刻度，fixed）、JS 函数 `initDepth()`（滚动→刻度推进+`document.body.style.setProperty('--dive',0..1)`）。

- [ ] **Step 1: 币阵带（有光的币阵，程序化生成，非扁平字符网格）**

HERO `</header>` 后插入：

```html
<section id="seabed" aria-label="海床币阵（教学示意）">
  <div class="sb-inner">
    <div class="sb-field" id="sbField" aria-hidden="true"></div>
    <p class="sb-cap">海床上的储备，一枚一枚，码放整齐。<span>教学示意 · 非实际持仓数</span></p>
  </div>
</section>
```

```css
#seabed{background:linear-gradient(#071018,#05090E);padding:10px 0 30px;position:relative}
.sb-inner{max-width:960px;margin:0 auto;padding:0 22px}
.sb-field{height:180px;position:relative;overflow:hidden}
.sb-b{position:absolute;font-family:Georgia,serif;color:var(--btc);user-select:none}
.sb-cap{text-align:center;font:400 12.5px/1.9 var(--sans);color:var(--mist);letter-spacing:.12em}
.sb-cap span{display:block;font-size:10.5px;opacity:.75;font-family:var(--mono);letter-spacing:.22em}
```

生成 JS（加入 body 末尾脚本块；5 排透视币阵：后排小/暗/糊，前排大/亮，光衰由 opacity+blur 车出景深）：

```js
(function(){
  var f=document.getElementById('sbField');if(!f)return;
  var rows=[{y:18,s:9,o:.10,n:22,b:1.2},{y:52,s:11,o:.16,n:18,b:.8},
            {y:88,s:13,o:.26,n:15,b:.4},{y:124,s:16,o:.42,n:12,b:0},
            {y:158,s:19,o:.72,n:10,b:0}];
  rows.forEach(function(r){
    for(var i=0;i<r.n;i++){
      var e=document.createElement('span');e.className='sb-b';e.textContent='₿';
      var jx=(Math.sin(i*7.3+r.y)*8);
      e.style.cssText='left:'+(4+(92/(r.n-1))*i+jx/10)+'%;top:'+r.y+'px;font-size:'+r.s+
        'px;opacity:'+r.o+(r.b?';filter:blur('+r.b+'px)':'');
      f.appendChild(e);
    }
  });
})();
```

- [ ] **Step 2: 右缘深度刻度（全站签名部件）**

```html
<div id="depthRail" aria-hidden="true">
  <div class="dr-line"><i id="drCur"></i></div>
  <span class="dr-t" id="drNum">0 米</span>
</div>
```

```css
#depthRail{position:fixed;top:50%;right:14px;transform:translateY(-50%);z-index:40;
  display:flex;flex-direction:column;align-items:center;gap:8px}
.dr-line{width:1px;height:130px;background:rgba(49,88,107,.5);position:relative}
.dr-line i{position:absolute;left:-2px;top:0;width:5px;height:5px;border-radius:50%;
  background:var(--titan);transition:top .15s linear}
.dr-t{writing-mode:vertical-rl;font:400 9.5px/1 var(--mono);letter-spacing:.22em;color:var(--mist)}
@media(max-width:768px){#depthRail{display:none}}
```

```js
function initDepth(){
  var cur=document.getElementById('drCur'),num=document.getElementById('drNum'),tick=false;
  function on(){tick=false;
    var h=document.documentElement,p=Math.min(1,(h.scrollTop||document.body.scrollTop)/(h.scrollHeight-h.clientHeight));
    cur.style.top=(p*125)+'px';
    num.textContent='−'+Math.round(p*1025)+' 米';
    document.body.style.setProperty('--dive',p.toFixed(3));
  }
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(on)}},{passive:true});
  on();
}
initDepth();
```

- [ ] **Step 3: 滚动潜深（水色渐深）**

利用 `--dive`（0→1）给主体加一层随深度加深的底色（伪元素，opacity 由 `--dive` 驱动，transform/opacity 之外唯一允许的 custom-property 联动，rAF 已节流）：

```css
body::after{content:"";position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:-1;
  background:#03070C;opacity:calc(var(--dive,0)*.55)}
```

- [ ] **Step 4: 验证 + Commit**

滚动全页：刻度数字从 0 到 −1025 米、圆点走满、页面越滚越深；币阵有景深有光衰、前亮后暗；`教学示意` 字样在。桌面窄至 768 刻度隐藏无报错。

```bash
git add index.html && git commit -m "v4 T4：海床₿阵列（景深光衰）+右缘深度刻度+滚动潜深"
```

---

### Task 5: Ch01 换装 + 简笔画清除（椭圆+箭头处决）

**Files:**
- Modify: `index.html`（`section#corridor` 全节）

**Interfaces:**
- Consumes: `.plate/.hairline/.serif` (Task 1)。
- Produces: `.chap-k`（章节眉：`font:400 11px var(--mono);letter-spacing:.4em;color:var(--mist)`，中文如「第一章 · 这是什么」）。全站章节眉统一此类（Task 6-8 复用）。

- [ ] **Step 1: 删除简笔画**

找到 Ch01 内「其一 · 独立」的椭圆+箭头 SVG（站长截图那个：`<ellipse>` + 三条带箭头折线 + 内嵌英文 Nothing flows out），**整块删除**。同节其余「其二/其三…」若含同类简笔 SVG 一并删除。

- [ ] **Step 2: 概念改由排版承载**

原「独立/闭环/无出口」各小节改为图录铭牌（`.plate` 栅格，2 列 768 下 1 列）：

```html
<div class="c1-grid">
  <div class="plate">
    <div class="chap-k">其一 · 独立</div>
    <h3 class="serif">一片不依赖任何人的海</h3>
    <p>里海不与任何大洋相通，也没有一个流向外海的出口。它不理会全球海平面，不受潮汐与洋流摆布——一个<b>不依赖外部、自成一体</b>的完整系统。这正是比特币「自托管」的镜像：不经过银行、不依赖第三方清算。<b>安全不靠藏，靠的是不接任何一根管道。</b></p>
  </div>
  <!-- 其余小节同构：眉+宋体题+原文案 -->
</div>
```

```css
.c1-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:768px){.c1-grid{grid-template-columns:1fr}}
.chap-k{font:400 11px/1 var(--mono);letter-spacing:.4em;color:var(--mist);margin-bottom:12px}
```

文案一字不动（上例正文即 v3 原文）。章节眉「Chapter 01 · 这是什么」改为中文「第一章 · 这是什么」（全站各章同步，Task 6-8 执行各自章）。

- [ ] **Step 3: 验证 + Commit**

`grep -c "Nothing flows out" index.html` 应只剩页脚/铭章 ≤2 处；Ch01 无任何 `<ellipse>`；视觉过一遍雅不雅。

```bash
git add index.html && git commit -m "v4 T5：Ch01 铭牌化，处决椭圆+箭头简笔画，章节眉中文化"
```

---

### Task 6: Ch02 数据图重绘（购买力冷青线 / 减半橙阶梯 / 代码块换装）

**Files:**
- Modify: `index.html`（`section#why` 内两个互动 SVG 的配色与坐标系、代码块样式）

**Interfaces:**
- Consumes: 令牌；v3 已有的滑块逻辑 JS（`#ppYear`、`#mN`、`#supSvg` 相关函数——只换视觉不动计算）。
- Produces: `.axis`（坐标轴样式：线 `rgba(49,88,107,.4)`、刻度字 `.depth-t` 同款 mono 10px）。

- [ ] **Step 1: 购买力曲线**

曲线 stroke 改 `--titan`、线宽 1.6；坐标轴/网格 `.axis`；图注中文化（「1913–2026 · 一美元还剩多少购买力」）；滑块轨道冷色（`accent-color:#31586B`，不支持则默认）。**此图零暖色**（是法币的曲线）。

- [ ] **Step 2: 减半时刻表**

BTC 供应阶梯 stroke 改 `--btc` 线宽 1.8（唯一暖色的合法舞台）；已发行区填充 `rgba(232,129,58,.08)`；减半刻线 `--steel`；标注中文 mono。图注补一行：「法币的曲线向下，比特币的阶梯恒定——对比即论点。」（新增图注属图注级新增，允许。）

- [ ] **Step 3: GetBlockSubsidy 代码块**

```css
pre.code{background:#0A141B;border:1px solid rgba(49,88,107,.35);border-radius:2px;
  font:12.5px/1.75 var(--mono);color:#B9CAD4;padding:20px 22px;overflow-x:auto}
pre.code .kw{color:var(--titan)}pre.code .cm{color:var(--mist)}
```

关键行 `nSubsidy >>= halvings` 的注释允许一处 `--btc` 高亮（它就是资产本体的发行规则）。

- [ ] **Step 4: 验证 + Commit**

拖两个滑块：计算行为与 v3 一致（只换皮）；曲线冷、阶梯暖、对比成立；本节除阶梯与该行注释外无暖色。

```bash
git add index.html && git commit -m "v4 T6：Ch02 图录级重绘——法币冷线/比特币橙阶梯/代码块换装"
```

---

### Task 7: 引导带 + Ch03 换装（四柱铭牌化 / 每股含币量橙色大数字）

**Files:**
- Modify: `index.html`（`#bridge`、`section#vault`）

**Interfaces:**
- Consumes: `.plate/.chap-k/.knum`。
- Produces: `.pillar`（四柱铭牌）、`.pershare`（含币量数字板）。

- [ ] **Step 1: 引导带制图铭牌式**

保留 v3 文案（「想真正读懂比特币…这里是公司，那里是学堂，泾渭分明。」），容器改细线框铭牌居中；眉标「学堂在胡侃 · 公司在这里」（中文替换原英文 `Company here · Education there`）；按钮改冷色细框（`border:1px solid var(--steel);color:var(--titan)`，hover 边框转 `--titan`，无暖色）。

- [ ] **Step 2: 四柱删图标、纯排版铭牌**

v3 四柱的鎏金线描 SVG 图标（保险库/家族/盾/天平）**删除**，改：

```html
<div class="pillar plate">
  <div class="chap-k">柱一</div>
  <h3 class="serif">机构级冷藏</h3>
  <p><!-- v3 原文案 --></p>
</div>
```

（四柱标题以 v3 现文为准，不改写。）

- [ ] **Step 3: 每股含币量——全站唯一橙色大数字**

```html
<div class="pershare plate">
  <div class="chap-k">每股含币量 · 唯一要紧的仪表</div>
  <div class="ps-num knum" style="color:var(--btc)">0.0000&nbsp;₿<span>／股</span></div>
  <p class="ps-note"><!-- v3 原说明文案 --></p>
</div>
```

```css
.ps-num{font-size:clamp(2.2rem,6vw,3.4rem);letter-spacing:.04em}
.ps-num span{font-size:.35em;color:var(--mist);letter-spacing:.2em}
```

（数值沿 v3 现值/占位，不造新数。）

- [ ] **Step 4: 验证 + Commit**

Ch03 无任何线描图标；含币量是页面上最醒目的暖色元素；五条刹车/长处/自律等列表换 `.plate`+hairline 分隔，文案未动。

```bash
git add index.html && git commit -m "v4 T7：引导带铭牌化+四柱去图标+每股含币量橙色大数字"
```

---

### Task 8: Ch04 诚实条款 + Ch05 深度时间轴 + 页脚

**Files:**
- Modify: `index.html`（`section#honest`、`section#road`、`footer`）

**Interfaces:**
- Consumes: 令牌、`.plate/.chap-k`、Task 2 的 `.seal-v4`。
- Produces: `.dd-bar`（回撤柱）、`.road-depth`（深度时间轴容器）。

- [ ] **Step 1: 诚实条款**

「先把最坏的话说在最前面」保宋体大题；「归零=全损」句放高对比银字铭牌（`background:#0A141B;border-left:2px solid var(--silver)`）；四次回撤柱：

```css
.dd-bar{background:var(--btc-dim);opacity:.85}
```

柱高与标注沿 v3 数据；轴线 `.axis`。中性法务行整段逐字保留（含「（措辞待持牌律师终审）」）。

- [ ] **Step 2: 路线图 → 深度时间轴**

竖向时间轴：左侧一条 1px `--steel` 垂线携带深度刻度（0 米 → −1025 米，mono 中文标注），里程碑挂不同深度：

```html
<div class="road-depth">
  <div class="rd-item" style="--d:0"><span class="rd-depth">0 米</span><h4 class="serif">教育（已完成）</h4><p><!-- v3 文案 --></p></div>
  <div class="rd-item is-here" style="--d:1"><span class="rd-depth">−260 米</span><h4 class="serif">Delaware 起步壳</h4><p><!-- v3 文案 --></p><span class="rd-now">● 正下潜至此</span></div>
  <div class="rd-item" style="--d:2"><span class="rd-depth">−520 米</span><h4 class="serif">创始记录期</h4><p><!-- v3 文案 --></p></div>
  <div class="rd-item" style="--d:3"><span class="rd-depth">−780 米</span><h4 class="serif">极小范围同行者</h4><p><!-- v3 文案 --></p></div>
  <div class="rd-item" style="--d:4"><span class="rd-depth">−1025 米</span><h4 class="serif">亚洲架构</h4><p><!-- v3 文案 --></p></div>
</div>
```

```css
.road-depth{position:relative;padding-left:96px;border-left:1px solid rgba(49,88,107,.5);margin-left:8px}
.rd-item{position:relative;margin:0 0 44px}
.rd-depth{position:absolute;left:-96px;top:6px;width:76px;text-align:right;
  font:400 10.5px/1 var(--mono);letter-spacing:.14em;color:var(--mist)}
.rd-item h4{margin:0 0 8px;font-size:1.1rem;letter-spacing:.1em}
.rd-now{font:400 11px/1 var(--mono);color:var(--titan);letter-spacing:.2em}
.is-here h4{color:var(--titan)}
```

「● 正下潜至此」的圆点用 `--titan`（冷色；不是资产本体，不得用橙）。

- [ ] **Step 3: 页脚**

保留全部 v3 文案与 `.fine` 免责；「熟人引荐/胡侃导流」段排版换令牌；末行英文铭文（合法三处之二）：`CASPIAN VAULT · EST. 2026`（mono 9px `--mist`）；`.seal-v4` 已由 Task 2 放置。删除 v3 旧 `.brand` 英文重复行若与铭文重复。

- [ ] **Step 4: 验证 + Commit**

Ch04 回撤柱是降饱和暗橙、法务行原文在；Ch05 里程碑深度递进、「你在这里」在 −260 米；页脚英文只两行（铭文+缩微）。

```bash
git add index.html && git commit -m "v4 T8：诚实条款高对比铭牌+路线图深度时间轴+页脚铭文"
```

---

### Task 9: 全站扫尾——瓷器遗产清除 / 声呐环 / reveal 统一 / 英文清点

**Files:**
- Modify: `index.html`（全局 CSS/JS 清理）

**Interfaces:**
- Consumes: 前八个任务全部产出。
- Produces: `initReveals()`（唯一 IntersectionObserver）、`.sonar`（点击反馈）。

- [ ] **Step 1: 删除瓷器遗产**

搜索并删除 v3 残留：瓷面噪点纹理（noise/grain 相关 CSS 或 SVG filter）、弦纹分隔、涟漪点击 JS（ripple）、旧印章样式（`.seal` 旧类）、v3 旧 `--gold/--paper` 类旧令牌及其引用。`grep -n "ripple\|noise\|grain\|d8b466\|c9a962" index.html` 逐条清零（favicon data-URI 中的历史色值除外——favicon 已在 T2 换新，不应再有）。

- [ ] **Step 2: 声呐环点击反馈**

```js
addEventListener('pointerdown',function(e){
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var s=document.createElement('i');s.className='sonar';
  s.style.left=e.clientX+'px';s.style.top=e.clientY+'px';
  document.body.appendChild(s);setTimeout(function(){s.remove()},700);
},{passive:true});
```

```css
.sonar{position:fixed;width:8px;height:8px;margin:-4px 0 0 -4px;border-radius:50%;
  border:1px solid var(--titan);opacity:.7;pointer-events:none;z-index:99;
  animation:sonar .7s var(--ease-velvet) forwards}
@keyframes sonar{to{transform:scale(7);opacity:0}}
```

- [ ] **Step 3: reveal 统一（淡入+2px 上移，无弹跳）**

```js
function initReveals(){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('on');io.unobserve(en.target)}});
  },{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
}
initReveals();
```

```css
.reveal{opacity:0;transform:translateY(2px);transition:opacity .9s var(--ease-velvet),transform .9s var(--ease-velvet)}
.reveal.on{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
```

确认全站只有这一个 IntersectionObserver（v3 若有旧的，合并进来）。

- [ ] **Step 4: 英文与禁词清点**

```bash
grep -o '[A-Za-z][A-Za-z .©°'\''&-]\{2,\}' index.html | grep -v -E 'html|head|body|div|span|class|style|script|svg|path|meta|link|font|media|animation|keyframes|http|css|Georgia|PingFang|Menlo|Noto|var|calc|clamp|px|rem|em|linear|gradient|scroll|top|left|right|bottom|width|height|opacity|transform' | sort -u
```

输出人工过目：界面可见英文应只剩 `CASPIAN VAULT`、页脚铭文、缩微文字（及 og/meta/代码块内属技术文本，不算界面文字）。再跑：

```bash
grep -c "升值\|增值\|回报\|保证收益\|保本" index.html   # 期望 0
grep -c "marker-end\|marker-start\|<marker" index.html  # 期望 0（无 SVG 箭头）
```

- [ ] **Step 5: Commit**

```bash
git add index.html && git commit -m "v4 T9：瓷器遗产清除+声呐环+reveal统一+英文/禁词清点"
```

---

### Task 10: 终验收与上线

**Files:**
- Modify: `index.html`（修验收发现的问题）、`README.md`（v4 条目）

- [ ] **Step 1: spec §8 验收逐条跑**

1. 简笔画/箭头：`grep -c "<marker\|marker-end" index.html` = 0；肉眼过每个 SVG。
2. 海形与地图截图并排对照（北宽/东湾/腰细/南圆）。
3. 刷新首页录屏或慢放：首帧只有水体。
4. 英文三处清点（Task 9 Step 4 复跑）。
5. slogan：`grep -c "聚流成海，藏金于渊" index.html` ≥ 1 且在 HERO。
6. 暖色审计：`grep -n "E8813A\|8A5A34\|--btc" index.html` 每处人工确认属资产本体。
7. DevTools Performance 录制滚动：无 layout thrash（只 transform/opacity）；模拟 reduced-motion 全静态。
8. 不变项：逐字搜索六段保留文案与 analytics 行、og 标签（Global Constraints ⑤⑥）。

- [ ] **Step 2: 四视口台**

`python3 -m http.server 8437` 后逐个视口（768×900 / 1024×768 / 390×844 / 360×780，DevTools 设备模拟）检查：无横滚、导航单行、币阵不溢出、深度刻度 768 以下隐藏、时间轴左标注不挤压。控制台零错误零警告。

- [ ] **Step 3: 体积预算**

```bash
wc -c index.html   # 期望 ≤ 120KB
```

超了先压 SVG path 精度（小数一位）与重复 CSS。

- [ ] **Step 4: README v4 条目**

`README.md`：标题改 v4；「版本沿革」加一行 `v4（2026-07-09，现行）：钢青精密/深海图录——唯一暖色=₿、真实地理海盆、中文 slogan「聚流成海，藏金于渊」、全站简笔画清除、深度刻度签名部件`；「页面结构」章按 v4 五章+海床带+深度刻度更新；待办勾掉「站长通读 v3 文案」改「站长通读 v4 文案」。

- [ ] **Step 5: 上线（唯一一次 push）**

```bash
git add index.html README.md && git commit -m "v4 上线：钢青精密/深海图录全站换装（spec 2026-07-08 验收通过）"
git push
```

约 1 分钟后 `curl -s "https://caspianvault.com/?cb=$(date +%s)" | grep -c "聚流成海"` 应 ≥1；线上肉眼终检一遍。

---

## Self-Review 记录

- **Spec 覆盖**：§1 美学系统→T1/T9；§2 Logo→T2；§3 Slogan→T3（HERO 无英文已入 T3 Step 2 注）；§4 HERO→T3/T4；§5 五章映射→T5-T8；§6 动画性能→T3/T4/T9；§7 不变项→Global Constraints+T10；§8 验收→T10；§9 范围外未越界。无缺口。
- **占位符扫描**：各任务文案处标注「v3 原文/不改写」为刻意约束（防实施者重写文案），非缺内容；结构与样式代码全给出。通过。
- **命名一致性**：`--ease-velvet`/`.plate`/`.chap-k`/`.knum`/`.depth-t`/`#basinMap`/`.rv`/`#depthRail`/`--dive`/`initReveals()` 跨任务引用一致。通过。
