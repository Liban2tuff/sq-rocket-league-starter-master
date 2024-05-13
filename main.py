# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.intent is not None:
            return
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1 > d2
        
        # if we are in front of the ball, retreat
        if is_in_front_of_ball:
            self.set_intent(goto(self.friend_goal.location))
            return
        # self.set_intent(short_shot(self.foe_goal.location))
        
        
        
        targets = {
            'at_opponents_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self, targets)
        
        avaliable_boosts = [boost for boost in self.boosts if boost.large and boost.active]

        if len(avaliable_boosts) > 0 and self.me.boost < 20:
            self.set_intent(goto(avaliable_boosts[0].location))
            print('going for boost', avaliable_boosts[0].index)
            return
        
        if len(hits['at_opponents_goal']) > 0:
            self.set_intent(hits["at_opponents_goal"][0])
            print('at their goal')
            return
        if len(hits["away_from_our_net"]) > 0:
            print("away from our goal")
            self.set_intent(hits['away_from_our_net'][0])
            return
        