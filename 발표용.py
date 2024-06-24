import pygame
import sys
import random
import time
import json

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collatz Conjecture Game")

# 색상 정의
colors = {"white": (255, 255, 255), "black": (0, 0, 0), "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 255, 0)}

# 폰트 설정
font_path = "DXHmchL-KSCpc-EUC-H.ttf"
font_sizes = [60, 36, 24, 150]

def load_fonts(path, sizes):
    fonts = {}
    for size in sizes:
        try:
            fonts[size] = pygame.font.Font(path, size)
        except FileNotFoundError:
            print(f"Font file not found: {path}")
            sys.exit()
    return fonts

fonts = load_fonts(font_path, font_sizes)

# 버튼버튼버튼
def create_button(rect, color, text, text_color):
    pygame.draw.rect(screen, color, rect)
    screen.blit(fonts[36].render(text, True, text_color), (rect.x + 20, rect.y + 10))

buttons = {
    "start": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100),
    "reset_all": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 100),
    "solo": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100),
    "vs_haon": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 100),
    "pause": pygame.Rect(screen_width - 200, screen_height - 100, 150, 50),
    "view_records": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100),
    "start_game": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 100),
    "resume": pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 100),
    "home": pygame.Rect(screen_width // 2 - 100, screen_height - 100, 200, 50),
    "reset_records": pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 100)
}

# 입력 상자
input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)

# 기록 저장
record_file, txt_record_file = "collatz_records.json", "collatz_records.txt"
records = {}
try:
    with open(record_file, "r") as f:
        records = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    records = {"SOLO": {str(i): float('inf') for i in range(2, 101)}, "VS HAON": {str(i): float('inf') for i in range(2, 101)}}

# 기록 초기화
def initialize_records():
    global records
    if "SOLO" not in records or not isinstance(records["SOLO"], dict):
        records["SOLO"] = {str(i): float('inf') for i in range(2, 101)}
    if "VS HAON" not in records or not isinstance(records["VS HAON"], dict):
        records["VS HAON"] = {str(i): float('inf') for i in range(2, 101)}

initialize_records()

# 콜라츠 추측 계산
def collatz_next(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

# 텍스트 그리는 함수
def draw_text(text, font, color, pos, center=True):
    text_surf = font.render(text, True, color)
    if center:
        pos = pos[0] - text_surf.get_width() // 2, pos[1]
    screen.blit(text_surf, pos)

# 게임 실행 화면
def draw_game_screen(target, current, mode, elapsed, input_text, feedback, penalty):
    screen.fill(colors["white"])
    draw_text(f"Target: {target}", fonts[60], colors["black"], (screen_width // 2, 150))
    draw_text(f"이전 숫자: {current}", fonts[36], colors["black"], (50, screen_height // 2), False)
    draw_text(f"모드: {mode}", fonts[36], colors["blue"], (50, 50), False)
    draw_text(f"시간: {elapsed:.2f}s", fonts[36], colors["red"], (screen_width - 200, 50), False)
    pygame.draw.rect(screen, colors["blue"], input_box, 2)
    draw_text(input_text, fonts[36], colors["black"], (input_box.x + 5, input_box.y + 5), False)
    if feedback:
        draw_text(feedback, fonts[150], colors["green"] if feedback == "O" else colors["red"], (screen_width // 2, screen_height // 2 - 150))
    if penalty:
        draw_text(penalty, fonts[36], colors["red"], (screen_width - 100, 100), False)
    create_button(buttons["pause"], colors["red"], "PAUSE", colors["white"])
    pygame.display.flip()

# 일시 정지 화면
def draw_pause_screen():
    screen.fill(colors["white"])
    create_button(buttons["resume"], colors["blue"], "RESUME", colors["white"])
    create_button(buttons["home"], colors["blue"], "HOME", colors["white"])
    pygame.display.flip()

# 결과 화면
def draw_result_screen(target, final_time, prev_record, mode, saved=False, admin_mode=False):
    screen.fill(colors["white"])
    if admin_mode and mode == "VS HAON":
        draw_text("기록 설정이 완료되었습니다", fonts[36], colors["black"], (screen_width // 2, 250))
    else:
        draw_text(f"결과: {final_time:.2f}s", fonts[60], colors["black"], (screen_width // 2, 150))
        draw_text(f"처음 숫자: {target}", fonts[36], colors["black"], (screen_width // 2, 250))
        if prev_record == float('inf'):
            record_text = "영광의 첫 번째 기록! 열심히 하세요!"
        elif final_time < prev_record:
            record_text = "하온이를 이기셨네요! 대단해요 ㄷㄷ" if mode == "VS HAON" else "신기록!"
            draw_text(f"이전 기록: {prev_record:.2f}s", fonts[36], colors["black"], (screen_width // 2, 350))
        else:
            record_text = "ㅉㅉ... 분발하세요!"
            draw_text(f"이전 기록: {prev_record:.2f}s", fonts[36], colors["black"], (screen_width // 2, 350))
        draw_text(record_text, fonts[36], colors["green"] if final_time < prev_record else colors["red"], (screen_width // 2, 450))
    create_button(buttons["home"], colors["blue"], "HOME", colors["white"])
    pygame.display.flip()

# 기록 보기 -> 스크롤 기능 추가
def draw_records_screen(mode, scroll_offset):
    screen.fill(colors["white"])
    draw_text("기록", fonts[36], colors["black"], (screen_width // 2, 50))
    y_offset = 150 - scroll_offset
    for number in range(2, 101):
        record = records[mode].get(str(number), float('inf'))
        color = colors["black"]
        draw_text(f"{number}: {record:.2f}s" if record != float('inf') else f"{number}: 기록 없음", fonts[24], color, (50, y_offset), False)
        y_offset += 30
    create_button(buttons["home"], colors["green"], "HOME", colors["white"])
    pygame.display.flip()

# 기록 텍스트 파일 저장
def save_records_to_txt():
    with open(txt_record_file, "w") as f:
        for mode in records:
            if isinstance(records[mode], dict):
                f.write(f"{mode} 모드 기록:\n")
                for number in range(2, 101):
                    record = records[mode].get(str(number), float('inf'))
                    f.write(f"{number}: {record:.2f}s\n" if record != float('inf') else f"{number}: 기록 없음\n")
                f.write("\n")

# 게임 시작 함수
def start_game(mode, target_number=None, admin_mode=False):
    target_number = target_number or random.randint(2, 100)
    current_number, input_text, feedback, penalty_feedback = target_number, '', '', ''
    start_time, feedback_start_time, penalty_start_time = time.time(), 0, 0
    paused, game_over = False, False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["pause"].collidepoint(event.pos):
                    paused = True
            elif event.type == pygame.KEYDOWN and not paused:
                if event.key == pygame.K_RETURN:
                    try:
                        next_number = int(input_text)
                        if next_number == collatz_next(current_number):
                            feedback = "O"
                            feedback_start_time = time.time()
                            current_number = next_number
                            if current_number == 1:
                                game_over = True
                        else:
                            feedback = "X"
                            feedback_start_time = time.time()
                            start_time -= 1
                            penalty_feedback = "+1.0s"
                            penalty_start_time = time.time()
                        input_text = ''
                    except ValueError:
                        input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        if paused:
            draw_pause_screen()
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons["resume"].collidepoint(event.pos):
                            paused = False
                        elif buttons["home"].collidepoint(event.pos):
                            return

        current_time = time.time()
        time_elapsed = current_time - start_time
        if feedback and current_time - feedback_start_time > 0.3:
            feedback = ''
        if penalty_feedback and current_time - penalty_start_time > 0.7:
            penalty_feedback = ''

        draw_game_screen(target_number, current_number, mode, time_elapsed, input_text, feedback, penalty_feedback)

    final_time = time.time() - start_time
    previous_record = records.get(mode, {}).get(str(target_number), float('inf'))
    record_saved = False
    if final_time < previous_record or admin_mode:
        records[mode][str(target_number)] = final_time
        with open(record_file, "w") as f:
            json.dump(records, f)
        record_saved = True
    save_records_to_txt()
    draw_result_screen(target_number, final_time, previous_record, mode, record_saved, admin_mode)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["home"].collidepoint(event.pos):
                    return

# VS HAON 모드에서 기록 설정 (관리자용)
def admin_set_record():
    password_input, input_active, reset_confirmed, input_text = '', False, False, ''
    while True:
        screen.fill(colors["white"])
        prompt_text = "비밀번호를 입력하세요:" if not reset_confirmed else "숫자를 선택하세요 (2-100):"
        draw_text(prompt_text, fonts[36], colors["black"], (screen_width // 2, screen_height // 4))
        pygame.draw.rect(screen, colors["blue"], input_box, 2)
        draw_text(password_input if not reset_confirmed else input_text, fonts[36], colors["black"], (input_box.x + 5, input_box.y + 5), False)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if not reset_confirmed:
                        if password_input == "haonispretty":
                            reset_confirmed = True
                            password_input = ''
                        else:
                            password_input = ''
                    else:
                        try:
                            target_number = int(input_text)
                            if 2 <= target_number <= 100:
                                start_game("VS HAON", target_number=target_number, admin_mode=True)
                                return
                        except ValueError:
                            input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    if not reset_confirmed:
                        password_input = password_input[:-1]
                    else:
                        input_text = input_text[:-1]
                else:
                    if not reset_confirmed:
                        password_input += event.unicode
                    else:
                        input_text += event.unicode

# 전체 기록 초기화
def reset_all_records():
    records.update({"SOLO": {str(i): float('inf') for i in range(2, 101)}})
    with open(record_file, "w") as f:
        json.dump(records, f)
    save_records_to_txt()

# 메인 루프
def main():
    mode, in_mode_selection, in_start_or_view_records, scroll_offset = None, False, False, 0

    while True:
        screen.fill(colors["white"])
        if mode is None:
            # 메인 화면
            draw_text("콜라츠의 음모", fonts[60], colors["black"], (screen_width // 2, screen_height // 4 - 30))
            create_button(buttons["start"], colors["blue"], "START", colors["white"])
            create_button(buttons["reset_all"], colors["red"], "전체 초기화", colors["white"])
        elif in_mode_selection:
            # 모드 선택 화면
            draw_text("모드를 선택하세요", fonts[36], colors["black"], (screen_width // 2, screen_height // 4))
            create_button(buttons["solo"], colors["green"], "SOLO", colors["white"])
            create_button(buttons["vs_haon"], colors["green"], "VS HAON", colors["white"])
        elif in_start_or_view_records:
            # 기록 보기 또는 게임 시작 화면
            draw_text("기록을 보거나 게임을 시작하세요", fonts[36], colors["black"], (screen_width // 2, screen_height // 4))
            create_button(buttons["view_records"], colors["green"], "기록 보기", colors["white"])
            create_button(buttons["start_game"], colors["green"], "게임 시작", colors["white"])
            if mode == "VS HAON":
                create_button(buttons["reset_records"], colors["red"], "기록 설정", colors["white"])
        else:
            # 기록 보기 화면
            draw_records_screen(mode, scroll_offset)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode is None:
                    if buttons["start"].collidepoint(event.pos):
                        mode, in_mode_selection = "SOLO", True
                    elif buttons["reset_all"].collidepoint(event.pos):
                        reset_all_records()
                elif in_mode_selection:
                    if buttons["solo"].collidepoint(event.pos):
                        mode, in_mode_selection, in_start_or_view_records = "SOLO", False, True
                    elif buttons["vs_haon"].collidepoint(event.pos):
                        mode, in_mode_selection, in_start_or_view_records = "VS HAON", False, True
                elif in_start_or_view_records:
                    if buttons["view_records"].collidepoint(event.pos):
                        in_start_or_view_records = False
                    elif buttons["start_game"].collidepoint(event.pos):
                        start_game(mode)
                        mode, in_mode_selection, in_start_or_view_records = None, False, False
                    elif mode == "VS HAON" and buttons["reset_records"].collidepoint(event.pos):
                        admin_set_record()
                        mode, in_mode_selection, in_start_or_view_records = None, False, False
                else:
                    if buttons["home"].collidepoint(event.pos):
                        mode, in_mode_selection, in_start_or_view_records = None, False, True
            elif event.type == pygame.MOUSEWHEEL and not in_start_or_view_records and mode:
                scroll_offset -= event.y * 30

if __name__ == "__main__":
    main()
