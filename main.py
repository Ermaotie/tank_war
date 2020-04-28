import pygame, time, random
import sys


_display = pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)

class MainGame:
    """主游戏类"""
    window = None  # 游戏主窗口
    SCREEN_HEIGHT = 500  # 窗口的高度
    SCREEN_WIDTH = 800  # 窗口的宽度
    tank_1 = None
    EnemyTank_list = []
    EnemyTank_count = 5
    Bullet_list = []
    Enemy_bullet_list = []  # 存储敌方坦克子弹的列表
    Wall_list = []
    Wall_Count = random.randint(5, 10)
    Boom_list = []
    music = None

    def __init__(self):
        pass

    def startGame(self):
        """开始游戏"""
        _display.init()  # 初始化窗口
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH,
                                             MainGame.SCREEN_HEIGHT])  # 创建窗口并加载窗口(借鉴官方文档)
        MainGame.tank_1 = Tank(MainGame.SCREEN_WIDTH // 2, MainGame.SCREEN_HEIGHT - 70)  # 创建我方坦克
        _display.set_caption("坦克大战v1.03")  # 设置游戏的标题
        MainGame.music = Music('media/background.mp3')
        MainGame.music.play()
        self.createEnemyTank()
        self.createWall()



        while True:#让窗口持续刷新
            MainGame.window.fill(COLOR_BLACK)#给窗口完成一个填充颜色

            MainGame.window.blit(self.textshow(("敌方剩余坦克{}辆".format(len(MainGame.EnemyTank_list)))), (5, 5))
            MainGame.window.blit(self.textshow(("我方剩余生命{}点".format(MainGame.tank_1.hp))), (5, 30))
            MainGame.tank_1.displayTank()
            self.getevent()
            if MainGame.tank_1 and not MainGame.tank_1.stop:
                MainGame.tank_1.move()
            self.blitEnemyTank()
            self.blitBullet()
            self.blitEnemyBullet()
            self.blitWall()
            self.blitBoom()
            self.correct()
            MainGame.music.Allplay()
            time.sleep(0.02)
            _display.update()

    def getevent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # print('向左移动')
                    MainGame.tank_1.direction = 'L'
                    # MainGame.tank_1.move()
                    MainGame.tank_1.stop = False
                elif event.key == pygame.K_RIGHT:
                    # print('向右移动')
                    MainGame.tank_1.direction = 'R'
                    # MainGame.tank_1.move()
                    MainGame.tank_1.stop = False
                elif event.key == pygame.K_UP:
                    # print('向上移动')
                    MainGame.tank_1.direction = 'U'
                    # MainGame.tank_1.move()
                    MainGame.tank_1.stop = False
                elif event.key == pygame.K_DOWN:
                    # print('向下移动')
                    MainGame.tank_1.direction = 'D'
                    # MainGame.tank_1.move()
                    MainGame.tank_1.stop = False
                elif event.key == pygame.K_SPACE:
                    # print('发射子弹')
                    if len(MainGame.Bullet_list) < 4 and MainGame.tank_1.hp > 0:
                        m = Bullet(MainGame.tank_1)
                        MainGame.Bullet_list.append(m)
                elif event.key == pygame.K_ESCAPE:
                    MainGame.tank_1.hp = 5
                elif event.key == pygame.K_KP_PLUS:
                    MainGame.createEnemyTank(self)
                elif event.key == pygame.K_KP_MINUS:
                    MainGame.EnemyTank_list =[]
                elif event.key == pygame.K_m:
                    MainGame.music.pause()




            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_UP) or (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                    MainGame.tank_1.stop = True
    def textshow(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 20)
        textSurface = font.render(text, True, COLOR_RED)
        return textSurface
    def createEnemyTank(self):
        top = 100
        for i in range(MainGame.EnemyTank_count):
            left = random.randint(1, 7)
            speed = random.randint(3, 6)
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_list.append(eTank)

    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.hp > 0:
                eTank.displayTank()
                eTank.randMove()
                eBullet = eTank.shot()
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            # 如果子弹还活着，绘制出来，否则，直接从列表中删除子弹
            if eBullet.live:
                eBullet.displayBullet()
                # 让子弹移动
                eBullet.bulletmove()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)
    def blitBullet(self):
        for bullet in MainGame.Bullet_list :
            if bullet.live:
                bullet.displayBullet()
                bullet.bulletmove()
                bullet.hitEnemyTank()
                bullet.hitWall()
            else:
                MainGame.Bullet_list.remove(bullet)
        for bullet2 in MainGame.Enemy_bullet_list:
            if bullet2.live:
                bullet2.hitMyTank()
                bullet2.hitWall()
                bullet2.bulletmove()
    def createWall(self):
        for wall in range(random.randint(5, 10)):
            l = random.randint(1, 5)
            t = random.randint(1, 5)
            W = Wall(l * 100, t * 100)
            MainGame.Wall_list.append(W)

    def blitWall(self):
        for wall in MainGame.Wall_list:
            if wall.hp > 0:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)

    def blitBoom(self):
        for boom in MainGame.Boom_list:
            if boom.live:
                boom.displayExplode()
                pygame.time.delay(1)
                boom.live = False
            else:
                MainGame.Boom_list.remove(boom)

    def correct(self):
        for tank in MainGame.EnemyTank_list:
            for wall in MainGame.Wall_list:
                if pygame.sprite.collide_rect(tank, wall):
                    MainGame.Wall_list.remove(wall)

    def endGame(self):
        """结束游戏"""
        sys.exit()



class BaseItem(pygame.sprite.Sprite):
    """作为bullet,tank继承精灵类的桥梁"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
    """坦克类"""

    def __init__(self, left, top):
        self.images = {
            'U': pygame.image.load('img/tank_U.jpg'),
            'L': pygame.image.load('img/tank_L.jpg'),
            'R': pygame.image.load('img/tank_R.jpg'),
            'D': pygame.image.load('img/tank_D.jpg')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        self.live = True
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        self.hp = 5

    def move(self):
        """坦克的移动"""
        self.oldleft = self.rect.left
        self.oldtop = self.rect.top
        if self.hp > 0:
            if self.direction == 'L':
                if self.rect.left > 0 :
                    self.rect.left -= self.speed
            elif self.direction == 'R':
                if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                    self.rect.left += self.speed
            elif self.direction == 'U':
                if self.rect.top > 50:  # 为了不遮蔽上方的标题
                    self.rect.top -= self.speed
            elif self.direction == 'D':
                if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                    self.rect.top += self.speed
    # def stay(self):
    #     for wall in MainGame.Wall_list:
    #         if pygame.sprite.collide_rect(self, wall):
    #             self.rect.left = self.oldleft
    #             self.rect.top = self.oldtop
    #     if pygame.sprite.collide_rect(self, MainGame.tank_1):
    #         self.rect.left = self.oldleft
    #         self.rect.top = self.oldtop

    def stay(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.rect.left = self.oldleft
                self.rect.top = self.oldtop
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(self, eTank):
                self.rect.left = self.oldleft
                self.rect.top = self.oldtop

    def shot(self):
        """坦克的射击"""
        if self.hp >0:
            return Bullet(self)

    def displayTank(self):
        """展示坦克"""
        if self.hp > 0:
            self.stay()
            self.image = self.images[self.direction]
            MainGame.window.blit(self.image, self.rect)





class MyTank(Tank):
    """我方坦克类"""

    def __init__(self):
        self.hp = 5





class EnemyTank(Tank):
    """敌方坦克类"""

    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        self.images = {
            'U': pygame.image.load('img/enemy_U.jpg'),
            'L': pygame.image.load('img/enemy_L.jpg'),
            'R': pygame.image.load('img/enemy_R.jpg'),
            'D': pygame.image.load('img/enemy_D.jpg')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step = 50
        self.hp = 1
        # self.live = True

    def randMove(self):
        """随机移动"""
        if self.hp >0:
            self.stay()
            if self.step == 0:
                self.direction = self.randDirection()
                self.step = 50
            else:
                self.move()
                self.step -= 1

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def stay(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.rect.left = self.oldleft
                self.rect.top = self.oldtop
        if pygame.sprite.collide_rect(self, MainGame.tank_1):
            self.rect.left = self.oldleft
            self.rect.top = self.oldtop

    def shot(self):
        num = random.randint(1, 1000)
        if num <= 30:
            return Bullet(self)

class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('img/zd.jpg')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        self.speed = 7  # 速度
        self.live = True

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):
                self.live = False
                eBoom = Explode(eTank)
                MainGame.Boom_list.append(eBoom)
                eTank.hp -= 1

    def hitMyTank(self):
        if pygame.sprite.collide_rect(MainGame.tank_1, self):
            self.live = False
            MainGame.tank_1.hp -= 1

    def hitWall(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):
                self.live = False
                wall.hp -= 1

    def bulletmove(self):
        """子弹的移动"""
        if self.direction == 'U':
            if self.rect.top > 50:
                self.rect.top -= self.speed
            else:
                self.live = False  # 修改状态值
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                self.live = False  # 修改状态值
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False  # 修改状态值
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                self.live = False  # 修改状态值

    def displayBullet(self):
        """展示子弹"""
        MainGame.window.blit(self.image, self.rect)


class Explode(BaseItem):
    """爆炸效果类"""

    def __init__(self, tank):
        self.image = pygame.image.load('img/boom.png')
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x
        self.rect.y = tank.rect.y

        self.live = True
    def displayExplode(self):
        """展示爆炸效果"""

        MainGame.window.blit(self.image, self.rect)


class Wall(BaseItem):
    """墙壁类"""

    def __init__(self, left, top):
        # super(Wall, self).__init__(left, top)
        self.image = pygame.image.load('img/wall_1.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.hp = 3


    def displayWall(self):
        """展示墙壁"""
        MainGame.window.blit(self.image, self.rect)


class Music:
    """音效类"""

    def __init__(self, filename):
        self.filename = filename
        pygame.mixer.init()
        self.music = pygame.mixer.music.load(self.filename)
        self.time = pygame.mixer.music.get_pos()
        self.old_time = self.time
        self.num = 1



    def play(self):
        """开始播放音乐"""
        pygame.mixer.music.play(loops=0)

    def pause(self):
        # self.time = pygame.mixer.music.get_pos()
        # if self.time == self.old_time:
        #     self.old_time = self.time
        #     pygame.mixer.music.unpause()
        # elif self.time != self.old_time:
        #     self.old_time = self.time
        #     pygame.mixer.music.pause()

        # 在流中即视为正在播放
        # if pygame.mixer.music.get_busy() == 1:
        #     pygame.mixer.music.pause()
        # else:
        #     pygame.mixer.music.unpause()

        if self.num % 2 == 1:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.num += 1

    def Allplay(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()


MainGame().startGame()

