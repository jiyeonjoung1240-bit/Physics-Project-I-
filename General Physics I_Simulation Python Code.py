"""
Bouncing to Rolling Transition — Experiment Visualization
Based on: "Transition from bouncing to rolling on a horizontal surface" (Rod Cross, AJP 2024)
Experiment data from Group 7 Physics Project Report (DGIST, 2026)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib.gridspec import GridSpec

# ──────────────────────────────────────────────
# 1. Experimental Data (from Table 2 in report)
# ──────────────────────────────────────────────
bounce_times   = [0.00, 0.94, 1.55, 1.97, 2.29, 2.58, 2.77, 2.94]  # time to reach max height (s)
bounce_heights = [1.10, 0.52, 0.30, 0.19, 0.12, 0.09, 0.07, 0.05]  # max height (m)
t_roll_exp     = 3.14   # experimentally observed rolling onset time (s)

g = 9.8  # m/s²

# ──────────────────────────────────────────────
# 2. Coefficient of Restitution (e_y)
# ──────────────────────────────────────────────
e_y_list = [np.sqrt(bounce_heights[i+1] / bounce_heights[i])
            for i in range(len(bounce_heights) - 1)]
e_y_avg = np.mean(e_y_list)

print("=" * 50)
print("  Bounce-to-Roll Experiment Analysis")
print("=" * 50)
for i, e in enumerate(e_y_list):
    print(f"  e_y{i+1} = sqrt({bounce_heights[i+1]:.2f}/{bounce_heights[i]:.2f}) = {e:.3f}")
print(f"\n  Average e_y = {e_y_avg:.3f}")

# ──────────────────────────────────────────────
# 3. Predicted Rolling Onset Time
# ──────────────────────────────────────────────
h0   = 1.10   # m
N    = 7      # number of bounces observed

v_y0 = np.sqrt(2 * g * h0)
v_y1 = e_y_avg * v_y0
t0   = np.sqrt(2 * h0 / g)                            # free-fall time

e_N  = e_y_avg ** N
t_bounce = (2 * v_y1 / g) * (1 - e_N) / (1 - e_y_avg)
t_roll_pred = t0 + t_bounce
error_pct   = abs(t_roll_pred - t_roll_exp) / t_roll_exp * 100

print(f"\n  Initial vertical velocity  v_y0 = {v_y0:.2f} m/s")
print(f"  Post-first-bounce velocity v_y1 = {v_y1:.2f} m/s")
print(f"  Free-fall time             t0   = {t0:.3f} s")
print(f"  Bouncing duration          t_b  = {t_bounce:.3f} s")
print(f"\n  Predicted rolling onset  : {t_roll_pred:.2f} s")
print(f"  Observed  rolling onset  : {t_roll_exp:.2f} s")
print(f"  Relative error           : {error_pct:.1f}%")
print("=" * 50)

# ──────────────────────────────────────────────
# 4. Build Full Trajectory for Animation
#    (piecewise parabolas per bounce)
# ──────────────────────────────────────────────
def build_trajectory(h0, e_y, N_bounces, g=9.8, dt=0.005):
    """
    Returns arrays (t_arr, y_arr, x_arr) for the ball trajectory.
    After rolling onset the ball travels horizontally.
    """
    t_all, y_all, x_all = [], [], []

    # --- free fall ---
    v0 = np.sqrt(2 * g * h0)
    t_fall = v0 / g
    ts = np.arange(0, t_fall, dt)
    ys = h0 - 0.5 * g * ts**2
    xs = np.zeros_like(ts)
    t_all.append(ts); y_all.append(ys); x_all.append(xs)

    t_cur = t_fall
    x_cur = 0.0
    v_up  = e_y * v0        # velocity just after 1st bounce
    x_speed = 0.3           # constant horizontal speed (m/s) for visual

    for n in range(N_bounces):
        t_apex = v_up / g
        t_seg  = 2 * t_apex
        ts = np.arange(0, t_seg, dt)
        ys = v_up * ts - 0.5 * g * ts**2
        xs = x_cur + x_speed * ts
        t_all.append(ts + t_cur)
        y_all.append(ys)
        x_all.append(xs)
        t_cur += t_seg
        x_cur  = xs[-1]
        v_up  *= e_y

    # --- rolling phase ---
    t_roll_dur = 1.5
    ts = np.arange(0, t_roll_dur, dt)
    ys = np.zeros_like(ts)
    xs = x_cur + x_speed * ts
    t_all.append(ts + t_cur)
    y_all.append(ys)
    x_all.append(xs)

    return (np.concatenate(t_all),
            np.concatenate(y_all),
            np.concatenate(x_all))

t_traj, y_traj, x_traj = build_trajectory(h0, e_y_avg, N)

# ──────────────────────────────────────────────
# 5. Figure Layout
# ──────────────────────────────────────────────
fig = plt.figure(figsize=(14, 9), facecolor="#0f0f1a")
fig.suptitle("Bouncing → Rolling Transition  |  Tennis Ball Experiment (DGIST Group 7)",
             fontsize=13, color="white", fontweight="bold", y=0.97)

gs = GridSpec(2, 2, figure=fig,
              left=0.07, right=0.97, top=0.92, bottom=0.08,
              hspace=0.42, wspace=0.32)

ax_anim  = fig.add_subplot(gs[0, :])   # top  — full width animation
ax_ht    = fig.add_subplot(gs[1, 0])   # bottom-left  — height decay
ax_pred  = fig.add_subplot(gs[1, 1])   # bottom-right — predicted vs exp

for ax in [ax_anim, ax_ht, ax_pred]:
    ax.set_facecolor("#12122a")
    for sp in ax.spines.values():
        sp.set_edgecolor("#444466")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

# ── Animation panel ──────────────────────────
ax_anim.set_xlim(-0.1, x_traj.max() + 0.3)
ax_anim.set_ylim(-0.05, h0 * 1.15)
ax_anim.set_xlabel("Horizontal position (m)", fontsize=10)
ax_anim.set_ylabel("Height (m)", fontsize=10)
ax_anim.set_title("Ball Trajectory Animation", fontsize=11)
ax_anim.axhline(0, color="#555577", lw=1.5, ls="--")

# Floor shading
ax_anim.fill_between([ax_anim.get_xlim()[0], ax_anim.get_xlim()[1]],
                     [-0.05, -0.05], [0, 0],
                     color="#2a2a4a", zorder=0)

# Rolling onset vertical line
x_roll_onset = x_traj[np.searchsorted(t_traj, t_roll_exp)]
ax_anim.axvline(x_roll_onset, color="#ff6b6b", lw=1.5, ls=":")
ax_anim.text(x_roll_onset + 0.03, h0 * 0.85,
             f"Rolling onset\n(t = {t_roll_exp} s)",
             color="#ff6b6b", fontsize=8.5)

# Trajectory ghost path
ax_anim.plot(x_traj, y_traj, color="#334455", lw=1.2, zorder=1, alpha=0.6)

BALL_R = 0.025
ball_patch = Circle((x_traj[0], y_traj[0] + BALL_R),
                    BALL_R, color="#4fc3f7", zorder=5)
ax_anim.add_patch(ball_patch)
time_text = ax_anim.text(0.02, 0.90, "", transform=ax_anim.transAxes,
                          color="white", fontsize=9)
phase_text = ax_anim.text(0.75, 0.90, "", transform=ax_anim.transAxes,
                           fontsize=9, fontweight="bold")

# ── Bounce Height Decay ───────────────────────
bounce_nums = list(range(len(bounce_heights)))
# Theoretical curve
n_arr  = np.linspace(0, N, 200)
h_theo = h0 * e_y_avg ** (2 * n_arr)

ax_ht.plot(n_arr, h_theo, color="#4fc3f7", lw=2,
           label=f"Theory  (e_y={e_y_avg:.2f})")
ax_ht.scatter(bounce_nums, bounce_heights,
              color="#ffb347", s=60, zorder=5, label="Experiment")
ax_ht.set_xlabel("Bounce number", fontsize=10)
ax_ht.set_ylabel("Max height (m)", fontsize=10)
ax_ht.set_title("Bounce Height Decay", fontsize=11)
ax_ht.legend(fontsize=8.5, facecolor="#1e1e3a", labelcolor="white",
             edgecolor="#444466")
ax_ht.grid(True, color="#2a2a4a", lw=0.8)

# ── Predicted vs Experimental ─────────────────
labels  = ["Predicted", "Experimental"]
values  = [t_roll_pred, t_roll_exp]
colors  = ["#4fc3f7", "#ffb347"]
bars    = ax_pred.bar(labels, values, color=colors, width=0.45,
                      edgecolor="#555577", linewidth=1.2)
for bar, val in zip(bars, values):
    ax_pred.text(bar.get_x() + bar.get_width() / 2,
                 val + 0.04, f"{val:.2f} s",
                 ha="center", color="white", fontsize=10, fontweight="bold")

ax_pred.set_ylabel("Rolling onset time (s)", fontsize=10)
ax_pred.set_title(f"Predicted vs Experimental\n(Error = {error_pct:.1f}%)",
                  fontsize=11)
ax_pred.set_ylim(0, max(values) * 1.2)
ax_pred.grid(True, axis="y", color="#2a2a4a", lw=0.8)

# ──────────────────────────────────────────────
# 6. Animation
# ──────────────────────────────────────────────
SKIP = 4   # render every N-th frame for speed

def animate(frame):
    i = frame * SKIP
    if i >= len(t_traj):
        i = len(t_traj) - 1
    t_now = t_traj[i]
    xb    = x_traj[i]
    yb    = y_traj[i] + BALL_R
    ball_patch.set_center((xb, yb))

    # colour: blue while bouncing, green while rolling
    if t_now < t_roll_exp:
        ball_patch.set_color("#4fc3f7")
        phase_text.set_text("● BOUNCING")
        phase_text.set_color("#4fc3f7")
    else:
        ball_patch.set_color("#69f0ae")
        phase_text.set_text("● ROLLING")
        phase_text.set_color("#69f0ae")

    time_text.set_text(f"t = {t_now:.2f} s")
    return ball_patch, time_text, phase_text

total_frames = len(t_traj) // SKIP
ani = animation.FuncAnimation(fig, animate,
                               frames=total_frames,
                               interval=20, blit=True, repeat=True)

plt.savefig("C:/Users/jiyeo/Downloads/bounce_to_roll_static.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("\n  Static preview saved → bounce_to_roll_static.png")

plt.show()
