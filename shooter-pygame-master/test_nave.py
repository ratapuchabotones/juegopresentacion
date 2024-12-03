import unittest
import pygame
from main import Player, Meteor, Bullet 

pygame.init()
WIDTH = 800
HEIGHT = 600
bullets = pygame.sprite.Group()  

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Crea un jugador para usar en las pruebas."""
        self.player = Player()

    def test_initial_position(self):
        """Verifica que el jugador esté en la posición inicial correcta."""
        self.assertEqual(self.player.rect.centerx, WIDTH // 2)
        self.assertEqual(self.player.rect.bottom, HEIGHT - 10)

    def test_movement_left(self):
        """Verifica que el jugador se mueva hacia la izquierda."""
        self.player.rect.x = 400  # Establecemos una posición de prueba
        self.player.speed_x = -5
        self.player.update()
        self.assertEqual(self.player.rect.x, 395)

    def test_movement_right(self):
        """Verifica que el jugador se mueva hacia la derecha."""
        self.player.rect.x = 400
        self.player.speed_x = 5
        self.player.update()
        self.assertEqual(self.player.rect.x, 405)

    def test_shoot(self):
        """Verifica que el jugador pueda disparar."""
        initial_bullet_count = len(bullets)
        self.player.shoot()
        self.assertEqual(len(bullets), initial_bullet_count + 1)

class TestMeteor(unittest.TestCase):

    def setUp(self):
        """Crea un meteor para usar en las pruebas."""
        self.meteor = Meteor()

    def test_initial_position(self):
        """Verifica que el meteoro esté dentro de los límites iniciales."""
        self.assertTrue(0 <= self.meteor.rect.x <= WIDTH - self.meteor.rect.width)
        self.assertTrue(-100 <= self.meteor.rect.y <= -40)

    def test_movement(self):
        """Verifica que el meteoro se mueva correctamente."""
        initial_x = self.meteor.rect.x
        initial_y = self.meteor.rect.y
        self.meteor.update()
        self.assertNotEqual(self.meteor.rect.y, initial_y)
        self.assertNotEqual(self.meteor.rect.x, initial_x)

class TestBullet(unittest.TestCase):

    def setUp(self):
        """Crea una bala para usar en las pruebas."""
        self.bullet = Bullet(400, 300)

    def test_initial_position(self):
        """Verifica que la bala se cree en la posición correcta."""
        self.assertEqual(self.bullet.rect.centerx, 400)
        self.assertEqual(self.bullet.rect.y, 300)

    def test_bullet_movement(self):
        """Verifica que la bala se mueva hacia arriba."""
        initial_y = self.bullet.rect.y
        self.bullet.update()
        self.assertEqual(self.bullet.rect.y, initial_y - 10)

if __name__ == "__main__":
    unittest.main()
