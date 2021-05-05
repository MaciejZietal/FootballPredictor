# -*- coding: utf-8 -*-

class Club():
    def __init__(self, name, points=1000):
        self.name = name
        self.points = points
        
    def update_points(self, opponent, homeresult, awayresult):
        homepredict = 1 / (1 + 10 ** (-(self.points - opponent.points + 100)/600))        
        awaypredict = 1 / (1 + 10 ** (-(opponent.points - self.points - 100)/600))
        
        self.points = self.points + 32 * (homeresult - homepredict)
        opponent.points = opponent.points + 32 * (awayresult - awaypredict)