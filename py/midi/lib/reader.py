from typing import List, Tuple, Iterator, NamedTuple

import mido


class Event(NamedTuple):
    t: int
    trk: int
    msg: mido.Message


class Note(NamedTuple):
    t0: int
    t1: int
    trk: int
    v: int


def all_events(f: mido.MidiFile) -> Iterator[Event]:
    times = [0 for i in range(len(f.tracks))]
    cursors = [0 for i in range(len(f.tracks))]

    while True:
        ev0 = None
        trk0 = None

        for trk, cursor in enumerate(cursors):
            if len(f.tracks[trk]) <= cursor:
                continue
            ev = f.tracks[trk][cursor]
            if trk0 is None or times[trk] + ev.time < times[trk0] + ev0.time:
                trk0 = trk
                ev0 = ev

        if trk0 is None:
            break
        else:
            times[trk0] += ev0.time
            cursors[trk0] += 1
            yield Event(times[trk0], trk0, ev0)


def all_notes(f: mido.MidiFile) -> Iterator[Note]:
    tempo_since_us = 0
    tempo_since_ticks = 0
    tempo_us_per_beat = 0
    last_event = None
    held = dict()

    def us(ticks):
        beats, rem_ticks = divmod(ticks - tempo_since_ticks, f.ticks_per_beat)
        return (
            tempo_since_us
            + beats * tempo_us_per_beat
            + int(rem_ticks * tempo_us_per_beat / f.ticks_per_beat)
        )

    for ev in all_events(f):
        if last_event is not None and ev.t < last_event.t:
            raise Exception("event times must be non-decreasing")

        m = ev.msg

        if m.type == "set_tempo":
            tempo_since_us = us(ev.t)
            tempo_since_ticks = ev.t
            tempo_us_per_beat = m.tempo

        elif m.type == "note_off" or (m.type == "note_on" and m.velocity == 0):
            k = (ev.trk, m.channel, m.note)
            if k in held:
                note = held[k]._replace(t1=us(ev.t))
                del held[k]
                yield note

        elif m.type == "note_on":
            k = (ev.trk, m.channel, m.note)
            if k not in held:
                held[k] = Note(us(ev.t), 0, ev.trk, m.note)

        last_event = ev