from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import sys
import katmanlar
import gorunurluk

pygame.init()
width = None
height = None
display = None
clock = pygame.time.Clock()
ground = 50
velocity = 2.0

# Gorunurluk sınıfınfa ekranı ayarlar
def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground
    gorunurluk.init(display)

# Tüm domuzlar (pigs), kuşlar (birds) ve blokların (blocks) hareketlerinin durup durmadığını kontrol eder:
def all_rest(pigs, birds, blocks):
    # Belirlenen threshold değerinden (0.15) daha yüksek bir hızda olan herhangi bir öğe varsa False döner.
    # Tüm öğeler belirlenen hızdan düşükse True döner.
    threshold = 0.15
    for pig in pigs:
        if pig.velocity.magnitude >= threshold:
            return False

    for bird in birds:
        if bird.velocity.magnitude >= threshold:
            return False

    for block in blocks:
        if block.velocity.magnitude >= threshold:
            return False

    return True

# Oyunu kapatmak için kullanılır:
def close():
    pygame.quit()
    sys.exit()

# this class, oyun haritaları ve seviyeleri yönetir.
class Maps:
    # Haritayı başlangıç seviyesine getirir
    def __init__(self):
        self.level = 1
        self.max_level = 3
        self.color = {'background': (51, 51, 51)}
        self.score = 0
    # Yeni bir seviyeye geçerken 3 saniye bekler. Bu süre zarfında kullanıcı girişlerini kontrol eder.
    def wait_level(self):
        time = 0
        while time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
            time += 1
            clock.tick(1)
        return

    # Domuzların ve kuşların varlığına bağlı olarak oyunun kazanılıp kazanılmadığını kontrol eder
    def check_win(self, pigs, birds):
        if pigs == []:
            print("WON!")
            return True
        if (not pigs == []) and birds == []:
            print("LOST!")
            return False

    # Oyun duraklatıldığında gösterilecek menüyü ve düğmeleri oluşturur:
    def pause(self):
        pause_text = gorunurluk.Label(700, 200, 400, 200, None, self.color['background'])
        pause_text.add_text("GAME PAUSED", 70, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = gorunurluk.Button(350, 500, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.add_text("RESTART", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        resume = gorunurluk.Button(750, 500, 300, 100, None, (88, 214, 141), (171, 235, 198))
        resume.add_text("RESUME", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = gorunurluk.Button(1150, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        bbms = gorunurluk.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        bbms.add_text("BBms", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_p:
                        return
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if resume.isActive():
                        return
                    if exit.isActive():
                        exit.action()

            replay.draw()
            resume.draw()
            exit.draw()
            pause_text.draw()
            bbms.draw()

            pygame.display.update()
            clock.tick(60)

    # Seviyeye göre oyun öğelerini (kuşlar, domuzlar, bloklar) oluşturur ve start_level fonksiyonunu çağırır.
    def draw_map(self):
        birds = []
        pigs = []
        blocks = []
        walls = []
        self.score = 0

        # Seviyeleri oluşturduk
        # levellerde rastgele pig ve block atamsı yapar.
        if self.level == 1:
            for i in range(3):
                new_bird = katmanlar.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(katmanlar.Pig(1100, height - 40, 20))
            pigs.append(katmanlar.Pig(1500, height - 40, 20))

            blocks.append(katmanlar.Block(1300, height - 60, 60))

        elif self.level == 2:
            for i in range(3):
                new_bird = katmanlar.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(katmanlar.Pig(1000, height - 40, 20))
            pigs.append(katmanlar.Pig(1400, height - 40, 20))

            blocks.append(katmanlar.Block(1200, height - 60, 60))
            blocks.append(katmanlar.Block(1200, height - 2*35, 60))
            blocks.append(katmanlar.Block(1500, height - 60, 60))

        elif self.level == 3:
            for i in range(3):
                new_bird = katmanlar.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(katmanlar.Pig(1200, height - 60, 30))
            pigs.append(katmanlar.Pig(1300, height - 60, 30))

            blocks.append(katmanlar.Block(1000, height - 100, 100))
            blocks.append(katmanlar.Block(1000, height - 2*60, 100))
            blocks.append(katmanlar.Block(1500, height - 100, 100))
            blocks.append(katmanlar.Block(1500, height - 2*60, 100))

        self.start_level(birds, pigs, blocks, walls)

    # Mevcut seviyeyi tekrar başlatır (seviye sayısını bir azaltır ve haritayı tekrar çizer).
    def replay_level(self):
        self.level -= 1
        self.draw_map()

    # Oyunu baştan başlatır (seviye 1'e döner ve haritayı tekrar çizer).
    def start_again(self):
        self.level = 1
        self.draw_map()

    #Seviyeyi geçtiğinde yapılacak işlemleri tanımlar:
    def level_cleared(self):
        self.level += 1

        level_cleared_text = gorunurluk.Label(700, 100, 400, 200, None, self.color['background'])
        if self.level <= self.max_level:
            level_cleared_text.add_text("LEVEL " + str(self.level - 1) + " CLEARED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        else:
            level_cleared_text.add_text("ALL LEVEL CLEARED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        score_text = gorunurluk.Label(750, 300, 300, 100, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = gorunurluk.Button(350, 500, 300, 100, self.replay_level, (244, 208, 63), (247, 220, 111))
        replay.add_text("PLAY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        if self.level <= self.max_level:
            next = gorunurluk.Button(750, 500, 300, 100, self.draw_map, (88, 214, 141), (171, 235, 198))
            next.add_text("CONTINUE", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        else:
            next = gorunurluk.Button(750, 500, 300, 100, self.start_again, (88, 214, 141), (171, 235, 198))
            next.add_text("START AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = gorunurluk.Button(1150, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        bbms = gorunurluk.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        bbms.add_text("BBMS", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        #Oynat (replay), devam et (next) veya tekrar başlat (start again) düğmelerini oluşturur.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if next.isActive():
                        next.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            next.draw()
            exit.draw()
            level_cleared_text.draw()
            score_text.draw()
            bbms.draw()

            pygame.display.update()
            clock.tick(60)

    # Seviye başarısız olduğunda yapılacak işlemleri tanımlar
    def level_failed(self):
        level_failed_text = gorunurluk.Label(700, 100, 400, 200, None, self.color['background'])
        level_failed_text.add_text("LEVEL FAILED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        score_text = gorunurluk.Label(750, 300, 300, 100, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = gorunurluk.Button(500, 500, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.add_text("TRY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = gorunurluk.Button(1000, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        bbms = gorunurluk.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        bbms.add_text("BBMS", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        # Tekrar dene (replay) ve çıkış (exit) düğmelerini oluşturur.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            exit.draw()
            level_failed_text.draw()
            score_text.draw()
            bbms.draw()

            pygame.display.update()
            clock.tick(60)

    # Seviyeyi başlatır ve ana oyun döngüsünü yönetir
    def start_level(self, birds, pigs, blocks, walls):
        # Oyun döngüsünün devam etmesini kontrol eder.
        loop = True
        
        # Sapanı ve ilk kuşu yükler.
        slingshot = katmanlar.Slingshot(200, height - 200, 30, 200)
        birds[0].load(slingshot)

        # Fare tıklamasını kontrol etmek için kullanılır.
        mouse_click = False
        # Kuşun yüklü olup olmadığını kontrol etmek için kullanılır.
        flag = 1

        # Çarpışma sonucu yok edilmesi gereken domuzlar ve bloklar için listeler.
        pigs_to_remove = []
        blocks_to_remove = []

        # oyun ekranında skor, kalan kuş sayısı ve kalan domuz sayısını göstermek için kullanılır.
        score_text = gorunurluk.Label(50, 10, 100, 50, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        birds_remaining = gorunurluk.Label(120, 50, 100, 50, None, self.color['background'])
        birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        pigs_remaining = gorunurluk.Label(110, 90, 100, 50, None, self.color['background'])
        pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        bbms = gorunurluk.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        bbms.add_text("BBMS", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        # Main Game
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        self.draw_map()
                    if event.key == pygame.K_p:
                        self.pause()
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                # Sapanın çekip bırakmayı kontrol eder
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if birds[0].mouse_selected():
                        mouse_click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = False
                    if birds[0].mouse_selected():
                        flag = 0
            #Kuş Yüklü değilse ve Tüm Öğeler Durduysa, ilk kuşun yüklü olup olmadığını ve tüm öğelerin durup durmadığını kontrol eder.
            if (not birds[0].loaded) and all_rest(pigs, birds, blocks):
                print("LOADED!")
                birds.pop(0)
                if self.check_win(pigs, birds) == 1:
                    self.score += len(birds)*100
                    self.level_cleared()
                elif self.check_win(pigs,birds) == 0:
                    self.level_failed()

                if not birds == []:
                    birds[0].load(slingshot)
                flag = 1

            # Fare tıklaması devam ettiği sürece, kuşun yeniden konumlandırılmasını sağlar.
            if mouse_click:
                birds[0].reposition(slingshot, mouse_click)
            # Kuş yüklü değilse, kuşu sapanla bırakır.
            if not flag:
                birds[0].unload()

            # Oyun ekranının arka planını çizer.
            display.fill(self.color['background'])
            color = self.color['background']
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(display, color, (0, i*300, width, 300))
            pygame.draw.rect(display, (77, 86, 86), (0, height, width, 50))
            slingshot.draw(birds[0])

            #Sapanı ve yüklenmiş kuşu çizer.
            # Domuzların bloklarla çarpışmasını kontrol eder ve hız değişikliklerine göre yok edilecek domuz ve blokları belirler.
            for i in range(len(pigs)):
                for j in range(len(blocks)):
                    pig_v, block_v = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    pigs[i], blocks[j], result_block_pig = katmanlar.collision_handler(pigs[i], blocks[j], "BALL_N_BLOCK")
                    pig_v1, block_v1 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block_pig:
                        if abs(pig_v - pig_v1) > velocity:
                            blocks_to_remove.append(blocks[j])
                            blocks[j].destroy()
                        if abs(block_v - block_v1) > velocity:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].dead()
            # Kuşların bloklarla çarpışmasını kontrol eder ve hız değişikliklerine göre yok edilecek blokları belirler.
            for i in range(len(birds)):
                if not (birds[i].loaded or birds[i].velocity.magnitude == 0):
                    for j in range(len(blocks)):
                        birds_v, block_v = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        birds[i], blocks[j], result_bird_block = katmanlar.collision_handler(birds[i], blocks[j], "BALL_N_BLOCK")
                        birds_v1, block_v1 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude

                        if result_bird_block:
                            if abs(birds_v - birds_v1) > velocity:
                                if not blocks[j] in blocks_to_remove:
                                    blocks_to_remove.append(blocks[j])
                                    blocks[j].destroy()
            # Domuzların hareketini ve diğer domuzlarla veya duvarlarla çarpışmasını kontrol eder. 
            # Çarpışma sonucunda yok edilmesi gereken domuzları belirler.
            for i in range(len(pigs)):
                pigs[i].move()
                for j in range(i+1, len(pigs)):
                    pig1_v, pig2_v = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    pigs[i], pigs[j], result = katmanlar.collision_handler(pigs[i], pigs[j], "BALL")
                    pig1_v1, pig2_v1 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    result = True
                    if result:
                        if abs(pig1_v - pig1_v1) > velocity:
                            if not pigs[j] in pigs_to_remove:
                                pigs_to_remove.append(pigs[j])
                                pigs[j].dead()
                        if abs(pig2_v - pig2_v1) > velocity:
                            if not pigs[i] in pigs_to_remove:
                                pigs_to_remove.append(pigs[i])
                                pigs[i].dead()

                for wall in walls:
                    pigs[i] = wall.collision_manager(pigs[i])

                pigs[i].draw()
            
            # Kuşların hareketini ve diğer kuşlarla veya duvarlarla çarpışmasını kontrol eder. 
            # Çarpışma sonucunda yok edilmesi gereken kuşları belirler.
            for i in range(len(birds)):
                if (not birds[i].loaded) and birds[i].velocity.magnitude:
                    birds[0].move()
                    for j in range(len(pigs)):
                        bird_v, pig_v = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        birds[i], pigs[j], result_bird_pig = katmanlar.collision_handler(birds[i], pigs[j], "BALL")
                        bird_v1, pig_v1 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        result = True
                        if result_bird_pig:
                            if abs(bird_v - bird_v1) > velocity:
                                if not pigs[j] in pigs_to_remove:
                                    pigs_to_remove.append(pigs[j])
                                    pigs[j].dead()

                if birds[i].loaded:
                    birds[i].project_path()

                for wall in walls:
                    birds[i] = wall.collision_manager(birds[i])

                birds[i].draw()

            # Blokların hareketini sağlar ve ekran
            for i in range(len(blocks)):
                for j in range(i + 1, len(blocks)):
                    block1_v, block2_v = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    blocks[i], blocks[j], result_block = katmanlar.block_collision_handler(blocks[i], blocks[j])
                    block1_v1, block2_v1 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block:
                        if abs(block1_v - block1_v1) > velocity:
                            if not blocks[j] in blocks_to_remove:
                                blocks_to_remove.append(blocks[j])
                                blocks[j].destroy()
                        if abs(block2_v - block2_v1) > velocity:
                            if not blocks[i] in blocks_to_remove:
                                blocks_to_remove.append(blocks[i])
                                blocks[i].destroy()

                blocks[i].move()

                for wall in walls:
                    blocks[i] = wall.collision_manager(blocks[i], "BLOCK")

                blocks[i].draw()

            for wall in walls:
                wall.draw()

            score_text.add_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            score_text.draw()

            birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            birds_remaining.draw()

            pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            pigs_remaining.draw()

            bbms.draw()

            pygame.display.update()

            # son işlemler
            if all_rest(pigs, birds, blocks):
                # Yok edilmesi gereken domuzların listesini döngüyle iter.
                for pig in pigs_to_remove:
                    if pig in pigs:
                        pigs.remove(pig)
                        self.score += 100

                # Yok edilmesi gereken blokların listesini döngüyle iter.
                for block in blocks_to_remove:
                    if block in blocks:
                        blocks.remove(block)
                        self.score += 50
                # listeleri boşaltılarak, bir sonraki çarpışma kontrolü için hazırlanır.
                pigs_to_remove = []
                blocks_to_remove = []
            clock.tick(60)