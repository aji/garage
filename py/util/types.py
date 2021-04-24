from typing import TypeVar, NamedTuple
import re, ast
from py.util.math import clamp


class RGB8(NamedTuple):
    r: int
    g: int
    b: int

    @staticmethod
    def parse(s: str):
        s = s.lower()

        def rgb(r, g, b):
            return RGB8(
                clamp(0, 255, r),
                clamp(0, 255, g),
                clamp(0, 255, b),
            )

        try:
            m = ast.parse(s, mode="eval")
            if (
                isinstance(m, ast.Expression)
                and isinstance(m.body, ast.Call)
                and isinstance(m.body.func, ast.Name)
                and m.body.func.id == "rgb"
                and len(m.body.args) == 3
                and isinstance(m.body.args[0], ast.Num)
                and isinstance(m.body.args[1], ast.Num)
                and isinstance(m.body.args[2], ast.Num)
            ):
                return rgb(*(x.n for x in m.body.args))
        except SyntaxError:
            pass

        m = re.match(r"#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$", s)
        if m is not None:
            return rgb(
                int(m.group(1), base=16),
                int(m.group(2), base=16),
                int(m.group(3), base=16),
            )

        m = re.match(r"#([0-9a-f])([0-9a-f])([0-9a-f])$", s)
        if m is not None:
            return rgb(
                int(m.group(1), base=16) * 0x11,
                int(m.group(2), base=16) * 0x11,
                int(m.group(3), base=16) * 0x11,
            )

        raise ValueError(s)

    def __repr__(self) -> str:
        return f"RGB8({self.r}, {self.g}, {self.b})"

    def __str__(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"


class Size2D(NamedTuple):
    w: int
    h: int

    @staticmethod
    def parse(s: str):
        fields = s.split("x")
        if len(fields) != 2:
            raise ValueError(f"{repr(s)} not in WxH format")
        return Size2D(int(fields[0]), int(fields[1]))

    def __repr__(self) -> str:
        return f"Size2D({self.w}x{self.h})"

    def __str__(self) -> str:
        return f"{self.w}x{self.h}"


Size2D._720p = Size2D(1280, 720)
Size2D._1080p = Size2D(1920, 1080)