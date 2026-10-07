"""Rebuild the vector overview of Chinese-SkillSpan model results.

All numerical inputs are the manuscript-precision values in the adjacent JSON.
Error bars are sample standard deviations across three training seeds.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
STEM = "model_comparison_20261006"


def load_data(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["score_range"] == [0, 1]
    assert [p["id"] for p in data["panels"]] == ["a", "b"]
    assert [len(p["models"]) for p in data["panels"]] == [6, 4]
    for panel in data["panels"]:
        for model in panel["models"]:
            assert 0 <= model["score"] <= 1
            assert model["source"]["file"] and model["source"]["entry"]
            if panel["id"] == "a":
                assert model["runs"] == 1 and model["sample_sd"] is None
            else:
                assert model["runs"] == 3 and model["seeds"] == [42, 43, 44]
                assert model["sample_sd"] is not None and model["sample_sd"] >= 0
    return data


def build_figure(data):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.labelsize": 9.5,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.8,
        "text.color": "#18212B",
        "axes.labelcolor": "#18212B",
        "xtick.color": "#495867",
        "ytick.color": "#18212B",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": False,
    })
    fig = plt.figure(figsize=(8.2, 4.1), facecolor="white")
    grid = fig.add_gridspec(1, 2, left=0.185, right=0.985,
                           bottom=0.155, top=0.785, wspace=0.70)
    axes = [fig.add_subplot(grid[0, index]) for index in range(2)]
    titles = []
    for panel_index, (ax, panel) in enumerate(zip(axes, data["panels"])):
        models = panel["models"]
        nrows = len(models)
        # Keep physical bar thickness consistent between six- and four-row panels.
        bar_height = 0.46 * nrows / 6.0
        for index, model in enumerate(models):
            accent = model.get("accent", False)
            color = "#256B70" if accent else ("#5C86A3" if panel_index == 0 else "#8EA8BA")
            ax.barh(index, model["score"], height=bar_height,
                    color=color, edgecolor=color, linewidth=0.5, zorder=2)
            sd = model["sample_sd"]
            if sd is not None:
                ax.errorbar(model["score"], index, xerr=sd, fmt="none",
                            ecolor="#263D4D", elinewidth=1.05,
                            capsize=3.4, capthick=1.05, zorder=3)
                label = "{:.3f} ± {:.3f}".format(model["score"], sd)
                right = model["score"] + sd
            else:
                label = "{:.3f}".format(model["score"])
                right = model["score"]
            ax.text(right + 0.023, index, label, ha="left", va="center",
                    fontsize=8.6, fontweight="bold" if accent else "normal",
                    zorder=4)
        ax.set_yticks(range(nrows))
        ax.set_yticklabels([m["display_name"] for m in models])
        for tick, model in zip(ax.get_yticklabels(), models):
            if model.get("accent", False):
                tick.set_fontweight("bold")
            tick.set_linespacing(1.15)
        ax.set_ylim(nrows - 0.48, -0.52)
        ax.set_xlim(0, 1)
        ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.tick_params(axis="y", length=0, pad=7)
        ax.tick_params(axis="x", length=3, width=0.6, pad=4)
        ax.set_axisbelow(True)
        ax.grid(axis="x", color="#DFE5EA", linewidth=0.65)
        for side in ["top", "right", "left"]:
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#718191")
        ax.spines["bottom"].set_linewidth(0.6)
        title_x = 0.025 if panel_index == 0 else 0.515
        titles.append(fig.text(title_x, 0.925,
                               "({}) {}".format(panel["id"], panel["title"]),
                               ha="left", va="top", fontsize=10.8, fontweight="bold"))
        titles.append(fig.text(title_x, 0.868, panel["summary"],
                               ha="left", va="top", fontsize=9.1, color="#536372"))
    fig.text(0.53, 0.035, "Typed exact-span micro-F1", ha="center", va="bottom", fontsize=10)
    return fig, axes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE / "model_comparison_data.json")
    parser.add_argument("--output-dir", type=Path, default=PAPER / "figures")
    parser.add_argument("--qa-dir", type=Path)
    args = parser.parse_args()
    data = load_data(args.data)
    fig, axes = build_figure(data)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = {"Title": data["figure"], "Subject": data["metric"],
                "Keywords": "Chinese-SkillSpan; human reference; micro-F1; sample SD"}
    for extension in ("pdf", "svg"):
        destination = args.output_dir / (STEM + "." + extension)
        if extension == "pdf":
            fig.savefig(destination, metadata=metadata, facecolor="white")
        else:
            fig.savefig(destination, metadata={"Title": data["figure"]}, facecolor="white")
        print(str(destination))
    if args.qa_dir:
        args.qa_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.qa_dir / (STEM + ".png"), dpi=220, facecolor="white")
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bounds = fig.bbox
        clipped_text = []
        for text_artist in fig.findobj(matplotlib.text.Text):
            if not text_artist.get_visible() or not text_artist.get_text():
                continue
            box = text_artist.get_window_extent(renderer)
            if box.x0 < bounds.x0 - 1 or box.y0 < bounds.y0 - 1 or box.x1 > bounds.x1 + 1 or box.y1 > bounds.y1 + 1:
                clipped_text.append(text_artist.get_text())
        audit = {
            "metric": data["metric"],
            "figure_inches": list(fig.get_size_inches()),
            "x_limits": [list(ax.get_xlim()) for ax in axes],
            "configurations": sum(len(p["models"]) for p in data["panels"]),
            "single_run_count": 6,
            "three_seed_mean_sd_count": 4,
            "plot_precision": "manuscript display values, three decimals",
            "clipped_text": clipped_text,
            "error_bars": "sample SD across seeds 42, 43, 44",
        }
        (args.qa_dir / "layout_check.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
        assert not clipped_text, "Text outside figure: {}".format(clipped_text)
    plt.close(fig)


if __name__ == "__main__":
    main()
