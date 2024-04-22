import pygame

local_ip = ""

is_running = False
has_connection = False
last_message = ""

exit_button = None
header_background = None


def gui(on_close=None):
    global is_running
    is_open = True
    pygame.init()
    pygame.display.set_caption("pablet")

    screen = pygame.display.set_mode((300, 300), pygame.NOFRAME)

    def draw_header():
        global exit_button, header_background
        mouse_pos = pygame.mouse.get_pos()

        header_background = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 300, 50))
        pygame.draw.line(screen, (255, 255, 255), (0, 50), (300, 50), 1)

        font = pygame.font.Font(None, 36)
        text = font.render("pablet", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        exit_button_color = (10, 10, 10)

        if exit_button and exit_button.collidepoint(mouse_pos):
            exit_button_color = (50, 50, 50)

        # Draw close button
        exit_button = pygame.draw.rect(
            screen, exit_button_color, (265, 10, 30, 30), border_radius=5
        )
        pygame.draw.line(screen, (255, 255, 255), (275, 20), (285, 30), 4)
        pygame.draw.line(screen, (255, 255, 255), (275, 30), (285, 20), 4)

    def draw_ip():
        global local_ip, is_running
        font = pygame.font.Font(None, 24)
        ip_text = font.render(f"IP: {local_ip}", True, (255, 255, 255))

        if is_running:
            running_text = font.render("running", True, (0, 255, 0))
            screen.blit(running_text, (230, 60))
        else:
            running_text = font.render("not running", True, (255, 0, 0))
            screen.blit(running_text, (200, 60))

        screen.blit(ip_text, (10, 60))

    def draw_connected():
        global has_connection
        font = pygame.font.Font(None, 24)
        if has_connection:
            text = font.render("connected", True, (0, 255, 0))
        else:
            text = font.render(f"not connected", True, (255, 0, 0))

        screen.blit(text, (10, 85))

    def draw_last_message():
        global last_message
        font = pygame.font.Font(None, 24)
        text = font.render(last_message, True, (255, 255, 255))

        # Automatically center the text
        text_rect = text.get_rect(center=(150, 175))
        screen.blit(text, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button.collidepoint(event.pos):
                        pygame.quit()
                        is_running = False
                        if on_close:
                            on_close()
                        quit()

        screen.fill((0, 0, 0))

        draw_header()
        draw_ip()
        draw_connected()
        draw_last_message()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    gui()
