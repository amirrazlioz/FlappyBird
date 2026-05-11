import pygame


class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Consolas", 18)

    def draw_background(self):
        self.screen.fill((5, 5, 15)) # BG הייטקי
        for x in range(0, 400, 40):
            pygame.draw.line(self.screen, (20, 20, 40), (x, 0), (x, 600))
        for y in range(0, 600, 40):
            pygame.draw.line(self.screen, (20, 20, 40), (0, y), (400, y))

    def draw_telemetry(self, state, score, player_name):
        # הצגת מרחקים (צבע ירוק הייטקי)
        txt = self.font.render(f"DIST_X: {state.dist_x} | DIST_Y: {state.dist_y}", True, (0, 255, 150))
        self.screen.blit(txt, (10, 10))

        # הצגת שם השחקן והניקוד (צבע לבן)
        # שים לב לשימוש ב-f-string כדי לחבר את השם והניקוד
        info_text = f"PLAYER: {player_name} | SCORE: {score}"
        score_surface = self.font.render(info_text, True, (255, 255, 255))
        
        # הצגה בשורה השנייה (גובה 40)
        self.screen.blit(score_surface, (10, 40))