import tkinter
import time
import pygame
import sys

scene=0
num=0
mouse_x=0
mouse_y=0
mouse_c=0

# 파이게임 초기화
pygame.init()

# 파이게임 창 크기 설정
screen_width, screen_height = 1000, 700

# 시간 변수 추가
game_start_time = 0
time_limit_seconds = 40

# 색상 정의
black = (0, 0, 0)
fade_color = (0, 0, 0)  # 페이드 아웃에 사용할 색상

# 플레이어 애니메이션 이미지
player_images = {
    'stand': pygame.image.load("dot1.png"),
    'walk_left_1': pygame.image.load("dot9.png"),
    'walk_left_2': pygame.image.load("dot12.png"),
    'walk_right_1': pygame.image.load("dot13.png"),
    'walk_right_2': pygame.image.load("dot16.png"),
    'walk_down_1': pygame.image.load("dot2.png"),
    'walk_down_2': pygame.image.load("dot4.png"),
    'walk_up_1': pygame.image.load("dot6.png"),
    'walk_up_2': pygame.image.load("dot8.png"),
    'swing': pygame.image.load("swing.png"),
    'swing2': pygame.image.load("swing2.png")
}

# 플레이어 애니메이션 상태
current_player_state = 'stand'

# 플레이어 애니메이션 프레임 인덱스
player_frame_index = 0
player_animation_frames = 4  # 각 애니메이션 상태에 대한 프레임 수

# 플레이어 애니메이션 상태 업데이트 함수에 변수 추가
last_frame_change_time = time.time()

# 플레이어 애니메이션 상태 업데이트 함수
def update_player_animation(keys):
    global player_frame_index, current_player_state, frame_change_delay, last_frame_change_time

    # 각 프레임 변경 간격을 정의합니다 (단위: 초)
    frame_change_delay = 0.2

    # 현재 시간을 가져옵니다
    current_time = time.time()

    # 프레임 변경 간격 이내에는 애니메이션을 변경하지 않습니다
    if current_time - last_frame_change_time < frame_change_delay:
        return
    if keys[pygame.K_LEFT]:
        current_player_state = 'walk_left_1' if player_frame_index % 2 == 0 else 'walk_left_2'
    elif keys[pygame.K_RIGHT]:
        current_player_state = 'walk_right_1' if player_frame_index % 2 == 0 else 'walk_right_2'
    elif keys[pygame.K_UP]:
        current_player_state = 'walk_up_1' if player_frame_index % 2 == 0 else 'walk_up_2'
    elif keys[pygame.K_DOWN]:
        current_player_state = 'walk_down_1' if player_frame_index % 2 == 0 else 'walk_down_2'
    elif keys[pygame.K_SPACE]and 'item4' in player_inventory: 
        current_player_state = 'swing2'
    else:
        current_player_state = 'stand'

    player_frame_index = (player_frame_index + 1) % player_animation_frames

    # 프레임 변경 시간을 갱신합니다
    last_frame_change_time = current_time

# 플레이어 이미지 로드
player_image = pygame.image.load("dot1.png")
player_rect = player_image.get_rect()

# 플레이어 초기 위치
player_rect.center = (screen_width // 6, screen_height // 3)

# 플레이어 이동 속도
player_speed = 12

# 플레이어가 가진 아이템 리스트
player_inventory = []

# 방 위치 및 크기
room1_width, room1_height = 600, 400
room2_width, room2_height = 2300, 950
room4_width, room4_height = 1392, 801
room1 = {"x": 50, "y": 50, "width": room1_width, "height": room1_height}
room2 = {"x": 2000, "y": 1000, "width": room2_width, "height": room2_height}
room3_width, room3_height = 600, 600
room3 = {"x": 5000, "y": 5000, "width": room3_width, "height": room3_height}
room4 = {"x": 6000, "y": 6000, "width": room4_width, "height": room4_height}



# 출입구 위치 및 크기
exit_width, exit_height = 20, 100
exit1 = {"x": room1["x"] + room1["width"] - exit_width, "y": room1["y"] + room1["height"] // 2 - exit_height // 2,
         "width": exit_width, "height": exit_height}
exit2_width, exit2_height = 20, 100
exit2 = {"x": room2["x"] + room2["width"] - exit2_width//1, "y": room2["y"] + room2["height"] - exit2_height // 0.80,
         "width": exit2_width, "height": exit2_height}
exit3_width, exit3_height = 20, 100
exit3 = {"x": room3["x"], "y": room3["y"] + room3["height"] // 2 - exit3_height // 2,
         "width": exit3_width, "height": exit3_height}


# 비밀번호 설정
room1_password = "D012559"
room2_password = "N05AH04"
room3_password = "F20"

# 현재 방 설정
current_room = room1


# 카메라 설정
camera_x, camera_y = room1["x"] + room1["width"] // 2 - screen_width // 2, room1["y"] + room1["height"] // 2 - screen_height // 2

# 아이템 이미지 로드
item_images = {
    'item1': pygame.image.load("item1.png"),
    'item2': pygame.image.load("item1.png"),
    'item3': pygame.image.load("item1.png"),
    'item4': pygame.image.load("hammer.png"),
    'item5': pygame.image.load("memo1.png"),
    'item6': pygame.image.load("pill1.png"),
    'item7': pygame.image.load("mamo1.png")
    
}

# room2의 아이템 리스트 (좌표 및 종류)
room2_items = [
    {"x": room2["x"] + 1900, "y": room2["y"] + 200, "type": 'item4'},
    {"x": room2["x"] + 1000, "y": room2["y"] + 350, "type": 'item5'},
    {"x": room2["x"] + 1300, "y": room2["y"] + 350, "type": 'item6'},
    {"x": room3["x"] + 516, "y": room3["y"] + 462, "type": 'item7'},
]
# 아이템 리스트 (좌표 및 종류)
room1_items = [
    {"x": room1["x"] + 20, "y": room1["y"] + 280, "type": 'item1'},
    {"x": room1["x"] + 380, "y": room1["y"] + 50, "type": 'item2'},
    {"x": room1["x"] + 500, "y": room1["y"] + 300, "type": 'item3'},
]

# room3에 마네킹 정보 추가
room3_items = [
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 10},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 70},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 130},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 190},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 250},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 310},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 370},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 430},
    {"type": "mannequin", "x": room3["x"] + 10, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 60, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 110, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 160, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 210, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 360, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 410, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 460, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 510, "y": room3["y"] + 490},
    {"type": "mannequin", "x": room3["x"] + 560, "y": room3["y"] + 490},

]
# 마네킹 이미지 로드 
mannequin_image = pygame.image.load("dummy1.png")
mannequin2_image = pygame.image.load("dummy2.png")
item_images['mannequin'] = mannequin_image
item_images['mannequin2'] = mannequin2_image

# 각 아이템에 대한 설명 정보를 담은 딕셔너리
item_descriptions = {
    "item1": "1:Circle",
    "item2": "2:[상자]에 [책]이 잔뜩 들었어",
    "item3": "3:[잎사귀]랑 [물병]을 [동전]으로 바꿀래?",
    "item4": "[스페이스바]로 무언가 부실수 있을것 같아",
    "item5": "102호실 : N05AH04",
    "item6": "이 약은 무슨 의미일까?",
    "item7": "F20 주의바람"

    # 다른 아이템들에 대한 설명도 추가할 수 있습니다.
}

# Dummy 클래스 수정: speed 매개변수 추가
class Dummy:
    def __init__(self, x, y, speed, image_path, boundary_rect):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed  # 더미의 이동 속도
        self.image = pygame.image.load(image_path)
        self.boundary_rect = boundary_rect  # 방 제한 영역
        self.active = False

    def chase_player(self, player_rect):
        if self.active:
            if self.rect.x < player_rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player_rect.x:
                self.rect.x -= self.speed

            if self.rect.y < player_rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player_rect.y:
                self.rect.y -= self.speed

            # 더미가 방을 벗어나지 못하도록 제한
            self.rect.x = max(self.boundary_rect["x"], min(self.rect.x, self.boundary_rect["x"] + self.boundary_rect["width"] - self.rect.width))
            self.rect.y = max(self.boundary_rect["y"], min(self.rect.y, self.boundary_rect["y"] + self.boundary_rect["height"] - self.rect.height))
 
# Dummy 객체 생성 (room2에서만 활동하도록 boundary 설정)
dummy_boundary_rect = {"x": room2["x"], "y": room2["y"], "width": room2["width"], "height": room2["height"]}
# Dummy 객체 생성 (room2에서만 활동하도록 boundary 설정)
dummy_speed = 4  # 더미의 이동 속도 조절
dummy_image_path = "dummy.png"
dummy = Dummy(room2["x"] + room2["width"] // 1.5, room2["y"] + room2["height"] // 4, speed=dummy_speed, image_path=dummy_image_path, boundary_rect=dummy_boundary_rect)

# 폰트 설정
font = pygame.font.SysFont("둥근모꼴regular", 36)

# 페이드 아웃 효과 설정
fade_alpha = 0  # 투명도 (0: 완전 투명, 255: 완전 불투명)
fade_speed = 5  # 페이드 아웃 속도

# 팝업창 설정
popup_font = pygame.font.SysFont("둥근모꼴regular", 36)
popup_rect = pygame.Rect(300, 200, 400, 150)
popup_input_rect = pygame.Rect(420, 280, 140, 30)
popup_active = False
popup_text = ""
input_text = ""

# 팝업창 설정
popup1_font = pygame.font.SysFont("둥근모꼴regular", 20)
popup1_rect = pygame.Rect(350, 200, 430, 130)
popup1_active = False
popup1_text = ""

#음악 파일
def play_background_music():
    # 배경 음악 로드 및 재생
    pygame.mixer.music.load("room2.ogg")
    pygame.mixer.music.play(-1)  # -1을 전달하여 음악을 반복 재생합니다.

# 발걸음 소리
walk_sound = pygame.mixer.Sound("walk_sound.ogg")
walk_channel = pygame.mixer.Channel(0)

# 엔딩 소리
def play_end_music():
    pygame.mixer.music.load("end_sound.ogg")
    pygame.mixer.music.play(-1)

#마네킹 없애는 소리
hit_music = pygame.mixer.Sound("hit_sound.ogg")
hit_channel = pygame.mixer.Channel(1)

# 게임 오버 화면을 표시하는 함수 정의
def game_over_screen():
    global player_rect, dummy, current_room, camera_x, camera_y, restart_clicked

    screen.fill((0, 0, 0))  # 흰색으로 화면 채우기
    game_over_font = pygame.font.SysFont("둥근모꼴regular", 72)
    game_over_text = game_over_font.render("게임 오버", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))
    # gameover.png 이미지 로드 및 표시
    game_over_image = pygame.image.load("gameover.png")
    screen.blit(game_over_image, (screen_width // 2 - game_over_image.get_width() // 2, screen_height // 2 - game_over_image.get_height() // 2))

    # 다시 시작 버튼 표시
    restart_font = pygame.font.SysFont("둥근모꼴regular", 36)
    restart_text = restart_font.render("다시 시작", True, (0, 0, 0))
    restart_button_rect = pygame.Rect(
        screen_width // 2 - restart_text.get_width() // 2,
        screen_height // 2,
        restart_text.get_width(),
        restart_text.get_height(),
    )
    pygame.draw.rect(screen, (255, 255, 255), restart_button_rect)
    screen.blit(restart_text, (restart_button_rect.x, restart_button_rect.y))

    pygame.display.flip()
    # 플레이어가 다시 시작 버튼을 클릭할 때까지 대기
    restart_clicked = False
    while not restart_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    # 다시 시작 버튼을 클릭한 경우 초기화
                    restart_clicked = True  # 클릭 여부 설정

        pygame.time.Clock().tick(60)
        
#게임 엔딩 스크린
def game_end_screen():
    global player_rect, dummy, current_room, camera_x, camera_y, restart_clicked

    screen.fill((0, 0, 0))  # 흰색으로 화면 채우기
    game_over_font = pygame.font.SysFont("둥근모꼴regular", 72)
    game_over_text = game_over_font.render("END", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))

    # 게임 종료 버튼 표시
    restart_font = pygame.font.SysFont("둥근모꼴regular", 36)
    restart_text = restart_font.render("close", True, (0, 0, 0))
    restart_button_rect = pygame.Rect(
        screen_width // 2 - restart_text.get_width() // 2,
        screen_height // 2,
        restart_text.get_width(),
        restart_text.get_height(),
    )
    pygame.draw.rect(screen, (0, 255, 0), restart_button_rect)
    screen.blit(restart_text, (restart_button_rect.x, restart_button_rect.y))

    pygame.display.flip()
    # 플레이어가 끄기 버튼을 클릭할 때까지 대기
    restart_clicked = False
    play_end_music()
    while not restart_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.time.Clock().tick(60)

    pygame.display.flip()
# 방 변경 함수 수정
def change_room(new_room):
    global current_room, camera_x, camera_y, player_rect, fade_alpha,game_start_time
    fade_alpha = 0
    while fade_alpha < 255:
        fade_alpha += fade_speed
        fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        fade_surface.fill((fade_color[0], fade_color[1], fade_color[2], fade_alpha))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    current_room = new_room
    game_start_time = pygame.time.get_ticks()
    if new_room == room3:
        # room3로 이동할 때 플레이어 위치 조정
        player_rect.x = new_room["x"] + new_room["width"] // 2 - player_rect.width // 2
        player_rect.y = new_room["y"]
        camera_x = player_rect.x - screen_width // 2
        camera_y = player_rect.y - screen_height // 2
    else:
        # room1 또는 room2로 이동할 때 플레이어 위치 조정
        player_rect.x = new_room["x"]
        player_rect.y = new_room["y"] + new_room["height"] // 2 - exit_height // 2
        camera_x = new_room["x"] + new_room["width"] // 2 - screen_width // 2
        camera_y = new_room["y"] + new_room["height"] // 2 - screen_height // 2
    fade_alpha = 255
# 마네킹 제거 함수 정의
def remove_mannequin():
    global room3_items,spacebar_count
    # 플레이어가 마네킹과 충돌하는지 확인
    for mannequin in room3_items:
        mannequin_rect = pygame.Rect(mannequin["x"], mannequin["y"], mannequin_image.get_width(), mannequin_image.get_height())
        if player_rect.colliderect(mannequin_rect):
            if spacebar_count == 1:  # 스페이스바를 1번 누를 때
                room3_items.remove(mannequin)
                spacebar_count = 0  # 스페이스바 입력 횟수 초기화
           

# 팝업창을 표시하는 함수
def show_popup(title, prompt):
    global popup_active, popup_text, input_text
    popup_active = True
    popup_text = prompt
    input_text = ""

# 팝업창 띄우기 함수 정의
def show_popup_for_item(item_type):
    global popup1_active, popup1_text

    # 여기서 item_type을 기반으로 아이템 설명을 설정합니다.
    item_description = item_descriptions.get(item_type, "아이템 설명이 없습니다.")
    popup1_text = f"{item_description}"
    popup1_active = True

# 미로의 크기를 늘린 예시
maze_layout = [
    "##############################################",
    "#..........................#.................#",
    "#..........................#.................#",
    "#..#######..#############..#..##########..#..#",
    "#..#.....#..#...........#..#..#........#..#..#",
    "#..#.....#..#...........#..#..#........#..#..#",
    "#..#..#..#..#..#######..#..#..#..####..#..#..#",
    "......#..#..#..#.....#..#..#..#..#.....#..#..#",
    "......#..#..#..#.....#..#..#..#..#.....#..#..#",
    "...####..#..#..#..#..#..#..#..#..#..#..#..#..#",
    "...#.....#..#.....#..#..#..#.....#..#..#..#..#",
    "#..#.....#..#.....#..#..#..#.....#..#..#..#..#",
    "#..#..####..#######..#..#..#######..#..#..#..#",
    "#..#.................#..#..............#..#..#",
    "#..#.................#..#..............#..#..#",
    "#..###################..###################..#",
    "#....................#..#.....................",
    "#....................#..#.....................",
    "##############################################",
]

# 스페이스바 입력 횟수 초기화
spacebar_count = 0

def start_pygame():
    global screen,popup_active,restart_clicked,popup_text, camera_x, camera_y, current_room,popup1_active,popup1_text,spacebar_count,game_start_time
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("더미포비아")

    # 게임 루프
    input_text = ""
    running = True
    while running:   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spacebar_count += 1
                if not popup_active and not popup1_active:
                    if event.key == pygame.K_RETURN:
                        # 팝업이 활성화되어 있지 않을 때 출입구에 도달하면 방 변경
                        if (
                            exit1["x"] <= player_rect.centerx <= exit1["x"] + exit1["width"]
                            and exit1["y"] <= player_rect.centery <= exit1["y"] + exit1["height"]
                        ):
                            show_popup("", "Enter the password")
                        elif (
                            exit2["x"] <= player_rect.centerx <= exit2["x"] + exit2["width"]
                            and exit2["y"] <= player_rect.centery <= exit2["y"] + exit2["height"]
                        ):
                            show_popup("", "Enter the password")
                        elif (
                            exit3["x"] <= player_rect.centerx <= exit3["x"] + exit3["width"]
                            and exit3["y"] <= player_rect.centery <= exit3["y"] + exit3["height"]
                        ):
                            show_popup("", "Enter the password")
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                    # 숫자키를 눌렀을 때 아이템 설명창 띄우기
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        item_index = event.key - pygame.K_1
                        if 0 <= item_index < len(player_inventory):
                            show_popup_for_item(player_inventory[item_index])
                            
                    # 플레이어와 충돌하는 마네킹을 제거하는 코드 추가
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        remove_mannequin()
                        hit_channel.play(hit_music)
                            
                elif popup1_active:
                    # 팝업1이 활성화되어 있을 때 엔터 키를 누르면 팝업1에서 동작
                    if event.key == pygame.K_RETURN:
                        # 팝업1 비활성화
                        popup1_active = False
                        # 팝업1에서의 동작 수행
                        
                elif popup_active:
                    # 팝업이 활성화되어 있을 때 엔터 키를 누르면 팝업에서 비밀번호 확인
                    if event.key == pygame.K_RETURN:
                        if current_room == room1 and input_text == room1_password:
                            change_room(room2)
                            play_background_music()
                            dummy.active = True  # 더미 활성화
                        elif current_room == room2 and input_text == room2_password:
                            change_room(room3)
                            pygame.mixer.music.stop()
                            dummy.active = False  # 더미 비활성화
                        elif current_room == room3 and input_text == room3_password:
                            change_room(room4)  # room4로 이동
                        input_text = ""  # 비밀번호 초기화
                        popup_active = False  # 팝업 비활성화
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            is_moving = True

        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # 플레이어가 이동 중일 때 효과음 재생
        if is_moving:
            if walk_channel.get_busy() == 0:  # 효과음이 재생 중이 아니면 재생
                walk_channel.play(walk_sound)

        else:
            walk_channel.stop()        
    
        # 플레이어 애니메이션 업데이트
        update_player_animation(keys)

        # 카메라 설정
        if current_room == room3:
            # room3로 이동할 때 플레이어 위치 조정
            camera_x = player_rect.x - screen_width // 2
            camera_y = player_rect.y - screen_height // 2
        else:
            # room1 또는 room2로 이동할 때 플레이어 위치 조정
            camera_x = current_room["x"] + current_room["width"] // 2 - screen_width // 2
            camera_y = current_room["y"] + current_room["height"] // 2 - screen_height // 2
        
        # 애니메이션 상태에 따라 플레이어 그리기
        player_image = player_images[current_player_state]
        player_width, player_height = player_rect.width, player_rect.height
        player_frame_width = player_width // player_animation_frames

        source_rect = pygame.Rect(player_frame_index * player_frame_width, 0, player_frame_width, player_height)
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y), source_rect)


        
        # 플레이어의 움직임 제약 조정
        player_rect.x = max(current_room["x"], min(player_rect.x, current_room["x"] + current_room["width"] - player_rect.width))
        player_rect.y = max(current_room["y"], min(player_rect.y, current_room["y"] + current_room["height"] - player_rect.height))

        
        if current_room == room2:
            camera_x = player_rect.x - screen_width // 2
            camera_y = player_rect.y - screen_height // 2
        # room2의 미로 벽과의 충돌 확인
        for i, row in enumerate(maze_layout):
            for j, cell in enumerate(row):
                if cell == "#":
                    wall_rect = pygame.Rect(room2["x"] + j * 50, room2["y"] + i * 50, 50, 50)
                    if player_rect.colliderect(wall_rect):
                        # 미로 벽과 충돌 시 플레이어 위치 조정
                        if keys[pygame.K_LEFT]:
                            player_rect.x = max(player_rect.x, wall_rect.right)
                        if keys[pygame.K_RIGHT]:
                            player_rect.x = min(player_rect.x, wall_rect.left - player_rect.width)
                        if keys[pygame.K_UP]:
                            player_rect.y = max(player_rect.y, wall_rect.bottom)
                        if keys[pygame.K_DOWN]:
                            player_rect.y = min(player_rect.y, wall_rect.top - player_rect.height)

        # Dummy가 플레이어를 쫓아오도록 처리
        dummy.chase_player(player_rect)

        # 더미의 활성/비활성 상태에 따라 Dummy 그리기
        if dummy.active:
            screen.blit(dummy.image, (dummy.rect.x - camera_x, dummy.rect.y - camera_y))

        # 플레이어와 더미 간의 충돌을 확인
        if player_rect.colliderect(dummy.rect):
            # 게임 오버 화면 함수 호출
            game_over_screen()

            # 다시 시작 버튼을 클릭한 경우 초기화
            if restart_clicked:
                player_rect.x = room2["x"] +2 # room2의 맨 왼쪽에 위치
                player_rect.y = room2["y"] + room2["height"] // 2 - player_rect.height // 1 # 중간 높이에 위치
                dummy.active = True  # 더미 활성화
                restart_clicked = False  # 클릭 여부 초기화



        # 그리기
        screen.fill(black)

        # 방 그리기
        pygame.draw.rect(screen, (0, 0, 255), (room1["x"] - camera_x, room1["y"] - camera_y, room1["width"], room1["height"]))
        pygame.draw.rect(screen, (255, 0, 0), (room2["x"] - camera_x, room2["y"] - camera_y, room2["width"], room2["height"]))
        pygame.draw.rect(screen, (0, 255, 0), (room3["x"] - camera_x, room3["y"] - camera_y, room3["width"], room3["height"]))

        # 출입구 그리기
        pygame.draw.rect(screen, (0, 255, 0), (exit1["x"] - camera_x, exit1["y"] - camera_y, exit1["width"], exit1["height"]))
        pygame.draw.rect(screen, (0, 255, 0), (exit2["x"] - camera_x, exit2["y"] - camera_y, exit2["width"], exit2["height"]))
        pygame.draw.rect(screen, (0, 100, 100), (exit3["x"] - camera_x, exit3["y"] - camera_y, exit3["width"], exit3["height"]))

        
        room2_image = pygame.image.load("mazebg.png")
        screen.blit(room2_image, (room2["x"] - camera_x, room2["y"] - camera_y))

        # room2에 대한 미로 그리기
        block_size = 50
        for i, row in enumerate(maze_layout):
            for j, cell in enumerate(row):
                if cell == "#":
                    # mazeblock.png 이미지 로드
                    block_image = pygame.image.load("mazeblock.png")
                    # 이미지를 미로 벽의 위치에 그립니다.
                    screen.blit(block_image, (room2["x"] + j * block_size - camera_x, room2["y"] + i * block_size - camera_y))
    
       # 이미지 불러오기
        rer_image = pygame.image.load("room1.png")

        # 방1 위에 이미지 덧씌우기
        screen.blit(rer_image, (room1["x"] - camera_x, room1["y"] - camera_y -130))

        # 이미지 불러오기
        rer1_image = pygame.image.load("room3.png")

        # 방1 위에 이미지 덧씌우기
        screen.blit(rer1_image, (room3["x"] - camera_x-42, room3["y"] - camera_y-130))
        
        # 아이템 그리기
        for item in room1_items + room2_items :
            item_image = item_images[item["type"]]
            screen.blit(item_image, (item["x"] - camera_x, item["y"] - camera_y))
            # 아이템과 플레이어 충돌 검사
            if player_rect.colliderect(pygame.Rect(item["x"], item["y"], item_image.get_width(), item_image.get_height())):
                # 엔터 키를 눌러 아이템 획득 팝업 띄우기
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # 플레이어 인벤토리에 아이템 추가
                    player_inventory.append(item["type"])
                    # 아이템 목록에서 제거
                    if item in room1_items:
                        room1_items.remove(item)
                    elif item in room2_items:
                        room2_items.remove(item)
                    # item5인 경우에만 이미지 표시
                    if item["type"] == "item5":
                        obtained_image_path = 'memo.png'
                        obtained_image = pygame.image.load(obtained_image_path)
                        screen.blit(obtained_image, (screen_width // 2 - obtained_image.get_width() // 2, screen_height // 2 - obtained_image.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.delay(2000)  # 이미지를 2초 동안 표시한 후 화면에서 제거 (원하는 시간으로 조정 가능)
                        # item5인 경우에만 이미지 표시
                    if item["type"] == "item6":
                        obtained_image_path = 'pill.png'
                        obtained_image = pygame.image.load(obtained_image_path)
                        screen.blit(obtained_image, (screen_width // 2 - obtained_image.get_width() // 2, screen_height // 2 - obtained_image.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.delay(3000)
                    if item["type"] == "item7":
                        obtained_image_path = 'mamo.png'
                        obtained_image = pygame.image.load(obtained_image_path)
                        screen.blit(obtained_image, (screen_width // 2 - obtained_image.get_width() // 2, screen_height // 2 - obtained_image.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.delay(2000)

        
        # Dummy 그리기
        screen.blit(dummy.image, (dummy.rect.x - camera_x, dummy.rect.y - camera_y))

        for mannequin in room3_items:
            screen.blit(mannequin_image, (mannequin["x"] - camera_x, mannequin["y"] - camera_y))
            

        # 인벤토리 표시
        inventory_font = pygame.font.SysFont("둥근모꼴regular", 20)
        inventory_text = inventory_font.render("IVENTORY: " , True, (255, 255, 255))
        screen.blit(inventory_text, (10, screen_height - 30))

         # 플레이어의 아이템 이미지를 인벤토리에 추가
        inventory_x = 120
        for index in range(len(player_inventory)):
            item_type = player_inventory[index]
            item_image = item_images[item_type]
            screen.blit(item_image, (inventory_x, screen_height - 50))
            
            # 숫자를 표시하는 사각형 테두리 그리기
            rect_width, rect_height = 20, 20
            rect_x, rect_y = inventory_x - 15, screen_height - 69
            pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), 2)  # 두께를 2로 지정

            # 숫자로 표시
            number_text = inventory_font.render(str(index + 1), True, (255, 255, 255))
            screen.blit(number_text, (inventory_x - 10, screen_height - 70))
            
            inventory_x += item_image.get_width() + 10
         # 플레이어 그리기
        screen.blit(player_image, (player_rect.x - camera_x, player_rect.y - camera_y))
   
        # 팝업창 그리기
        if popup_active:
            pygame.draw.rect(screen, (200, 200, 200), popup_rect)
            pygame.draw.rect(screen, (0, 0, 0), popup_input_rect, 2)
            popup_surface = font.render(popup_text, True, (0, 0, 0))
            screen.blit(popup_surface, (popup_rect.centerx - popup_surface.get_width() // 2, popup_rect.y + 20))
            input_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(input_surface, (popup_input_rect.x + 5, popup_input_rect.y + -3))

        if popup1_active:
            pygame.draw.rect(screen, (225, 225, 225), popup1_rect)
            popup1_surface = popup1_font.render(popup1_text, True, (0, 0, 0))
            screen.blit(popup1_surface, (popup1_rect.centerx - popup1_surface.get_width() // 2, popup1_rect.y + 50))
        # room3으로 이동한 후 시간 체크
        if current_room == room3:
            elapsed_time_seconds = (pygame.time.get_ticks() - game_start_time) // 1000
            remaining_time_seconds = max(0, time_limit_seconds - elapsed_time_seconds)

            # 시간이 다 떨어지면 게임 오버
            if remaining_time_seconds == 0:
                game_over_screen()
                # 다시 시작 버튼을 클릭한 경우 초기화
                if restart_clicked:
                    player_rect.x = room3["x"] + room3["width"] // 2 - player_rect.width // 2
                    player_rect.y = room3["y"]
                    dummy.active = True  # 더미 활성화
                    game_start_time = pygame.time.get_ticks()  # 게임 시작 시간 초기화
                    restart_clicked = False  # 클릭 여부 초기화
                continue  # 게임 오버 시 루프 종료

            # 시간 표시
            time_font = pygame.font.SysFont("둥근모꼴regular", 40)
            time_text = time_font.render(f"남은시간: {remaining_time_seconds} 초", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))   
            
        #애니메이션 그리기
        if current_room == room4:
            player_active = False
            End_bg1 = pygame.image.load("end_bg1.png")
            End_bg2 = pygame.image.load("end_bg2.png")
            black_bg = pygame.image.load("black_bg.png")

            end_bg1_width, end_bg1_height = End_bg1.get_width(), End_bg1.get_height()
            end_bg2_width, end_bg2_height = End_bg2.get_width(), End_bg2.get_height()
            black_bg_width, black_bg_height = black_bg.get_width(), black_bg.get_height()

            end_bg1_x = (1000 - end_bg1_width) // 2
            end_bg1_y = (700 - end_bg1_height) // 2
            end_bg2_x = (1000 - end_bg2_width) // 2
            end_bg2_y = (700 - end_bg2_height) // 2
            black_bg_x = (1000 - black_bg_width) // 2
            black_bg_y = (700 - black_bg_height) // 2

            walk_channel.play(walk_sound, loops=0, maxtime=2000)
            pygame.time.wait(2000) #나중에 발걸음 소리 넣을 부분
            screen.blit(End_bg1, (end_bg1_x, end_bg1_y))
            pygame.display.flip()
            pygame.time.wait(2000)
                   
            screen.blit(black_bg, (black_bg_x, black_bg_y))
            pygame.display.flip()
            pygame.time.wait(1000)
            
        
            screen.blit(End_bg2, (end_bg2_x, end_bg2_y))
            pygame.display.flip()
            pygame.time.wait(1000)
            game_end_screen()

        # 화면 업데이트
        pygame.display.flip()

        # 초당 프레임 수 제한
        pygame.time.Clock().tick(60)

    pygame.quit()

def mouse_move(e):
    global mouse_x,mouse_y
    mouse_x=e.x
    mouse_y=e.y
def mouse_press(e):
    global mouse_c
    mouse_c=1
def click_nbtn():
    global num
    text.delete("1.0", tkinter.END)
    text.insert("1.0",pname+"\n\n  ⌈ "+script[num]+" ⌋")
    time.sleep(0.5)
    num += 1

    # script의 끝에 도달하면 Tkinter를 종료하고 Pygame 시작
    if num >= len(script):
        root.destroy()
        start_pygame()

def start():
    global mouse_c,scene
    global text,num
    if scene==0:
        draw_txt("이름을 입력해주세요",480,300,20,"white","START")
        canvas.create_rectangle(370,430,600,465,fill="red",width=0,tag="START")
        draw_txt("START",480,445,22,"black","START")
        canvas.create_rectangle(370,475,600,510,fill="red",width=0,tag="START")
        draw_txt("HOW TO GAME",480,490,22,"black","START")
        if mouse_c==1:
            if 370<mouse_x and mouse_x<600 and 430<mouse_y and mouse_y<465:
                global pname
                pname=" "+entry.get()+" ▼" #캐릭터 이름 저장 해놓고 다음 장 말풍선부터 적용
                entry.place(x=1100,y=0)
                canvas.delete("START")
                time.sleep(0.5)
                scene=1
                canvas.create_image(500,400,image=bg1)   
                for i in range(2):  #눈 깜빡임 표현
                    canvas.create_rectangle(0,0,1000,800,fill="black",width=0,tag="WINK_EYE")
                    canvas.update()
                    time.sleep(0.8)
                    canvas.delete("WINK_EYE")
                    canvas.update()
                    time.sleep(0.5)
            elif 370<mouse_x and mouse_x<600 and 475<mouse_y and mouse_y<510: 
                canvas.create_image(500,650,image=htg,tag="START")
            mouse_c=0
    elif scene == 1:
        canvas.create_image(200, 500, image=player)
        next_button = tkinter.Button(text="next", font=("DungGeunMo", 20), bg="cadetblue", command=click_nbtn)
        next_button.place(x=900, y=500)
        text = tkinter.Text(width=70, height=7, font=("DungGeunMo", 16))
        text.place(x=200, y=600)
        text.insert("1.0", pname + "\n\n  ⌈ " + script[num] + " ⌋")  
        canvas.create_image(588, 675, image=balloon)
        scene = 2
    elif scene==2:
        canvas.delete()
    
    root.after(100,start)

root=tkinter.Tk()
root.title("병동 탈출 일지")
canvas=tkinter.Canvas(root,width=1000,height=800,bg="black")
canvas.pack()
canvas.create_text(500,200,text="더미 포비아",fill="white",font=("DungGeunMo",50),tag="START")
root.bind("<Motion>",mouse_move)
root.bind("<ButtonPress>",mouse_press)

def draw_txt(txt,x,y,siz,col,tg):
    fnt=("DungGeunMo",siz)
    canvas.create_text(x+2,y+2,text=txt,fill="black",font=fnt,tag=tg)
    canvas.create_text(x,y,text=txt,fill=col,font=fnt,tag=tg)


entry=tkinter.Entry(width=20,justify="center",borderwidth=5,font=("DungGeunMo",20))
entry.place(x=385,y=370,width=200,height=40)

bg1=tkinter.PhotoImage(file="bg.png")
player=tkinter.PhotoImage(file="player.png")
htg=tkinter.PhotoImage(file="how to game.png")
balloon=tkinter.PhotoImage(file="balloon.png")

script=["여긴 어디지..?","...","내가 왜 여기에 갇혀 있는 거지?...","아무리 생각해도 이상해","...","나가야겠어.",""]

start()
root.mainloop()