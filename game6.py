import os
import sys
import random
import pygame as pg
import math

# 必須条件：カレントディレクトリをこのファイルがある場所に変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------
# 【拡張機能のインポート領域】
# 各メンバーは担当機能が完成したらコメントアウトを外して統合する
# ---------------------------------------------------------
# import feature_player_ex  # 追加1：プレイヤーのダッシュ、アニメーション、残像エフェクト
# import feature_boss       # 追加2：定期的に襲来するボスキャラや妨害ビーム
# import feature_special    # 追加3：磁石や無敵などの特殊効果アイテム
# import feature_combo      # 追加4：連続キャッチによるコンボシステムと高度なスコア計算
# import feature_scene      # 追加5：本格的なタイトル画面、リザルト画面、BGM管理

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((80, 20))
        self.image.fill((0, 100, 255))
        self.rect = self.image.get_rect(center=(400, 550))

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 8
        if keys[pg.K_RIGHT] and self.rect.right < 800:
            self.rect.x += 8

class Apple(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(random.randint(20, 780), 0))
        self.speed = random.randint(4, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill() # 画面外に出たら消去


class SceneManager:
    def __init__(self):
        # 日本語フォント（Windows標準）
        FONT_NAME = "meiryo"

        self.font_title = pg.font.SysFont(FONT_NAME, 50, bold=True)
        self.font_large = pg.font.SysFont(FONT_NAME, 32, bold=True)
        self.font_small = pg.font.SysFont(FONT_NAME, 22)

        self.overlay = pg.Surface((800, 600))
        self.overlay.set_alpha(200)

    def handle_event(self, event, current_state):
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if current_state == "TITLE":
                return "PLAY"
            elif current_state == "RESULT":
                return "RESET"
        return current_state

    def draw(self, screen, state, score):
        ticks = pg.time.get_ticks()

        if state == "TITLE":
            self.overlay.fill((20, 25, 40))
            screen.blit(self.overlay, (0, 0))

            # タイトルロゴ
            bounce_y = math.sin(ticks * 0.004) * 8
            title_shadow = self.font_title.render("ITEM CATCH PANIC", True, (50, 50, 50))
            title = self.font_title.render("ITEM CATCH PANIC", True, (255, 215, 0))
            screen.blit(title_shadow, (400 - title_shadow.get_width() // 2 + 4, 160 + bounce_y + 4))
            screen.blit(title, (400 - title.get_width() // 2, 160 + bounce_y))

            # 操作説明ボックス
            desc_rect = pg.Rect(180, 250, 440, 110)
            pg.draw.rect(screen, (40, 50, 70), desc_rect, border_radius=10)
            pg.draw.rect(screen, (100, 150, 255), desc_rect, width=2, border_radius=10)

            info1 = self.font_small.render("【 ← / → 】 矢印キーで移動", True, (220, 220, 220))
            info2 = self.font_small.render("落ちてくるアイテムを集めよう！", True, (220, 220, 220))
            screen.blit(info1, (400 - info1.get_width() // 2, 270))
            screen.blit(info2, (400 - info2.get_width() // 2, 310))

            # スタート案内
            alpha = int((math.sin(ticks * 0.008) + 1) * 127.5)
            nav = self.font_large.render("- SPACEキーでスタート -", True, (255, 255, 255))
            nav.set_alpha(alpha)
            screen.blit(nav, (400 - nav.get_width() // 2, 420))

        elif state == "RESULT":
            self.overlay.fill((30, 10, 15))
            screen.blit(self.overlay, (0, 0))

            panel = pg.Rect(180, 100, 440, 380)
            pg.draw.rect(screen, (50, 20, 30), panel, border_radius=16)
            pg.draw.rect(screen, (255, 100, 100), panel, width=3, border_radius=16)

            result_title = self.font_title.render("TIME UP!", True, (255, 80, 80))
            screen.blit(result_title, (400 - result_title.get_width() // 2, 140))

            score_t = self.font_large.render(f"最終スコア: {score}", True, (255, 255, 255))
            screen.blit(score_t, (400 - score_t.get_width() // 2, 230))

            if score >= 300:
                rank_str, rank_color = "ランク: S (素晴らしい！)", (255, 215, 0)
            elif score >= 200:
                rank_str, rank_color = "ランク: A (すごい！)", (180, 255, 180)
            elif score >= 100:
                rank_str, rank_color = "ランク: B (イイ感じ！)", (200, 200, 255)
            else:
                rank_str, rank_color = "ランク: C (もう一度！)", (200, 200, 200)

            rank_t = self.font_small.render(rank_str, True, rank_color)
            screen.blit(rank_t, (400 - rank_t.get_width() // 2, 290))

            alpha = int((math.sin(ticks * 0.008) + 1) * 127.5)
            restart_t = self.font_small.render("- SPACEキーで再挑戦 -", True, (255, 255, 255))
            restart_t.set_alpha(alpha)
            screen.blit(restart_t, (400 - restart_t.get_width() // 2, 380))


def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("アイテムキャッチ・パニック - 完全版ベース")
    clock = pg.time.Clock()
    font = pg.font.SysFont("meiryo", 28)

    all_sprites = pg.sprite.Group()
    apples = pg.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    start_ticks = pg.time.get_ticks()
    game_duration = 60000 # 60秒
    seconds_left = 60

    game_state = "TITLE"
    scene_manager = SceneManager()

    # ---------------------------------------------------------
    # 【拡張機能の初期化領域】
    # ---------------------------------------------------------
    # boss_manager = feature_boss.BossManager()
    # combo_system = feature_combo.ComboSystem()

    while True:
        # 1. イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


            next_state = scene_manager.handle_event(event, game_state)

            if next_state == "RESET":
                score = 0
                for apple in apples:
                    apple.kill()
                player.rect.center = (400, 550)
                start_ticks = pg.time.get_ticks()
                game_state = "PLAY"
            elif game_state == "TITLE" and next_state == "PLAY":
                start_ticks = pg.time.get_ticks()
                game_state = "PLAY"
            else:
                game_state = next_state

        # 2. 更新処理
        if game_state == "PLAY":
            seconds_left = max(0, (game_duration - (pg.time.get_ticks() - start_ticks)) // 1000)
            all_sprites.update()
            
            # アイテムのランダム生成
            if random.randint(1, 30) == 1:
                apple = Apple()
                all_sprites.add(apple)
                apples.add(apple)

            # 当たり判定（キャッチ）
            caught_apples = pg.sprite.spritecollide(player, apples, True)
            for apple in caught_apples:
                score += 10
                # combo_system.add_combo() # 拡張機能4への連携例
                
            # boss_manager.update(player.rect) # 拡張機能2への連携例

            if seconds_left <= 0:
                game_state = "RESULT"

        # 3. 描画処理
        screen.fill((240, 255, 240))
        all_sprites.draw(screen)


        if game_state == "PLAY":
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            time_text = font.render(f"Time: {seconds_left}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            screen.blit(time_text, (680, 10))

        if seconds_left == 0:
            end_text = font.render("TIME UP!", True, (255, 0, 0))
            final_score_text = font.render(f"FINAL SCORE: {score}", True, (255, 0, 0))

            screen.blit(end_text, (400 - end_text.get_width() // 2, 260))
            screen.blit(final_score_text, (400 - final_score_text.get_width() // 2, 310))

        scene_manager.draw(screen, game_state, score)

        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()