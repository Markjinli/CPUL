#!/usr/bin/env python3
"""Build the CPU+GPU Viewer HTML file by embedding JSON data into a single HTML file."""

import json
import os

DIR = os.path.dirname(__file__)
CPU_INPUT = os.path.join(DIR, "cpus_decrypted.json")
GPU_INPUT = os.path.join(DIR, "gpus_decrypted.json")
OUTPUT = os.path.join(DIR, "cpu-gpu-viewer.html")

with open(CPU_INPUT, "r", encoding="utf-8") as f:
    cpu_data = json.load(f)
with open(GPU_INPUT, "r", encoding="utf-8") as f:
    gpu_data = json.load(f)

# Merge into one dict
merged = {**cpu_data, **gpu_data}
data_json = json.dumps(merged, ensure_ascii=False)

# Use a marker to split the template so we can inject data_json safely
PART1 = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CPU & GPU Viewer — AMD, Intel & NVIDIA Database</title>
<style>
/* ===== RESET & BASE ===== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--bg2:#181b23;--bg3:#1e222d;--bg4:#262a36;
  --text:#e4e6eb;--text2:#a0a4b0;--text3:#6b7080;
  --amd:#ed1c24;--amd2:#ff4d55;--intel:#0071c5;--intel2:#3d9fe8;
  --nvidia:#76b900;--nvidia2:#99d620;
  --accent:#6c63ff;--accent2:#8b83ff;
  --green:#00c853;--orange:#ff9800;--red:#ff1744;
  --border:#2a2e3a;--shadow:0 4px 24px rgba(0,0,0,.4);
  --radius:8px;--radius2:12px;
  --sidebar-w:240px;
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
  --mono:'SF Mono','Fira Code','Cascadia Code',Consolas,monospace;
}
html{font-size:14px;scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;overflow:hidden;height:100vh}
a{color:var(--accent2);text-decoration:none}
a:hover{text-decoration:underline}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--bg4);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--text3)}

/* ===== LAYOUT ===== */
.app{display:flex;height:100vh;overflow:hidden}
.sidebar{width:var(--sidebar-w);background:var(--bg2);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;overflow-y:auto;z-index:100}
.sidebar-header{padding:20px 16px 12px;border-bottom:1px solid var(--border)}
.sidebar-header h1{font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,var(--amd),var(--intel),var(--nvidia));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sidebar-header small{color:var(--text3);font-size:.75rem}
.nav{flex:1;padding:8px 0}
.nav-section{padding:4px 16px;font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text3);margin-top:8px}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 16px;cursor:pointer;color:var(--text2);transition:all .15s;font-size:.88rem;border-left:3px solid transparent}
.nav-item:hover{background:var(--bg3);color:var(--text)}
.nav-item.active{background:var(--bg3);color:#fff;border-left-color:var(--accent)}
.nav-item .icon{font-size:1.1rem;width:22px;text-align:center;flex-shrink:0}
.sidebar-footer{padding:12px 16px;border-top:1px solid var(--border);font-size:.7rem;color:var(--text3);text-align:center}

/* ===== MAIN ===== */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden}
.topbar{height:48px;background:var(--bg2);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:12px;flex-shrink:0}
.topbar-title{font-size:1rem;font-weight:600;flex:1}
.topbar-right{display:flex;align-items:center;gap:10px}
.topbar-search{position:relative;width:320px}
.topbar-search input{width:100%;padding:6px 12px 6px 32px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);font-size:.85rem;outline:none;transition:border-color .2s}
.topbar-search input:focus{border-color:var(--accent)}
.topbar-search::before{content:"\1F50D";position:absolute;left:8px;top:50%;transform:translateY(-50%);font-size:.85rem;pointer-events:none}
.lang-btn{padding:4px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text2);cursor:pointer;font-size:.8rem;transition:all .15s;white-space:nowrap}
.lang-btn:hover{background:var(--bg4);color:var(--text);border-color:var(--accent)}
.content{flex:1;overflow-y:auto;padding:20px}

/* ===== PAGES ===== */
.page{display:none}
.page.active{display:block}

/* ===== CARDS ===== */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-bottom:24px}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius2);padding:20px;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.card-label{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--text3);margin-bottom:6px}
.card-value{font-size:1.8rem;font-weight:700;line-height:1.2}
.card-sub{font-size:.75rem;color:var(--text2);margin-top:4px}
.card-amd .card-value{color:var(--amd)}
.card-intel .card-value{color:var(--intel)}
.card-nvidia .card-value{color:var(--nvidia)}
.card-accent .card-value{color:var(--accent2)}

/* ===== TABLES ===== */
.table-wrap{overflow-x:auto;margin-bottom:16px;border-radius:var(--radius2);border:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:.84rem}
thead{background:var(--bg3);position:sticky;top:0;z-index:5}
th{padding:10px 14px;text-align:left;font-weight:600;color:var(--text2);cursor:pointer;white-space:nowrap;user-select:none;border-bottom:1px solid var(--border);transition:color .15s}
th:hover{color:var(--text)}
th .sort-arrow{font-size:.6rem;margin-left:4px;opacity:.4}
th.sorted .sort-arrow{opacity:1;color:var(--accent)}
td{padding:8px 14px;border-bottom:1px solid var(--border);white-space:nowrap;max-width:260px;overflow:hidden;text-overflow:ellipsis}
tr{cursor:pointer;transition:background .1s}
tbody tr:hover{background:var(--bg3)}
tbody tr:active{background:var(--bg4)}

/* ===== BRAND BADGE ===== */
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:700;letter-spacing:.03em}
.badge-amd{background:rgba(237,28,36,.15);color:var(--amd2)}
.badge-intel{background:rgba(0,113,197,.15);color:var(--intel2)}
.badge-nvidia{background:rgba(118,185,0,.15);color:var(--nvidia2)}

/* ===== FILTERS ===== */
.filters{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:16px;align-items:flex-end}
.filter-group{display:flex;flex-direction:column;gap:4px}
.filter-group label{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:var(--text3)}
.filter-group select,.filter-group input{padding:6px 10px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);font-size:.82rem;outline:none}
.filter-group select:focus,.filter-group input:focus{border-color:var(--accent)}
.filter-group input[type=range]{width:120px;accent-color:var(--accent)}

/* ===== PAGINATION ===== */
.pagination{display:flex;align-items:center;gap:8px;justify-content:center;padding:12px 0}
.pagination button{padding:6px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);cursor:pointer;font-size:.82rem;transition:all .15s}
.pagination button:hover:not(:disabled){background:var(--bg4);border-color:var(--accent)}
.pagination button:disabled{opacity:.3;cursor:default}
.pagination button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.pagination-info{font-size:.78rem;color:var(--text3)}

/* ===== DETAIL PANEL ===== */
.detail-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;opacity:0;pointer-events:none;transition:opacity .25s}
.detail-overlay.open{opacity:1;pointer-events:auto}
.detail-panel{position:fixed;top:0;right:0;width:min(720px,90vw);height:100vh;background:var(--bg2);border-left:1px solid var(--border);z-index:501;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);overflow-y:auto;box-shadow:-8px 0 32px rgba(0,0,0,.5)}
.detail-panel.open{transform:translateX(0)}
.detail-header{padding:20px 24px;border-bottom:1px solid var(--border);display:flex;align-items:flex-start;gap:16px;position:sticky;top:0;background:var(--bg2);z-index:5}
.detail-header h2{font-size:1.2rem;font-weight:700;flex:1}
.detail-close{background:none;border:none;color:var(--text3);font-size:1.5rem;cursor:pointer;padding:4px 8px;border-radius:var(--radius);transition:all .15s}
.detail-close:hover{color:var(--text);background:var(--bg3)}
.detail-body{padding:20px 24px 40px}
.detail-section{margin-bottom:24px}
.detail-section h3{font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;color:var(--accent2);margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--border)}
.detail-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px 20px}
.detail-field{display:flex;justify-content:space-between;padding:4px 0;font-size:.82rem;border-bottom:1px dotted var(--border)}
.detail-field .label{color:var(--text3);flex-shrink:0;margin-right:8px}
.detail-field .value{color:var(--text);text-align:right;font-family:var(--mono);font-size:.78rem}

/* ===== BENCHMARK BARS ===== */
.bench-bar-wrap{margin-bottom:8px}
.bench-bar-label{display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:2px}
.bench-bar-label .name{color:var(--text);max-width:60%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bench-bar-label .val{color:var(--text2);font-family:var(--mono)}
.bench-bar{height:20px;background:var(--bg4);border-radius:4px;overflow:hidden;position:relative}
.bench-bar-fill{height:100%;border-radius:4px;transition:width .5s ease;min-width:2px}
.bench-bar-fill.amd{background:linear-gradient(90deg,var(--amd),var(--amd2))}
.bench-bar-fill.intel{background:linear-gradient(90deg,var(--intel),var(--intel2))}
.bench-bar-fill.nvidia{background:linear-gradient(90deg,var(--nvidia),var(--nvidia2))}

/* ===== COMPARE ===== */
.compare-bar{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.compare-bar .chip{display:flex;align-items:center;gap:6px;padding:4px 10px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;font-size:.8rem}
.compare-bar .chip .remove{background:none;border:none;color:var(--text3);cursor:pointer;font-size:.9rem;padding:0 2px}
.compare-bar .chip .remove:hover{color:var(--red)}
.compare-bar button{padding:6px 14px;background:var(--accent);border:none;border-radius:var(--radius);color:#fff;font-size:.8rem;cursor:pointer}
.compare-bar button:hover{background:var(--accent2)}
.compare-table{border:1px solid var(--border);border-radius:var(--radius2);overflow:auto}
.compare-table table{min-width:100%}
.compare-table th{background:var(--bg3);position:sticky;top:0;white-space:normal;word-wrap:break-word;max-width:220px}
.compare-table td{white-space:normal;word-wrap:break-word;max-width:220px;line-height:1.5}
.compare-table td.field{color:var(--text3);font-size:.78rem;font-weight:600;white-space:nowrap}
.compare-table td.diff{background:rgba(108,99,255,.08)}

/* ===== COMPARE MINI SEARCH ===== */
.compare-search-wrap{position:relative;flex-shrink:0}
.compare-search-wrap input{padding:6px 12px 6px 30px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;color:var(--text);font-size:.82rem;outline:none;width:260px;transition:border-color .2s}
.compare-search-wrap input:focus{border-color:var(--accent)}
.compare-search-wrap::before{content:"\1F50D";position:absolute;left:10px;top:50%;transform:translateY(-50%);font-size:.8rem;pointer-events:none}
.mini-results{position:absolute;top:calc(100% + 4px);left:0;width:480px;max-height:400px;overflow-y:auto;background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);z-index:300;display:none}
.mini-results.visible{display:block}
.mini-result{display:flex;align-items:center;gap:10px;padding:8px 12px;cursor:pointer;transition:background .1s;border-bottom:1px solid var(--border);font-size:.82rem}
.mini-result:last-child{border-bottom:none}
.mini-result:hover{background:var(--bg3)}
.mini-result .mr-name{flex:1;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mini-result .mr-type{font-size:.65rem;padding:1px 6px;border-radius:3px;font-weight:600;flex-shrink:0}
.mini-result .mr-type.cpu{background:rgba(108,99,255,.15);color:var(--accent2)}
.mini-result .mr-type.gpu{background:rgba(118,185,0,.15);color:var(--nvidia2)}
.mini-result .mr-specs{display:flex;gap:8px;font-size:.72rem;color:var(--text2);flex-shrink:0}
.mini-result .mr-add{background:var(--accent);border:none;border-radius:var(--radius);color:#fff;padding:3px 10px;font-size:.72rem;cursor:pointer;flex-shrink:0;transition:background .15s}
.mini-result .mr-add:hover{background:var(--accent2)}
.mini-result .mr-added{background:var(--green);border:none;border-radius:var(--radius);color:#fff;padding:3px 10px;font-size:.72rem;flex-shrink:0;cursor:default}

/* ===== SEARCH PAGE ===== */
.search-box{position:relative;margin-bottom:20px}
.search-box input{width:100%;padding:12px 16px 12px 44px;background:var(--bg2);border:2px solid var(--border);border-radius:var(--radius2);color:var(--text);font-size:1rem;outline:none;transition:border-color .2s}
.search-box input:focus{border-color:var(--accent)}
.search-box::before{content:"\1F50D";position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:1.1rem}
.search-results{display:flex;flex-direction:column;gap:8px}
.search-result{display:flex;align-items:center;gap:16px;padding:12px 16px;background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);cursor:pointer;transition:all .15s}
.search-result:hover{background:var(--bg3);border-color:var(--accent)}
.search-result .sr-name{font-weight:600;flex:1}
.search-result .sr-specs{display:flex;gap:12px;font-size:.78rem;color:var(--text2)}
.search-result .sr-specs span{white-space:nowrap}

/* ===== LOADING ===== */
.loading{display:flex;align-items:center;justify-content:center;padding:60px;color:var(--text3)}
.spinner{width:28px;height:28px;border:3px solid var(--bg4);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;margin-right:12px}
@keyframes spin{to{transform:rotate(360deg)}}

/* ===== SECTION TITLE ===== */
.section-title{font-size:1.2rem;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.section-title .icon{font-size:1.3rem}

/* ===== COMPARE FLOAT ===== */
.compare-float{position:fixed;bottom:20px;right:20px;background:var(--accent);color:#fff;padding:10px 18px;border-radius:30px;font-size:.85rem;font-weight:600;cursor:pointer;z-index:200;box-shadow:0 4px 16px rgba(108,99,255,.4);transition:all .2s;display:none;align-items:center;gap:8px}
.compare-float:hover{background:var(--accent2);transform:translateY(-2px)}
.compare-float.visible{display:flex}

/* ===== TOAST ===== */
.toast{position:fixed;bottom:70px;right:20px;background:var(--bg3);border:1px solid var(--border);color:var(--text);padding:10px 18px;border-radius:var(--radius);font-size:.84rem;z-index:600;opacity:0;transform:translateY(10px);transition:all .3s;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}

/* ===== RESPONSIVE ===== */
@media(max-width:768px){
  .sidebar{width:60px}
  .sidebar-header h1,.sidebar-header small,.nav-item span:not(.icon),.nav-section,.sidebar-footer{display:none}
  .nav-item{justify-content:center;padding:12px}
  .topbar-search{width:200px}
  .detail-panel{width:100vw}
  .cards{grid-template-columns:1fr 1fr}
  .mini-results{width:300px}
}

/* ===== FADE IN ===== */
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.page.active{animation:fadeIn .25s ease}
</style>
</head>
<body>
<div class="app">
  <!-- SIDEBAR -->
  <nav class="sidebar">
    <div class="sidebar-header">
      <h1>CPU &amp; GPU Viewer</h1>
      <small>AMD &bull; Intel &bull; NVIDIA</small>
    </div>
    <div class="nav">
      <div class="nav-section" data-i18n="nav-overview">Overview</div>
      <div class="nav-item active" data-page="dashboard"><span class="icon">&#x1F4CA;</span><span data-i18n="nav-dashboard">Dashboard</span></div>
      <div class="nav-section" data-i18n="nav-cpus">CPUs</div>
      <div class="nav-item" data-page="amd"><span class="icon">&#x1F534;</span><span>AMD CPUs</span></div>
      <div class="nav-item" data-page="intel"><span class="icon">&#x1F535;</span><span>Intel CPUs</span></div>
      <div class="nav-section" data-i18n="nav-gpus">GPUs</div>
      <div class="nav-item" data-page="nvidia_gpu"><span class="icon">&#x1F7E2;</span><span>NVIDIA GPUs</span></div>
      <div class="nav-item" data-page="amd_gpu"><span class="icon">&#x1F534;</span><span>AMD GPUs</span></div>
      <div class="nav-item" data-page="intel_gpu"><span class="icon">&#x1F535;</span><span>Intel GPUs</span></div>
      <div class="nav-section" data-i18n="nav-tools">Tools</div>
      <div class="nav-item" data-page="search"><span class="icon">&#x1F50D;</span><span data-i18n="nav-search">Search</span></div>
      <div class="nav-item" data-page="compare"><span class="icon">&#x2696;&#xFE0F;</span><span data-i18n="nav-compare">Compare</span></div>
      <div class="nav-item" data-page="benchmarks"><span class="icon">&#x1F4C8;</span><span data-i18n="nav-benchmarks">Benchmarks</span></div>
    </div>
    <div class="sidebar-footer" data-i18n="sidebar-footer">Built from cpus + gpus data</div>
  </nav>

  <!-- MAIN -->
  <div class="main">
    <div class="topbar">
      <div class="topbar-title" id="topbar-title">Dashboard</div>
      <div class="topbar-right">
        <div class="topbar-search">
          <input type="text" id="global-search" placeholder="Quick search CPUs & GPUs..." autocomplete="off" data-i18n-placeholder="topbar-search-ph">
        </div>
        <button class="lang-btn" id="lang-toggle" onclick="toggleLang()">EN / CN</button>
      </div>
    </div>
    <div class="content">
      <!-- DASHBOARD -->
      <div class="page active" id="page-dashboard"></div>
      <!-- CPU PAGES -->
      <div class="page" id="page-amd"></div>
      <div class="page" id="page-intel"></div>
      <!-- GPU PAGES -->
      <div class="page" id="page-nvidia_gpu"></div>
      <div class="page" id="page-amd_gpu"></div>
      <div class="page" id="page-intel_gpu"></div>
      <!-- TOOLS -->
      <div class="page" id="page-search"></div>
      <div class="page" id="page-compare"></div>
      <div class="page" id="page-benchmarks"></div>
    </div>
  </div>
</div>

<!-- COMPARE FLOATING BUTTON -->
<div class="compare-float" id="compare-float" onclick="navigateTo('compare')"><span data-i18n="compare-float">Compare</span> (<span id="compare-count">0</span>)</div>
<!-- TOAST -->
<div class="toast" id="toast"></div>

<!-- DETAIL PANEL -->
<div class="detail-overlay" id="detail-overlay"></div>
<div class="detail-panel" id="detail-panel">
  <div class="detail-header">
    <h2 id="detail-title">Name</h2>
    <button class="detail-close" id="detail-close">&times;</button>
  </div>
  <div class="detail-body" id="detail-body"></div>
</div>

<script>
// ===== EMBEDDED DATA =====
const DATA = """

PART2 = r""";

// ===== I18N =====
let currentLang = 'en';
const i18n = {
  en: {
    'nav-overview':'Overview','nav-dashboard':'Dashboard','nav-browse':'Browse',
    'nav-cpus':'CPUs','nav-gpus':'GPUs',
    'nav-tools':'Tools','nav-search':'Search','nav-compare':'Compare','nav-benchmarks':'Benchmarks',
    'sidebar-footer':'Built from cpus + gpus data',
    'topbar-search-ph':'Quick search CPUs & GPUs...',
    'compare-float':'Compare',
    'page-dashboard':'Dashboard','page-amd':'AMD CPUs','page-intel':'Intel CPUs',
    'page-nvidia_gpu':'NVIDIA GPUs','page-amd_gpu':'AMD GPUs','page-intel_gpu':'Intel GPUs',
    'page-search':'Search','page-compare':'Compare','page-benchmarks':'Benchmarks',
    'total-cpus':'Total CPUs','total-gpus':'Total GPUs','in-database':'In database',
    'amd-cpus':'AMD CPUs','intel-cpus':'Intel CPUs','of-total':'of total',
    'nvidia-gpus':'NVIDIA GPUs','amd-gpus':'AMD GPUs','intel-gpus':'Intel GPUs',
    'year-range':'Year Range','years-covered':'years covered',
    'socket-types':'Socket Types',
    'top10-cores':'Top 10 Core Counts','top10-clock':'Top 10 Clock Speeds',
    'latest-launched':'Latest CPUs Launched',
    'brand':'Brand','name':'Name','cores':'Cores','clock':'Clock','launch':'Launch',
    'threads':'Threads','clock-boost':'Clock/Boost','socket':'Socket','tdp':'TDP','fab':'Fab',
    'results':'results','clear':'Clear','all':'All',
    'year-from':'Year From','year-to':'Year To',
    'global-search-title':'Global CPU & GPU Search',
    'search-ph':'Search by name, code name, SSPEC, part number...',
    'type-at-least':'Type at least 2 characters to search',
    'no-results':'No results found',
    'result':'result','results-suffix':'s','showing-up-to':'showing up to 200',
    'cpu-comparison':'CPU & GPU Comparison','clear-all':'Clear All',
    'select-at-least':'Select at least 2 items to compare. Use the browse tables or search to add.',
    'spec':'Spec',
    'benchmark-rankings':'Benchmark Rankings','benchmark':'Benchmark','top-n':'Top N',
    'no-benchmark-data':'No data for this benchmark',
    'already-in-compare':'Already in comparison',
    'added-to-compare':'added to compare',
    // detail section headers
    'sec-product':'Product Line','sec-basic':'Basic Info','sec-core':'Core Configuration',
    'sec-fab':'Fabrication','sec-cache':'Cache','sec-mem':'Memory','sec-bus':'Bus / IO',
    'sec-gpu':'Graphics','sec-npu':'NPU','sec-isa':'Instruction Set & Features',
    'sec-bench':'Benchmarks','sec-notes':'Notes','no-bench':'No benchmark data available',
    // GPU detail sections
    'sec-gpu-basic':'Basic Info','sec-gpu-cores':'Core Config','sec-gpu-clock':'Clock & Performance',
    'sec-gpu-mem':'Memory','sec-gpu-features':'Features & API','sec-gpu-misc':'Miscellaneous',
    // detail fields
    'f-series':'Series','f-family':'Product Family','f-code':'Code Name','f-sspec':'SSPEC',
    'f-part':'Part Number','f-launch':'Launch','f-released':'Released','f-price':'Launch Price',
    'f-variant':'Variant','f-socket':'Socket','f-threads':'Threads','f-arch':'Core Arch',
    'f-config':'Core Config','f-baseclk':'Base Clock','f-boostclk':'Boost Clock',
    'f-maxclk':'Max Clock','f-boostdetail':'Boost Detail','f-multiplier':'Multiplier','f-multmax':'Multiplier Max',
    'f-multunlocked':'Multiplier Unlocked','f-vcore':'VCore','f-tdp':'TDP','f-ctdpdn':'cTDP Down',
    'f-ctdpup':'cTDP Up','f-maxtemp':'Max Temp','f-stepping':'Core Stepping',
    'f-foundry':'Foundry','f-fabproc':'Fab Process','f-fabdetail':'Fab Detail',
    'f-diesize':'Die Size','f-transistors':'Transistors','f-datawidth':'Data Width',
    'f-pkgsize':'Package Size','f-mcm':'MCM','f-mcmcfg':'MCM Config','f-multicpus':'Multi CPUs',
    'f-l1i':'L1 Instruction','f-l1d':'L1 Data','f-l2':'L2','f-l3':'L3','f-l4':'L4','f-slc':'SLC',
    'f-memtype':'Memory Type','f-memmax':'Max Memory','f-memch':'Memory Channels',
    'f-membw':'Memory Bandwidth','f-memecc':'ECC Support',
    'f-bus':'Bus','f-busspeed':'Bus Speed','f-busclk':'Bus Clock',
    'f-pcielanes':'PCIe Lanes','f-pcierev':'PCIe Revision','f-pciecfg':'PCIe Config',
    'f-ports':'Ports','f-networks':'Networks',
    'f-gpuname':'GPU Name','f-gpuclk':'GPU Clock','f-gpuboost':'GPU Boost',
    'f-gpufp32':'GPU FP32','f-gpucorecfg':'GPU Core Config',
    'f-npuname':'NPU Name','f-npuperf':'NPU Performance',
    'f-instrset':'Instruction Set','f-features':'Features',
    // GPU fields
    'f-chip':'Chip','f-codename':'Codename','f-shaderclk':'Shader Clock',
    'f-unifiedshaders':'Unified Shaders','f-pixelshaders':'Pixel Shaders','f-vertexshaders':'Vertex Shaders',
    'f-rops':'ROPs','f-tmus':'TMUs','f-cu':'Compute Units','f-cuda':'CUDA Cores',
    'f-rtcores':'RT Cores','f-tensorcores':'Tensor Cores',
    'f-pxfillrate':'Pixel Fill Rate','f-txfillrate':'Texture Fill Rate',
    'f-gfpssingle':'FP32 GFLOPS','f-gfpshalf':'FP16 GFLOPS','f-gfpsdouble':'FP64 GFLOPS',
    'f-memclk':'Memory Clock','f-memclkeff':'Memory Clock (Effective)',
    'f-mimbuswidth':'Memory Bus Width','f-numgpu':'Num GPUs','f-multi-gpu':'Multi GPU',
    'f-directx':'DirectX','f-directxfl':'DirectX Feature Level','f-opengl':'OpenGL',
    'f-opencl':'OpenCL','f-vulkan':'Vulkan',
    'f-gflopshalf':'FP16 GFLOPS','f-gfpssingleboost':'FP32 Boost','f-gfpshalfboost':'FP16 Boost',
    'f-gfpsdoubleboost':'FP64 Boost','f-multigpu':'Multi GPU',
    'yes':'Yes','no':'No',
    // compare mini search
    'mini-search-ph':'Search CPUs or GPUs to add...',
    'added':'Added',
    'add-compare':'+ Compare',
    // benchmark categories
    'bm-cat-cpu':'CPU Benchmarks','bm-cat-gpu':'GPU Benchmarks (GFLOPS)',
  },
  cn: {
    'nav-overview':'概览','nav-dashboard':'仪表盘','nav-browse':'浏览',
    'nav-cpus':'CPU','nav-gpus':'GPU',
    'nav-tools':'工具','nav-search':'搜索','nav-compare':'对比','nav-benchmarks':'跑分排行',
    'sidebar-footer':'基于 cpus + gpus 数据构建',
    'topbar-search-ph':'快速搜索 CPU 和 GPU...',
    'compare-float':'对比',
    'page-dashboard':'仪表盘','page-amd':'AMD CPU','page-intel':'Intel CPU',
    'page-nvidia_gpu':'NVIDIA GPU','page-amd_gpu':'AMD GPU','page-intel_gpu':'Intel GPU',
    'page-search':'搜索','page-compare':'对比','page-benchmarks':'跑分排行',
    'total-cpus':'CPU 总数','total-gpus':'GPU 总数','in-database':'数据库中',
    'amd-cpus':'AMD CPU','intel-cpus':'Intel CPU','of-total':'占总数',
    'nvidia-gpus':'NVIDIA GPU','amd-gpus':'AMD GPU','intel-gpus':'Intel GPU',
    'year-range':'年份范围','years-covered':'年数据',
    'socket-types':'插槽类型',
    'top10-cores':'核心数 Top 10','top10-clock':'频率 Top 10',
    'latest-launched':'最新发布的 CPU',
    'brand':'品牌','name':'名称','cores':'核心','clock':'频率','launch':'发布',
    'threads':'线程','clock-boost':'频率/睿频','socket':'插槽','tdp':'TDP','fab':'工艺',
    'results':'条结果','clear':'清除','all':'全部',
    'year-from':'起始年份','year-to':'截止年份',
    'global-search-title':'全局 CPU & GPU 搜索',
    'search-ph':'搜索名称、代号、SSPEC、部件号...',
    'type-at-least':'请输入至少 2 个字符',
    'no-results':'未找到结果',
    'result':'条','results-suffix':'','showing-up-to':'最多显示 200 条',
    'cpu-comparison':'CPU & GPU 对比','clear-all':'清空',
    'select-at-least':'请至少选择 2 项进行对比。可在浏览表格或搜索中添加。',
    'spec':'规格',
    'benchmark-rankings':'跑分排行榜','benchmark':'跑分项目','top-n':'显示数量',
    'no-benchmark-data':'暂无跑分数据',
    'already-in-compare':'已在对比列表中',
    'added-to-compare':'已加入对比',
    'sec-product':'产品线','sec-basic':'基本信息','sec-core':'核心配置',
    'sec-fab':'制造工艺','sec-cache':'缓存','sec-mem':'内存','sec-bus':'总线 / IO',
    'sec-gpu':'集成显卡','sec-npu':'NPU','sec-isa':'指令集与特性',
    'sec-bench':'跑分','sec-notes':'备注','no-bench':'暂无跑分数据',
    'sec-gpu-basic':'基本信息','sec-gpu-cores':'核心配置','sec-gpu-clock':'频率与性能',
    'sec-gpu-mem':'显存','sec-gpu-features':'特性与 API','sec-gpu-misc':'其他',
    'f-series':'系列','f-family':'产品族','f-code':'代号','f-sspec':'SSPEC',
    'f-part':'部件号','f-launch':'发布','f-released':'已发布','f-price':'首发价',
    'f-variant':'变体','f-socket':'插槽','f-threads':'线程','f-arch':'核心架构',
    'f-config':'核心配置','f-baseclk':'基础频率','f-boostclk':'睿频',
    'f-maxclk':'最大频率','f-boostdetail':'睿频详情','f-multiplier':'倍频','f-multmax':'最大倍频',
    'f-multunlocked':'倍频解锁','f-vcore':'核心电压','f-tdp':'TDP','f-ctdpdn':'cTDP 下限',
    'f-ctdpup':'cTDP 上限','f-maxtemp':'最高温度','f-stepping':'步进',
    'f-foundry':'代工厂','f-fabproc':'工艺制程','f-fabdetail':'工艺详情',
    'f-diesize':'芯片面积','f-transistors':'晶体管','f-datawidth':'数据位宽',
    'f-pkgsize':'封装尺寸','f-mcm':'MCM','f-mcmcfg':'MCM 配置','f-multicpus':'多路',
    'f-l1i':'L1 指令','f-l1d':'L1 数据','f-l2':'L2','f-l3':'L3','f-l4':'L4','f-slc':'SLC',
    'f-memtype':'内存类型','f-memmax':'最大内存','f-memch':'内存通道',
    'f-membw':'内存带宽','f-memecc':'ECC 支持',
    'f-bus':'总线','f-busspeed':'总线速度','f-busclk':'总线频率',
    'f-pcielanes':'PCIe 通道','f-pcierev':'PCIe 版本','f-pciecfg':'PCIe 配置',
    'f-ports':'端口','f-networks':'网络',
    'f-gpuname':'GPU 名称','f-gpuclk':'GPU 频率','f-gpuboost':'GPU 睿频',
    'f-gpufp32':'GPU FP32','f-gpucorecfg':'GPU 核心配置',
    'f-npuname':'NPU 名称','f-npuperf':'NPU 性能',
    'f-instrset':'指令集','f-features':'特性',
    'f-chip':'芯片','f-codename':'代号','f-shaderclk':'着色器频率',
    'f-unifiedshaders':'统一着色器','f-pixelshaders':'像素着色器','f-vertexshaders':'顶点着色器',
    'f-rops':'ROPs','f-tmus':'TMUs','f-cu':'计算单元','f-cuda':'CUDA 核心',
    'f-rtcores':'RT 核心','f-tensorcores':'Tensor 核心',
    'f-pxfillrate':'像素填充率','f-txfillrate':'纹理填充率',
    'f-gfpssingle':'FP32 GFLOPS','f-gfpshalf':'FP16 GFLOPS','f-gfpsdouble':'FP64 GFLOPS',
    'f-memclk':'显存频率','f-memclkeff':'显存等效频率',
    'f-mimbuswidth':'显存位宽','f-numgpu':'GPU 数量','f-multi-gpu':'多 GPU',
    'f-directx':'DirectX','f-directxfl':'DirectX 功能级别','f-opengl':'OpenGL',
    'f-opencl':'OpenCL','f-vulkan':'Vulkan',
    'f-gflopshalf':'FP16 GFLOPS','f-gfpssingleboost':'FP32 Boost','f-gfpshalfboost':'FP16 Boost',
    'f-gfpsdoubleboost':'FP64 Boost','f-multigpu':'多 GPU',
    'yes':'是','no':'否',
    'mini-search-ph':'搜索要添加的 CPU 或 GPU...',
    'added':'已添加',
    'add-compare':'+ 对比',
    'bm-cat-cpu':'CPU 跑分','bm-cat-gpu':'GPU 跑分 (GFLOPS)',
  }
};

function t(key) { return (i18n[currentLang] && i18n[currentLang][key]) || i18n.en[key] || key; }

function applyLang() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (i18n[currentLang][key] !== undefined) el.textContent = i18n[currentLang][key];
    else if (i18n.en[key] !== undefined) el.textContent = i18n.en[key];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const val = i18n[currentLang][key] || i18n.en[key];
    if (val) el.placeholder = val;
  });
  $('#topbar-title').textContent = t('page-' + currentPage);
}

function toggleLang() {
  currentLang = currentLang === 'en' ? 'cn' : 'en';
  applyLang();
  if (currentPage === 'dashboard') renderDashboard();
  if (currentPage === 'amd') renderCpuBrowse('amd');
  if (currentPage === 'intel') renderCpuBrowse('intel');
  if (currentPage === 'nvidia_gpu') renderGpuBrowse('nvidia');
  if (currentPage === 'amd_gpu') renderGpuBrowse('amd');
  if (currentPage === 'intel_gpu') renderGpuBrowse('intel');
  if (currentPage === 'search') renderSearchPage();
  if (currentPage === 'compare') renderCompare();
  if (currentPage === 'benchmarks') renderBenchmarks();
}

// ===== HELPERS =====
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const pf = v => { if(v===null||v===undefined||v==='') return '—'; const n=parseFloat(v); return isNaN(n)?v:n; };
const fmt = (v,unit) => { if(v===null||v===undefined||v==='') return '—'; const n=parseFloat(v); if(isNaN(n)) return v; return unit?n.toLocaleString()+' '+unit:n.toLocaleString(); };
const safe = v => (v===null||v===undefined)?'':String(v);

// ===== CPU DATA =====
const amdCpuById = {}, intelCpuById = {};
DATA.amd_cpu.forEach(c=>{ amdCpuById[c.id]=c; });
DATA.intel_cpu.forEach(c=>{ intelCpuById[c.id]=c; });
const amdDataByCpuId = {}, intelDataByCpuId = {};
DATA.amd_cpu_data.forEach(d=>{ amdDataByCpuId[d.id_cpu]=d; });
DATA.intel_cpu_data.forEach(d=>{ intelDataByCpuId[d.id_cpu]=d; });
const cpuSeriesById = {};
DATA.amd_series.forEach(s=>{ cpuSeriesById['a_'+s.id]=s; });
DATA.intel_series.forEach(s=>{ cpuSeriesById['i_'+s.id]=s; });
const cpuProductsById = {};
DATA.amd_products.forEach(p=>{ cpuProductsById['a_'+p.id]=p; });
DATA.intel_products.forEach(p=>{ cpuProductsById['i_'+p.id]=p; });
const amdSockets = {};
DATA.amd_socket.forEach(s=>{ amdSockets[s.id]=s.name; });
const intelSockets = {};
DATA.intel_socket.forEach(s=>{ intelSockets[s.id]=s.name; });

function mergeCpus(cpuList, dataList, brand) {
  const byId = {};
  dataList.forEach(d => { byId[d.id_cpu] = d; });
  return cpuList.map(c => {
    const d = byId[c.id] || {};
    return { ...c, ...d, _type:'cpu', _brand:brand, _id:c.id };
  });
}
const amdMerged = mergeCpus(DATA.amd_cpu, DATA.amd_cpu_data, 'amd');
const intelMerged = mergeCpus(DATA.intel_cpu, DATA.intel_cpu_data, 'intel');
const allCpus = [...amdMerged, ...intelMerged];

// ===== GPU DATA =====
const gpuSeriesById = {};
DATA.amd_series.forEach(s=>{ gpuSeriesById['a_'+s.id]=s; });
DATA.intel_series.forEach(s=>{ gpuSeriesById['i_'+s.id]=s; });
DATA.nvidia_series.forEach(s=>{ gpuSeriesById['n_'+s.id]=s; });
const gpuProductsById = {};
DATA.amd_products.forEach(p=>{ gpuProductsById['a_'+p.id]=p; });
DATA.intel_products.forEach(p=>{ gpuProductsById['i_'+p.id]=p; });
DATA.nvidia_products.forEach(p=>{ gpuProductsById['n_'+p.id]=p; });

function mergeGpus(gpuList, dataList, brand) {
  const byId = {};
  dataList.forEach(d => { byId[d.id_gpu] = d; });
  return gpuList.map(g => {
    const d = byId[g.id] || {};
    return { ...g, ...d, _type:'gpu', _brand:brand, _id:g.id };
  });
}
const nvidiaMerged = mergeGpus(DATA.nvidia_gpu, DATA.nvidia_gpu_data, 'nvidia');
const amdGpuMerged = mergeGpus(DATA.amd_gpu, DATA.amd_gpu_data, 'amd');
const intelGpuMerged = mergeGpus(DATA.intel_gpu, DATA.intel_gpu_data, 'intel');
const allGpus = [...nvidiaMerged, ...amdGpuMerged, ...intelGpuMerged];
const allItems = [...allCpus, ...allGpus];

// Build gflops lookup for GPUs
const gpuGflopsById = {};
DATA.nvidia_gflops.forEach(g=>{ if(!gpuGflopsById[g.name]) gpuGflopsById[g.name]=[]; gpuGflopsById[g.name].push(g); });
DATA.amd_gflops.forEach(g=>{ if(!gpuGflopsById[g.name]) gpuGflopsById[g.name]=[]; gpuGflopsById[g.name].push(g); });
DATA.intel_gflops.forEach(g=>{ if(!gpuGflopsById[g.name]) gpuGflopsById[g.name]=[]; gpuGflopsById[g.name].push(g); });

// ===== NAVIGATION =====
let currentPage = 'dashboard';
const pageTitles = {
  dashboard:'page-dashboard', amd:'page-amd', intel:'page-intel',
  nvidia_gpu:'page-nvidia_gpu', amd_gpu:'page-amd_gpu', intel_gpu:'page-intel_gpu',
  search:'page-search', compare:'page-compare', benchmarks:'page-benchmarks'
};

function navigateTo(page) {
  currentPage = page;
  $$('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.page === page));
  $$('.page').forEach(p => p.classList.toggle('active', p.id === 'page-' + page));
  $('#topbar-title').textContent = t(pageTitles[page] || page);
  if (page === 'dashboard') renderDashboard();
  if (page === 'amd') renderCpuBrowse('amd');
  if (page === 'intel') renderCpuBrowse('intel');
  if (page === 'nvidia_gpu') renderGpuBrowse('nvidia');
  if (page === 'amd_gpu') renderGpuBrowse('amd');
  if (page === 'intel_gpu') renderGpuBrowse('intel');
  if (page === 'search') renderSearchPage();
  if (page === 'compare') renderCompare();
  if (page === 'benchmarks') renderBenchmarks();
}

$$('.nav-item').forEach(n => n.addEventListener('click', () => navigateTo(n.dataset.page)));

// Global search in topbar
$('#global-search').addEventListener('input', e => {
  const q = e.target.value.trim();
  if (q.length >= 2) {
    navigateTo('search');
    $('#search-input').value = q;
    renderSearchResults(q);
  }
});

// ===== DASHBOARD =====
function renderDashboard() {
  const el = $('#page-dashboard');
  const amdCpuCount = DATA.amd_cpu.length;
  const intelCpuCount = DATA.intel_cpu.length;
  const totalCpus = amdCpuCount + intelCpuCount;
  const nvidiaGpuCount = DATA.nvidia_gpu.length;
  const amdGpuCount = DATA.amd_gpu.length;
  const intelGpuCount = DATA.intel_gpu.length;
  const totalGpus = nvidiaGpuCount + amdGpuCount + intelGpuCount;

  const cpuYears = allCpus.map(c => extractYear(c.launch)).filter(Boolean);
  const gpuYears = allGpus.map(g => extractYear(g.launch)).filter(Boolean);
  const allYears = [...cpuYears, ...gpuYears];
  const minYear = allYears.length ? Math.min(...allYears) : 0;
  const maxYear = allYears.length ? Math.max(...allYears) : 0;

  const latestCpus = allCpus.filter(c => c.launch).sort((a,b) => (b.launch||'').localeCompare(a.launch||'')).slice(0, 8);
  const latestGpus = allGpus.filter(g => g.launch).sort((a,b) => (b.launch||'').localeCompare(a.launch||'')).slice(0, 8);

  const badgeClass = item => item._type === 'gpu' ? 'badge-' + item._brand : 'badge-' + item._brand;

  el.innerHTML =
    '<div class="cards">' +
      '<div class="card card-accent"><div class="card-label">'+t('total-cpus')+'</div><div class="card-value">'+totalCpus.toLocaleString()+'</div><div class="card-sub">'+t('in-database')+'</div></div>' +
      '<div class="card card-amd"><div class="card-label">'+t('amd-cpus')+'</div><div class="card-value">'+amdCpuCount.toLocaleString()+'</div><div class="card-sub">'+(amdCpuCount/totalCpus*100).toFixed(1)+'% '+t('of-total')+'</div></div>' +
      '<div class="card card-intel"><div class="card-label">'+t('intel-cpus')+'</div><div class="card-value">'+intelCpuCount.toLocaleString()+'</div><div class="card-sub">'+(intelCpuCount/totalCpus*100).toFixed(1)+'% '+t('of-total')+'</div></div>' +
      '<div class="card card-accent"><div class="card-label">'+t('total-gpus')+'</div><div class="card-value">'+totalGpus.toLocaleString()+'</div><div class="card-sub">'+t('in-database')+'</div></div>' +
      '<div class="card card-nvidia"><div class="card-label">'+t('nvidia-gpus')+'</div><div class="card-value">'+nvidiaGpuCount.toLocaleString()+'</div><div class="card-sub">'+(nvidiaGpuCount/totalGpus*100).toFixed(1)+'% '+t('of-total')+'</div></div>' +
      '<div class="card card-amd"><div class="card-label">'+t('amd-gpus')+'</div><div class="card-value">'+amdGpuCount.toLocaleString()+'</div><div class="card-sub">'+(amdGpuCount/totalGpus*100).toFixed(1)+'% '+t('of-total')+'</div></div>' +
      '<div class="card card-intel"><div class="card-label">'+t('intel-gpus')+'</div><div class="card-value">'+intelGpuCount.toLocaleString()+'</div><div class="card-sub">'+(intelGpuCount/totalGpus*100).toFixed(1)+'% '+t('of-total')+'</div></div>' +
      '<div class="card"><div class="card-label">'+t('year-range')+'</div><div class="card-value">'+minYear+'–'+maxYear+'</div><div class="card-sub">'+(maxYear-minYear+1)+' '+t('years-covered')+'</div></div>' +
    '</div>' +
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:8px">' +
      '<div>' +
        '<h3 class="section-title"><span class="icon">&#x1F195;</span> '+t('latest-launched')+' (CPU)</h3>' +
        '<div class="table-wrap"><table>' +
          '<thead><tr><th>'+t('brand')+'</th><th>'+t('name')+'</th><th>'+t('cores')+'</th><th>'+t('f-baseclk')+'</th><th>'+t('f-boostclk')+'</th><th>'+t('launch')+'</th></tr></thead>' +
          '<tbody>'+latestCpus.map(c=>'<tr onclick="openCpuDetail(\''+c._brand+'\','+c._id+')">' +
            '<td><span class="badge badge-'+c._brand+'">'+c._brand.toUpperCase()+'</span></td>' +
            '<td>'+safe(c.name)+'</td><td>'+safe(c.cores)+'</td><td>'+fmt(c.core_clk,'MHz')+'</td><td>'+fmt(c.core_clk_boost,'MHz')+'</td><td>'+safe(c.launch)+'</td>' +
          '</tr>').join('')+'</tbody>' +
        '</table></div>' +
      '</div>' +
      '<div>' +
        '<h3 class="section-title"><span class="icon">&#x1F195;</span> '+t('latest-launched')+' (GPU)</h3>' +
        '<div class="table-wrap"><table>' +
          '<thead><tr><th>'+t('brand')+'</th><th>'+t('name')+'</th><th>'+t('f-cuda')+'</th><th>'+t('f-boostclk')+'</th><th>'+t('f-memtype')+'</th><th>'+t('launch')+'</th></tr></thead>' +
          '<tbody>'+latestGpus.map(g=>'<tr onclick="openGpuDetail(\''+g._brand+'\','+g._id+')">' +
            '<td><span class="badge badge-'+g._brand+'">'+g._brand.toUpperCase()+'</span></td>' +
            '<td>'+safe(g.name)+'</td><td>'+safe(g.cuda||g.cores)+'</td><td>'+fmt(g.core_clk_boost,'MHz')+'</td><td>'+safe(g.memory_type)+'</td><td>'+safe(g.launch)+'</td>' +
          '</tr>').join('')+'</tbody>' +
        '</table></div>' +
      '</div>' +
    '</div>';
}

// ===== CPU BROWSE TABLES =====
const cpuBrowseState = {
  amd: { page:1, sort:'name', sortDir:1, filters:{ socket:'', cores:'', fab:'', yearStart:'', yearEnd:'' } },
  intel: { page:1, sort:'name', sortDir:1, filters:{ socket:'', cores:'', fab:'', yearStart:'', yearEnd:'' } }
};
const PAGE_SIZE = 50;

function extractYear(launch) {
  if (!launch) return null;
  if (/^\d{6}$/.test(launch)) return parseInt(launch.substring(0, 4));
  const m = launch.match(/(\d{4})/);
  return m ? parseInt(m[1]) : null;
}

function getFilteredCpus(brand) {
  const st = cpuBrowseState[brand];
  const merged = brand === 'amd' ? amdMerged : intelMerged;
  let rows = [...merged];
  const f = st.filters;
  if (f.socket) rows = rows.filter(r => safe(r.socket).toLowerCase().includes(f.socket.toLowerCase()));
  if (f.cores) rows = rows.filter(r => String(r.cores) === f.cores);
  if (f.fab) rows = rows.filter(r => safe(r.fab).toLowerCase().includes(f.fab.toLowerCase()));
  if (f.yearStart) { const ys = parseInt(f.yearStart); rows = rows.filter(r => { const y = extractYear(r.launch); return y !== null && y >= ys; }); }
  if (f.yearEnd) { const ye = parseInt(f.yearEnd); rows = rows.filter(r => { const y = extractYear(r.launch); return y !== null && y <= ye; }); }
  const key = st.sort, dir = st.sortDir;
  rows.sort((a, b) => {
    let va = a[key], vb = b[key];
    if (va === null || va === undefined) va = '';
    if (vb === null || vb === undefined) vb = '';
    const na = parseFloat(va), nb = parseFloat(vb);
    if (!isNaN(na) && !isNaN(nb)) return (na - nb) * dir;
    return String(va).localeCompare(String(vb)) * dir;
  });
  return rows;
}

function renderCpuBrowse(brand) {
  const el = $('#page-' + brand);
  const st = cpuBrowseState[brand];
  const rows = getFilteredCpus(brand);
  const totalPages = Math.ceil(rows.length / PAGE_SIZE);
  if (st.page > totalPages) st.page = totalPages || 1;
  const start = (st.page - 1) * PAGE_SIZE;
  const pageRows = rows.slice(start, start + PAGE_SIZE);
  const merged = brand === 'amd' ? amdMerged : intelMerged;
  const sockets = [...new Set(merged.map(r => r.socket).filter(Boolean))].sort();
  const coresList = [...new Set(merged.map(r => r.cores).filter(Boolean))].sort((a,b)=>parseInt(a)-parseInt(b));
  const fabs = [...new Set(merged.map(r => r.fab).filter(Boolean))].sort();
  const sortArrow = col => '<span class="sort-arrow">'+(st.sort===col?(st.sortDir===1?'▲':'▼'):'⇅')+'</span>';
  const thStyle = col => st.sort === col ? 'sorted' : '';
  const makeSort = col => 'onclick="sortCpuBrowse(\''+brand+'\',\''+col+'\')"';

  el.innerHTML =
    '<div class="filters">' +
      '<div class="filter-group"><label>'+t('socket')+'</label><select onchange="filterCpuBrowse(\''+brand+'\',\'socket\',this.value)"><option value="">'+t('all')+'</option>'+sockets.map(s=>'<option value="'+s+'" '+(st.filters.socket===s?'selected':'')+'>'+s+'</option>').join('')+'</select></div>' +
      '<div class="filter-group"><label>'+t('cores')+'</label><select onchange="filterCpuBrowse(\''+brand+'\',\'cores\',this.value)"><option value="">'+t('all')+'</option>'+coresList.map(c=>'<option value="'+c+'" '+(st.filters.cores===c?'selected':'')+'>'+c+'</option>').join('')+'</select></div>' +
      '<div class="filter-group"><label>'+t('fab')+' (nm)</label><select onchange="filterCpuBrowse(\''+brand+'\',\'fab\',this.value)"><option value="">'+t('all')+'</option>'+fabs.map(f=>'<option value="'+f+'" '+(st.filters.fab===f?'selected':'')+'>'+f+'</option>').join('')+'</select></div>' +
      '<div class="filter-group"><label>'+t('year-from')+'</label><input type="number" min="1990" max="2030" value="'+st.filters.yearStart+'" placeholder="e.g. 2020" onchange="filterCpuBrowse(\''+brand+'\',\'yearStart\',this.value)"></div>' +
      '<div class="filter-group"><label>'+t('year-to')+'</label><input type="number" min="1990" max="2030" value="'+st.filters.yearEnd+'" placeholder="e.g. 2025" onchange="filterCpuBrowse(\''+brand+'\',\'yearEnd\',this.value)"></div>' +
      '<div class="filter-group"><label>&nbsp;</label><button onclick="clearCpuFilters(\''+brand+'\')" style="padding:6px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);cursor:pointer;font-size:.82rem">'+t('clear')+'</button></div>' +
    '</div>' +
    '<div style="font-size:.78rem;color:var(--text3);margin-bottom:8px">'+rows.length.toLocaleString()+' '+t('results')+'</div>' +
    '<div class="table-wrap"><table>' +
      '<thead><tr>' +
        '<th class="'+thStyle('name')+'" '+makeSort('name')+'>'+t('name')+' '+sortArrow('name')+'</th>' +
        '<th class="'+thStyle('cores')+'" '+makeSort('cores')+'>'+t('cores')+' '+sortArrow('cores')+'</th>' +
        '<th class="'+thStyle('threads')+'" '+makeSort('threads')+'>'+t('threads')+' '+sortArrow('threads')+'</th>' +
        '<th class="'+thStyle('core_clk')+'" '+makeSort('core_clk')+'>'+t('f-baseclk')+' '+sortArrow('core_clk')+'</th>' +
        '<th class="'+thStyle('core_clk_boost')+'" '+makeSort('core_clk_boost')+'>'+t('f-boostclk')+' '+sortArrow('core_clk_boost')+'</th>' +
        '<th class="'+thStyle('core_clk_max')+'" '+makeSort('core_clk_max')+'>'+t('f-maxclk')+' '+sortArrow('core_clk_max')+'</th>' +
        '<th class="'+thStyle('socket')+'" '+makeSort('socket')+'>'+t('socket')+' '+sortArrow('socket')+'</th>' +
        '<th class="'+thStyle('tdp')+'" '+makeSort('tdp')+'>'+t('tdp')+' '+sortArrow('tdp')+'</th>' +
        '<th class="'+thStyle('launch')+'" '+makeSort('launch')+'>'+t('launch')+' '+sortArrow('launch')+'</th>' +
        '<th class="'+thStyle('fab')+'" '+makeSort('fab')+'>'+t('fab')+' '+sortArrow('fab')+'</th>' +
        '<th style="cursor:default;width:40px"></th>' +
      '</tr></thead>' +
      '<tbody>'+pageRows.map(r => '<tr onclick="openCpuDetail(\''+brand+'\','+r._id+')">' +
        '<td title="'+safe(r.name)+'">'+safe(r.name)+'</td>' +
        '<td>'+safe(r.cores)+'</td><td>'+safe(r.threads)+'</td>' +
        '<td>'+fmt(r.core_clk,'MHz')+'</td><td>'+fmt(r.core_clk_boost,'MHz')+'</td><td>'+fmt(r.core_clk_max,'MHz')+'</td>' +
        '<td>'+safe(r.socket)+'</td><td>'+fmt(r.tdp,'W')+'</td><td>'+safe(r.launch)+'</td><td>'+fmt(r.fab,'nm')+'</td>' +
        '<td onclick="event.stopPropagation();addToCompare(\''+r._type+'\',\''+brand+'\','+r._id+')" title="'+t('add-compare')+'" style="text-align:center;cursor:pointer;font-size:1.1rem;color:var(--accent)">+</td>' +
      '</tr>').join('')+'</tbody>' +
    '</table></div>' +
    '<div class="pagination">' +
      '<button '+(st.page<=1?'disabled':'')+' onclick="goCpuPage(\''+brand+'\',1)">«</button>' +
      '<button '+(st.page<=1?'disabled':'')+' onclick="goCpuPage(\''+brand+'\','+(st.page-1)+')">‹</button>' +
      '<span class="pagination-info">Page '+st.page+' / '+totalPages+'</span>' +
      '<button '+(st.page>=totalPages?'disabled':'')+' onclick="goCpuPage(\''+brand+'\','+(st.page+1)+')">›</button>' +
      '<button '+(st.page>=totalPages?'disabled':'')+' onclick="goCpuPage(\''+brand+'\','+totalPages+')">»</button>' +
    '</div>';
}
function sortCpuBrowse(brand,col){const st=cpuBrowseState[brand];if(st.sort===col)st.sortDir*=-1;else{st.sort=col;st.sortDir=1;}renderCpuBrowse(brand);}
function filterCpuBrowse(brand,key,val){cpuBrowseState[brand].filters[key]=val;cpuBrowseState[brand].page=1;renderCpuBrowse(brand);}
function clearCpuFilters(brand){cpuBrowseState[brand].filters={socket:'',cores:'',fab:'',yearStart:'',yearEnd:''};cpuBrowseState[brand].page=1;renderCpuBrowse(brand);}
function goCpuPage(brand,p){cpuBrowseState[brand].page=p;renderCpuBrowse(brand);}

// ===== GPU BROWSE TABLES =====
const gpuBrowseState = {
  nvidia: { page:1, sort:'name', sortDir:1, filters:{ arch:'', memType:'', yearStart:'', yearEnd:'' } },
  amd: { page:1, sort:'name', sortDir:1, filters:{ arch:'', memType:'', yearStart:'', yearEnd:'' } },
  intel: { page:1, sort:'name', sortDir:1, filters:{ arch:'', memType:'', yearStart:'', yearEnd:'' } }
};

function getFilteredGpus(vendor) {
  const st = gpuBrowseState[vendor];
  const merged = vendor === 'nvidia' ? nvidiaMerged : vendor === 'amd' ? amdGpuMerged : intelGpuMerged;
  let rows = [...merged];
  const f = st.filters;
  if (f.arch) rows = rows.filter(r => safe(r.arch).toLowerCase().includes(f.arch.toLowerCase()));
  if (f.memType) rows = rows.filter(r => safe(r.memory_type).toLowerCase().includes(f.memType.toLowerCase()));
  if (f.yearStart) { const ys = parseInt(f.yearStart); rows = rows.filter(r => { const y = extractYear(r.launch); return y !== null && y >= ys; }); }
  if (f.yearEnd) { const ye = parseInt(f.yearEnd); rows = rows.filter(r => { const y = extractYear(r.launch); return y !== null && y <= ye; }); }
  const key = st.sort, dir = st.sortDir;
  rows.sort((a, b) => {
    let va = a[key], vb = b[key];
    if (va === null || va === undefined) va = '';
    if (vb === null || vb === undefined) vb = '';
    const na = parseFloat(va), nb = parseFloat(vb);
    if (!isNaN(na) && !isNaN(nb)) return (na - nb) * dir;
    return String(va).localeCompare(String(vb)) * dir;
  });
  return rows;
}

function renderGpuBrowse(vendor) {
  const pageKey = vendor + '_gpu';
  const el = $('#page-' + pageKey);
  const st = gpuBrowseState[vendor];
  const rows = getFilteredGpus(vendor);
  const totalPages = Math.ceil(rows.length / PAGE_SIZE);
  if (st.page > totalPages) st.page = totalPages || 1;
  const start = (st.page - 1) * PAGE_SIZE;
  const pageRows = rows.slice(start, start + PAGE_SIZE);
  const merged = vendor === 'nvidia' ? nvidiaMerged : vendor === 'amd' ? amdGpuMerged : intelGpuMerged;
  const archs = [...new Set(merged.map(r => r.arch).filter(Boolean))].sort();
  const memTypes = [...new Set(merged.map(r => r.memory_type).filter(Boolean))].sort();
  const sortArrow = col => '<span class="sort-arrow">'+(st.sort===col?(st.sortDir===1?'▲':'▼'):'⇅')+'</span>';
  const thStyle = col => st.sort === col ? 'sorted' : '';
  const makeSort = col => 'onclick="sortGpuBrowse(\''+vendor+'\',\''+col+'\')"';

  el.innerHTML =
    '<div class="filters">' +
      '<div class="filter-group"><label>'+t('f-arch')+'</label><select onchange="filterGpuBrowse(\''+vendor+'\',\'arch\',this.value)"><option value="">'+t('all')+'</option>'+archs.map(a=>'<option value="'+a+'" '+(st.filters.arch===a?'selected':'')+'>'+a+'</option>').join('')+'</select></div>' +
      '<div class="filter-group"><label>'+t('f-memtype')+'</label><select onchange="filterGpuBrowse(\''+vendor+'\',\'memType\',this.value)"><option value="">'+t('all')+'</option>'+memTypes.map(m=>'<option value="'+m+'" '+(st.filters.memType===m?'selected':'')+'>'+m+'</option>').join('')+'</select></div>' +
      '<div class="filter-group"><label>'+t('year-from')+'</label><input type="number" min="1990" max="2030" value="'+st.filters.yearStart+'" placeholder="e.g. 2020" onchange="filterGpuBrowse(\''+vendor+'\',\'yearStart\',this.value)"></div>' +
      '<div class="filter-group"><label>'+t('year-to')+'</label><input type="number" min="1990" max="2030" value="'+st.filters.yearEnd+'" placeholder="e.g. 2025" onchange="filterGpuBrowse(\''+vendor+'\',\'yearEnd\',this.value)"></div>' +
      '<div class="filter-group"><label>&nbsp;</label><button onclick="clearGpuFilters(\''+vendor+'\')" style="padding:6px 14px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);cursor:pointer;font-size:.82rem">'+t('clear')+'</button></div>' +
    '</div>' +
    '<div style="font-size:.78rem;color:var(--text3);margin-bottom:8px">'+rows.length.toLocaleString()+' '+t('results')+'</div>' +
    '<div class="table-wrap"><table>' +
      '<thead><tr>' +
        '<th class="'+thStyle('name')+'" '+makeSort('name')+'>'+t('name')+' '+sortArrow('name')+'</th>' +
        '<th class="'+thStyle('arch')+'" '+makeSort('arch')+'>'+t('f-arch')+' '+sortArrow('arch')+'</th>' +
        '<th class="'+thStyle('cuda')+'" '+makeSort('cuda')+'>'+t('f-cuda')+' '+sortArrow('cuda')+'</th>' +
        '<th class="'+thStyle('core_clk')+'" '+makeSort('core_clk')+'>'+t('f-baseclk')+' '+sortArrow('core_clk')+'</th>' +
        '<th class="'+thStyle('core_clk_boost')+'" '+makeSort('core_clk_boost')+'>'+t('f-boostclk')+' '+sortArrow('core_clk_boost')+'</th>' +
        '<th class="'+thStyle('memory_size')+'" '+makeSort('memory_size')+'>'+t('f-memmax')+' '+sortArrow('memory_size')+'</th>' +
        '<th class="'+thStyle('memory_type')+'" '+makeSort('memory_type')+'>'+t('f-memtype')+' '+sortArrow('memory_type')+'</th>' +
        '<th class="'+thStyle('memory_bus_width')+'" '+makeSort('memory_bus_width')+'>'+t('f-mimbuswidth')+' '+sortArrow('memory_bus_width')+'</th>' +
        '<th class="'+thStyle('tdp')+'" '+makeSort('tdp')+'>'+t('tdp')+' '+sortArrow('tdp')+'</th>' +
        '<th class="'+thStyle('launch')+'" '+makeSort('launch')+'>'+t('launch')+' '+sortArrow('launch')+'</th>' +
        '<th style="cursor:default;width:40px"></th>' +
      '</tr></thead>' +
      '<tbody>'+pageRows.map(r => '<tr onclick="openGpuDetail(\''+vendor+'\','+r._id+')">' +
        '<td title="'+safe(r.name)+'">'+safe(r.name)+'</td>' +
        '<td>'+safe(r.arch)+'</td><td>'+safe(r.cuda||r.cores)+'</td>' +
        '<td>'+fmt(r.core_clk,'MHz')+'</td><td>'+fmt(r.core_clk_boost,'MHz')+'</td>' +
        '<td>'+fmt(r.memory_size,'MB')+'</td><td>'+safe(r.memory_type)+'</td><td>'+fmt(r.memory_bus_width,'bit')+'</td>' +
        '<td>'+fmt(r.tdp,'W')+'</td><td>'+safe(r.launch)+'</td>' +
        '<td onclick="event.stopPropagation();addToCompare(\'gpu\',\''+vendor+'\','+r._id+')" title="'+t('add-compare')+'" style="text-align:center;cursor:pointer;font-size:1.1rem;color:var(--accent)">+</td>' +
      '</tr>').join('')+'</tbody>' +
    '</table></div>' +
    '<div class="pagination">' +
      '<button '+(st.page<=1?'disabled':'')+' onclick="goGpuPage(\''+vendor+'\',1)">«</button>' +
      '<button '+(st.page<=1?'disabled':'')+' onclick="goGpuPage(\''+vendor+'\','+(st.page-1)+')">‹</button>' +
      '<span class="pagination-info">Page '+st.page+' / '+totalPages+'</span>' +
      '<button '+(st.page>=totalPages?'disabled':'')+' onclick="goGpuPage(\''+vendor+'\','+(st.page+1)+')">›</button>' +
      '<button '+(st.page>=totalPages?'disabled':'')+' onclick="goGpuPage(\''+vendor+'\','+totalPages+')">»</button>' +
    '</div>';
}
function sortGpuBrowse(vendor,col){const st=gpuBrowseState[vendor];if(st.sort===col)st.sortDir*=-1;else{st.sort=col;st.sortDir=1;}renderGpuBrowse(vendor);}
function filterGpuBrowse(vendor,key,val){gpuBrowseState[vendor].filters[key]=val;gpuBrowseState[vendor].page=1;renderGpuBrowse(vendor);}
function clearGpuFilters(vendor){gpuBrowseState[vendor].filters={arch:'',memType:'',yearStart:'',yearEnd:''};gpuBrowseState[vendor].page=1;renderGpuBrowse(vendor);}
function goGpuPage(vendor,p){gpuBrowseState[vendor].page=p;renderGpuBrowse(vendor);}

// ===== CPU DETAIL PANEL =====
function openCpuDetail(brand, cpuId) {
  const cpuList = brand === 'amd' ? DATA.amd_cpu : DATA.intel_cpu;
  const dataList = brand === 'amd' ? DATA.amd_cpu_data : DATA.intel_cpu_data;
  const cpu = cpuList.find(c => parseInt(c.id) === cpuId);
  const data = dataList.find(d => parseInt(d.id_cpu) === cpuId);
  if (!cpu && !data) return;
  const d = { ...(cpu||{}), ...(data||{}) };

  $('#detail-title').innerHTML = '<span class="badge badge-'+brand+'">'+brand.toUpperCase()+' CPU</span> '+safe(d.name)+' <button onclick="addToCompare(\'cpu\',\''+brand+'\','+cpuId+')" style="margin-left:12px;padding:4px 12px;background:var(--accent);border:none;border-radius:var(--radius);color:#fff;font-size:.75rem;cursor:pointer;vertical-align:middle">'+t('add-compare')+'</button>';

  let seriesInfo = '';
  if (cpu && cpu.id_serie) {
    const sk = brand[0] + '_' + cpu.id_serie;
    const s = cpuSeriesById[sk];
    if (s) {
      const pk = brand[0] + '_' + s.id_product_family;
      const p = cpuProductsById[pk];
      seriesInfo = field(t('f-series'), s.serie_name);
      if (p) seriesInfo += field(t('f-family'), p.product_name+' ('+p.type+')');
    }
  }

  const field = (label, value, unit) => {
    if (value === null || value === undefined || value === '') return '';
    const v = unit ? fmt(value, unit) : safe(value);
    return '<div class="detail-field"><span class="label">'+label+'</span><span class="value">'+v+'</span></div>';
  };

  const bmFields = [
    ['Geekbench 4 Single', 'bm_geekbench4_single'],['Geekbench 4 Multi', 'bm_geekbench4_multi'],
    ['Geekbench 5 Single', 'bm_geekbench5_single'],['Geekbench 5 Multi', 'bm_geekbench5_multi'],
    ['Cinebench R15 Single', 'bm_cinebenchr15_single'],['Cinebench R15 Multi', 'bm_cinebenchr15_multi'],
    ['Cinebench R20 Single', 'bm_cinebenchr20_single'],['Cinebench R20 Multi', 'bm_cinebenchr20_multi'],
    ['Cinebench R23 Single', 'bm_cinebenchr23_single'],['Cinebench R23 Multi', 'bm_cinebenchr23_multi'],
  ];
  const bmVals = bmFields.map(([l,k]) => ({label:l,val:parseFloat(d[k])})).filter(b => !isNaN(b.val) && b.val > 0);
  const bmMax = bmVals.length > 0 ? Math.max(...bmVals.map(b=>b.val)) : 1;
  const bmHtml = bmVals.length > 0 ? bmVals.map(b =>
    '<div class="bench-bar-wrap"><div class="bench-bar-label"><span class="name">'+b.label+'</span><span class="val">'+b.val.toLocaleString()+'</span></div><div class="bench-bar"><div class="bench-bar-fill '+brand+'" style="width:'+(b.val/bmMax*100).toFixed(1)+'%"></div></div></div>'
  ).join('') : '<div style="color:var(--text3);font-size:.82rem">'+t('no-bench')+'</div>';

  const body = $('#detail-body');
  body.innerHTML =
    (seriesInfo ? '<div class="detail-section"><h3>'+t('sec-product')+'</h3><div class="detail-grid">'+seriesInfo+'</div></div>' : '') +
    '<div class="detail-section"><h3>'+t('sec-basic')+'</h3><div class="detail-grid">' +
      field(t('name'), d.name)+field(t('f-code'), d.code_name)+field(t('f-sspec'), d.sspec)+field(t('f-part'), d.part_number) +
      field(t('f-launch'), d.launch)+field(t('f-released'), d.released)+field(t('f-price'), d.lauch_price, '$') +
      field(t('f-variant'), d.variant)+field(t('f-socket'), d.socket) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-core')+'</h3><div class="detail-grid">' +
      field(t('cores'), d.cores)+field(t('f-threads'), d.threads)+field(t('f-arch'), d.core_arch)+field(t('f-config'), d.core_config) +
      field(t('f-baseclk'), d.core_clk, 'MHz')+field(t('f-boostclk'), d.core_clk_boost, 'MHz')+field(t('f-maxclk'), d.core_clk_max, 'MHz')+field(t('f-boostdetail'), d.core_clk_boost_detail) +
      field(t('f-multiplier'), d.multiplier)+field(t('f-multmax'), d.multiplier_max)+field(t('f-multunlocked'), d.multiplier_unlock==='1'?t('yes'):t('no')) +
      field(t('f-vcore'), d.vcore, 'V')+field(t('f-tdp'), d.tdp, 'W')+field(t('f-ctdpdn'), d.ctdp_down, 'W')+field(t('f-ctdpup'), d.ctdp_up, 'W') +
      field(t('f-maxtemp'), d.max_temp, '°C')+field(t('f-stepping'), d.core_stepping) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-fab')+'</h3><div class="detail-grid">' +
      field(t('f-foundry'), d.foundry)+field(t('f-fabproc'), d.fab, 'nm')+field(t('f-fabdetail'), d.fab_detail) +
      field(t('f-diesize'), d.die_size, 'mm²')+field(t('f-transistors'), d.transistor_count, 'M') +
      field(t('f-datawidth'), d.data_width, 'bit')+field(t('f-pkgsize'), d.pkg_size) +
      field(t('f-mcm'), d.mcm==='1'?t('yes'):t('no'))+field(t('f-mcmcfg'), d.mcm_config)+field(t('f-multicpus'), d.multi_cpus) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-cache')+'</h3><div class="detail-grid">' +
      field(t('f-l1i'), d.cache_l1_inst, 'KB')+field(t('f-l1d'), d.cache_l1_data, 'KB') +
      field(t('f-l2'), d.cache_l2, 'KB')+field(t('f-l3'), d.cache_l3, 'KB')+field(t('f-l4'), d.cache_l4, 'KB')+field(t('f-slc'), d.cache_slc, 'KB') +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-mem')+'</h3><div class="detail-grid">' +
      field(t('f-memtype'), d.mem_type)+field(t('f-memmax'), d.mem_max, 'GB') +
      field(t('f-memch'), d.mem_channels)+field(t('f-membw'), d.mem_bandwidth, 'GB/s') +
      field(t('f-memecc'), d.mem_ecc==='1'?t('yes'):d.mem_ecc==='0'?t('no'):d.mem_ecc) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-bus')+'</h3><div class="detail-grid">' +
      field(t('f-bus'), d.bus)+field(t('f-busspeed'), d.bus_speed)+field(t('f-busclk'), d.bus_clk, 'MHz') +
      field(t('f-pcielanes'), d.pcie_lanes)+field(t('f-pcierev'), d.pcie_revision)+field(t('f-pciecfg'), d.pcie_config) +
      field(t('f-ports'), d.ports)+field(t('f-networks'), d.networks) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu')+'</h3><div class="detail-grid">' +
      field(t('f-gpuname'), d.graphics_name)+field(t('f-gpuclk'), d.graphics_clk, 'MHz')+field(t('f-gpuboost'), d.graphics_clk_boost, 'MHz') +
      field(t('f-gpufp32'), d.graphics_fp32, 'GFLOPS')+field(t('f-gpucorecfg'), d.graphics_core_config) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-npu')+'</h3><div class="detail-grid">' +
      field(t('f-npuname'), d.npu_name)+field(t('f-npuperf'), d.npu_perf, 'TOPS') +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-isa')+'</h3><div class="detail-grid">' +
      field(t('f-instrset'), d.instruction_set)+field(t('f-features'), d.features) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-bench')+'</h3>'+bmHtml+'</div>' +
    (d.notes ? '<div class="detail-section"><h3>'+t('sec-notes')+'</h3><div style="font-size:.84rem;color:var(--text2);line-height:1.6">'+safe(d.notes)+'</div></div>' : '');

  $('#detail-overlay').classList.add('open');
  $('#detail-panel').classList.add('open');
}

// ===== GPU DETAIL PANEL =====
function openGpuDetail(vendor, gpuId) {
  const gpuList = vendor === 'nvidia' ? DATA.nvidia_gpu : vendor === 'amd' ? DATA.amd_gpu : DATA.intel_gpu;
  const dataList = vendor === 'nvidia' ? DATA.nvidia_gpu_data : vendor === 'amd' ? DATA.amd_gpu_data : DATA.intel_gpu_data;
  const gpu = gpuList.find(g => parseInt(g.id) === gpuId);
  const data = dataList.find(d => parseInt(d.id_gpu) === gpuId);
  if (!gpu && !data) return;
  const d = { ...(gpu||{}), ...(data||{}) };

  $('#detail-title').innerHTML = '<span class="badge badge-'+vendor+'">'+vendor.toUpperCase()+' GPU</span> '+safe(d.name)+' <button onclick="addToCompare(\'gpu\',\''+vendor+'\','+gpuId+')" style="margin-left:12px;padding:4px 12px;background:var(--accent);border:none;border-radius:var(--radius);color:#fff;font-size:.75rem;cursor:pointer;vertical-align:middle">'+t('add-compare')+'</button>';

  let seriesInfo = '';
  if (gpu && gpu.id_serie) {
    const sk = vendor[0] + '_' + gpu.id_serie;
    const s = gpuSeriesById[sk];
    if (s) {
      const pk = vendor[0] + '_' + s.id_product_family;
      const p = gpuProductsById[pk];
      seriesInfo = field(t('f-series'), s.serie_name);
      if (p) seriesInfo += field(t('f-family'), p.product_name+' ('+p.type+')');
    }
  }

  const field = (label, value, unit) => {
    if (value === null || value === undefined || value === '') return '';
    const v = unit ? fmt(value, unit) : safe(value);
    return '<div class="detail-field"><span class="label">'+label+'</span><span class="value">'+v+'</span></div>';
  };

  // GFLOPS benchmarks for this GPU
  const gflopsList = gpuGflopsById[d.name] || [];
  const gflopsHtml = gflopsList.length > 0 ? gflopsList.map(g =>
    '<div class="bench-bar-wrap"><div class="bench-bar-label"><span class="name">@ '+fmt(g.max_clock,'MHz')+'</span><span class="val">'+fmt(g.gflops,'GFLOPS')+'</span></div><div class="bench-bar"><div class="bench-bar-fill '+vendor+'" style="width:'+(g.gflops/Math.max(...gflopsList.map(x=>x.gflops))*100).toFixed(1)+'%"></div></div></div>'
  ).join('') : '<div style="color:var(--text3);font-size:.82rem">'+t('no-bench')+'</div>';

  const body = $('#detail-body');
  body.innerHTML =
    (seriesInfo ? '<div class="detail-section"><h3>'+t('sec-product')+'</h3><div class="detail-grid">'+seriesInfo+'</div></div>' : '') +
    '<div class="detail-section"><h3>'+t('sec-gpu-basic')+'</h3><div class="detail-grid">' +
      field(t('name'), d.name)+field(t('f-chip'), d.chip)+field(t('f-codename'), d.codename) +
      field(t('f-launch'), d.launch)+field(t('f-released'), d.released)+field(t('f-price'), d.launch_price, '$') +
      field(t('f-variant'), d.variant)+field(t('f-foundry'), d.foundry)+field(t('f-fabproc'), d.fab, 'nm') +
      field(t('f-diesize'), d.die_size, 'mm²')+field(t('f-transistors'), d.transistor_count, 'M') +
      field(t('f-tdp'), d.tdp, 'W')+field(t('f-bus'), d.bus) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu-cores')+'</h3><div class="detail-grid">' +
      field(t('f-arch'), d.arch)+field(t('f-cuda'), d.cuda)+field(t('f-cu'), d.cu) +
      field(t('f-unifiedshaders'), d.unified_shaders)+field(t('f-pixelshaders'), d.pixel_shaders)+field(t('f-vertexshaders'), d.vertex_shaders) +
      field(t('f-rops'), d.rops)+field(t('f-tmus'), d.tmus) +
      field(t('f-rtcores'), d.rt_cores)+field(t('f-tensorcores'), d.tensor_cores) +
      field(t('f-pxfillrate'), d.px_fill_rate, 'GP/s')+field(t('f-pxfillrate')+' Boost', d.px_fill_rate_boost, 'GP/s') +
      field(t('f-txfillrate'), d.tx_fill_rate, 'GT/s')+field(t('f-txfillrate')+' Boost', d.tx_fill_rate_boost, 'GT/s') +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu-clock')+'</h3><div class="detail-grid">' +
      field(t('f-baseclk'), d.core_clk, 'MHz')+field(t('f-boostclk'), d.core_clk_boost, 'MHz') +
      field(t('f-shaderclk'), d.shader_clk, 'MHz') +
      field(t('f-gfpssingle'), d.gflops_single, 'GFLOPS')+field(t('f-gfpssingleboost'), d.gflops_single_boost, 'GFLOPS') +
      field(t('f-gflopshalf'), d.gflops_half, 'GFLOPS')+field(t('f-gfpshalfboost'), d.gflops_half_boost, 'GFLOPS') +
      field(t('f-gfpsdouble'), d.gflops_double, 'GFLOPS')+field(t('f-gfpsdoubleboost'), d.gflops_double_boost, 'GFLOPS') +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu-mem')+'</h3><div class="detail-grid">' +
      field(t('f-memtype'), d.memory_type)+field(t('f-memmax'), d.memory_size, 'MB') +
      field(t('f-memclk'), d.memory_clk, 'MHz')+field(t('f-memclkeff'), d.memory_clk_effective, 'MHz') +
      field(t('f-mimbuswidth'), d.memory_bus_width, 'bit')+field(t('f-membw'), d.memory_band_width, 'GB/s') +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu-features')+'</h3><div class="detail-grid">' +
      field(t('f-directx'), d.directx)+field(t('f-directxfl'), d.directx_fl) +
      field(t('f-opengl'), d.opengl)+field(t('f-opencl'), d.opencl)+field(t('f-vulkan'), d.vulkan) +
      field(t('f-multi-gpu'), d.multi_gpu)+field(t('f-numgpu'), d.num_gpu) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-gpu-misc')+'</h3><div class="detail-grid">' +
      field('Cache L1', d.cache_l1)+field('Cache L1 Detail', d.cache_l1_detail) +
      field('Cache L2', d.cache_l2)+field('Cache L3', d.cache_l3) +
      field(t('f-multigpu'), d.multi_gpu) +
    '</div></div>' +
    '<div class="detail-section"><h3>'+t('sec-bench')+' (GFLOPS)</h3>'+gflopsHtml+'</div>' +
    (d.notes ? '<div class="detail-section"><h3>'+t('sec-notes')+'</h3><div style="font-size:.84rem;color:var(--text2);line-height:1.6">'+safe(d.notes)+'</div></div>' : '');

  $('#detail-overlay').classList.add('open');
  $('#detail-panel').classList.add('open');
}

function closeDetail() {
  $('#detail-overlay').classList.remove('open');
  $('#detail-panel').classList.remove('open');
}
$('#detail-overlay').addEventListener('click', closeDetail);
$('#detail-close').addEventListener('click', closeDetail);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeDetail(); });

// ===== SEARCH PAGE =====
function renderSearchPage() {
  const el = $('#page-search');
  el.innerHTML =
    '<h3 class="section-title"><span class="icon">&#x1F50D;</span> '+t('global-search-title')+'</h3>' +
    '<div class="search-box"><input type="text" id="search-input" placeholder="'+t('search-ph')+'" autocomplete="off"></div>' +
    '<div id="search-results" class="search-results"></div>';
  const input = $('#search-input');
  input.addEventListener('input', e => renderSearchResults(e.target.value));
  input.focus();
}

function renderSearchResults(query) {
  const el = $('#search-results');
  if (!query || query.length < 2) {
    el.innerHTML = '<div style="color:var(--text3);padding:20px;text-align:center">'+t('type-at-least')+'</div>';
    return;
  }
  const q = query.toLowerCase();
  const cpuResults = allCpus.filter(c =>
    safe(c.name).toLowerCase().includes(q) ||
    safe(c.code_name).toLowerCase().includes(q) ||
    safe(c.sspec).toLowerCase().includes(q) ||
    safe(c.part_number).toLowerCase().includes(q)
  );
  const gpuResults = allGpus.filter(g =>
    safe(g.name).toLowerCase().includes(q) ||
    safe(g.codename).toLowerCase().includes(q) ||
    safe(g.chip).toLowerCase().includes(q) ||
    safe(g.variant).toLowerCase().includes(q)
  );
  const results = [...cpuResults, ...gpuResults].slice(0, 200);

  if (results.length === 0) {
    el.innerHTML = '<div style="color:var(--text3);padding:20px;text-align:center">'+t('no-results')+'</div>';
    return;
  }

  el.innerHTML = '<div style="font-size:.78rem;color:var(--text3);margin-bottom:8px">'+results.length+' '+t('result')+(results.length>1?t('results-suffix'):'')+' ('+t('showing-up-to')+')</div>' +
    results.map(item => {
      if (item._type === 'cpu') {
        return '<div class="search-result" onclick="openCpuDetail(\''+item._brand+'\','+item._id+')">' +
          '<span class="badge badge-'+item._brand+'">CPU</span>' +
          '<span class="sr-name">'+safe(item.name)+'</span>' +
          '<span class="sr-specs">' +
            '<span>'+safe(item.cores)+'C</span>' +
            '<span>'+safe(item.core_clk)+(item.core_clk_boost?'/'+item.core_clk_boost:'')+(item.core_clk_max?'/'+item.core_clk_max:'')+' MHz</span>' +
            '<span>'+safe(item.socket)+'</span>' +
            '<span>'+fmt(item.tdp,'W')+'</span>' +
            '<span>'+safe(item.launch)+'</span>' +
          '</span>' +
          '<button onclick="event.stopPropagation();addToCompare(\'cpu\',\''+item._brand+'\','+item._id+')" title="'+t('add-compare')+'" style="background:var(--accent);border:none;border-radius:var(--radius);color:#fff;padding:4px 10px;font-size:.75rem;cursor:pointer;flex-shrink:0">'+t('add-compare')+'</button>' +
        '</div>';
      } else {
        return '<div class="search-result" onclick="openGpuDetail(\''+item._brand+'\','+item._id+')">' +
          '<span class="badge badge-'+item._brand+'">GPU</span>' +
          '<span class="sr-name">'+safe(item.name)+'</span>' +
          '<span class="sr-specs">' +
            '<span>'+safe(item.cuda||item.cores)+' cores</span>' +
            '<span>'+safe(item.core_clk)+(item.core_clk_boost?'/'+item.core_clk_boost:'')+' MHz</span>' +
            '<span>'+fmt(item.memory_size,'MB')+' '+safe(item.memory_type)+'</span>' +
            '<span>'+fmt(item.tdp,'W')+'</span>' +
            '<span>'+safe(item.launch)+'</span>' +
          '</span>' +
          '<button onclick="event.stopPropagation();addToCompare(\'gpu\',\''+item._brand+'\','+item._id+')" title="'+t('add-compare')+'" style="background:var(--accent);border:none;border-radius:var(--radius);color:#fff;padding:4px 10px;font-size:.75rem;cursor:pointer;flex-shrink:0">'+t('add-compare')+'</button>' +
        '</div>';
      }
    }).join('');
}

// ===== COMPARE =====
let compareList = []; // {type:'cpu'|'gpu', brand, id}
let miniSearchTimer = null;

function showToast(msg) {
  const el = $('#toast');
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2000);
}
function updateCompareFloat() {
  const el = $('#compare-float');
  const cnt = $('#compare-count');
  cnt.textContent = compareList.length;
  el.classList.toggle('visible', compareList.length > 0);
}
function addToCompare(type, brand, id) {
  if (compareList.find(c => c.type === type && c.brand === brand && c.id === id)) { showToast(t('already-in-compare')); return; }
  let name = '?';
  if (type === 'cpu') {
    const cpu = (brand === 'amd' ? DATA.amd_cpu : DATA.intel_cpu).find(x => parseInt(x.id) === id);
    if (cpu) name = cpu.name;
  } else {
    const gpu = (brand === 'nvidia' ? DATA.nvidia_gpu : brand === 'amd' ? DATA.amd_gpu : DATA.intel_gpu).find(x => parseInt(x.id) === id);
    if (gpu) name = gpu.name;
  }
  compareList.push({ type, brand, id });
  updateCompareFloat();
  showToast(name + ' ' + t('added-to-compare'));
  if (currentPage === 'compare') renderCompare();
}

function removeFromCompare(idx) {
  compareList.splice(idx, 1);
  updateCompareFloat();
  renderCompare();
}

function getItemName(item) {
  if (item.type === 'cpu') {
    const cpu = (item.brand === 'amd' ? DATA.amd_cpu : DATA.intel_cpu).find(x => parseInt(x.id) === item.id);
    return cpu ? cpu.name : '?';
  } else {
    const gpu = (item.brand === 'nvidia' ? DATA.nvidia_gpu : item.brand === 'amd' ? DATA.amd_gpu : DATA.intel_gpu).find(x => parseInt(x.id) === item.id);
    return gpu ? gpu.name : '?';
  }
}

function getMergedItem(item) {
  if (item.type === 'cpu') {
    const cpuList = item.brand === 'amd' ? DATA.amd_cpu : DATA.intel_cpu;
    const dataList = item.brand === 'amd' ? DATA.amd_cpu_data : DATA.intel_cpu_data;
    const cpu = cpuList.find(x => parseInt(x.id) === item.id);
    const data = dataList.find(d => parseInt(d.id_cpu) === item.id);
    return { ...(cpu||{}), ...(data||{}), _brand:item.brand, _type:'cpu' };
  } else {
    const gpuList = item.brand === 'nvidia' ? DATA.nvidia_gpu : item.brand === 'amd' ? DATA.amd_gpu : DATA.intel_gpu;
    const dataList = item.brand === 'nvidia' ? DATA.nvidia_gpu_data : item.brand === 'amd' ? DATA.amd_gpu_data : DATA.intel_gpu_data;
    const gpu = gpuList.find(x => parseInt(x.id) === item.id);
    const data = dataList.find(d => parseInt(d.id_gpu) === item.id);
    return { ...(gpu||{}), ...(data||{}), _brand:item.brand, _type:'gpu' };
  }
}

// ===== COMPARE MINI SEARCH =====
function miniSearch(query) {
  const dropdown = $('#mini-dropdown');
  if (!dropdown) return;
  if (!query || query.length < 2) { dropdown.classList.remove('visible'); return; }
  const q = query.toLowerCase();
  const cpuResults = allCpus.filter(c =>
    safe(c.name).toLowerCase().includes(q) ||
    safe(c.code_name).toLowerCase().includes(q) ||
    safe(c.sspec).toLowerCase().includes(q)
  ).map(c => ({...c, _type:'cpu'}));
  const gpuResults = allGpus.filter(g =>
    safe(g.name).toLowerCase().includes(q) ||
    safe(g.codename).toLowerCase().includes(q) ||
    safe(g.chip).toLowerCase().includes(q)
  ).map(g => ({...g, _type:'gpu'}));
  const results = [...cpuResults, ...gpuResults].slice(0, 25);

  if (results.length === 0) {
    dropdown.innerHTML = '<div style="padding:12px;color:var(--text3);text-align:center;font-size:.82rem">'+t('no-results')+'</div>';
    dropdown.classList.add('visible');
    return;
  }

  dropdown.innerHTML = results.map(c => {
    const already = compareList.find(x => x.type === c._type && x.brand === c._brand && x.id === c._id);
    const typeLabel = c._type === 'cpu' ? 'CPU' : 'GPU';
    const specs = c._type === 'cpu'
      ? '<span>'+safe(c.cores)+'C</span><span>'+safe(c.core_clk)+'MHz</span><span>'+safe(c.socket)+'</span>'
      : '<span>'+safe(c.cuda||c.cores)+' cores</span><span>'+safe(c.core_clk)+'MHz</span><span>'+safe(c.memory_type)+'</span>';
    return '<div class="mini-result">' +
      '<span class="mr-type '+c._type+'">'+typeLabel+'</span>' +
      '<span class="badge badge-'+c._brand+'">'+c._brand.toUpperCase()+'</span>' +
      '<span class="mr-name" title="'+safe(c.name)+'">'+safe(c.name)+'</span>' +
      '<span class="mr-specs">'+specs+'</span>' +
      (already
        ? '<span class="mr-added">✓ '+t('added')+'</span>'
        : '<button class="mr-add" onclick="event.stopPropagation();addToCompareMini(\''+c._type+'\',\''+c._brand+'\','+c._id+')">'+t('add-compare')+'</button>'
      ) +
    '</div>';
  }).join('');
  dropdown.classList.add('visible');
}

function addToCompareMini(type, brand, id) {
  addToCompare(type, brand, id);
  const input = $('#mini-search-input');
  if (input) miniSearch(input.value);
}

function setupMiniSearch() {
  const wrap = $('#mini-search-wrap');
  if (!wrap) return;
  const dropdown = $('#mini-dropdown');
  document.addEventListener('click', e => { if (!wrap.contains(e.target)) dropdown.classList.remove('visible'); });
  wrap.addEventListener('mouseleave', () => { miniSearchTimer = setTimeout(() => dropdown.classList.remove('visible'), 3000); });
  wrap.addEventListener('mouseenter', () => { if (miniSearchTimer) { clearTimeout(miniSearchTimer); miniSearchTimer = null; } });
}

function renderCompare() {
  const el = $('#page-compare');
  const chips = compareList.map((c, i) => {
    const name = getItemName(c);
    const typeLabel = c.type === 'cpu' ? 'CPU' : 'GPU';
    return '<div class="chip"><span class="mr-type '+c.type+'" style="font-size:.6rem">'+typeLabel+'</span><span class="badge badge-'+c.brand+'">'+c.brand.toUpperCase()+'</span> '+safe(name)+' <button class="remove" onclick="removeFromCompare('+i+')">&times;</button></div>';
  }).join('');

  const miniSearchHtml =
    '<div class="compare-search-wrap" id="mini-search-wrap">' +
      '<input type="text" id="mini-search-input" placeholder="'+t('mini-search-ph')+'" autocomplete="off" oninput="miniSearch(this.value)">' +
      '<div class="mini-results" id="mini-dropdown"></div>' +
    '</div>';

  let tableHtml = '';
  if (compareList.length >= 2) {
    const items = compareList.map(c => getMergedItem(c));
    const hasCpu = items.some(i => i._type === 'cpu');
    const hasGpu = items.some(i => i._type === 'gpu');

    // Common fields for all items
    const commonFields = [
      [t('name'),'name'],[t('brand'),'_brand'],[t('f-launch'),'launch'],[t('f-price'),'launch_price'],
      [t('f-foundry'),'foundry'],[t('f-fabproc'),'fab'],[t('f-diesize'),'die_size'],[t('f-transistors'),'transistor_count'],[t('f-tdp'),'tdp'],
    ];
    // CPU-specific fields
    const cpuFields = [
      [t('cores'),'cores'],[t('f-threads'),'threads'],[t('f-baseclk'),'core_clk'],[t('f-boostclk'),'core_clk_boost'],[t('f-maxclk'),'core_clk_max'],
      [t('f-socket'),'socket'],[t('f-arch'),'core_arch'],['L2 '+t('sec-cache'),'cache_l2'],['L3 '+t('sec-cache'),'cache_l3'],
      [t('f-memtype'),'mem_type'],[t('f-memmax'),'mem_max'],[t('f-pcielanes'),'pcie_lanes'],
      ['GB5 Single','bm_geekbench5_single'],['GB5 Multi','bm_geekbench5_multi'],
      ['CB R23 S','bm_cinebenchr23_single'],['CB R23 M','bm_cinebenchr23_multi'],
    ];
    // GPU-specific fields
    const gpuFields = [
      [t('f-arch'),'arch'],[t('f-cuda'),'cuda'],[t('f-cu'),'cu'],
      [t('f-baseclk'),'core_clk'],[t('f-boostclk'),'core_clk_boost'],[t('f-shaderclk'),'shader_clk'],
      [t('f-rops'),'rops'],[t('f-tmus'),'tmus'],[t('f-rtcores'),'rt_cores'],[t('f-tensorcores'),'tensor_cores'],
      [t('f-gfpssingle'),'gflops_single'],[t('f-gfpssingleboost'),'gflops_single_boost'],
      [t('f-memtype'),'memory_type'],[t('f-memmax'),'memory_size'],[t('f-mimbuswidth'),'memory_bus_width'],[t('f-membw'),'memory_band_width'],
      [t('f-memclk'),'memory_clk'],[t('f-memclkeff'),'memory_clk_effective'],
      [t('f-directx'),'directx'],[t('f-vulkan'),'vulkan'],[t('f-opengl'),'opengl'],[t('f-opencl'),'opencl'],
    ];

    let specFields = [...commonFields];
    if (hasCpu) specFields = specFields.concat(cpuFields);
    if (hasGpu) specFields = specFields.concat(gpuFields);

    const headerRow = '<tr><th>'+t('spec')+'</th>' + items.map(c => {
      const typeLabel = c._type === 'cpu' ? 'CPU' : 'GPU';
      return '<th><span class="mr-type '+c._type+'" style="font-size:.6rem">'+typeLabel+'</span> <span class="badge badge-'+c._brand+'">'+c._brand.toUpperCase()+'</span><br>'+safe(c.name)+'</th>';
    }).join('') + '</tr>';
    const bodyRows = specFields.map(([label, key]) => {
      const vals = items.map(c => {
        let v = c[key];
        if (key === 'launch_price' && v) v = '$' + v;
        if (key === 'memory_size' && v) v = v + ' MB';
        if (key === 'fab' && v) v = v + ' nm';
        return safe(v) || '—';
      });
      const allSame = vals.every(v => v === vals[0]);
      return '<tr><td class="field">'+label+'</td>'+vals.map(v => '<td class="'+(allSame?'':'diff')+'">'+v+'</td>').join('')+'</tr>';
    }).join('');

    tableHtml = '<div class="compare-table"><table><thead>'+headerRow+'</thead><tbody>'+bodyRows+'</tbody></table></div>';
  } else {
    tableHtml = '<div style="color:var(--text3);padding:40px;text-align:center">'+t('select-at-least')+'</div>';
  }

  el.innerHTML =
    '<h3 class="section-title"><span class="icon">&#x2696;&#xFE0F;</span> '+t('cpu-comparison')+'</h3>' +
    '<div class="compare-bar">' +
      chips +
      miniSearchHtml +
      (compareList.length > 0 ? '<button onclick="compareList=[];updateCompareFloat();renderCompare()">'+t('clear-all')+'</button>' : '') +
    '</div>' +
    tableHtml;

  setTimeout(setupMiniSearch, 0);
}

// ===== BENCHMARKS =====
const cpuBmOptions = [
  { key:'bm_geekbench4_single', label:'Geekbench 4 Single', cat:'cpu' },
  { key:'bm_geekbench4_multi', label:'Geekbench 4 Multi', cat:'cpu' },
  { key:'bm_geekbench5_single', label:'Geekbench 5 Single', cat:'cpu' },
  { key:'bm_geekbench5_multi', label:'Geekbench 5 Multi', cat:'cpu' },
  { key:'bm_cinebenchr15_single', label:'Cinebench R15 Single', cat:'cpu' },
  { key:'bm_cinebenchr15_multi', label:'Cinebench R15 Multi', cat:'cpu' },
  { key:'bm_cinebenchr20_single', label:'Cinebench R20 Single', cat:'cpu' },
  { key:'bm_cinebenchr20_multi', label:'Cinebench R20 Multi', cat:'cpu' },
  { key:'bm_cinebenchr23_single', label:'Cinebench R23 Single', cat:'cpu' },
  { key:'bm_cinebenchr23_multi', label:'Cinebench R23 Multi', cat:'cpu' },
];
const gpuBmOptions = [
  { key:'gflops_single', label:'FP32 GFLOPS', cat:'gpu' },
  { key:'gflops_single_boost', label:'FP32 GFLOPS (Boost)', cat:'gpu' },
  { key:'gflops_half', label:'FP16 GFLOPS', cat:'gpu' },
  { key:'gflops_half_boost', label:'FP16 GFLOPS (Boost)', cat:'gpu' },
  { key:'gflops_double', label:'FP64 GFLOPS', cat:'gpu' },
  { key:'gflops_double_boost', label:'FP64 GFLOPS (Boost)', cat:'gpu' },
];
const allBmOptions = [...cpuBmOptions, ...gpuBmOptions];
let benchState = { metric:'bm_geekbench5_multi', cat:'cpu', brand:'both', limit:20 };

function renderBenchmarks() {
  const el = $('#page-benchmarks');
  const cpuOpts = cpuBmOptions.map(o => '<option value="'+o.key+'" '+(benchState.metric===o.key?'selected':'')+'>'+o.label+'</option>').join('');
  const gpuOpts = gpuBmOptions.map(o => '<option value="'+o.key+'" '+(benchState.metric===o.key?'selected':'')+'>'+o.label+'</option>').join('');

  const isCpu = cpuBmOptions.some(o => o.key === benchState.metric);
  const brandOptions = isCpu
    ? '<option value="both" '+(benchState.brand==='both'?'selected':'')+'>Both</option><option value="amd" '+(benchState.brand==='amd'?'selected':'')+'>AMD</option><option value="intel" '+(benchState.brand==='intel'?'selected':'')+'>Intel</option>'
    : '<option value="both" '+(benchState.brand==='both'?'selected':'')+'>All</option><option value="nvidia" '+(benchState.brand==='nvidia'?'selected':'')+'>NVIDIA</option><option value="amd" '+(benchState.brand==='amd'?'selected':'')+'>AMD</option><option value="intel" '+(benchState.brand==='intel'?'selected':'')+'>Intel</option>';

  let rows;
  if (isCpu) {
    rows = allCpus.map(c => ({ name:c.name, val:parseFloat(c[benchState.metric]), brand:c._brand, type:'cpu', id:c._id }));
  } else {
    rows = allGpus.map(g => ({ name:g.name, val:parseFloat(g[benchState.metric]), brand:g._brand, type:'gpu', id:g._id }));
  }
  rows = rows.filter(r => !isNaN(r.val) && r.val > 0);
  if (benchState.brand !== 'both') rows = rows.filter(r => r.brand === benchState.brand);
  rows.sort((a,b) => b.val - a.val);
  rows = rows.slice(0, benchState.limit);
  const maxVal = rows.length > 0 ? rows[0].val : 1;

  el.innerHTML =
    '<h3 class="section-title"><span class="icon">&#x1F4C8;</span> '+t('benchmark-rankings')+'</h3>' +
    '<div class="filters">' +
      '<div class="filter-group"><label>'+t('bm-cat-cpu')+'</label><select onchange="benchState.metric=this.value;benchState.brand=\'both\';renderBenchmarks()">'+cpuOpts+'</select></div>' +
      '<div class="filter-group"><label>'+t('bm-cat-gpu')+'</label><select onchange="benchState.metric=this.value;benchState.brand=\'both\';renderBenchmarks()">'+gpuOpts+'</select></div>' +
      '<div class="filter-group"><label>'+t('brand')+'</label><select onchange="benchState.brand=this.value;renderBenchmarks()">'+brandOptions+'</select></div>' +
      '<div class="filter-group"><label>'+t('top-n')+'</label><select onchange="benchState.limit=parseInt(this.value);renderBenchmarks()">'+[10,20,50,100].map(n=>'<option value="'+n+'" '+(benchState.limit===n?'selected':'')+'>'+n+'</option>').join('')+'</select></div>' +
    '</div>' +
    '<div style="max-width:800px">' +
      (rows.length === 0 ? '<div style="color:var(--text3);padding:40px;text-align:center">'+t('no-benchmark-data')+'</div>' :
        rows.map((r,i) =>
          '<div class="bench-bar-wrap" style="cursor:pointer" onclick="'+(r.type==='cpu'?'openCpuDetail':'openGpuDetail')+'(\''+r.brand+'\','+r.id+')">' +
            '<div class="bench-bar-label">' +
              '<span class="name"><span class="badge badge-'+r.brand+'" style="margin-right:6px">'+(i+1)+'</span>'+r.name+'</span>' +
              '<span class="val">'+r.val.toLocaleString()+'</span>' +
            '</div>' +
            '<div class="bench-bar"><div class="bench-bar-fill '+r.brand+'" style="width:'+(r.val/maxVal*100).toFixed(1)+'%"></div></div>' +
          '</div>'
        ).join('')) +
    '</div>';
}

// ===== INIT =====
renderDashboard();
applyLang();
</script>
</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(PART1)
    f.write(data_json)
    f.write(PART2)

print(f"Written {os.path.getsize(OUTPUT):,} bytes to {OUTPUT}")
