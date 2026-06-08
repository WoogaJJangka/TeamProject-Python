"""
기본 게임 테스트
"""
import sys
import os

# 프로젝트 루트 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import GameManager, Player
from config import settings


def test_player_creation():
    """플레이어 생성 테스트"""
    player = Player(0, 'red')
    assert player.color == 'red'
    assert player.money == settings.INITIAL_MONEY
    assert player.position == 0
    assert not player.is_bankrupt
    print("✅ test_player_creation 통과")


def test_player_movement():
    """플레이어 이동 테스트"""
    player = Player(0, 'red')
    player.move(5)
    assert player.position == 5
    player.move(18)
    assert player.position == 3  # (5 + 18) % 20 = 3
    print("✅ test_player_movement 통과")


def test_player_payment():
    """플레이어 결제 테스트"""
    player = Player(0, 'red')
    initial_money = player.money
    
    # 성공적인 결제
    assert player.pay(1000) == True
    assert player.money == initial_money - 1000
    
    # 실패한 결제
    assert player.pay(10000) == False
    assert player.money == initial_money - 1000  # 변화 없음
    print("✅ test_player_payment 통과")


def test_game_manager_creation():
    """게임 매니저 생성 테스트"""
    gm = GameManager()
    assert len(gm.players) == 4
    assert gm.board_size == 20
    assert len(gm.tiles) == 20
    print("✅ test_game_manager_creation 통과")


def test_turn_over():
    """턴 넘김 테스트"""
    gm = GameManager()
    assert gm.current_player_index == 0
    
    gm.turn_over()
    assert gm.current_player_index == 1
    
    gm.turn_over()
    assert gm.current_player_index == 2
    
    gm.turn_over()
    assert gm.current_player_index == 3
    
    gm.turn_over()
    assert gm.current_player_index == 0
    print("✅ test_turn_over 통과")


def test_buy_tile():
    """타일 구매 테스트"""
    gm = GameManager()
    player = gm.players[0]
    initial_money = player.money
    
    # 일반 타일 구매
    success, msg = gm.buy_tile(1, 0)  # 경복궁 타일
    assert success == True
    assert player.money == initial_money - 1300  # 경복궁 가격
    assert len(player.properties) == 1
    assert gm.tiles[1].owner == player
    print("✅ test_buy_tile 통과")


def test_cannot_buy_special_tiles():
    """특수 타일 구매 불가 테스트"""
    gm = GameManager()
    
    # 출도 (0번)
    success, msg = gm.buy_tile(0, 0)
    assert success == False
    
    # 무주도 (10번)
    success, msg = gm.buy_tile(10, 0)
    assert success == False
    print("✅ test_cannot_buy_special_tiles 통과")


def test_upgrade_tile():
    """타일 업그레이드 테스트"""
    gm = GameManager()
    player = gm.players[0]
    
    # 타일 구매
    gm.buy_tile(1, 0)
    initial_money = player.money
    
    # 업그레이드
    success, msg = gm.upgrade_tile(1, 0)
    assert success == True
    assert gm.tiles[1].upgrade_level == 1
    assert player.money == initial_money - 500
    print("✅ test_upgrade_tile 통과")


def test_check_winner_bankruptcy():
    """파산으로 인한 우승자 확인 테스트"""
    gm = GameManager()
    
    # 3명 파산 처리
    for i in range(1, 4):
        gm.players[i].is_bankrupt = True
    
    winner, reason = gm.check_winner()
    assert winner == gm.players[0]
    assert reason == 'bankruptcy'
    print("✅ test_check_winner_bankruptcy 통과")


def test_check_winner_property():
    """건물 개수로 인한 우승자 확인 테스트"""
    gm = GameManager()
    
    # 플레이어 0이 5개 이상 건물 구매
    for i in range(1, 6):
        tile = gm.tiles[i]
        gm.players[0].properties.append(tile)
        tile.owner = gm.players[0]
    
    winner, reason = gm.check_winner()
    assert winner == gm.players[0]
    assert reason == 'property'
    print("✅ test_check_winner_property 통과")


def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 게임 로직 테스트 시작...\n")
    
    try:
        test_player_creation()
        test_player_movement()
        test_player_payment()
        test_game_manager_creation()
        test_turn_over()
        test_buy_tile()
        test_cannot_buy_special_tiles()
        test_upgrade_tile()
        test_check_winner_bankruptcy()
        test_check_winner_property()
        
        print("\n✅ 모든 테스트 통과!")
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 예기치 않은 오류: {e}")
        return False
    
    return True


if __name__ == "__main__":
    run_all_tests()
