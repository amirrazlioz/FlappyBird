import pygame
import random
from State import State
from Action import Action

# --- מחלקות ה-Sprite ---
class AgentSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((34, 24), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 255, 255), [(0, 0), (34, 12), (0, 24)])
        self.rect = self.image.get_rect(center=(50, 300))
        self.velocity = 0

    def update(self):
        # 1. כוח משיכה - תמיד מוסיף (חיובי) כדי למשוך למטה
        self.velocity += 0.25
        
        # 2. עדכון המיקום לפי המהירות
        self.rect.y += int(self.velocity)
        
        # 3. חסימה לרצפה
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.velocity = 0
            
        # 4. חסימה לתקרה - חשוב לא לאפס כאן למהירות שלילית!
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0.5 # נותן דחיפה קלה למטה כדי שלא יידבק

    def flap(self):
        # קפיצה - מהירות שלילית חדה שמושכת למעלה
        self.velocity = -8 # הגדלתי מעט ל-8 כדי שתהיה קפיצה מורגשת יותר מול המשיכה

class PipeSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top):
        super().__init__()
        self.image = pygame.Surface((50, 600), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 255), (0, 0, 50, 600), 2)
        if is_top:
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.rect = self.image.get_rect(midtop=(x, y + 160)) # 160 = Gap

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

# --- מחלקת הסביבה ---
class Environment:
    def __init__(self):
        self.bird = AgentSprite()
        self.pipes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.bird)
        self.score = 0  
        self.spawn_timer = 0

    def get_state(self):
        upcoming_pipes = [p for p in self.pipes if p.rect.right > self.bird.rect.left]
        if not upcoming_pipes:
            return State(400, 0, self.bird.velocity)
        
        target_pipe = upcoming_pipes[0]
        dist_x = target_pipe.rect.left - self.bird.rect.right
        dist_y = target_pipe.rect.centery - self.bird.rect.centery
        return State(dist_x, dist_y, self.bird.velocity)

    def step(self, action):
        if action == Action.FLAP:
            self.bird.flap()

        # יצירת צינורות כל 1.5 שניות בערך
        self.spawn_timer += 1
        if self.spawn_timer > 90:
            ry = random.randint(100, 400)
            p_top = PipeSprite(450, ry, True)
            p_bottom = PipeSprite(450, ry, False)
            self.pipes.add(p_top, p_bottom)
            self.all_sprites.add(p_top, p_bottom)
            self.spawn_timer = 0

        # --- לוגיקת עדכון הניקוד ---
        for pipe in self.pipes:
            # בודקים אם הציפור עברה את הצינור ושהוא עוד לא נספר
            if pipe.rect.right < self.bird.rect.left and not hasattr(pipe, 'passed'):
                pipe.passed = True # סימון שהצינור כבר נספר
                self.score += 1 

        self.all_sprites.update()
        
        # בדיקת פסילה
        done = pygame.sprite.spritecollideany(self.bird, self.pipes) or self.bird.rect.bottom >= 600
        
        # חישוב ה-Reward לסוכן
        if done:
            reward = -100
        else:
            reward = 0.1
            # בונוס לסוכן אם הוא עבר צינור בפריים הזה
            if any(hasattr(p, 'passed') and not hasattr(p, 'rewarded') for p in self.pipes):
                for p in self.pipes:
                    if hasattr(p, 'passed'): p.rewarded = True
                reward = 10 
            
        return self.get_state(), reward, done