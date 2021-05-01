import sys
import time
import math
import os

import pygame
from pygame.locals import *

from py.util.math import lerp_unlerp

width, height = (1920, 1080)
screen = pygame.display.set_mode((width, height))

uh_plot_rect = pygame.Rect(100, 135, 810, 810)
pd_plot_rect = pygame.Rect(1010, 135, 810, 810)

uh_to_plot_re, uh_fr_plot_x = lerp_unlerp(-3, uh_plot_rect.left, 3, uh_plot_rect.right)
uh_to_plot_im, uh_fr_plot_y = lerp_unlerp(0, uh_plot_rect.bottom, 6, uh_plot_rect.top)

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
    drawing = False

    t_start = time.monotonic()
    t_last = t_start

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

        unit_circle = pygame.Rect(
            (pd_to_plot_re(-1), pd_to_plot_im(1)),
            (
                pd_to_plot_re(1) - pd_to_plot_re(-1),
                pd_to_plot_im(-1) - pd_to_plot_im(1),
            ),
        )

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

        pygame.display.flip()


run_realtime()