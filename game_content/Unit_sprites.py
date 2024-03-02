class Unit(MapObject):
    def __init__(self, grid_pos):
        super().__init__(grid_pos)
        self.name = "unit"
        self.max_stamina = None
        self.stamina = None
        self.price = None
        self.view_range = 4
        self.hexes_viewed = []

    def move(self, grid_pos, distance):
        self.grid_pos = grid_pos
        self.stamina -= distance
        # self.map_coord = self.calculate_coordinate_by_hex_position(self.grid_pos)

    def restore_stamina(self):
        self.stamina = self.max_stamina

    def hide_hexes(self):
        [hex.hide_hex() for hex in self.hexes_viewed]
        self.hexes_viewed = []

    def view_hexes(self):
        [hex.view_hex() for hex in self.hexes_viewed]


class MilitaryUnit(Unit):
    def __init__(self, grid_pos, player_id, ):
        super().__init__(grid_pos)
        self.player_id = player_id
        self.attack = None
        self.hp = 10
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw()
        self.discovery_range = 2

    def __repr__(self):
        return f"{self.__class__}, {self.player_id}, {self.hp}"

    def draw_shape(self):
        pass

    def draw(self):
        self.draw_shape()
        self.health_bar = Health_bar(0, 0, self.width, self.height / 4, self.hp)
        self.health_bar.draw(self.image, self.hp)

    def strike(self):
        self.stamina = 0
        return self.attack * (random.random() / 2 + 0.75)

    def defend(self):
        return self.attack * (random.random() / 2 + 0.25)

    def update_hp(self, ):
        if self.hp > 0:
            self.health_bar.draw(self.image, self.hp)


class TriangularUnit(MilitaryUnit):

    def __init__(self, grid_pos, player_id, color=(255, 0, 0)):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.price = 30
        self.hp = 3
        self.name = "triangular unit"
        self.attack = 3
        self.max_stamina = 1
        self.stamina = 1
        self.draw()

    def draw_shape(self):
        pygame.draw.polygon(self.image, self.color, [(0, self.height / 4 + 2), (self.width / 2, self.height),
                                                     (self.width - 1, self.height / 4 + 2)])

    def __repr__(self):
        return f" unit {self.__class__} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class SquareUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.name = "square unit"
        self.price = 30
        self.attack = 2
        self.hp = 3
        self.max_stamina = 2
        self.stamina = 2
        self.draw()

    def draw_shape(self):
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))

    def __repr__(self):
        return f"{self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]} player {self.player_id}"


class WarBase(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id)
        self.name = "war base"
        self.max_stamina = 0
        self.stamina = 0

        self.attack = 0
        self.hp = 10
        self.draw()

    def draw_shape(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, self.height / 4 + 2, self.width,
                                                 self.height - self.height / 4 + 2))

    def __repr__(self):
        return f"{self.name} on hex {self.grid_pos[0]}, {self.grid_pos[1]}, player {self.player_id}"


class CircleUnit(MilitaryUnit):
    def __init__(self, grid_pos, player_id, color):
        self.color = color
        super().__init__(grid_pos, player_id, )
        self.name = "circle unit"
        self.price = 30
        self.attack = 1
        self.hp = 3
        self.max_stamina = 3
        self.stamina = 3
        self.draw()

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.width / 2, self.height / 2), 10)
