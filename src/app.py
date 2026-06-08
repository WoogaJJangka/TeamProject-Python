"""
메인 애플리케이션 (Application Entry Point)
"""
import pygame
import os
from config import settings
from src.game import GameManager
from src.ui import UIState, DiceUI, Renderer
from src.core.constants import COLORS, PLAYER_COLORS, FONTS_PATH
from src.core.resource_loader import resource_loader
from src.core.types import TileEventType

class Game:
    """메인 게임 애플리케이션"""
    
    def __init__(self):
        """게임 초기화"""
        pygame.init()
        
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        # 게임 로직
        self.game_manager = GameManager()
        
        # UI
        self.ui_state = UIState()
        
        # 주사위 UI
        dice_assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'dice')
        self.dice_ui = DiceUI(dice_assets_path, size=(100, 100))
        
        # 렌더러
        self.renderer = Renderer(self.screen, self.game_manager, self.ui_state, self.dice_ui)
        
        # 플레이어 말 이미지 로드
        self._load_player_pieces()
        
        # 게임 상태
        self.running = True
    
    def _load_player_pieces(self):
        """플레이어 말 이미지 로드"""
        piece_size = (40, 40)
        pieces_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'pieces')
        
        for player in self.game_manager.players:
            piece_file = os.path.join(pieces_path, f'{player.color}.png')
            img = resource_loader.load_image(piece_file, piece_size, piece_size)
            player.piece_image = img
    
    def run(self):
        """메인 게임 루프"""
        while self.running:
            self.clock.tick(settings.FPS)
            
            # 파산한 플레이어 턴 자동 스킵
            if not self._skip_bankrupt_and_check_winner():
                break
            
            mouse_pos = pygame.mouse.get_pos()
            
            # 순간이동 중
            if self.ui_state.is_teleporting:
                self._handle_teleport(mouse_pos)
            else:
                # 일반 게임 상태
                self.renderer.render(mouse_pos)
                self._handle_events(mouse_pos)
        
        pygame.quit()
        print("프로그램 종료")
    
    def _skip_bankrupt_and_check_winner(self) -> bool:
        """파산 플레이어 스킵 및 우승자 확인"""
        while self.game_manager.get_current_player().is_bankrupt:
            self.ui_state.add_message(
                f"{self.game_manager.get_current_player_color()} 플레이어는 파산했으므로 턴을 옮깁니다."
            )
            self.game_manager.turn_over()
            
            winner, reason = self.game_manager.check_winner()
            if winner:
                self._handle_game_end(winner, reason)
                return False
        
        return True
    
    def _handle_game_end(self, winner, reason: str):
        """게임 종료 처리"""
        if reason == 'bankruptcy':
            self.ui_state.add_message(
                f"{winner.color} 플레이어를 제외한 모두가 파산했습니다. {winner.color} 플레이어 우승!"
            )
        elif reason == 'property':
            self.ui_state.add_message(
                f"땅 개수 차이로 {winner.color} 플레이어 우승!"
            )
        else:
            self.ui_state.add_message(
                f"{winner.color} 플레이어가 우승했습니다!"
            )
        
        self.running = False
    
    def _handle_events(self, mouse_pos: tuple):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 구매 대화 버튼
            elif self.ui_state.ask_buy and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_buy_response(event.pos)
            
            # 업그레이드 대화 버튼
            elif self.ui_state.ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_upgrade_response(event.pos)
            
            # 스페이스: 주사위 굴리기
            elif not self.ui_state.ask_buy and not self.ui_state.ask_upgrade and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._handle_dice_roll()
                elif event.key == pygame.K_F1 and pygame.key.get_pressed()[pygame.K_p]:
                    positions = [p.position for p in self.game_manager.players]
                    self.ui_state.add_message(f'현재 플레이어 위치: {positions}')
                elif event.key == pygame.K_F1 and pygame.key.get_pressed()[pygame.K_m]:
                    money = [p.money for p in self.game_manager.players]
                    self.ui_state.add_message(f'현재 플레이어 돈: {money}')
            
            # 타일 클릭
            elif not self.ui_state.ask_buy and not self.ui_state.ask_upgrade and event.type == pygame.MOUSEBUTTONDOWN:
                for idx, tile in enumerate(self.game_manager.tiles):
                    if tile.is_clicked(mouse_pos):
                        self.ui_state.add_message(f"{tile.name} 타일 클릭")
                        break
    
    def _handle_dice_roll(self):
        """주사위 굴리기 처리"""
        current_player = self.game_manager.get_current_player()
        self.ui_state.add_message(f"{current_player.color} 플레이어의 턴입니다.")
        
        dice_pos = (44, 600)
        
        if current_player.is_bankrupt:
            self.ui_state.add_message(f"{current_player.color} 플레이어는 파산 상태입니다. 턴을 넘깁니다.")
            self.game_manager.turn_over()
            return
        
        # 무주도에서 나오기
        if getattr(current_player, 'stop_turns', 0) > 0:
            self.ui_state.add_message(
                f"{current_player.color} 플레이어는 이동불가 상태입니다. (남은 턴: {current_player.stop_turns})"
            )
            dice1, dice2 = self.dice_ui.roll_two_dice(self.screen, group_pos=dice_pos)
            self.ui_state.add_message(f"주사위 결과: {dice1}, {dice2}")
            
            if dice1 == dice2:
                steps = dice1 + dice2
                current_player.move(steps)
                self.ui_state.add_message(f"두 눈이 같아 {steps}칸 이동합니다!")
                current_player.stop_turns = 0
                player_index = self.game_manager.current_player_index
                self._handle_tile_arrival(current_player, player_index)
            else:
                self.ui_state.add_message("이동하지 못합니다.")
                current_player.stop_turns -= 1
                self.game_manager.turn_over()
            return
        
        # 일반 이동
        steps = 0
        double_count = 0
        
        while True:
            dice1, dice2 = self.dice_ui.roll_two_dice(self.screen, group_pos=dice_pos)
            steps += dice1 + dice2
            
            if dice1 == dice2:
                double_count += 1
                current_player.add_money(500)
                self.ui_state.add_message("더블 보너스! 500원을 받았습니다.")
                continue
            else:
                break
        
        current_player.move(steps)
        self.ui_state.add_message(f"{current_player.color} 플레이어가 {steps}칸 이동했습니다.")
        
        player_index = self.game_manager.current_player_index
        self._handle_tile_arrival(current_player, player_index)
    
    def _handle_tile_arrival(self, current_player, player_index: int):
        """타일 도착 처리"""
        tiles = self.game_manager.tiles
        arrived_tile = tiles[current_player.position]
        
        self.ui_state.add_message(f"{current_player.color} 플레이어가 {arrived_tile.name} 칸에 도착했습니다.")
        
        # 특수 타일 처리
        if current_player.position == 0:  # 출도
            current_player.add_money(settings.GO_BONUS)
            self.ui_state.add_message(f"{current_player.color} 플레이어가 출도 칸에 도착했습니다. {settings.GO_BONUS}원을 받았습니다.")
            self.game_manager.turn_over()
            winner, reason = self.game_manager.check_winner()
            if winner:
                self._handle_game_end(winner, reason)
            return
        
        elif current_player.position == 5:  # 미정 - 업그레이드 자동 수행
            if current_player.properties:
                upgraded = False
                for upgrade_tile in current_player.properties:
                    upgrade_tile_index = tiles.index(upgrade_tile)
                    success, message = self.game_manager.upgrade_tile(upgrade_tile_index, player_index)
                    if success:
                        self.ui_state.add_message(f"미정 칸 효과: {message}")
                        upgraded = True
                        break
                    else:
                        self.ui_state.add_message(f"미정 칸 효과: {message}")
                if not upgraded:
                    self.ui_state.add_message("미정 칸 효과: 업그레이드 가능한 땅이 없습니다.")
            else:
                self.ui_state.add_message("미정 칸 효과: 소유한 땅이 없어 업그레이드할 수 없습니다.")
            self.game_manager.turn_over()
            return
        
        elif current_player.position == 10:  # 무주도
            current_player.stop_turns = settings.JAIL_STOP_TURNS
            self.ui_state.add_message(
                f"{current_player.color} 플레이어는 무주도에 도착해 {settings.JAIL_STOP_TURNS}턴간 이동할 수 없습니다."
            )
            self.game_manager.turn_over()
            return
        
        elif current_player.position == 15:  # 학 - 순간이동
            self.ui_state.add_message("학 칸에 도착했습니다! 원하는 타일을 클릭해 이동하세요.")
            self.ui_state.start_teleport(player_index)
            return
        
        # 일반 타일 처리
        event_type, data = self.game_manager.tile_event(current_player.position, player_index)
        
        if event_type == TileEventType.GET_BONUS:
            # 출도 보너스는 위에서 처리됨
            pass
        elif event_type == TileEventType.PURCHASE_POSSIBLE:
            if current_player.money >= arrived_tile.price:
                self._show_buy_dialog(player_index)
            else:
                self.ui_state.add_message(f"{current_player.color} 플레이어는 구매할 돈이 부족합니다.")
                self.game_manager.turn_over()
        elif event_type == TileEventType.UPGRADE_POSSIBLE:
            self._show_upgrade_dialog(player_index)
        elif event_type == TileEventType.PAY_TOLL:
            success, logs = self.game_manager.pay_toll(current_player.position, player_index)
            self.ui_state.add_message(logs)
            self.game_manager.turn_over()
            winner, reason = self.game_manager.check_winner()
            if winner:
                self._handle_game_end(winner, reason)
        else:
            self.game_manager.turn_over()
    
    def _show_buy_dialog(self, player_index: int):
        """구매 대화 표시"""
        font_btn = pygame.font.SysFont('arial', 18)
        self.ui_state.start_buy_dialog(
            self.game_manager.get_current_player().position,
            player_index,
            font_btn,
            self.screen.get_height()
        )
    
    def _handle_buy_response(self, pos: tuple):
        """구매 응답 처리"""
        for idx, btn in enumerate(self.ui_state.buy_buttons):
            if btn.is_clicked(pos):
                if idx == 0:  # 예
                    success, message = self.game_manager.buy_tile(
                        self.ui_state.buy_tile_index,
                        self.ui_state.buy_player_index
                    )
                    self.ui_state.add_message(message)
                else:  # 아니요
                    self.ui_state.add_message("구매를 취소했습니다.")
                
                self.ui_state.end_buy_dialog()
                self.game_manager.turn_over()
                
                winner, reason = self.game_manager.check_winner()
                if winner:
                    self._handle_game_end(winner, reason)
                break
    
    def _show_upgrade_dialog(self, player_index: int):
        """업그레이드 대화 표시"""
        font_btn = pygame.font.SysFont('arial', 18)
        self.ui_state.start_upgrade_dialog(
            self.game_manager.get_current_player().position,
            player_index,
            font_btn,
            self.screen.get_height()
        )
    
    def _handle_upgrade_response(self, pos: tuple):
        """업그레이드 응답 처리"""
        for idx, btn in enumerate(self.ui_state.upgrade_buttons):
            if btn.is_clicked(pos):
                if idx == 0:  # 예
                    success, message = self.game_manager.upgrade_tile(
                        self.ui_state.upgrade_tile_index,
                        self.ui_state.upgrade_player_index
                    )
                    self.ui_state.add_message(message)
                else:  # 아니요
                    self.ui_state.add_message("업그레이드를 취소했습니다.")
                
                self.ui_state.end_upgrade_dialog()
                self.game_manager.turn_over()
                
                winner, reason = self.game_manager.check_winner()
                if winner:
                    self._handle_game_end(winner, reason)
                break
    
    def _handle_teleport(self, mouse_pos: tuple):
        """순간이동 타일 선택 처리"""
        self.renderer.render_teleport_selection(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, tile in enumerate(self.game_manager.tiles):
                    if tile.is_clicked(mouse_pos):
                        success, message = self.game_manager.teleport_player(
                            self.ui_state.teleport_player_index,
                            idx
                        )
                        if success:
                            self.ui_state.add_message(message)
                            # 순간이동 후 타일 이벤트 처리
                            current_player = self.game_manager.get_current_player()
                            self._handle_tile_arrival(current_player, self.ui_state.teleport_player_index)
                        else:
                            self.ui_state.add_message(message)
                        
                        self.ui_state.end_teleport()
                        break


def main():
    """엔트리 포인트"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
