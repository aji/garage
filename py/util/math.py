def lerp(x, y0, y1):
    return y0 + (y1 - y0) * x


def lerp2(x0, y0, x1, y1, x):
    return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))


def lerper(x0, y0, x1, y1):
    dy = y1 - y0
    dx = x1 - x0
    return lambda x: y0 + dy * ((x - x0) / dx)


def plot_lerps(w, h, cx, cy, sx, sy):
    if sx is None:
        if sy is None:
            raise ValueError("sx and sy cannot both be None")
        sx = sy * w / h
    elif sy is None:
        sy = sx * h / w
    return (
        lerper(cx - sx / 2, 0, cx + sx / 2, w),
        lerper(cy - sy / 2, h, cy + sy / 2, 0),
    )


def clamp(x0, x1, x):
    return min(x1, max(x0, x))


def clamper(x0, x1):
    return lambda x: min(x1, max(x0, x))