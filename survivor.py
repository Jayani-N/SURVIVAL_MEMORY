import os
# FORCE WINDOWS TO SHOW WINDOW FRAMES CORRECTLY
os.environ['SDL_VIDEO_WINDOW_POS'] = "center"
import pygame
import random
import sys
import math
import array

pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2)
except Exception:
    pass 

# =========================
# CONFIG & DISPLAY SETUP
# =========================
WIDTH, HEIGHT = 1100, 660
DISPLAY_TIME_START = 10 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Survival")
clock = pygame.time.Clock()

# =========================
# LOAD BACKGROUND
# =========================
try:
    bg = pygame.image.load("background.jfif")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    has_bg = True
except pygame.error:
    has_bg = False

# =========================
# BEAUTIFUL TYPOGRAPHY
# =========================
TITLE_FONT = pygame.font.SysFont("Trebuchet MS", 56, bold=True)
ROUND_FONT = pygame.font.SysFont("Trebuchet MS", 42, bold=True)
SUB_FONT = pygame.font.SysFont("Georgia", 22, italic=True)
CARD_FONT = pygame.font.SysFont("Trebuchet MS", 24, bold=True)
QUESTION_FONT = pygame.font.SysFont("Georgia", 25, bold=False)  
INPUT_FONT = pygame.font.SysFont("Consolas", 28) # Restored missing font variable here!
MENU_BTN_FONT = pygame.font.SysFont("Trebuchet MS", 26, bold=True)

# =========================
# COLORS
# =========================
WHITE = (255, 255, 255)
CYAN = (0, 255, 220)
GOLD = (255, 210, 0)
RED = (255, 70, 70)
MENU_BOX_BG = (15, 22, 32, 235)

# =========================
# SOUND & MUSIC GENERATOR
# =========================
def generate_tone(frequency, duration, volume=0.1, type='sine'):
    try:
        num_samples = int(duration * 22050)
        buf = array.array('h', [0] * num_samples)
        for i in range(num_samples):
            t = float(i) / 22050.0
            if type == 'triangle':
                val = 2.0 * abs(2.0 * (t * frequency - math.floor(t * frequency + 0.5))) - 1.0
            else:
                val = math.sin(2.0 * math.pi * frequency * t)
            buf[i] = int(volume * 32767.0 * val)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None

sound_tick = generate_tone(600, 0.05, volume=0.12)
sound_warning = generate_tone(350, 0.12, volume=0.2)
sound_correct = generate_tone(880, 0.22, volume=0.18)
sound_wrong = generate_tone(160, 0.35, volume=0.25)

def play_procedural_music():
    try:
        notes = [110, 130, 146, 165]
        buffer_list = []
        for note in notes:
            num_samples = int(0.8 * 22050)
            for i in range(num_samples):
                t = float(i) / 22050.0
                val = math.sin(2.0 * math.pi * note * t) * 0.04
                buffer_list.append(int(val * 32767.0))
        
        music_sound = pygame.mixer.Sound(buffer=array.array('h', buffer_list))
        music_sound.play(loops=-1)
        return music_sound
    except Exception:
        return None

bg_music_channel = play_procedural_music()
music_enabled = True

# =========================
# ITEM POOL DATA
# =========================
ITEM_POOL = [
    {"name": "Key", "situation": "the escape door lock is jammed solid"},
    {"name": "Fire Extinguisher", "situation": "an electrical fire breaks out blocking the room"},
    {"name": "Rope", "situation": "you must drop down safely through a broken floor gap"},
    {"name": "Flashlight", "situation": "a complete blackout leaves the area pitch black"},
    {"name": "Hammer", "situation": "a fragile barricaded window can be broken open"},
    {"name": "Box", "situation": "you need to block a leaking pipe venting toxic air"},
    {"name": "Battery", "situation": "your backup life support monitor loses power"},
    {"name": "Radio", "situation": "you need to broadcast coordinates to a rescue unit"},
    {"name": "Ladder", "situation": "an open maintenance manhole is high up in the ceiling"},
    {"name": "Screwdriver", "situation": "the primary control box panel needs to be opened"},
    {"name": "Medkit", "situation": "a sudden structural collapse causes a deep cut"},
    {"name": "Knife", "situation": "thick tangled cables are blocking the power lever"},
    {"name": "Map", "situation": "the building blueprint paths become unrecognizable"},
    {"name": "Crowbar", "situation": "a heavy steel ventilation hatch is stuck tightly shut"}
]

# =========================
# STATE SYSTEM ENGINE
# =========================
GAME_STATE_MENU = "MENU"
GAME_STATE_HOW_TO = "HOW_TO"
GAME_STATE_PLAYING = "PLAYING"
current_state = GAME_STATE_MENU

round_number = 1
showing_objects = True
wrong_answer_delay = False 

start_time = pygame.time.get_ticks()
last_ticked_second = -1
input_text = ""
score = 0
current_round_data = {}

def generate_dynamic_round(lvl):
    if lvl == 1:
        total_items = 6
    elif lvl == 2:
        total_items = 8
    else:
        total_items = min(12, 6 + (lvl - 1))

    selected = random.sample(ITEM_POOL, total_items)
    possible_solution_count = min(2, len(selected))
    solutions = random.sample(selected, possible_solution_count)

    situations_text = " or ".join([s['situation'] for s in solutions])
    scenario = f"What if {situations_text}?"

    return {
        "objects": [item["name"] for item in selected],
        "question": scenario,
        "correct_display": [item["name"] for item in solutions], 
        "correct": [item["name"].lower() for item in solutions],
        "cols": 4 if total_items > 6 else 3
    }

def start_new_game():
    global round_number, score, showing_objects, wrong_answer_delay, input_text, start_time, last_ticked_second, current_round_data, current_state
    round_number = 1
    score = 0
    input_text = ""
    wrong_answer_delay = False
    showing_objects = True
    last_ticked_second = -1
    current_round_data = generate_dynamic_round(round_number)
    start_time = pygame.time.get_ticks()
    current_state = GAME_STATE_PLAYING

# =========================
# TEXT WORD WRAPPER
# =========================
def render_wrapped_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        if font.size(test_line)[0] > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return [font.render(line, True, color) for line in lines]

# =========================
# REUSABLE GRAPHICS DRAWERS
# =========================
def normalize(text):
    return text.lower().replace(" ", "").strip()

def draw_background():
    if has_bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill((20, 22, 28))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(140)
    overlay.fill((10, 12, 18))
    screen.blit(overlay, (0, 0))

def draw_game_header():
    round_txt = ROUND_FONT.render(f"ROUND {round_number}", True, GOLD)
    screen.blit(round_txt, (WIDTH // 2 - round_txt.get_width() // 2, 25))

# =========================
# SCREEN - HOME MENU & HOW TO PLAY
# =========================
def draw_home_menu():
    draw_background()
    
    title = TITLE_FONT.render("MEMORY SURVIVAL", True, CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 110))
    
    tagline = SUB_FONT.render("Test your recall thresholds under environmental pressure.", True, WHITE)
    screen.blit(tagline, (WIDTH // 2 - tagline.get_width() // 2, 185))

    btn_start = pygame.Rect((WIDTH - 280) // 2, 270, 280, 55)
    btn_how = pygame.Rect((WIDTH - 280) // 2, 350, 280, 55)
    btn_music = pygame.Rect((WIDTH - 280) // 2, 430, 280, 55)

    for btn in [btn_start, btn_how, btn_music]:
        btn_surf = pygame.Surface((btn.width, btn.height), pygame.SRCALPHA)
        btn_surf.fill(MENU_BOX_BG)
        screen.blit(btn_surf, (btn.x, btn.y))
        pygame.draw.rect(screen, CYAN, btn, 2, border_radius=6)

    t1 = MENU_BTN_FONT.render("START GAME", True, WHITE)
    t2 = MENU_BTN_FONT.render("HOW TO PLAY", True, WHITE)
    m_status = "ON" if music_enabled else "OFF"
    t3 = MENU_BTN_FONT.render(f"MUSIC: {m_status}", True, GOLD if music_enabled else RED)

    screen.blit(t1, (btn_start.x + (btn_start.width - t1.get_width()) // 2, btn_start.y + (btn_start.height - t1.get_height()) // 2))
    screen.blit(t2, (btn_how.x + (btn_how.width - t2.get_width()) // 2, btn_how.y + (btn_how.height - t2.get_height()) // 2))
    screen.blit(t3, (btn_music.x + (btn_music.width - t3.get_width()) // 2, btn_music.y + (btn_music.height - t3.get_height()) // 2))

    return btn_start, btn_how, btn_music

def draw_how_to_play():
    draw_background()
    
    panel_width = 840
    panel = pygame.Rect((WIDTH - panel_width) // 2, 85, panel_width, 470)
    panel_surf = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    panel_surf.fill(MENU_BOX_BG)
    screen.blit(panel_surf, (panel.x, panel.y))
    pygame.draw.rect(screen, CYAN, panel, 2, border_radius=12)

    title = MENU_BTN_FONT.render("INSTRUCTIONS & CRITICAL OPERATING MANUAL", True, CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 115))

    rules = [
        "1. Every round reveals a grid layout of tool cards.",
        "2. Memorize all item locations before your timer reaches 00.",
        "3. Once time expires, an unexpected emergency scenario prompts.",
        "4. Input EXACTLY ONE correct tool name that matches the crisis.",
        "5. The system console completely ignores capitals and spaces.",
        "6. Surviving a level advances you deeper into faster rounds."
    ]

    y_offset = 180
    max_text_width = panel_width - 80 

    for rule in rules:
        wrapped_lines = render_wrapped_text(rule, QUESTION_FONT, WHITE, max_text_width)
        for line in wrapped_lines:
            screen.blit(line, (panel.x + 40, y_offset))
            y_offset += 34
        y_offset += 8 

    btn_back = pygame.Rect((WIDTH - 200) // 2, 490, 200, 48)
    pygame.draw.rect(screen, GOLD, btn_back, 2, border_radius=6)
    b_txt = MENU_BTN_FONT.render("BACK", True, GOLD)
    screen.blit(b_txt, (btn_back.x + (btn_back.width - b_txt.get_width()) // 2, btn_back.y + (btn_back.height - b_txt.get_height()) // 2))

    return btn_back

# =========================
# SCREEN - GAME LAYOUTS
# =========================
def draw_objects():
    global last_ticked_second, showing_objects
    draw_background()
    draw_game_header()

    level_time_allotted = max(5, DISPLAY_TIME_START - (round_number // 2))
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = max(0, level_time_allotted - elapsed)

    if elapsed != last_ticked_second:
        if remaining > 0:
            try:
                if remaining <= 3:
                    if sound_warning: sound_warning.play()
                else:
                    if sound_tick: sound_tick.play()
            except Exception:
                pass
        last_ticked_second = elapsed

    timer_lbl = SUB_FONT.render("TIME REMAINING", True, WHITE)
    screen.blit(timer_lbl, (WIDTH - 190, 20))
    timer_color = RED if remaining <= 3 else GOLD
    timer_val = TITLE_FONT.render(f"{remaining:02d}", True, timer_color)
    screen.blit(timer_val, (WIDTH - 110, 45))

    objects = current_round_data["objects"]
    cols = current_round_data["cols"]
    
    card_w = 240 if cols == 4 else 280
    card_h = 110 if len(objects) > 6 else 130
    gap_x, gap_y = 25, 20
    
    start_x = (WIDTH - (cols * card_w + (cols - 1) * gap_x)) // 2
    start_y = 160

    for i, obj in enumerate(objects):
        c = i % cols
        r = i // cols
        x = start_x + c * (card_w + gap_x)
        y = start_y + r * (card_h + gap_y)

        tile_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        tile_surf.fill((10, 18, 28, 195))
        screen.blit(tile_surf, (x, y))
        pygame.draw.rect(screen, CYAN, (x, y, card_w, card_h), 2, border_radius=10)

        text = CARD_FONT.render(obj, True, WHITE)
        screen.blit(text, (x + (card_w - text.get_width()) // 2, y + (card_h - text.get_height()) // 2))

    if remaining == 0:
        showing_objects = False

def draw_question():
    draw_background()
    draw_game_header()

    wrapped_surfaces = render_wrapped_text(current_round_data["question"], QUESTION_FONT, WHITE, WIDTH - 100)
    y_offset = 180
    for text_surf in wrapped_surfaces:
        screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y_offset))
        y_offset += 40

    input_box = pygame.Rect((WIDTH - 600) // 2, 360, 600, 60)
    box_bg = pygame.Surface((600, 60), pygame.SRCALPHA)
    box_bg.fill((10, 18, 28, 210))
    screen.blit(box_bg, (input_box.x, input_box.y))
    
    box_color = RED if wrong_answer_delay else CYAN
    pygame.draw.rect(screen, box_color, input_box, 2, border_radius=8)

    user_text = INPUT_FONT.render(input_text, True, RED if wrong_answer_delay else GOLD)
    screen.blit(user_text, (input_box.x + 20, input_box.y + (input_box.height - user_text.get_height()) // 2))
    
    if wrong_answer_delay:
        ans_str = " or ".join(current_round_data["correct_display"])
        err_msg = QUESTION_FONT.render(f"WRONG! Valid choices were: {ans_str}", True, RED)
        screen.blit(err_msg, (WIDTH // 2 - err_msg.get_width() // 2, 455))
        
        continue_lbl = SUB_FONT.render("Press SPACEBAR to view final score summary evaluation", True, WHITE)
        screen.blit(continue_lbl, (WIDTH // 2 - continue_lbl.get_width() // 2, 515))
    else:
        hint = SUB_FONT.render("Type 1 correct item name from memory and press Enter", True, WHITE)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 455))

# =========================
# GAME MECHANICS EVALUATION
# =========================
def check_answer():
    global round_number, input_text, score, showing_objects, start_time, last_ticked_second, current_round_data, wrong_answer_delay

    user_val = normalize(input_text)
    valid_answers = current_round_data["correct"]

    if user_val in valid_answers:
        try:
            if sound_correct: sound_correct.play()
        except Exception: pass
        score += 1
        round_number += 1
        input_text = ""
        current_round_data = generate_dynamic_round(round_number)
        showing_objects = True
        last_ticked_second = -1
        start_time = pygame.time.get_ticks()
    else:
        try:
            if sound_wrong: sound_wrong.play()
        except Exception: pass
        wrong_answer_delay = True 

def end_screen():
    while True:
        draw_background()
        
        title = TITLE_FONT.render("GAME OVER", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))

        msg = QUESTION_FONT.render(f"Final Survival Score: {score} Rounds Passed", True, GOLD)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 10))
        
        restart_lbl = SUB_FONT.render("Press ENTER to return to Main Menu.", True, WHITE)
        screen.blit(restart_lbl, (WIDTH // 2 - restart_lbl.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    global current_state
                    current_state = GAME_STATE_MENU
                    return

# =========================
# CORE APPLICATION LOOP ENGINE
# =========================
running = True
while running:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == GAME_STATE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                b_start, b_how, b_music = draw_home_menu()
                if b_start.collidepoint(mx, my):
                    start_new_game()
                elif b_how.collidepoint(mx, my):
                    current_state = GAME_STATE_HOW_TO
                elif b_music.collidepoint(mx, my):
                    music_enabled = not music_enabled
                    try:
                        if music_enabled:
                            if bg_music_channel: bg_music_channel.play(loops=-1)
                        else:
                            pygame.mixer.stop()
                    except Exception:
                        pass

        elif current_state == GAME_STATE_HOW_TO:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                b_back = draw_how_to_play()
                if b_back.collidepoint(mx, my):
                    current_state = GAME_STATE_MENU

        elif current_state == GAME_STATE_PLAYING:
            if not showing_objects:
                if event.type == pygame.KEYDOWN:
                    if wrong_answer_delay:
                        if event.key == pygame.K_SPACE:
                            end_screen()
                    else:
                        if event.key == pygame.K_RETURN:
                            if input_text.strip() != "":
                                check_answer()
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if event.unicode.isprintable():
                                input_text += event.unicode

    if current_state == GAME_STATE_MENU:
        draw_home_menu()
    elif current_state == GAME_STATE_HOW_TO:
        draw_how_to_play()
    elif current_state == GAME_STATE_PLAYING:
        if showing_objects:
            draw_objects()
            level_time_allotted = max(5, DISPLAY_TIME_START - (round_number // 2))
            if (pygame.time.get_ticks() - start_time) > level_time_allotted * 1000:
                showing_objects = False
        else:
            draw_question()

    pygame.display.flip()

pygame.quit()
sys.exit()