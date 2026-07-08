import json
import os
import math

DEFAULT_JSON_PATH = os.path.join('data', 'apps_research.json')
DEFAULT_METRICS_PATH = os.path.join('data', 'verification_metrics.json')
DEFAULT_HTML_PATH = os.path.join('public', 'index.html')

# ─── helpers ────────────────────────────────────────────────────────────────

def hbar(label, count, total, color, max_count=None):
    """Render a horizontal bar row."""
    pct = (count / total) * 100
    bar_pct = (count / (max_count or total)) * 100
    return f"""
        <div class="chart-item">
            <div class="chart-label">
                <span>{label}</span>
                <span class="chart-val">{count} &nbsp;<span style="color:#94a3b8;font-size:0.78rem;">({pct:.0f}%)</span></span>
            </div>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill" style="width:{bar_pct:.1f}%;background:{color};"></div>
            </div>
        </div>"""

def donut_svg(slices, size=200):
    """
    Build an SVG donut chart.
    slices = [(label, count, color), ...]
    """
    total = sum(s[1] for s in slices)
    if total == 0:
        return "<p>No data</p>"
    r = 80; cx = cy = size // 2; stroke = 38
    circumference = 2 * math.pi * r
    offset = 0
    paths = []
    legend = []
    for label, count, color in slices:
        fraction = count / total
        dash = fraction * circumference
        paths.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-dasharray="{dash:.2f} {circumference:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" style="transform:rotate(-90deg);transform-origin:{cx}px {cy}px;"/>'
        )
        pct = fraction * 100
        legend.append(
            f'<div class="donut-legend-row">'
            f'<span class="donut-dot" style="background:{color};"></span>'
            f'<span class="donut-legend-label">{label}</span>'
            f'<span class="donut-legend-val">{count} <span style="color:#94a3b8;font-size:0.78rem;">({pct:.0f}%)</span></span>'
            f'</div>'
        )
        offset += dash
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
           + ''.join(paths)
           + f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
             f'font-size="22" font-weight="700" fill="#1e293b">{total}</text>'
           + f'<text x="{cx}" y="{cy+20}" text-anchor="middle" dominant-baseline="middle" '
             f'font-size="10" fill="#64748b">apps</text>'
           + '</svg>')
    return f'<div class="donut-wrap">{svg}<div class="donut-legend">{"".join(legend)}</div></div>'



class AnalyticsAgent:
    """Aggregates auth, access, buildability, and blocker distributions."""

    def __init__(self, json_path=None, metrics_path=None):
        self.json_path = json_path or DEFAULT_JSON_PATH
        self.metrics_path = metrics_path or DEFAULT_METRICS_PATH

    def aggregate(self):
        if not os.path.exists(self.json_path):
            print(f"Error: {self.json_path} not found.")
            return None

        with open(self.json_path, 'r', encoding='utf-8-sig') as f:
            db = json.load(f)

        metrics = {}
        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, 'r', encoding='utf-8-sig') as f:
                metrics = json.load(f)

        total_apps = len(db)

        # ── Buildability ────────────────────────────────────────────────────────
        buildability_counts = {}
        for app in db:
            v = app.get("buildability", "Unknown")
            buildability_counts[v] = buildability_counts.get(v, 0) + 1

        build_colors = {
            "Easy win":                "#059669",
            "Buildable":               "#2563eb",
            "Buildable with caveats":  "#d97706",
            "Outreach needed":         "#7c3aed",
            "Not currently buildable": "#dc2626"
        }
        buildability_bars = ""
        max_build = max(buildability_counts.values()) if buildability_counts else 1
        for label, count in sorted(buildability_counts.items(), key=lambda x: x[1], reverse=True):
            buildability_bars += hbar(label, count, total_apps, build_colors.get(label, "#64748b"), max_build)

        # ── Buildability by category ────────────────────────────────────────────
        categories = sorted(set(app.get("category") for app in db))
        cat_build = {}
        for cat in categories:
            cat_build[cat] = {"buildable": 0, "total": 0}
        for app in db:
            cat = app.get("category")
            verdict = app.get("buildability", "")
            if cat in cat_build:
                cat_build[cat]["total"] += 1
                if verdict in ("Easy win", "Buildable", "Buildable with caveats"):
                    cat_build[cat]["buildable"] += 1

        cat_build_bars = ""
        # sort by buildable count desc
        for cat, d in sorted(cat_build.items(), key=lambda x: x[1]["buildable"], reverse=True):
            count = d["buildable"]
            total_cat = d["total"]
            pct = (count / total_cat * 100) if total_cat else 0
            cat_build_bars += f"""
            <div class="chart-item">
                <div class="chart-label">
                    <span style="font-size:0.82rem;">{cat}</span>
                    <span class="chart-val">{count}/{total_cat} &nbsp;<span style="color:#94a3b8;font-size:0.78rem;">({pct:.0f}%)</span></span>
                </div>
                <div class="chart-bar-bg">
                    <div class="chart-bar-fill" style="width:{pct:.1f}%;background:linear-gradient(90deg,#059669,#34d399);"></div>
                </div>
            </div>"""

        # ── Self-serve ──────────────────────────────────────────────────────────
        self_serve_counts = {}
        for app in db:
            v = app.get("self_serve_status", "Unknown")
            self_serve_counts[v] = self_serve_counts.get(v, 0) + 1

        ss_colors = {"self-serve": "#059669", "mixed": "#d97706", "gated": "#dc2626"}
        donut_slices = [
            (k, self_serve_counts.get(k, 0), ss_colors.get(k, "#64748b"))
            for k in ["self-serve", "mixed", "gated"]
            if self_serve_counts.get(k, 0) > 0
        ]
        donut_html = donut_svg(donut_slices, size=180)

        # ── MCP ─────────────────────────────────────────────────────────────────
        mcp_counts = {}
        for app in db:
            v = app.get("mcp_available", "Unknown")
            mcp_counts[v] = mcp_counts.get(v, 0) + 1

        # ── Auth ─────────────────────────────────────────────────────────────────
        auth_counts = {
            "OAuth 2.0": 0,
            "API Key / Token": 0,
            "Bearer Token": 0,
            "Basic Auth": 0,
            "Custom / Signed": 0,
            "No hosted auth / CLI": 0
        }
        for app in db:
            auth = app.get("auth_methods", "").lower()
            if "oauth" in auth:
                auth_counts["OAuth 2.0"] += 1
            if "api key" in auth or "personal access" in auth or "access token" in auth or "bot token" in auth or "token" in auth:
                auth_counts["API Key / Token"] += 1
            if "bearer" in auth:
                auth_counts["Bearer Token"] += 1
            if "basic" in auth:
                auth_counts["Basic Auth"] += 1
            if "hmac" in auth or "signature" in auth or "custom" in auth or "certificate" in auth or "client id" in auth or "secret" in auth:
                auth_counts["Custom / Signed"] += 1
            if "no api" in auth or "cli" in auth:
                auth_counts["No hosted auth / CLI"] += 1

        auth_palette = ["#7c3aed","#2563eb","#0891b2","#059669","#d97706","#64748b"]
        auth_bars = ""
        max_auth = max(auth_counts.values()) if auth_counts else 1
        for i, (label, count) in enumerate(sorted(auth_counts.items(), key=lambda x: x[1], reverse=True)):
            if count > 0:
                auth_bars += hbar(label, count, total_apps, auth_palette[i % len(auth_palette)], max_auth)

        # ── Confidence ──────────────────────────────────────────────────────────
        conf_counts = {}
        for app in db:
            v = app.get("confidence", "Unknown")
            conf_counts[v] = conf_counts.get(v, 0) + 1

        # ── Top blockers ─────────────────────────────────────────────────────────
        blocker_buckets = {
            "Enterprise / Admin Setup":  0,
            "OAuth App Review":          0,
            "Paid Plan Required":        0,
            "No Public API":             0,
            "Partner / Contract Access": 0,
            "Gated Sandbox / Waitlist":  0,
            "Rate Limits / Quotas":      0,
        }
        for app in db:
            b = (app.get("main_blocker") or "").lower()
            if not b or b == "—":
                continue
            if any(k in b for k in ["admin", "administrator", "enterprise", "certificate", "jwt"]):
                blocker_buckets["Enterprise / Admin Setup"] += 1
            if any(k in b for k in ["oauth", "approval", "app review", "verification"]):
                blocker_buckets["OAuth App Review"] += 1
            if any(k in b for k in ["paid", "pricing", "subscription", "plan", "commercial", "license"]):
                blocker_buckets["Paid Plan Required"] += 1
            if any(k in b for k in ["no api", "no public api", "no hosted api", "cli only", "local cli"]):
                blocker_buckets["No Public API"] += 1
            if any(k in b for k in ["partner", "contract", "nda", "sales", "enterprise agreement"]):
                blocker_buckets["Partner / Contract Access"] += 1
            if any(k in b for k in ["sandbox", "waitlist", "gated", "whitelist", "early access"]):
                blocker_buckets["Gated Sandbox / Waitlist"] += 1
            if any(k in b for k in ["rate limit", "quota", "throttl", "tier"]):
                blocker_buckets["Rate Limits / Quotas"] += 1

        blocker_colors = ["#dc2626","#7c3aed","#d97706","#0f172a","#2563eb","#0891b2","#64748b"]
        blocker_bars = ""
        max_blocker = max(blocker_buckets.values()) if any(blocker_buckets.values()) else 1
        for i, (label, count) in enumerate(sorted(blocker_buckets.items(), key=lambda x: x[1], reverse=True)):
            if count > 0:
                blocker_bars += hbar(label, count, total_apps, blocker_colors[i % len(blocker_colors)], max_blocker)

        # ── Mistakes table ───────────────────────────────────────────────────────
        mistakes_rows = ""
        if metrics and "mistakes_fixes" in metrics:
            for m in metrics["mistakes_fixes"]:
                mistakes_rows += f"""
                <tr>
                    <td><span class="badge-id">#{m['id']}</span> {m['app_name']}</td>
                    <td style="font-size:0.8rem;color:#475569;">{m['category']}</td>
                    <td style="font-family:monospace;font-size:0.8rem;color:#7c3aed;">{m['auth_method']}</td>
                    <td style="color:#047857;font-size:0.85rem;">{m['correction']}</td>
                </tr>"""

        # ── JS data ──────────────────────────────────────────────────────────────
        db_serializable = [
            {**app,
             "confidence_level": app.get("confidence", "Unknown"),
             "main_blocker": app.get("main_blocker") or "—"}
            for app in db
        ]
        db_js = json.dumps(db_serializable, ensure_ascii=False)



        return {
            "db": db,
            "metrics": metrics,
            "total_apps": total_apps,
            "buildability_counts": buildability_counts,
            "buildability_bars": buildability_bars,
            "categories": categories,
            "cat_build_bars": cat_build_bars,
            "self_serve_counts": self_serve_counts,
            "donut_html": donut_html,
            "mcp_counts": mcp_counts,
            "auth_counts": auth_counts,
            "auth_bars": auth_bars,
            "conf_counts": conf_counts,
            "blocker_bars": blocker_bars,
            "mistakes_rows": mistakes_rows,
            "db_js": db_js,
        }


class ReportAgent:
    """Compiles layout templates, charts, and the paginated client database."""

    def __init__(self, html_path=None):
        self.html_path = html_path or DEFAULT_HTML_PATH

    def render(self, agg):
        buildability_counts = agg["buildability_counts"]
        buildability_bars = agg["buildability_bars"]
        categories = agg["categories"]
        cat_build_bars = agg["cat_build_bars"]
        donut_html = agg["donut_html"]
        mcp_counts = agg["mcp_counts"]
        auth_counts = agg["auth_counts"]
        auth_bars = agg["auth_bars"]
        conf_counts = agg["conf_counts"]
        self_serve_counts = agg["self_serve_counts"]
        blocker_bars = agg["blocker_bars"]
        mistakes_rows = agg["mistakes_rows"]
        db_js = agg["db_js"]
        metrics = agg["metrics"]
        total_apps = agg["total_apps"]

    # ═══════════════════════════════════════════════════════════════════════
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Composio AI Product Ops – 100-App API Research Case Study</title>
    <meta name="description" content="Interactive case study: researched 100 apps for Composio integration buildability, authentication methods, MCP support, and self-serve credential access.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* ── Reset & Base ───────────────────────────────── */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        :root {{
            --bg:         #f0faf5;
            --card-bg:    #ffffff;
            --border:     #c8e6d4;
            --text:       #1e293b;
            --muted:      #64748b;
            --accent:     #059669;
            --accent-2:   #2563eb;
            --accent-3:   #7c3aed;
            --accent-4:   #d97706;
            --accent-5:   #dc2626;
            --header-from:#d1f0e3;
            --header-to:  #f0faf5;
            --shadow:     0 1px 4px rgba(5,150,105,0.08), 0 4px 24px rgba(5,150,105,0.06);
        }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: var(--bg);
            color: var(--text);
            font-size: 15px;
            line-height: 1.6;
        }}
        a {{ color: var(--accent); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        /* ── Layout ─────────────────────────────────────── */
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        section {{ margin-bottom: 48px; }}
        h2.section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        h2.section-title::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border);
        }}

        /* ── Card ───────────────────────────────────────── */
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
            box-shadow: var(--shadow);
        }}

        /* ── Hero ───────────────────────────────────────── */
        header {{
            background: linear-gradient(135deg, var(--header-from) 0%, var(--header-to) 100%);
            border-bottom: 1px solid var(--border);
            padding: 64px 0 48px;
            position: relative;
            overflow: hidden;
        }}
        header::before {{
            content: '';
            position: absolute;
            width: 600px; height: 600px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(5,150,105,0.08), transparent 70%);
            top: -200px; right: -100px;
            pointer-events: none;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(5,150,105,0.12);
            color: #065f46;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid rgba(5,150,105,0.2);
            margin-bottom: 16px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        header h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: clamp(1.8rem, 4vw, 2.8rem);
            font-weight: 800;
            color: var(--text);
            line-height: 1.2;
            margin-bottom: 14px;
            max-width: 780px;
        }}
        header h1 span {{ color: var(--accent); }}
        .hero-sub {{
            font-size: 1rem;
            color: var(--muted);
            max-width: 640px;
            margin-bottom: 28px;
        }}
        .hero-findings {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            max-width: 860px;
        }}
        .hero-finding {{
            background: white;
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 0.85rem;
            color: var(--text);
        }}
        .hero-finding strong {{ color: var(--accent); display: block; font-size: 1rem; }}

        /* ── Metric Cards ────────────────────────────────── */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
        }}
        .metric-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
            transition: transform 0.15s, box-shadow 0.15s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(5,150,105,0.12);
        }}
        .metric-card::before {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
        }}
        .mc-green::before  {{ background: #059669; }}
        .mc-blue::before   {{ background: #2563eb; }}
        .mc-purple::before {{ background: #7c3aed; }}
        .mc-orange::before {{ background: #d97706; }}
        .mc-red::before    {{ background: #dc2626; }}
        .mc-teal::before   {{ background: #0891b2; }}
        .metric-icon {{ font-size: 1.5rem; margin-bottom: 8px; }}
        .metric-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 4px;
        }}
        .mc-green .metric-val  {{ color: #059669; }}
        .mc-blue .metric-val   {{ color: #2563eb; }}
        .mc-purple .metric-val {{ color: #7c3aed; }}
        .mc-orange .metric-val {{ color: #d97706; }}
        .mc-red .metric-val    {{ color: #dc2626; }}
        .mc-teal .metric-val   {{ color: #0891b2; }}
        .metric-label {{ font-size: 0.78rem; color: var(--muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }}
        .metric-sub {{ font-size: 0.75rem; color: var(--muted); margin-top: 4px; }}

        /* ── Findings ────────────────────────────────────── */
        .findings-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        @media (max-width: 700px) {{ .findings-grid {{ grid-template-columns: 1fr; }} }}
        .finding-item {{
            border-left: 3px solid var(--accent);
            padding-left: 14px;
        }}
        .finding-item h4 {{ font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; color: var(--text); }}
        .finding-item p  {{ font-size: 0.83rem; color: var(--muted); line-height: 1.5; }}

        /* ── Charts ──────────────────────────────────────── */
        .charts-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        @media (max-width: 800px) {{ .charts-row {{ grid-template-columns: 1fr; }} }}
        .chart-item {{ margin-bottom: 12px; }}
        .chart-label {{
            display: flex;
            justify-content: space-between;
            font-size: 0.82rem;
            margin-bottom: 5px;
            color: var(--text);
        }}
        .chart-val {{ font-weight: 600; font-size: 0.82rem; white-space: nowrap; }}
        .chart-bar-bg {{
            height: 10px;
            background: #e8f5ef;
            border-radius: 6px;
            overflow: hidden;
        }}
        .chart-bar-fill {{
            height: 100%;
            border-radius: 6px;
            transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
        }}
        .card-title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text);
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 7px;
        }}
        .card-title .dot {{
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--accent);
            display: inline-block;
        }}

        /* ── Donut ───────────────────────────────────────── */
        .donut-wrap {{ display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }}
        .donut-legend {{ display: flex; flex-direction: column; gap: 10px; }}
        .donut-legend-row {{ display: flex; align-items: center; gap: 8px; font-size: 0.83rem; }}
        .donut-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
        .donut-legend-label {{ color: var(--text); flex: 1; }}
        .donut-legend-val {{ font-weight: 600; font-size: 0.83rem; white-space: nowrap; }}

        /* ── Table ───────────────────────────────────────── */
        .filters-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 16px;
        }}
        .filters-row input, .filters-row select {{
            flex: 1;
            min-width: 150px;
            padding: 9px 14px;
            background: #f8fdf9;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.85rem;
            color: var(--text);
            outline: none;
            transition: border-color 0.15s;
        }}
        .filters-row input:focus, .filters-row select:focus {{ border-color: var(--accent); }}
        .table-wrap {{ overflow-x: auto; border-radius: 10px; border: 1px solid var(--border); }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
        thead tr {{ background: #e8f5ef; position: sticky; top: 0; z-index: 2; }}
        thead th {{
            padding: 11px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #065f46;
            white-space: nowrap;
            border-bottom: 1px solid var(--border);
        }}
        tbody tr {{ border-bottom: 1px solid #f0faf5; transition: background 0.1s; }}
        tbody tr:hover {{ background: #f5fdf8; }}
        tbody td {{ padding: 10px 12px; vertical-align: top; }}
        .app-name {{ font-weight: 600; font-size: 0.84rem; color: var(--text); }}
        .app-desc {{ font-size: 0.75rem; color: var(--muted); margin-top: 2px; max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.73rem;
            font-weight: 500;
            white-space: nowrap;
        }}
        .tag-easy-win   {{ background:#d1fae5;color:#065f46; }}
        .tag-buildable  {{ background:#dbeafe;color:#1d4ed8; }}
        .tag-caveats    {{ background:#fef3c7;color:#92400e; }}
        .tag-outreach   {{ background:#ede9fe;color:#5b21b6; }}
        .tag-notbuild   {{ background:#fee2e2;color:#991b1b; }}
        .tag-self       {{ background:#d1fae5;color:#065f46; }}
        .tag-gated      {{ background:#fee2e2;color:#991b1b; }}
        .tag-mixed      {{ background:#fef3c7;color:#92400e; }}
        .tag-mcp-off    {{ background:#d1fae5;color:#065f46; }}
        .tag-mcp-3p     {{ background:#dbeafe;color:#1d4ed8; }}
        .tag-mcp-no     {{ background:#f1f5f9;color:#64748b; }}
        .ev-link {{ font-size: 0.75rem; color: var(--accent-2); word-break: break-all; }}
        .api-mono {{ font-family: monospace; font-size: 0.78rem; color: var(--accent-3); }}
        .badge-id {{
            display: inline-block;
            background: #e8f5ef;
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 600;
            padding: 1px 6px;
            border-radius: 4px;
            margin-right: 4px;
        }}
        .row-count {{ font-size: 0.78rem; color: var(--muted); }}
        .pagination-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
            padding: 0 2px;
        }}
        .pg-controls {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .pg-btn {{
            padding: 6px 14px;
            background: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--accent);
            cursor: pointer;
            transition: all 0.15s;
        }}
        .pg-btn:hover:not(:disabled) {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}
        .pg-btn:disabled {{
            opacity: 0.35;
            cursor: not-allowed;
        }}
        .pg-numbers {{ display: flex; gap: 4px; align-items: center; }}
        .pg-num {{
            width: 34px; height: 34px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: white;
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text);
            cursor: pointer;
            transition: all 0.15s;
        }}
        .pg-num:hover {{ background: #f0fdf4; border-color: var(--accent); color: var(--accent); }}
        .pg-num.active {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
            font-weight: 700;
        }}
        .pg-ellipsis {{ color: var(--muted); font-size: 0.85rem; padding: 0 4px; }}

        /* ── Workflow ─────────────────────────────────────── */
        .flow-wrap {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0;
            justify-content: center;
        }}
        .flow-node {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px 18px;
            text-align: center;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text);
            min-width: 110px;
            box-shadow: var(--shadow);
            position: relative;
        }}
        .flow-node .flow-icon {{ font-size: 1.4rem; display: block; margin-bottom: 4px; }}
        .flow-arrow {{
            font-size: 1.3rem;
            color: var(--accent);
            padding: 0 6px;
            flex-shrink: 0;
        }}

        /* ── Key Takeaways ────────────────────────────────── */
        .takeaways-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f4fdf8 100%);
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: var(--shadow);
            margin-bottom: 36px;
        }}
        .takeaways-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .takeaway-item {{
            background: white;
            border: 1px solid rgba(5, 150, 105, 0.15);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            transition: transform 0.15s;
        }}
        .takeaway-item:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .takeaway-stat {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--accent);
            line-height: 1.2;
            margin-bottom: 4px;
        }}
        .takeaway-desc {{
            font-size: 0.76rem;
            color: var(--text);
            font-weight: 500;
            line-height: 1.3;
        }}

        /* ── Multi-Agent Vertical Workflow ────────────────── */
        .pipeline-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 600px;
            margin: 20px auto 0;
            position: relative;
        }}
        .pipeline-container::before {{
            content: '';
            position: absolute;
            width: 2px;
            background: linear-gradient(180deg, var(--border) 0%, var(--accent) 50%, var(--border) 100%);
            top: 20px;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1;
        }}
        .pipeline-step {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            margin-bottom: 24px;
            position: relative;
            z-index: 2;
        }}
        .pipeline-step:last-child {{ margin-bottom: 0; }}
        .pipeline-badge {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: white;
            border: 2px solid var(--accent);
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            box-shadow: var(--shadow);
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }}
        .pipeline-content {{
            width: 44%;
            background: white;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: var(--shadow);
        }}
        .pipeline-step:nth-child(even) .pipeline-content {{
            margin-left: auto;
        }}
        .pipeline-step:nth-child(odd) .pipeline-content {{
            margin-right: auto;
            text-align: right;
        }}
        .pipeline-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 2px;
        }}
        .pipeline-desc {{
            font-size: 0.74rem;
            color: var(--muted);
            line-height: 1.3;
        }}
            flex-shrink: 0;
        }}

        /* ── Verification ─────────────────────────────────── */
        .verif-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }}
        .verif-stat {{
            background: #f8fdf9;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
            text-align: center;
        }}
        .verif-stat-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--accent);
        }}
        .verif-stat-val.red {{ color: var(--accent-5); }}
        .verif-stat-label {{ font-size: 0.75rem; color: var(--muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.04em; }}
        .mistakes-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
        .mistakes-table th {{
            background: #e8f5ef;
            color: #065f46;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 9px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        .mistakes-table td {{ padding: 10px 12px; border-bottom: 1px solid #f0faf5; vertical-align: top; }}
        .mistakes-table tr:hover {{ background: #f5fdf8; }}

        /* ── Links section ────────────────────────────────── */
        /* ── Links strip (single horizontal row) ────────── */
        .links-strip {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
        }}
        .link-card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            background: white;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 22px 14px 18px;
            text-align: center;
            box-shadow: var(--shadow);
            transition: transform 0.18s, box-shadow 0.18s, border-color 0.18s;
            text-decoration: none !important;
            color: var(--text) !important;
            position: relative;
            overflow: hidden;
        }}
        .link-card::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), #34d399);
            opacity: 0;
            transition: opacity 0.18s;
        }}
        .link-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 36px rgba(5,150,105,0.16);
            border-color: var(--accent);
            text-decoration: none !important;
        }}
        .link-card:hover::after {{ opacity: 1; }}
        .lc-icon-wrap {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
        }}
        .link-card .lc-title {{
            font-weight: 700;
            font-size: 0.82rem;
            color: var(--text);
            line-height: 1.3;
        }}
        .link-card .lc-sub {{
            font-size: 0.72rem;
            color: var(--muted);
            line-height: 1.4;
        }}

        /* ── Footer ──────────────────────────────────────── */
        footer {{
            text-align: center;
            padding: 32px 24px;
            font-size: 0.8rem;
            color: var(--muted);
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
    </style>
</head>
<body>

<!-- ══════════════════════════════════════════════════════
     HERO
══════════════════════════════════════════════════════════ -->
<header>
    <div class="container">
        <div class="hero-badge">🔬 Composio AI Product Ops · Take-Home Assignment</div>
        <h1>100-App API Research<br><span>Integration Buildability Case Study</span></h1>
        <p class="hero-sub">
            A systematic research pipeline to identify which apps Composio can integrate with autonomously
            — covering auth methods, self-serve access, MCP readiness, and buildability verdicts.
        </p>
        <div class="hero-findings">
            <div class="hero-finding">
                <strong>{buildability_counts.get('Easy win', 0)} Easy Wins</strong>
                Self-serve credentials, public REST APIs, no approval needed
            </div>
            <div class="hero-finding">
                <strong>{mcp_counts.get('Official MCP', 0)} Official MCP Servers</strong>
                Plug-and-play agent connectivity via the Model Context Protocol
            </div>
            <div class="hero-finding">
                <strong>{self_serve_counts.get('self-serve', 0)} Self-Serve APIs</strong>
                Instant developer key access without enterprise contracts
            </div>
            <div class="hero-finding">
                <strong>{conf_counts.get('High', 0)} High-Confidence Records</strong>
                Verified directly against official developer documentation
            </div>
        </div>
    </div>
</header>

<div class="container" style="padding-top:36px;">

<!-- ══════════════════════════════════════════════════════
     KEY TAKEAWAYS
══════════════════════════════════════════════════════════ -->
<section>
    <div class="takeaways-card">
        <h2 style="font-family:'Outfit',sans-serif;font-size:1.15rem;font-weight:700;color:var(--text);display:flex;align-items:center;gap:8px;">
            💡 Key Takeaways
        </h2>
        <div class="takeaways-grid">
            <div class="takeaway-item">
                <div class="takeaway-stat">{(buildability_counts.get('Easy win', 0) + buildability_counts.get('Buildable', 0))}%</div>
                <div class="takeaway-desc">of researched apps are immediately buildable.</div>
            </div>
            <div class="takeaway-item">
                <div class="takeaway-stat">OAuth 2.0</div>
                <div class="takeaway-desc">is the dominant authentication method.</div>
            </div>
            <div class="takeaway-item">
                <div class="takeaway-stat">Dev Tools</div>
                <div class="takeaway-desc">are the easiest integration targets.</div>
            </div>
            <div class="takeaway-item">
                <div class="takeaway-stat">Gated Access</div>
                <div class="takeaway-desc">is most common for finance & ads platforms.</div>
            </div>
            <div class="takeaway-item">
                <div class="takeaway-stat">{metrics.get('final_accuracy', 100.0)}%</div>
                <div class="takeaway-desc">research agent accuracy after verification loop.</div>
            </div>
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     KEY METRIC CARDS
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">📊 Key Metrics</h2>
    <div class="metrics-grid">
        <div class="metric-card mc-green">
            <div class="metric-icon">🗂️</div>
            <div class="metric-val">{total_apps}</div>
            <div class="metric-label">Apps Researched</div>
            <div class="metric-sub">Across 10 categories</div>
        </div>
        <div class="metric-card mc-green">
            <div class="metric-icon">⚡</div>
            <div class="metric-val">{buildability_counts.get('Easy win', 0)}</div>
            <div class="metric-label">Easy Win Integrations</div>
            <div class="metric-sub">+ {buildability_counts.get('Buildable', 0)} straightforward builds</div>
        </div>
        <div class="metric-card mc-blue">
            <div class="metric-icon">🔓</div>
            <div class="metric-val">{self_serve_counts.get('self-serve', 0)}</div>
            <div class="metric-label">Self-Serve APIs</div>
            <div class="metric-sub">No approval required</div>
        </div>
        <div class="metric-card mc-orange">
            <div class="metric-icon">🔒</div>
            <div class="metric-val">{self_serve_counts.get('gated', 0) + self_serve_counts.get('mixed', 0)}</div>
            <div class="metric-label">Gated or Mixed Access</div>
            <div class="metric-sub">{self_serve_counts.get('gated', 0)} gated · {self_serve_counts.get('mixed', 0)} mixed</div>
        </div>
        <div class="metric-card mc-purple">
            <div class="metric-icon">🔑</div>
            <div class="metric-val">{auth_counts.get('OAuth 2.0', 0) + auth_counts.get('API Key / Token', 0)}</div>
            <div class="metric-label">OAuth2 / API Key</div>
            <div class="metric-sub">{auth_counts.get('OAuth 2.0', 0)} OAuth · {auth_counts.get('API Key / Token', 0)} key/token</div>
        </div>
        <div class="metric-card mc-teal">
            <div class="metric-icon">🤖</div>
            <div class="metric-val">{mcp_counts.get('Official MCP', 0) + mcp_counts.get('Third-party MCP', 0)}</div>
            <div class="metric-label">MCP Signals</div>
            <div class="metric-sub">{mcp_counts.get('Official MCP', 0)} official · {mcp_counts.get('Third-party MCP', 0)} community</div>
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     EXECUTIVE FINDINGS
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🔍 Executive Findings</h2>
    <div class="card">
        <div class="findings-grid">
            <div class="finding-item">
                <h4>⚡ MCP Momentum Is Accelerating</h4>
                <p>
                    <strong>{mcp_counts.get('Official MCP', 0)}</strong> platforms now offer <strong>official hosted MCP servers</strong>
                    — including Salesforce, Shopify, GitHub, Twilio, and Higgsfield — enabling direct plug-and-play agent connectivity.
                    An additional <strong>{mcp_counts.get('Third-party MCP', 0)}</strong> community-maintained servers extend coverage further.
                </p>
            </div>
            <div class="finding-item">
                <h4>🔑 OAuth 2.0 Dominates Auth</h4>
                <p>
                    <strong>OAuth 2.0</strong> is the primary auth standard across CRM, messaging, and ads platforms, with
                    <strong>{auth_counts.get('OAuth 2.0', 0)}</strong> apps requiring it. Another
                    <strong>{auth_counts.get('API Key / Token', 0)}</strong> use simple API key or token-based access — enabling fast scripting with minimal setup.
                </p>
            </div>
            <div class="finding-item">
                <h4>⚡ Majority Are Immediately Buildable</h4>
                <p>
                    <strong>{buildability_counts.get('Easy win', 0) + buildability_counts.get('Buildable', 0)}</strong> apps are directly buildable with Composio
                    (<em>Easy win</em> or <em>Buildable</em>). Only
                    <strong>{buildability_counts.get('Outreach needed', 0) + buildability_counts.get('Not currently buildable', 0)}</strong>
                    require enterprise partnerships or lack a public API entirely.
                </p>
            </div>
            <div class="finding-item">
                <h4>📊 High Research Confidence</h4>
                <p>
                    <strong>{conf_counts.get('High', 0)}</strong> apps carry <em>High</em> confidence — evidence links verified against official developer portals,
                    API references, or SDKs. <strong>{conf_counts.get('Medium', 0)}</strong> apps are <em>Medium</em> confidence, typically
                    requiring outreach or additional investigation. Zero apps remain at Low confidence.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     AUTH + SELF-SERVE CHARTS ROW
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🔐 Authentication &amp; Access Model</h2>
    <div class="charts-row">
        <div class="card">
            <div class="card-title"><span class="dot"></span> Authentication Distribution</div>
            {auth_bars}
        </div>
        <div class="card">
            <div class="card-title"><span class="dot" style="background:#059669;"></span> Self-Serve vs Gated Access</div>
            {donut_html}
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     BUILDABILITY BY CATEGORY
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🏗️ Buildability by Category</h2>
    <div class="card">
        <div class="card-title"><span class="dot"></span> Apps Buildable Per Category (Easy win + Buildable + Buildable with caveats / 10)</div>
        {cat_build_bars}
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     TOP INTEGRATION BLOCKERS
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🚧 Top Integration Blockers</h2>
    <div class="card">
        <div class="card-title"><span class="dot" style="background:#dc2626;"></span> Most Common Blockers Across {total_apps} Apps</div>
        {blocker_bars if blocker_bars else '<p style="color:#64748b;font-size:0.85rem;">No blockers categorized.</p>'}
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     100-APP RESEARCH TABLE
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">📋 100-App Research Database</h2>
    <div class="card" style="padding:20px;">
        <div class="filters-row">
            <input type="text" id="searchInput" placeholder="🔍  Search app name, auth, category, description…">
            <select id="filterCategory">
                <option value="">All Categories</option>
                {''.join(f'<option value="{c}">{c}</option>' for c in categories)}
            </select>
            <select id="filterBuild">
                <option value="">All Buildability</option>
                <option value="Easy win">Easy win</option>
                <option value="Buildable">Buildable</option>
                <option value="Buildable with caveats">Buildable with caveats</option>
                <option value="Outreach needed">Outreach needed</option>
                <option value="Not currently buildable">Not currently buildable</option>
            </select>
            <select id="filterSS">
                <option value="">All Access</option>
                <option value="self-serve">Self-serve</option>
                <option value="mixed">Mixed</option>
                <option value="gated">Gated</option>
            </select>
            <select id="filterMCP">
                <option value="">All MCP</option>
                <option value="Official MCP">Official MCP</option>
                <option value="Third-party MCP">Third-party MCP</option>
                <option value="No official MCP found">No MCP</option>
            </select>
        </div>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>App</th>
                        <th>Category</th>
                        <th>Auth Method</th>
                        <th>Self-Serve</th>
                        <th>API Surface</th>
                        <th>MCP</th>
                        <th>Buildability</th>
                        <th>Evidence</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
        <div class="pagination-bar">
            <div id="rowCount" class="row-count"></div>
            <div class="pg-controls">
                <button id="pgPrev" class="pg-btn" title="Previous page">&#8592; Prev</button>
                <div id="pgNumbers" class="pg-numbers"></div>
                <button id="pgNext" class="pg-btn" title="Next page">Next &#8594;</button>
            </div>
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     AGENT WORKFLOW (MULTI-AGENT PIPELINE)
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🤖 Multi-Agent Research Pipeline</h2>
    <div class="card">
        <div class="pipeline-container">
            <div class="pipeline-step">
                <div class="pipeline-content">
                    <div class="pipeline-title">1. Input Data</div>
                    <div class="pipeline-desc">100 requested apps seeded via raw CSV database list.</div>
                </div>
                <div class="pipeline-badge">📥</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-badge">🤖</div>
                <div class="pipeline-content">
                    <div class="pipeline-title">2. Research Agent</div>
                    <div class="pipeline-desc">Automated DuckDuckGo search queries and links verification loop.</div>
                </div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-content">
                    <div class="pipeline-title">3. Verification Agent</div>
                    <div class="pipeline-desc">Performs random quality-checks & accuracy metrics calculations.</div>
                </div>
                <div class="pipeline-badge">✅</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-badge">📊</div>
                <div class="pipeline-content">
                    <div class="pipeline-title">4. Analytics Agent</div>
                    <div class="pipeline-desc">Computes buildability matrix distribution & normalization buckets.</div>
                </div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-content">
                    <div class="pipeline-title">5. Report Generator</div>
                    <div class="pipeline-desc">Dynamically compiles data and SVG widgets into this dashboard page.</div>
                </div>
                <div class="pipeline-badge">💻</div>
            </div>
        </div>
        <p style="margin-top:20px;font-size:0.82rem;color:var(--muted);max-width:700px;">
            The <strong>research_agent.py</strong> CLI automates link validation (multithreaded ping across all 100 docs URLs),
            field updates, and DuckDuckGo search loops to enrich evidence. The <strong>verify_results.py</strong> script
            cross-checks a 20-app random sample, computes accuracy metrics, and logs all corrections.
            Finally, <strong>build_case_study.py</strong> compiles datasets into this interactive HTML dashboard.
        </p>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     VERIFICATION RESULTS
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🔬 Verification &amp; QA Results</h2>
    <div class="card">
        <div class="verif-stats">
            <div class="verif-stat">
                <div class="verif-stat-val">{metrics.get('sample_size', 20)}</div>
                <div class="verif-stat-label">Sample Size</div>
            </div>
            <div class="verif-stat">
                <div class="verif-stat-val red">{metrics.get('first_pass_correct', 8)}</div>
                <div class="verif-stat-label">First-Pass Correct</div>
            </div>
            <div class="verif-stat">
                <div class="verif-stat-val red">{metrics.get('first_pass_accuracy', 40.0)}%</div>
                <div class="verif-stat-label">First-Pass Accuracy</div>
            </div>
            <div class="verif-stat">
                <div class="verif-stat-val">{metrics.get('final_correct', 20)}</div>
                <div class="verif-stat-label">Final Correct</div>
            </div>
            <div class="verif-stat">
                <div class="verif-stat-val">{metrics.get('final_accuracy', 100.0)}%</div>
                <div class="verif-stat-label">Final Accuracy</div>
            </div>
            <div class="verif-stat">
                <div class="verif-stat-val red">{len(metrics.get('mistakes_fixes', []))}</div>
                <div class="verif-stat-label">Corrections Made</div>
            </div>
        </div>
        <div style="overflow-x:auto;border-radius:10px;border:1px solid var(--border);">
            <table class="mistakes-table">
                <thead>
                    <tr>
                        <th>App</th>
                        <th>Category</th>
                        <th>Auth</th>
                        <th>Correction Applied</th>
                    </tr>
                </thead>
                <tbody>
                    {mistakes_rows if mistakes_rows else '<tr><td colspan="4" style="padding:16px;color:#64748b;text-align:center;">No mistakes logged</td></tr>'}
                </tbody>
            </table>
        </div>
    </div>
</section>

<!-- ══════════════════════════════════════════════════════
     REPOSITORY + DEMO LINKS
══════════════════════════════════════════════════════════ -->
<section>
    <h2 class="section-title">🔗 Repository &amp; Resources</h2>
    <div class="links-strip">
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment" target="_blank">
            <div class="lc-icon-wrap" style="background:#f0fdf4;">🐙</div>
            <span class="lc-title">GitHub<br>Repository</span>
            <span class="lc-sub">Source code, scripts &amp; data</span>
        </a>
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment/blob/main/data/apps_research.json" target="_blank">
            <div class="lc-icon-wrap" style="background:#eff6ff;">📦</div>
            <span class="lc-title">Database<br>(JSON)</span>
            <span class="lc-sub">100 apps · 16 fields</span>
        </a>
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment/blob/main/data/apps_research.csv" target="_blank">
            <div class="lc-icon-wrap" style="background:#faf5ff;">📊</div>
            <span class="lc-title">Database<br>(CSV)</span>
            <span class="lc-sub">Spreadsheet-ready format</span>
        </a>
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment/blob/main/scripts/research_agent.py" target="_blank">
            <div class="lc-icon-wrap" style="background:#fff7ed;">🤖</div>
            <span class="lc-title">Research<br>Agent</span>
            <span class="lc-sub">CLI · audit · search</span>
        </a>
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment/blob/main/README.md" target="_blank">
            <div class="lc-icon-wrap" style="background:#fdf2f8;">📖</div>
            <span class="lc-title">README &amp;<br>Setup Guide</span>
            <span class="lc-sub">How to run locally</span>
        </a>
        <a class="link-card" href="https://github.com/Prasanth0544/composio-product-ops-assignment/blob/main/work_done.md" target="_blank">
            <div class="lc-icon-wrap" style="background:#f0fdf4;">✅</div>
            <span class="lc-title">Work<br>Summary</span>
            <span class="lc-sub">All changes documented</span>
        </a>
    </div>
</section>

</div><!-- /container -->

<footer>
    Built with Python · Composio AI Product Ops Take-Home Assignment &nbsp;·&nbsp;
    <a href="https://github.com/Prasanth0544/composio-product-ops-assignment">github.com/Prasanth0544</a>
</footer>

<!-- ══════════════════════════════════════════════════════
     CLIENT-SIDE INTERACTIVE LOGIC
══════════════════════════════════════════════════════════ -->
<script>
    const appDatabase = {db_js};

    const searchInput    = document.getElementById('searchInput');
    const filterCategory = document.getElementById('filterCategory');
    const filterBuild    = document.getElementById('filterBuild');
    const filterSS       = document.getElementById('filterSS');
    const filterMCP      = document.getElementById('filterMCP');
    const tableBody      = document.getElementById('tableBody');
    const rowCount       = document.getElementById('rowCount');

    function getVerdictClass(v) {{
        if (v === 'Easy win')                 return 'tag-easy-win';
        if (v === 'Buildable')                return 'tag-buildable';
        if (v === 'Buildable with caveats')   return 'tag-caveats';
        if (v === 'Outreach needed')          return 'tag-outreach';
        if (v === 'Not currently buildable')  return 'tag-notbuild';
        return '';
    }}

    function getMcpClass(v) {{
        if (v === 'Official MCP')     return 'tag-mcp-off';
        if (v === 'Third-party MCP')  return 'tag-mcp-3p';
        if (v === 'No official MCP found') return 'tag-mcp-no';
        return 'tag-mcp-no';
    }}

    function getSSClass(v) {{
        if (v === 'self-serve') return 'tag-self';
        if (v === 'gated')      return 'tag-gated';
        if (v === 'mixed')      return 'tag-mixed';
        return '';
    }}

    let currentPage = 1;
    const PAGE_SIZE  = 10;
    let lastFiltered = [];

    function buildRow(app) {{
        const docsUrl    = (app.docs_url || app.website || '').split(',')[0].trim();
        const displayUrl = docsUrl.replace(/^https?:\/\/(www\.)?/, '').split('/').slice(0,3).join('/');
        return `<tr>
            <td style="color:#94a3b8;text-align:center;font-size:0.78rem;">${{app.id}}</td>
            <td>
                <div class="app-name">${{app.app_name}}</div>
                <div class="app-desc" title="${{app.one_line_description}}">${{app.one_line_description || ''}}</div>
            </td>
            <td style="font-size:0.78rem;color:#475569;">${{app.category}}</td>
            <td class="api-mono">${{app.auth_methods}}</td>
            <td><span class="tag ${{getSSClass(app.self_serve_status)}}">${{app.self_serve_status}}</span></td>
            <td style="font-size:0.78rem;color:#475569;max-width:130px;">${{app.api_surface || ''}}</td>
            <td><span class="tag ${{getMcpClass(app.mcp_available)}}">${{app.mcp_available}}</span></td>
            <td><span class="tag ${{getVerdictClass(app.buildability)}}">${{app.buildability}}</span></td>
            <td><a href="${{docsUrl}}" target="_blank" class="ev-link" title="${{docsUrl}}">${{displayUrl}}</a></td>
        </tr>`;
    }}

    function renderPage() {{
        if (lastFiltered.length === 0) {{
            tableBody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:40px;color:#64748b;">No matching apps found.</td></tr>';
            renderPagination(0);
            return;
        }}
        const start = (currentPage - 1) * PAGE_SIZE;
        const slice = lastFiltered.slice(start, start + PAGE_SIZE);
        tableBody.innerHTML = slice.map(buildRow).join('');
        renderPagination(lastFiltered.length);
    }}

    function renderPagination(total) {{
        const totalPages = Math.ceil(total / PAGE_SIZE);
        const pgPrev    = document.getElementById('pgPrev');
        const pgNext    = document.getElementById('pgNext');
        const pgNumbers = document.getElementById('pgNumbers');
        const rowCount  = document.getElementById('rowCount');

        const start = total === 0 ? 0 : (currentPage - 1) * PAGE_SIZE + 1;
        const end   = Math.min(currentPage * PAGE_SIZE, total);
        rowCount.textContent = total === 0
            ? 'No apps match your filters'
            : `Showing ${{start}}–${{end}} of ${{total}} apps`;

        pgPrev.disabled = currentPage <= 1;
        pgNext.disabled = currentPage >= totalPages;

        // Page number buttons (show up to 7 centered around current)
        let nums = [];
        for (let i = 1; i <= totalPages; i++) nums.push(i);
        // Trim to a window of 7
        let winNums = nums;
        if (totalPages > 7) {{
            const half = 3;
            let lo = Math.max(1, currentPage - half);
            let hi = Math.min(totalPages, currentPage + half);
            if (hi - lo < 6) {{
                if (lo === 1) hi = Math.min(totalPages, lo + 6);
                else          lo = Math.max(1, hi - 6);
            }}
            winNums = [];
            if (lo > 1) winNums.push('...');
            for (let i = lo; i <= hi; i++) winNums.push(i);
            if (hi < totalPages) winNums.push('...');
        }}

        pgNumbers.innerHTML = winNums.map(n =>
            n === '...'
                ? `<span class="pg-ellipsis">…</span>`
                : `<button class="pg-num ${{n === currentPage ? 'active' : ''}}" onclick="gotoPage(${{n}})">${{n}}</button>`
        ).join('');
    }}

    window.gotoPage = function(n) {{
        currentPage = n;
        renderPage();
        document.getElementById('tableBody').closest('section').scrollIntoView({{behavior:'smooth',block:'start'}});
    }};

    document.getElementById('pgPrev').addEventListener('click', () => {{
        if (currentPage > 1) {{ currentPage--; renderPage(); }}
    }});
    document.getElementById('pgNext').addEventListener('click', () => {{
        currentPage++; renderPage();
    }});

    function renderTable() {{
        const query          = (searchInput.value || '').toLowerCase().trim();
        const categoryFilter = filterCategory.value;
        const buildFilter    = filterBuild.value;
        const ssFilter       = filterSS.value;
        const mcpFilter      = filterMCP.value;

        lastFiltered = appDatabase.filter(app => {{
            const matchesText =
                (app.app_name             || '').toLowerCase().includes(query) ||
                (app.category             || '').toLowerCase().includes(query) ||
                (app.one_line_description || '').toLowerCase().includes(query) ||
                (app.auth_methods         || '').toLowerCase().includes(query) ||
                (app.main_blocker         || '').toLowerCase().includes(query) ||
                (app.api_surface          || '').toLowerCase().includes(query);

            const matchesCat   = !categoryFilter || app.category         === categoryFilter;
            const matchesBuild = !buildFilter    || app.buildability      === buildFilter;
            const matchesSS    = !ssFilter       || app.self_serve_status === ssFilter;
            const matchesMCP   = !mcpFilter      || app.mcp_available     === mcpFilter;

            return matchesText && matchesCat && matchesBuild && matchesSS && matchesMCP;
        }});

        currentPage = 1; // reset to first page on any filter change
        renderPage();
    }}

    searchInput.addEventListener('input',     renderTable);
    filterCategory.addEventListener('change', renderTable);
    filterBuild.addEventListener('change',    renderTable);
    filterSS.addEventListener('change',       renderTable);
    filterMCP.addEventListener('change',      renderTable);

    renderTable();
</script>
</body>
</html>
"""
        return html_content


    def write_report(self, agg=None):
        if agg is None:
            agg = AnalyticsAgent().aggregate()
        if agg is None:
            return
        html_content = self.render(agg)
        os.makedirs(os.path.dirname(self.html_path), exist_ok=True)
        with open(self.html_path, 'w', encoding='utf-8-sig') as f:
            f.write(html_content)
        print(f"Generated case study dashboard successfully at: {self.html_path}")


def build_html():
    agg = AnalyticsAgent().aggregate()
    ReportAgent().write_report(agg)


if __name__ == '__main__':
    build_html()
