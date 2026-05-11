import pygame
from HumanAgent import HumanAgent 
from Action import Action
from Environment import Environment
from Graphics import Graphics

class FlappyGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Flappy Bird AI")
        
        self.state = "MENU"
        self.player_name = ""
        self.high_scores = {}  # מילון לשמירת התוצאות
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.env = Environment()
        self.agent = HumanAgent()
        self.graphics = Graphics(self.screen)
        self.clock = pygame.time.Clock()

    def draw_menu(self):
        self.screen.fill((30, 30, 60))
        title = self.font.render("ENTER NAME:", True, (255, 255, 255))
        # הצגת השם תוך כדי הקלדה
        name_display = self.font.render(self.player_name + "_", True, (0, 255, 150))
        self.screen.blit(title, (100, 200))
        self.screen.blit(name_display, (100, 250))
        pygame.display.flip()

    def draw_leaderboard(self):
        self.screen.fill((20, 20, 40))
        title = self.font.render("--- TOP 10 SCORES ---", True, (255, 215, 0))
        self.screen.blit(title, (100, 50))

        # מיון המילון לפי הניקוד מהגבוה לנמוך
        sorted_scores = sorted(self.high_scores.items(), key=lambda x: x[1], reverse=True)
        
        y_offset = 120
        # לולאה להצגת עד 10 תוצאות
        for name, score in sorted_scores[:10]:
            score_txt = self.font.render(f"{name}: {score}", True, (255, 255, 255))
            self.screen.blit(score_txt, (100, y_offset))
            y_offset += 40
            
        hint = self.font.render("Press SPACE to play again", True, (100, 100, 100))
        self.screen.blit(hint, (80, 500))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            if self.state == "MENU":
                self.draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.player_name != "":
                            self.state = "GAME"
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if len(self.player_name) < 10:
                                self.player_name += event.unicode

            elif self.state == "GAME":
                action = Action.IDLE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE: action = Action.FLAP

                # קבלת החלטה מהסוכן במידה ולא נלחץ רווח
                if action == Action.IDLE:
                    action = self.agent.get_action(self.env.get_state())
                
                _, _, done = self.env.step(action)
                
                # עדכון תצוגת המשחק
                self.graphics.draw_background()
                self.env.all_sprites.draw(self.screen)
                self.graphics.draw_telemetry(self.env.get_state(), self.env.score, self.player_name)
                pygame.display.flip()
                self.clock.tick(60)

                if done:
                # אנחנו שומרים את הניקוד במילון גם אם הוא 0
                    # אם לשחקן כבר יש שיא גבוה יותר, נשמור את הגבוה מביניהם
                    current_best = self.high_scores.get(self.player_name, 0)
                    self.high_scores[self.player_name] = max(current_best, self.env.score)
                    
                    # print(f"Player: {self.player_name} | Final Score: {self.env.score}") 
                    self.state = "LEADERBOARD"

            elif self.state == "LEADERBOARD":
                self.draw_leaderboard()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.env = Environment() # אתחול הסביבה למשחק חדש
                            self.state = "MENU"

        pygame.quit()

if __name__ == "__main__":
    game = FlappyGame()
    game.run()