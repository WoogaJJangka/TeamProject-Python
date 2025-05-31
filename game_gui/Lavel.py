import pygame
import pygame_gui

def EnglishName(tile_name_kr):
    tile_name_map = {
        "북한산성": "Bukhansanseong",
        "성균관": "Seonggyungwan",
        "숭례문": "Sungnyemun",
        "병산서원": "Byeongsanseowon",
        "숙정문": "Sukjeongmun",
        "종묘": "Jongmyo",
        "해인사": "Haeinsa",
        "돈의문": "Donuimun",
        "경회루": "Gyehoeru",
        "수원화성": "Suwon Hwaseong",
        "흥인지문": "Heunginjimun",
        "남한산성": "Namsanseong",
        "덕수궁": "Deoksugung",
        "창경궁": "Changgyeonggung",
        "창덕궁": "Changdeokgung",
        "경복궁": "Gyeongbokgung"
    }

    return tile_name_map.get(tile_name_kr, "Unknown Place")




def TileBUY(tile_name_kr, manager):

    text = EnglishName(tile_name_kr)
    label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 80), (300, 60)),
        text=text,
        manager=manager
    )