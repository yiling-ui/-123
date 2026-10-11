# -*- coding: utf-8 -*-
"""生成同济《高等数学》第八版 第一章第一节《映射与函数》教学图。
图1 映射概念：像唯一、原像不唯一、R_f⊂Y
图2 单射 / 满射 / 双射 对比
图3 复合映射：R_g⊂D_f 与 (f∘g)(x)=f[g(x)]
图4 函数图形法：y=f(x) 的图形、定义域与值域在坐标轴上的投影
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def ellipse_pt(ax, cx, cy, rx, ry, color, edge, lw=1.6):
    e = mpatches.Ellipse((cx, cy), 2 * rx, 2 * ry, fill=True,
                         facecolor=color, edgecolor=edge, lw=lw, zorder=1)
    ax.add_patch(e)


def elem_circle(ax, x, y, label, fc, r=0.034, fs=13, zorder=3):
    c = Circle((x, y), r, facecolor=fc, edgecolor="black", lw=1.3, zorder=zorder)
    ax.add_patch(c)
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, zorder=4)


def arrow(ax, x1, y1, x2, y2, rad=0.12, color="black", lw=1.6,
          style="-|>", ms=12, zorder=2):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=ms, color=color, lw=lw,
                        connectionstyle=f"arc3,rad={rad}", zorder=zorder)
    ax.add_patch(a)


def box_text(ax, x, y, s, fs=13, color="black", ha="center", va="center",
             fc="white", ec="black", lw=1.0, zorder=5):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, zorder=zorder,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=fc, edgecolor=ec, lw=lw))


def title(ax, s, fs=15, y=1.02):
    ax.text(0.5, y, s, ha="center", va="bottom", fontsize=fs, fontweight="bold")


# ---------------------------------------------------------------- 图1
fig, ax = plt.subplots(figsize=(8.6, 5.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
title(ax, "映射 f : X → Y —— 像唯一，原像可以不唯一，值域是 Y 的子集")

ellipse_pt(ax, 0.22, 0.52, 0.115, 0.34, "#eaf3fb", "#2f6fb0")
ellipse_pt(ax, 0.79, 0.52, 0.115, 0.40, "#fdf3e7", "#c07a2a")
ax.text(0.22, 0.90, "X", ha="center", fontsize=16, fontweight="bold", color="#1d4f8f")
ax.text(0.79, 0.96, "Y", ha="center", fontsize=16, fontweight="bold", color="#a3611c")

for y, lab in zip([0.80, 0.52, 0.24], ["1", "2", "3"]):
    elem_circle(ax, 0.22, y, lab, "#cfe3f7")
for y, lab in zip([0.92, 0.70, 0.48, 0.26], ["a", "b", "c", "d"]):
    elem_circle(ax, 0.79, y, lab, "#f7d9a8" if lab in ("a", "b") else "#efe0c8")

arrow(ax, 0.335, 0.80, 0.655, 0.92, rad=0.10)
arrow(ax, 0.335, 0.52, 0.655, 0.70, rad=0.05)
arrow(ax, 0.335, 0.24, 0.655, 0.70, rad=-0.28)

box_text(ax, 0.50, 0.155, r"R$_f$ = {a, b} $\subset$ Y，c、d 不是任何元素的像", fs=13)
box_text(ax, 0.50, 0.045, "定义域 D$_f$ = X = {1, 2, 3}", fs=13)
ax.text(0.565, 0.855, "f(1) = a：1 的像", fontsize=12, ha="left")
ax.text(0.565, 0.63, "f(2) = f(3) = b：\n两个原像射向同一个 b", fontsize=12, ha="left")
ax.annotate("b 的原像有两个：2 和 3\n（原像不唯一）", xy=(0.79, 0.70), xytext=(0.92, 0.42),
            fontsize=12, ha="center",
            arrowprops=dict(arrowstyle="->", color="#c07a2a", lw=1.4))
plt.tight_layout()
plt.savefig(os.path.join(OUT, "图1-映射概念.png"), dpi=200)
plt.close(fig)


# ---------------------------------------------------------------- 图2
fig, axs = plt.subplots(1, 3, figsize=(10.5, 4.0))
for a in axs:
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")


def draw_pair(ax, xpts, xlabels, ypts, ylabels, pairs, extra):
    ellipse_pt(ax, 0.25, 0.5, 0.1, 0.36, "#eaf3fb", "#2f6fb0")
    ellipse_pt(ax, 0.78, 0.5, 0.1, 0.36, "#fdf3e7", "#c07a2a")
    ax.text(0.25, 0.90, "X", ha="center", fontsize=14, fontweight="bold", color="#1d4f8f")
    ax.text(0.78, 0.90, "Y", ha="center", fontsize=14, fontweight="bold", color="#a3611c")
    for y, lab in zip(xpts, xlabels):
        elem_circle(ax, 0.25, y, lab, "#cfe3f7")
    for y, lab in zip(ypts, ylabels):
        elem_circle(ax, 0.78, y, lab, "#f7d9a8")
    for i, j in pairs:
        arrow(ax, 0.35, xpts[i], 0.68, ypts[j], rad=0.10, lw=1.4)
    ax.text(0.5, 0.03, extra, ha="center", fontsize=12)


draw_pair(axs[0], [0.80, 0.52, 0.24], ["1", "2", "3"],
          [0.86, 0.64, 0.42, 0.20], ["a", "b", "c", "d"],
          [(0, 0), (1, 1), (2, 2)],
          "单射：不同 x 的像必不同\n1→a, 2→b, 3→c；d 没有原像，故不是满射")
draw_pair(axs[1], [0.80, 0.52, 0.24], ["1", "2", "3"],
          [0.68, 0.32], ["a", "b"],
          [(0, 0), (1, 1), (2, 0)],
          "满射：R$_f$ = Y，每个 y 都有原像\n1→a, 2→b, 3→a；1 与 3 同像 a，故不是单射")
draw_pair(axs[2], [0.80, 0.52, 0.24], ["1", "2", "3"],
          [0.80, 0.52, 0.24], ["a", "b", "c"],
          [(0, 0), (1, 1), (2, 2)],
          "双射（一一映射）：既单又满\n1→a, 2→b, 3→c，逆映射存在")
for i, a in enumerate(axs):
    a.set_title(["单射", "满射", "双射"][i], fontsize=15, pad=4)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "图2-单射满射双射.png"), dpi=200)
plt.close(fig)


# ---------------------------------------------------------------- 图3
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
title(ax, r"复合映射 $f\circ g$：X →g→ Y$_1$ $\subset$ Y$_2$ →f→ Z，条件 R$_g$ $\subset$ D$_f$", y=1.04)

box_text(ax, 0.13, 0.55, "X\nx", fs=15, fc="#eaf3fb", ec="#2f6fb0")
box_text(ax, 0.47, 0.55, r"Y$_1$ = R$_g$  $\subset$  Y$_2$ = D$_f$" + "\ng(x)", fs=14,
         fc="#fdf3e7", ec="#c07a2a")
box_text(ax, 0.83, 0.55, "Z\nf[g(x)]", fs=15, fc="#eaf3fb", ec="#2f6fb0")

arrow(ax, 0.21, 0.55, 0.38, 0.55, rad=0, lw=2.0, color="#2f6fb0")
arrow(ax, 0.56, 0.55, 0.74, 0.55, rad=0, lw=2.0, color="#c07a2a")
ax.text(0.295, 0.64, "g", fontsize=16, ha="center", color="#1d4f8f")
ax.text(0.65, 0.64, "f", fontsize=16, ha="center", color="#a3611c")

ax.text(0.50, 0.84, r"先 g 后 f：$(f\circ g)(x) = f[g(x)]$，x ∈ X", ha="center",
        fontsize=14, color="#111111")
box_text(ax, 0.50, 0.20, r"能复合的条件：g 的值域 R$_g$ 必须包含在 f 的定义域 D$_f$ 内" + "\n" +
         r"（图中 Y$_1$ $\subset$ Y$_2$）；次序不能颠倒：$f\circ g$ 有意义，$g\circ f$ 未必有意义", fs=13)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "图3-复合映射.png"), dpi=200)
plt.close(fig)


# ---------------------------------------------------------------- 图4
fig, ax = plt.subplots(figsize=(8.4, 5.8))
xs = [x / 100 for x in range(-200, 301)]
f = lambda x: 1 + (x - 1) ** 2 / 2          # 顶点(1,1)，开口向上
ys = [f(x) for x in xs]

ax.plot(xs, ys, color="#1d4f8f", lw=2.4, zorder=3)
ax.axhline(0, color="black", lw=1.0)
ax.axvline(0, color="black", lw=1.0)
ax.set_xlim(-3.2, 3.7); ax.set_ylim(-0.6, 3.9)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("x", fontsize=13)
ax.set_ylabel("y", fontsize=13, rotation=0, labelpad=10)

ax.plot([-2, 3], [0, 0], color="#c0392b", lw=8, solid_capstyle="butt", zorder=2)
ax.text(0.5, -0.42, "定义域 D$_f$ = [−2, 3]", ha="center", fontsize=13, color="#c0392b")
ax.plot([0, 0], [1, 3], color="#27ae60", lw=8, solid_capstyle="butt", zorder=2)
ax.text(3.45, 1.75, "值域 R$_f$ = [1, 3]", ha="right", fontsize=13, color="#1e8449")

px, py = 1.6, f(1.6)
ax.plot([px], [py], "o", color="#c0392b", ms=9, zorder=5)
ax.plot([px, px], [0, py], ls="--", color="#888888", lw=1.1, zorder=1)
ax.plot([0, py], [py, py], ls="--", color="#888888", lw=1.1, zorder=1)
ax.text(px + 0.18, py + 0.28, "P(x, y) = (x, f(x))", fontsize=13, color="#c0392b")
ax.text(-3.05, 3.55, "函数 y = f(x) 的图形\n= { P(x,y) | y = f(x), x ∈ D }",
        fontsize=13, va="top", color="#111111")
ax.text(3.45, 3.25, "y = 1 + (x−1)²/2", fontsize=12, ha="right", color="#1d4f8f")
ax.set_title("图形法表示函数：曲线上每一点 P(x, y) 满足 y = f(x)",
             fontsize=15, pad=10)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "图4-函数图形法.png"), dpi=200)
plt.close(fig)

print("生成完成：", os.listdir(OUT))
