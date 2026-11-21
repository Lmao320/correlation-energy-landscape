# Correlation Energy Landscape
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import yfinance as yf
import pandas as pd

# -----------------------
# CONFIG
# -----------------------

ASSET_COUNT = 30
LANDSCAPE_SCALE = 2.5
ANIMATION_INTERVAL = 40
WINDOW = 60
LAG = 5

surf = None
wire = None

# -----------------------
# DOWNLOAD MARKET DATA
# -----------------------

sp500 = yf.download("^GSPC", start="2018-01-01")
ndx = yf.download("^NDX", start="2018-01-01")

sp = sp500["Close"].squeeze()
nd = ndx["Close"].squeeze()

data = pd.concat([sp, nd], axis=1)
data.columns = ["SP500", "NDX"]
data = data.dropna()

# -----------------------
# RETURNS
# -----------------------

returns = np.log(data).diff().dropna()

# -----------------------
# ROLLING CORRELATION
# -----------------------

rolling_corr = returns["SP500"].rolling(WINDOW).corr(returns["NDX"]).dropna()
corr_series = rolling_corr.values

# -----------------------
# LEAD / LAG ANALYSIS
# -----------------------

lead_series = []

for i in range(len(returns) - WINDOW):

    window_sp = returns["SP500"].iloc[i:i+WINDOW]
    window_nd = returns["NDX"].iloc[i:i+WINDOW]

    lags = range(-LAG, LAG+1)

    corrs = []

    for lag in lags:

        if lag > 0:
            corr = window_nd[:-lag].corr(window_sp[lag:])
        elif lag < 0:
            corr = window_nd[-lag:].corr(window_sp[:lag])
        else:
            corr = window_nd.corr(window_sp)

        corrs.append(corr)

    best_lag = lags[np.argmax(corrs)]

    lead_series.append(best_lag)

lead_series = np.array(lead_series)

# -----------------------
# LANDSCAPE GENERATION
# -----------------------

def generate_correlation_energy(t):

    x = np.linspace(-1, 1, ASSET_COUNT)
    y = np.linspace(-1, 1, ASSET_COUNT)

    X, Y = np.meshgrid(x, y)

    idx = int(t) % len(corr_series)

    corr = corr_series[idx]
    lead = lead_series[idx]

    Z = (
        corr * np.sin(2*np.pi*X) *
        np.cos(2*np.pi*Y)
    ) * LANDSCAPE_SCALE

    # inclinación según liderazgo
    Z += lead * 0.3 * X

    return X, Y, Z, corr, lead


# -----------------------
# PLOT INITIALIZATION
# -----------------------

def init_plot():

    fig = plt.figure(figsize=(10,8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.grid(True, color='white', linewidth=0.5, alpha=0.3)

    ax.set_xlabel('Asset Axis X', color='white')
    ax.set_ylabel('Asset Axis Y', color='white')
    ax.set_zlabel('Correlation Energy', color='white')

    ax.tick_params(colors='white')

    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(-LANDSCAPE_SCALE*2, LANDSCAPE_SCALE*2)

    ax.set_title(
        "Correlation Energy Landscape\nS&P 500 vs NASDAQ-100",
        color="#C800FF",
        fontsize=16
    )

    return fig, ax

# -----------------------
# ANIMATION UPDATE
# -----------------------

def update(frame):

    global surf, wire

    X, Y, Z, corr, lead = generate_correlation_energy(frame)

    if surf is not None:
        surf.remove()

    if wire is not None:
        wire.remove()

    surf = ax.plot_surface(
        X,
        Y,
        Z,
        cmap=cm.magma,
        edgecolor='none',
        alpha=0.7
    )

    wire = ax.plot_wireframe(
        X,
        Y,
        Z,
        color="#C800FF",
        linewidth=0.2,
        alpha=0.25
    )

    if lead > 0:
        leader = "NASDAQ leads"
    elif lead < 0:
        leader = "SP500 leads"
    else:
        leader = "Synchronized"

    ax.set_title(
        f"Correlation Energy Landscape\nSP500 vs NASDAQ\nCorrelation: {corr:.2f}",
        color="#C800FF"
    )

    ax.text2D(
        0.02,
        0.92,
        f"Market Leadership: {leader}",
        transform=ax.transAxes,
        color="white",
        fontsize=11
    )

# -----------------------
# MAIN EXECUTION
# -----------------------

fig, ax = init_plot()

ani = FuncAnimation(
    fig,
    update,
    frames=300,
    interval=ANIMATION_INTERVAL
)

plt.show()