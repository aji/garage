import sys
import time
import math
import os

from mpmath import mp

import pygame
from pygame.locals import *

from bazel_tools.tools.python.runfiles import runfiles

R = runfiles.Create()

from py.util.math import plot_lerps


class ZetaImLine(object):
    def __init__(self, re, limit=10):
        self.re = re
        self.limit = limit
        self.pts = []

    def extend(self, t):
        self.pts.append((t, mp.zeta(self.re + t * 1j)))
        while len(self.pts) > 0 and self.pts[0][0] < t - self.limit:
            self.pts.pop(0)

    def plots(self, re_lerp, im_lerp):
        return [[(re_lerp(mp.re(z)), im_lerp(mp.im(z))) for t, z in self.pts]]


class ZetaGridLines(object):
    def __init__(self, res, limit=10, interval=1):
        self.res = res
        self.next = 0
        self.limit = limit
        self.interval = interval
        self.pts = []

    def extend(self, t):
        while self.next <= t:
            self.pts.append(
                (self.next, [mp.zeta(re + self.next * 1j) for re in self.res])
            )
            self.next += self.interval
        while len(self.pts) > 0 and self.pts[0][0] < t - self.limit:
            self.pts.pop(0)

    def plots(self, re_lerp, im_lerp):
        return [
            [(re_lerp(mp.re(z)), im_lerp(mp.im(z))) for z in zs] for t, zs in self.pts
        ]


class ZetaPlot(object):
    def __init__(self, surface, color, re_lerp, im_lerp, line):
        self.surface = surface
        self.color = color
        self.re_lerp = re_lerp
        self.im_lerp = im_lerp
        self.line = line

    def extend_and_plot(self, t):
        self.line.extend(t)
        for plot in self.line.plots(self.re_lerp, self.im_lerp):
            if len(plot) > 2:
                pygame.draw.aalines(self.surface, self.color, False, plot)


pygame.init()

width, height = (1920, 1080)
screen = pygame.display.set_mode((width, height))
font_path = R.Rlocation("__main__/fonts/iosevka-term-slab-regular.ttf")
if font_path is None:
    raise Exception("could not find font")
font = pygame.font.Font(font_path, 24)

re_lerp, im_lerp = plot_lerps(width, height, 1.0, 0.0, None, 8)

plots = [
    ZetaPlot(
        screen,
        (128, 128, 128),
        re_lerp,
        im_lerp,
        ZetaGridLines([0.45, 0.5, 0.55], interval=0.05, limit=20),
    ),
    ZetaPlot(
        screen,
        (255, 255, 255),
        re_lerp,
        im_lerp,
        ZetaGridLines([0.45, 0.5, 0.55], interval=1, limit=20),
    ),
    ZetaPlot(screen, (128, 128, 128), re_lerp, im_lerp, ZetaImLine(0.45, limit=20)),
    ZetaPlot(screen, (128, 128, 128), re_lerp, im_lerp, ZetaImLine(0.55, limit=20)),
    ZetaPlot(screen, (255, 255, 255), re_lerp, im_lerp, ZetaImLine(0.5, limit=20)),
]


def render(t, dt):
    screen.fill((0, 0, 0))

    screen.blit(
        font.render(
            "t={:.6f}".format(t),
            True,
            (255, 255, 255),
            (0, 0, 0),
        ),
        (10, 10),
    )

    pygame.draw.aalines(
        screen,
        (128, 128, 128),
        True,
        [
            (re_lerp(0.05), im_lerp(0)),
            (re_lerp(0), im_lerp(0.05)),
            (re_lerp(-0.05), im_lerp(0)),
            (re_lerp(0), im_lerp(-0.05)),
        ],
    )

    for plot in plots:
        plot.extend_and_plot(t)


def run_realtime():
    t_start = time.monotonic()
    t_last = t_start

    while True:
        t_now = time.monotonic()
        t = t_now - t_start
        dt = t_now - t_last
        t_last = t_now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        render(t, dt)
        pygame.display.flip()


def run_animated(upto=120, fps=60, outdir=None):
    for frame in range(upto * fps):
        t = frame / fps
        dt = 1 / fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        render(t, dt)
        pygame.display.flip()

        if outdir is not None:
            fname = os.path.join(outdir, "frame{:06}.png".format(frame))
            with open(fname, "wb") as f:
                pygame.image.save(screen, f, fname)
                print(f"wrote {fname}")


run_realtime()
# run_animated(outdir="Z:\\tmp\\zeta")
