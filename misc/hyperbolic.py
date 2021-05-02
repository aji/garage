import sys
import time
import math
import os

import kiwisolver as K

import pygame
from pygame.locals import *

from py.util.math import lerp_unlerp

solver = K.Solver()

width = K.Variable("width")
height = K.Variable("height")
pad = K.Variable("pad")

plots_x = K.Variable("plots_x")
plots_y = K.Variable("plots_y")
plot_sz = K.Variable("plot_sz")

solver.addEditVariable(width, "strong")
solver.addEditVariable(height, "strong")
solver.addEditVariable(pad, "strong")

solver.addConstraint(pad <= plots_x)
solver.addConstraint(pad <= plots_y)
solver.addConstraint(plots_x + plot_sz + pad + plot_sz + plots_x == width)
solver.addConstraint(plots_y + plot_sz + plots_y == height)

uh_plot_rect, uh_to_plot, uh_fr_plot = None, None, None
pd_plot_rect, pd_to_plot, pd_fr_plot = None, None, None


def set_size(w=1920, h=1080):
    global uh_plot_rect, uh_to_plot, uh_fr_plot
    global pd_plot_rect, pd_to_plot, pd_fr_plot

    solver.suggestValue(width, w)
    solver.suggestValue(height, h)
    solver.suggestValue(pad, 50)

    solver.updateVariables()

    uh_plot_rect = pygame.Rect(
        plots_x.value(), plots_y.value(), plot_sz.value(), plot_sz.value()
    )
    pd_plot_rect = pygame.Rect(
        plots_x.value() + plot_sz.value() + pad.value(),
        plots_y.value(),
        plot_sz.value(),
        plot_sz.value(),
    )

    uh_to_plot_re, uh_fr_plot_x = lerp_unlerp(
        -3, uh_plot_rect.left, 3, uh_plot_rect.right
    )
    uh_to_plot_im, uh_fr_plot_y = lerp_unlerp(
        0, uh_plot_rect.bottom, 6, uh_plot_rect.top
    )

    pd_to_plot_re, pd_fr_plot_x = lerp_unlerp(
        -1.2, pd_plot_rect.left, 1.2, pd_plot_rect.right
    )
    pd_to_plot_im, pd_fr_plot_y = lerp_unlerp(
        -1.2, pd_plot_rect.bottom, 1.2, pd_plot_rect.top
    )

    uh_to_plot = lambda re, im: (uh_to_plot_re(re), uh_to_plot_im(im))
    pd_to_plot = lambda re, im: (pd_to_plot_re(re), pd_to_plot_im(im))

    uh_fr_plot = lambda x, y: (uh_fr_plot_x(x), uh_fr_plot_y(y))
    pd_fr_plot = lambda x, y: (pd_fr_plot_x(x), pd_fr_plot_y(y))


def cayley(re, im):
    num = re + (im - 1) * 1j
    den = re + (im + 1) * 1j
    q = num / den
    return q.real, q.imag


def un_cayley(re, im):
    num = (re + 1) + im * 1j
    den = (re - 1) + im * 1j
    z = -1j * num / den
    return z.real, z.imag


def run_realtime():
    screen = None
    drawing = False

    t_start = time.monotonic()
    t_last = t_start

    def set_display(w, h):
        nonlocal screen
        screen = pygame.display.set_mode((w, h), flags=pygame.RESIZABLE)
        set_size(w, h)

    set_display(1920, 1080)

    def clear():
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (80, 50, 50), uh_plot_rect)
        pygame.draw.rect(screen, (50, 50, 80), pd_plot_rect)

        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-2, 0), uh_to_plot(-2, 6))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-1, 0), uh_to_plot(-1, 6))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(1, 0), uh_to_plot(1, 6))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(2, 0), uh_to_plot(2, 6))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-3, 1), uh_to_plot(3, 1))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-3, 2), uh_to_plot(3, 2))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-3, 3), uh_to_plot(3, 3))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-3, 4), uh_to_plot(3, 4))
        pygame.draw.line(screen, (130, 40, 40), uh_to_plot(-3, 5), uh_to_plot(3, 5))
        pygame.draw.line(screen, (255, 40, 40), uh_to_plot(0, 0), uh_to_plot(0, 6))
        pygame.draw.line(screen, (255, 40, 40), uh_to_plot(-3, 0), uh_to_plot(3, 0))

        left, top = pd_to_plot(-1, 1)
        right, bottom = pd_to_plot(1, -1)
        unit_circle = pygame.Rect(left, top, right - left, bottom - top)

        pygame.draw.ellipse(screen, (40, 40, 255), unit_circle, width=1)
        pygame.draw.line(screen, (40, 40, 255), pd_to_plot(-1.2, 0), pd_to_plot(1.2, 0))
        pygame.draw.line(screen, (40, 40, 255), pd_to_plot(0, -1.2), pd_to_plot(0, 1.2))

    clear()

    while True:
        t_now = time.monotonic()
        t = t_now - t_start
        dt = t_now - t_last
        t_last = t_now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if uh_plot_rect.collidepoint(event.pos):
                        re, im = uh_fr_plot(*event.pos)
                        pygame.draw.circle(
                            screen, (255, 255, 255), uh_to_plot(re, im), 2
                        )
                        re, im = cayley(re, im)
                        pygame.draw.circle(
                            screen, (255, 255, 255), pd_to_plot(re, im), 2
                        )
                    elif pd_plot_rect.collidepoint(event.pos):
                        re, im = pd_fr_plot(*event.pos)
                        pygame.draw.circle(
                            screen, (255, 255, 255), pd_to_plot(re, im), 2
                        )
                        re, im = un_cayley(re, im)
                        pygame.draw.circle(
                            screen, (255, 255, 255), uh_to_plot(re, im), 2
                        )
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                if event.button == 3:
                    clear()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            if event.type == pygame.VIDEORESIZE:
                set_display(*event.size)
                clear()

        pygame.display.flip()


run_realtime()