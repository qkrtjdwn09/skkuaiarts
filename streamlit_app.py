import io
import random, math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import streamlit as st

# ----------------------------
# Core functions from your code
# ----------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def vivid_palette(k=5):
    colors = []
    for _ in range(k):
        h = random.random()
        s = random.uniform(0.8, 1.0)
        v = random.uniform(0.8, 1.0)
        colors.append(tuple(mcolors.hsv_to_rgb((h,s,v))))
    return colors

def generate_poster(style="Vivid",
                    seed=None,
                    n_layers=8,
                    wobble_min=0.05,
                    wobble_max=0.2,
                    bg=(0.98,0.98,0.97),
                    palette_size=6,
                    fig_w=7,
                    fig_h=10):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = plt.gca()
    ax.axis("off")
    ax.set_facecolor(bg)

    palette = vivid_palette(palette_size)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob(center=(cx, cy), r=rr,
                    wobble=random.uniform(wobble_min, wobble_max))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold',
            transform=ax.transAxes, color=(0.1,0.1,0.1))
    ax.text(0.05, 0.91, f"Style: {style}, Seed={seed}", fontsize=11,
            transform=ax.transAxes, color=(0.2,0.2,0.2))

    ax.set_xlim(0,1); ax.set_ylim(0,1)
    fig.tight_layout(pad=0)
    return fig

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="GenPoster", page_icon="🎨", layout="centered")

st.title("🎨 Generative Poster")
st.caption("Matplotlib + Streamlit (vivid blob layers)")

with st.sidebar:
    st.header("Controls")
    seed_on = st.toggle("Fix seed?", value=True)
    seed_val = st.number_input("Seed", value=42, step=1) if seed_on else None

    n_layers = st.slider("Layers", 1, 20, 8)
    wobble_min, wobble_max = st.slider("Wobble range", 0.0, 0.6, (0.05, 0.20), step=0.01)
    palette_size = st.slider("Palette size", 3, 12, 6)

    bg_hex = st.color_picker("Background", value="#fbfbf8")
    # convert hex to rgb tuple in 0-1
    bg_rgb = tuple(int(bg_hex[i:i+2], 16)/255.0 for i in (1,3,5))

    fig_w = st.slider("Width (inches)", 4, 12, 7)
    fig_h = st.slider("Height (inches)", 4, 16, 10)

    redraw = st.button("Redraw")

# Redraw on every interaction or button press
if redraw or True:
    fig = generate_poster(
        style="Vivid",
        seed=seed_val if seed_on else None,
        n_layers=n_layers,
        wobble_min=wobble_min,
        wobble_max=wobble_max,
        bg=bg_rgb,
        palette_size=palette_size,
        fig_w=fig_w,
        fig_h=fig_h
    )

    st.pyplot(fig, clear_figure=True, use_container_width=False)

    # Download PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    st.download_button(
        "Download PNG",
        data=buf,
        file_name=f"poster_vivid_seed{seed_val if seed_on else 'random'}.png",
        mime="image/png"
    )
