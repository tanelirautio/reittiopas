from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Map Finnish line names to colors Graphviz understands
LINE_COLORS = {
    "keltainen": "gold",
    "punainen": "red",
    "vihreä": "green",
    "sininen": "blue",
}

DARK_FILLS = {"red", "blue", "green"}  # choose white text on these


def load_network(json_path: Path) -> dict:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_line_edges(linjastot: Dict[str, List[str]]) -> Dict[str, Set[Tuple[str, str]]]:
    edges_by_line: Dict[str, Set[Tuple[str, str]]] = {}
    for line_name, stops in linjastot.items():
        s: Set[Tuple[str, str]] = set()
        for a, b in zip(stops, stops[1:]):
            s.add((a, b))
            s.add((b, a))  # assume both directions
        edges_by_line[line_name] = s
    return edges_by_line


def pick_edge_color(u: str, v: str, edges_by_line: Dict[str, Set[Tuple[str, str]]]) -> str | None:
    serving_lines = [ln for ln, es in edges_by_line.items() if (u, v) in es]
    if len(serving_lines) == 1:
        return LINE_COLORS.get(serving_lines[0], "gray35")
    if len(serving_lines) > 1:
        return "gray35"
    return None


def make_dot(data: dict, undirected: bool) -> str:
    stops: List[str] = data["pysakit"]
    roads: List[dict] = data["tiet"]
    linjastot: Dict[str, List[str]] = data["linjastot"]

    edges_by_line = build_line_edges(linjastot)

    gtype = "graph" if undirected else "digraph"
    connector = "--" if undirected else "->"

    lines: List[str] = []
    lines.append(f"{gtype} reittiopas {{")
    lines.append('  rankdir=LR;')
    lines.append('  nodesep=0.6;')
    lines.append('  ranksep=0.7;')
    lines.append('  bgcolor="transparent";')
    lines.append('  graph [overlap=false, splines=true, fontname="Arial"];')
    lines.append('  node  [shape=circle, style="filled", fillcolor="white", color="gray40", fontname="Arial"];')
    lines.append('  edge  [color="gray55", fontname="Arial", fontsize=9, labeldistance=1.2];')
    lines.append("")
    lines.append('  labelloc="t";')
    lines.append('  label="Reittiopas - Bus network (stops, roads, durations)";')
    lines.append("")

    for s in stops:
        lines.append(f'  "{s}";')

    lines.append("")

    for r in roads:
        u = r["mista"]
        v = r["mihin"]
        d = r["kesto"]

        color = pick_edge_color(u, v, edges_by_line)
        attrs = [f'label="{d}"', 'fontcolor="gray40"']
        if color:
            attrs.append(f'color="{color}"')
            attrs.append("penwidth=2")
        lines.append(f'  "{u}" {connector} "{v}" [{", ".join(attrs)}];')

    # Legend (single row, filled)
    lines.append("")
    lines.append("  subgraph cluster_legend {")
    lines.append('    label="Lines";')
    lines.append('    fontsize=11;')
    lines.append('    color="gray80";')
    lines.append('    style="rounded";')
    lines.append('    fontname="Arial";')
    lines.append("    rankdir=LR;")
    lines.append("    rank=same;")
    lines.append('    node [shape=box, style="filled,rounded", margin="0.10,0.06", fontname="Arial"];')

    legend_nodes: List[str] = []
    for i, ln in enumerate(linjastot.keys()):
        clr = LINE_COLORS.get(ln, "gray35")
        fontcolor = "white" if clr in DARK_FILLS else "black"

        # Use ASCII node ids to avoid any Unicode weirdness in IDs.
        node_id = f"legend_{i}"
        legend_nodes.append(node_id)

        # But keep the human-visible label in Finnish (includes ä)
        lines.append(
            f'    "{node_id}" [label="{ln}", fillcolor="{clr}", color="{clr}", fontcolor="{fontcolor}"];'
        )

    for a, b in zip(legend_nodes, legend_nodes[1:]):
        lines.append(f'    "{a}" {connector} "{b}" [style=invis];')

    lines.append("  }")
    lines.append("}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        default="routeplanner/static/json/reittiopas.json",
        help="Path to the network JSON",
    )
    parser.add_argument(
        "--undirected",
        action="store_true",
        help="Render roads as undirected (graph) instead of directed (digraph).",
    )
    parser.add_argument(
        "--out",
        default="",
        help="If set, write DOT to this file (UTF-8) instead of printing to stdout.",
    )
    args = parser.parse_args()

    data = load_network(Path(args.json))
    dot = make_dot(data, undirected=args.undirected)

    if args.out:
        Path(args.out).write_text(dot, encoding="utf-8", newline="\n")
    else:
        print(dot)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
