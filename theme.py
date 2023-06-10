from color import Color

class Theme:
    def __init__(self,light_bg,dark_bg,light_trace,dark_trace,light_moves,dark_moves) -> None:
        self.square_color=Color(light_bg,dark_bg)
        self.trace_color=Color(light_trace,dark_trace)
        self.moves_color=Color(light_moves,dark_moves)