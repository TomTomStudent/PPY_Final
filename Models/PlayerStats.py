class PlayerStats(object):
    def __init__(self, rk, player, pos, age, team, g, gs, mp, fg, fga, fg_pct, three_p, three_pa, three_pct, two_p, two_pa, two_pct, efg_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts):
        self.rk = rk
        self.player = player
        self.pos = pos
        self.age = age
        self.team = team
        self.g = g
        self.gs = gs
        self.mp = mp
        self.fg = fg
        self.fga = fga
        self.fg_pct = fg_pct
        self.three_p = three_p
        self.three_pa = three_pa
        self.three_pct = three_pct
        self.two_p = two_p
        self.two_pa = two_pa
        self.two_pct = two_pct
        self.efg_pct = efg_pct
        self.ft = ft
        self.fta = fta
        self.ft_pct = ft_pct
        self.orb = orb
        self.drb = drb
        self.trb = trb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.tov = tov
        self.pf = pf
        self.pts = pts

    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
