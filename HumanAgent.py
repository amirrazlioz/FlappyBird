import random
from Action import Action

class HumanAgent:
    def __init__(self):
        self.q_table = {} # כאן יישמר הידע שיילמד

    #def get_action(self, state):
        # כרגע החלטה אקראית, בהמשך: החלטה לפי המדיניות המיטבית
    #    return Action.FLAP if random.random() > 0.9 else Action.IDLE
    
    def get_action(self, state):
        # שנה ל-IDLE כדי לראות שהמשולש באמת נופל כשלא עושים כלום
        return Action.IDLE

    def update_knowledge(self, state, action, reward, next_state):
        # כאן תיושם משוואת בלמן בעתיד
        pass