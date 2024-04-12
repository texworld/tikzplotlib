import functools
import re
import matplotlib.transforms
import numpy as np


def has_legend(axes):
    return axes.get_legend() is not None


def get_legend_text(obj):
    """Check if line is in legend."""
    leg = obj.axes.get_legend()
    if leg is None:
        return None

    keys = [h.get_label() for h in leg.legendHandles if h is not None]
    values = [t.get_text() for t in leg.texts]

    label = obj.get_label()
    d = dict(zip(keys, values))
    if label in d:
        return d[label]

    return None


def transform_to_data_coordinates(obj, xdata, ydata):
    """The coordinates might not be in data coordinates, but could be sometimes in axes
    coordinates. For example, the matplotlib command
      axes.axvline(2)
    will have the y coordinates set to 0 and 1, not to the limits. Therefore, a
    two-stage transform has to be applied:
      1. first transforming to display coordinates, then
      2. from display to data.
    """
    if obj.axes is not None and obj.get_transform() != obj.axes.transData:
        points = np.array([xdata, ydata]).T
        transform = matplotlib.transforms.composite_transform_factory(
            obj.get_transform(), obj.axes.transData.inverted()
        )
        return transform.transform(points).T
    return xdata, ydata


_NO_ESCAPE = r"(?<!\\)(?:\\\\)*"
_split_math = re.compile(_NO_ESCAPE + r"\$").split
_replace_mathdefault = functools.partial(
    # Replace \mathdefault (when not preceded by an escape) by empty string.
    re.compile(_NO_ESCAPE + r"(\\mathdefault)").sub, "")

def _common_texification(text):
    return _tex_escape(text)

def _tex_escape(text):
    r"""
    Do some necessary and/or useful substitutions for texts to be included in
    LaTeX documents.
    This distinguishes text-mode and math-mode by replacing the math separator
    ``$`` with ``\(\displaystyle %s\)``. Escaped math separators (``\$``)
    are ignored.
    """
    # Sometimes, matplotlib adds the unknown command \mathdefault.
    # Not using \mathnormal instead since this looks odd for the latex cm font.
    text = _replace_mathdefault(text)
    text = text.replace("\N{MINUS SIGN}", r"\ensuremath{-}")
    # Work around <https://github.com/matplotlib/matplotlib/issues/15493>
    text = text.replace("&", r"\&")
    # split text into normaltext and inline math parts
    parts = _split_math(text)
    for i, s in enumerate(parts):
        if i % 2:  # mathmode replacements
            s = r"\(\displaystyle %s\)" % s
        parts[i] = s
    return "".join(parts)
