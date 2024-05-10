#%%
def plot():
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib.animation as animation

    fig, ax = plt.subplots()
    scat = ax.scatter(range(10), [0] * 10)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 10)

    def update(frame):
        y_data = [yi + frame * 0.2 for yi in range(10)]
        scat.set_offsets(list(zip(range(10), y_data)))
        ax.set_title(f"Frame {frame+1}/20")

    ani = animation.FuncAnimation(fig, update, frames=20, repeat=False)
    return ani


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")

# %%
ani = plot()
# %%
