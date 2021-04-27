from typing import NamedTuple, NewType, Callable
import argparse
import mido
import sys
import os
from py.midi.lib import reader
from py.util.types import RGB8, Size2D


class Graphics(object):
    pass


class Song(object):
    def __init__(self, mido_file):
        self.mido = mido_file
        self.notes = list(reader.all_notes(self.mido))


Us = NewType("Us", int)
LayerRenderer = Callable[[Graphics, Us, Us, Us], None]
LayerFactory = Callable[[Song], LayerRenderer]


class Layer(object):
    def __init__(self, label, factory):
        self._label = label
        self._factory = factory

    def __str__(self):
        return self._label

    def __repr__(self):
        return f"Layer({self._label})"


def layer_bars(maj=None, min=None, on=None):
    def factory(song):
        def renderer(self, g: Graphics, t0: Us, t1: Us, t: Us):
            # do something with the tempo map
            pass

        return renderer

    return Layer(f"bars(maj={maj}, min={min}, on={on})", factory)


def layer_drums(track, off=RGB8(40, 40, 40), on=RGB8(255, 255, 255)):
    def factory(song):
        def renderer(self, g: Graphics, t0: Us, t1: Us, t: Us):
            # do something with the drums map
            pass

        return renderer

    return Layer(f"drums(track={track}, off={off}, on={on})", factory)


def layer_mono(track, color=None, on=RGB8(255, 255, 255), glide=0):
    def factory(song):
        def renderer(self, g: Graphics, t0: Us, t1: Us, t: Us):
            pass

        return renderer

    return Layer(f"mono(track={track}, color={color}, on={on}, glide={glide})", factory)


def layer_poly(track, color=None, on=RGB8(255, 255, 255)):
    def factory(song):
        def renderer(self, g: Graphics, t0: Us, t1: Us, t: Us):
            pass

        return renderer

    return Layer(f"poly(track={track}, color={color}, on={on})", factory)


def parse_layer(s):
    return eval(
        s,
        {
            "bars": layer_bars,
            "drums": layer_drums,
            "mono": layer_mono,
            "poly": layer_poly,
            "rgb": RGB8,
        },
    )


parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
parser.add_argument(
    "--size",
    help="Specify the size of the output images",
    type=Size2D.parse,
    default=Size2D._1080p,
)
parser.add_argument(
    "--input", help="Specify the MIDI input file", required=True, type=str
)
parser.add_argument(
    "--output-dir",
    help="Specify the output directory for images. Will be created if it doesn't exist",
    required=True,
    type=str,
)
parser.add_argument(
    "--output-prefix",
    help="Filename prefix for generated images, before the frame number.",
    default="frame",
    type=str,
)
parser.add_argument(
    "--output-suffix",
    help="Filename suffix for generated images, including the extension.",
    default=".png",
    type=str,
)
parser.add_argument(
    "--layer",
    help="Add a layer to the output",
    action="append",
    default=[],
    type=parse_layer,
)
parser.add_argument(
    "--time-range",
    help="Time range, in seconds, to display",
    default=10,
    type=int,
)
parser.add_argument(
    "--fps",
    help="Frames per second",
    default=60,
    type=int,
)


def main(args):
    song = Song(mido.MidiFile(args.input))

    fmt = os.path.join(args.output_dir, f"{args.output_prefix}%06d{args.output_suffix}")
    os.makedirs(args.output_dir, exist_ok=True)

    frame = 0
    while True:
        frame += 1


main(parser.parse_args())
