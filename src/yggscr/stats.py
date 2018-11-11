# -*- coding: utf-8 -*-

import time


class Stats():
    def __init__(self):
        self.first = {"time": None,
                      "up": None, "down": None}
        self.last = {"time": None,
                     "up": None, "down": None}

    def upd_speed(self):
        GiB = 1024*1024
        ctime = time.time()
        if self.last["time"] is None:
            i_up = i_down = "?"
        else:
            i_up = round(GiB*(self.up-self.last["up"])/(
                ctime-self.last["time"]))
            i_down = round(GiB*(self.down-self.last["down"])/(
                ctime-self.last["time"]))
        self.last = {"time": ctime, "up": self.up, "down": self.down}
        if self.first["time"] is None:
            self.first = {
                "time": time.time(),
                "up": self.up,
                "down": self.down
            }
            m_up = m_down = "?"
        else:
            m_up = round(GiB*(self.up-self.first["up"])/(
                ctime-self.first["time"]))
            m_down = round(GiB*(self.down-self.first["down"])/(
                ctime-self.first["time"]))
        return i_up, m_up, i_down, m_down

    # Will only work for ratio above 1 but makes the search more robust
    # Note that website is inconsistent (TiB vs TB, GiB vs GB)
    def add(self, vals):
        self.down, self.up = sorted(
            float(e[0]) if e[1] == 'G' else float(e[0]) * 1024
            for e in vals)
        self.i_up, self.m_up, self.i_down, self.m_down = self.upd_speed()
        self.ratio = round(self.up/self.down, 4)
