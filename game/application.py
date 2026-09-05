from pathlib import Path

import pygame

from board_set.BoardScreen import BoardScreen
from board_set.button import Button
from board_set.console import ConsoleLog
from game.game_manager import GameManager
from roll_dices.roller import DiceRoller


class GameApplication:
    SCREEN_SIZE = (1500, 1000)
    MAX_CONSOLE_LINES = 8
    SPECIAL_TILE_NAMES = {"출도", "학", "무주도", "미정"}

    def __init__(self, project_root=None):
        self.project_root = Path(project_root or Path(__file__).resolve().parent.parent)
        self.font_path = self.project_root / "board_set" / "font.ttf"
        self.player_asset_path = self.project_root / "game" / "assets"
        self.dice_asset_path = self.project_root / "roll_dices" / "assets"
        self.screen = None
        self.clock = None
        self.game_manager = None
        self.roller = None
        self.running = False
        self.console = ConsoleLog(self.font_path, self.MAX_CONSOLE_LINES)
        self.prompt = None
        self.player_images = {}

    @property
    def tiles(self):
        return self.game_manager.tiles

    def initialize(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.screen.fill((255, 255, 255))
        BoardScreen(self.screen, self.project_root)
        self.game_manager = GameManager()
        self.roller = DiceRoller(self.screen, str(self.dice_asset_path))
        self._load_player_images()

    def _load_player_images(self):
        for color in ("red", "blue", "green", "yellow"):
            image_path = self.player_asset_path / f"{color}.png"
            image = pygame.image.load(str(image_path))
            self.player_images[color] = pygame.transform.scale(image, (40, 40))
        for player in self.game_manager.players:
            player.piece_image = self.player_images[player.color]

    def run(self):
        self.initialize()
        self.running = True
        try:
            while self.running:
                self.clock.tick(120)
                self._update()
                self._draw()
                pygame.display.update()
        finally:
            pygame.quit()

    def _update(self):
        if not self._skip_bankrupt_players():
            return
        for event in pygame.event.get():
            self._handle_event(event)

    def _draw(self):
        mouse_position = pygame.mouse.get_pos()
        highlighted_tile = next(
            (tile for tile in self.tiles if tile.is_clicked(mouse_position)), None
        )

        for tile in self.tiles:
            tile.draw_owner_box(self.screen)
            tile.visual.draw(self.screen, tile.name, tile is highlighted_tile)

        selected_tile = highlighted_tile or self.tiles[self.game_manager.get_current_player().position]
        selected_tile.draw_info(self.screen, pos=(50, 50))
        self._draw_players()
        self.console.draw(self.screen)
        self._draw_prompt()

    def _draw_players(self):
        for index, player in enumerate(self.game_manager.players):
            player.draw_info(self.screen, pos=(1200, 50 + index * 160))
            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (1195, 45 + index * 160, 260, 160),
                4,
            )
            tile = self.tiles[player.position]
            original_position = tile.player_positions[player.turn]
            image_rect = player.piece_image.get_rect(
                center=(int(original_position[0] + 10), int(original_position[1] + 10))
            )
            self.screen.blit(player.piece_image, image_rect)

        current_index = self.game_manager.current_player_index
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (1195, 45 + current_index * 160, 260, 160),
            4,
        )

    def _draw_prompt(self):
        if self.prompt is None:
            return
        question = "땅을 구매하겠습니까?" if self.prompt["kind"] == "buy" else "땅을 업그레이드 하시겠습니까?"
        font = pygame.font.Font(str(self.font_path), 18)
        rendered = font.render(question, True, (0, 0, 0))
        self.screen.blit(rendered, (60, self.screen.get_height() - 180))
        for button in self.prompt["buttons"]:
            button.draw(self.screen)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if self.prompt and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_prompt_click(event.pos)
            return
        if self.prompt:
            return
        if event.type == pygame.KEYDOWN:
            self._handle_key_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_tile_click(event.pos)

    def _handle_key_event(self, event):
        if event.key == pygame.K_SPACE:
            self._play_turn()
        elif event.key == pygame.K_p and pygame.key.get_pressed()[pygame.K_F1]:
            self.add_message(f"현재 플레이어들의 위치: {[p.position for p in self.game_manager.players]}")
        elif event.key == pygame.K_m and pygame.key.get_pressed()[pygame.K_F1]:
            self.add_message(f"현재 플레이어들의 돈: {[p.money for p in self.game_manager.players]}")

    def _handle_tile_click(self, position):
        for tile in self.tiles:
            if tile.is_clicked(position):
                self.add_message(f"{tile.name} 타일 클릭")
                return

    def _handle_prompt_click(self, position):
        for index, button in enumerate(self.prompt["buttons"]):
            if not button.is_clicked(position):
                continue
            prompt = self.prompt
            if index == 0:
                if prompt["kind"] == "buy":
                    _, message = self.game_manager.buy_tile(prompt["tile_index"], prompt["player_index"])
                else:
                    _, message = self.game_manager.upgrade_tile(prompt["tile_index"], prompt["player_index"])
                self.add_message(message)
            else:
                self.add_message("구매를 취소했습니다." if prompt["kind"] == "buy" else "업그레이드를 취소했습니다.")
            self.prompt = None
            self.game_manager.turn_over()
            self._finish_turn_if_winner()
            return

    def _play_turn(self):
        player = self.game_manager.get_current_player()
        self.add_message(f"{player.color} 플레이어의 턴입니다.")
        if player.is_bankrupt:
            self.add_message(f"{player.color} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
            self.game_manager.turn_over()
            return

        if player.stop_turns > 0:
            self._play_stopped_turn(player)
            return

        steps = 0
        while True:
            dice1, dice2 = self.roller.roll_two_dice(group_pos=(44, 600))
            steps += dice1 + dice2
            if dice1 != dice2:
                break
            player.money += 500
            self.add_message("더블 보너스! 500원을 받았습니다.")
        player.move(steps, self.game_manager.board_size)
        self.add_message(f"{player.color} 플레이어가 {steps}칸 이동했습니다.")
        self._handle_arrival(player)

    def _play_stopped_turn(self, player):
        self.add_message(f"{player.color} 플레이어는 이동불가 상태입니다. (남은 턴: {player.stop_turns})")
        dice1, dice2 = self.roller.roll_two_dice(group_pos=(44, 600))
        self.add_message(f"주사위 결과: {dice1}, {dice2}")
        if dice1 == dice2:
            player.move(dice1 + dice2, self.game_manager.board_size)
            player.stop_turns = 0
            self._handle_arrival(player)
        else:
            player.stop_turns -= 1
            self.game_manager.turn_over()

    def _handle_arrival(self, player):
        tile_index = player.position
        tile = self.tiles[tile_index]
        self.add_message(f"{player.color} 플레이어가 {tile.name} 칸에 도착했습니다.")
        special_handlers = {
            0: self._handle_start_tile,
            5: self._apply_upgrade_event,
            10: self._handle_stop_tile,
            15: self._teleport_player,
        }
        if tile_index in special_handlers:
            special_handlers[tile_index](player)
        elif tile.owner is None and tile.price > 0 and tile.name not in self.SPECIAL_TILE_NAMES:
            if player.money < tile.price:
                self.add_message(f"{player.color} 플레이어는 {tile.name}을(를) 구매할 돈이 부족합니다.")
                self.game_manager.turn_over()
            else:
                self._open_prompt("buy", tile_index, self.game_manager.current_player_index)
        elif tile.owner == player and tile.upgrade_level < 2:
            cost = 500 if tile.upgrade_level == 0 else 1000
            if player.money < cost:
                self.add_message(f"{player.color} 플레이어는 업그레이드 비용 ₩{cost}가 부족합니다.")
                self.game_manager.turn_over()
            else:
                self._open_prompt("upgrade", tile_index, self.game_manager.current_player_index)
        else:
            _, message = self.game_manager.tile_event(tile_index, self.game_manager.current_player_index)
            self.add_message(message)
            self.game_manager.turn_over()
            self._finish_turn_if_winner()

    def _handle_start_tile(self, player):
        player.money += 2000
        self.add_message(f"{player.color} 플레이어가 출도 칸에 도착했습니다. 2000원을 받았습니다.")
        self.game_manager.turn_over()
        self._finish_turn_if_winner()

    def _handle_stop_tile(self, player):
        player.stop_turns = 2
        self.add_message(f"{player.color} 플레이어는 무주도에 도착해 2턴간 이동할 수 없습니다.")
        self.game_manager.turn_over()

    def _apply_upgrade_event(self, player):
        if not player.properties:
            self.add_message("미정 칸 효과: 소유한 땅이 없어 업그레이드할 수 없습니다.")
            return
        for tile in player.properties:
            success, message = self.game_manager.upgrade_tile(tile.board_index, player.turn)
            if success:
                self.add_message(f"미정 칸 효과: {tile.name} 땅이 업그레이드 되었습니다!")
                return
            self.add_message(f"미정 칸 효과: {tile.name} 업그레이드 실패 - {message}")
        self.add_message("미정 칸 효과: 업그레이드 가능한 땅이 없습니다.")

    def _teleport_player(self, player):
        self.add_message("학 칸에 도착했습니다! 원하는 타일을 클릭해 이동하세요.")
        while self.running:
            is_active, destination = self._read_teleport_destination()
            if not is_active:
                return
            if destination is not None:
                _, message = self.game_manager.teleport_player(player.turn, destination)
                self.add_message(message)
                return self._handle_arrival(player)
            self._draw()
            pygame.display.update()

    def _read_teleport_destination(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False, None
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            for index, tile in enumerate(self.tiles):
                if not tile.is_clicked(event.pos):
                    continue
                if index == 15:
                    self.add_message("학 타일로는 순간이동할 수 없습니다.")
                    return True, None
                return True, index
        return True, None

    def _open_prompt(self, kind, tile_index, player_index):
        font = pygame.font.Font(str(self.font_path), 18)
        bottom = self.screen.get_height() - 140
        self.prompt = {
            "kind": kind,
            "tile_index": tile_index,
            "player_index": player_index,
            "buttons": [
                Button((60, bottom, 80, 40), "예", font),
                Button((160, bottom, 80, 40), "아니요", font),
            ],
        }

    def _skip_bankrupt_players(self):
        while self.game_manager.get_current_player().is_bankrupt:
            player = self.game_manager.get_current_player()
            self.add_message(f"{player.color} 플레이어는 파산했으므로 턴을 넘깁니다.")
            self.game_manager.turn_over()
            if not self._finish_turn_if_winner():
                return False
        return True

    def _finish_turn_if_winner(self):
        winner, reason = self.game_manager.check_winner()
        if winner:
            if reason == "bankruptcy":
                self.add_message(f"{winner.color} 플레이어를 제외한 모두가 파산했습니다. {winner.color} 플레이어 우승!")
            elif reason == "property":
                self.add_message(f"땅 개수 차이로 {winner.color} 플레이어 우승!")
            else:
                self.add_message(f"{winner.color} 플레이어가 우승했습니다!")
            self.running = False
            return False
        return True

    def add_message(self, message):
        self.console.add(message)


def main():
    GameApplication().run()


if __name__ == "__main__":
    main()
