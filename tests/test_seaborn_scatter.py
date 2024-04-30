def plot():
    import numpy as np
    from matplotlib import pyplot as plt
    import seaborn as sns

    np.random.seed(123)
    data = np.random.rand(4, 64)

    fig, ax = plt.subplots()
    sns.scatterplot({str(i): d for i, d in enumerate(data)}, ax=ax)

    return fig


def test():
    from .helpers import assert_equality

    assert_equality(plot, __file__[:-3] + "_reference.tex")
