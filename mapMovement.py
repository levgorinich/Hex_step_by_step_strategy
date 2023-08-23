import pygame

class MapMovementTracker(pygame.sprite.Group):
    def __init__(self, internal_surface_size, display_surface_size):
        super().__init__()
        self.internal_surface_size = internal_surface_size
        self.internal_surface_size_vector = pygame.math.Vector2(internal_surface_size)
        self.display_surface_size = display_surface_size



        self.offset = pygame.math.Vector2(0,0)
        self.display_surface_half_width = self.display_surface_size[0] // 2
        self.display_surface_half_height = self.display_surface_size[1] // 2

        # moving camera with mouse
        self.camera_borders = {'left':10, 'right':10, 'top':10, 'bottom':10}
        l = self.camera_borders['left']
        r = self.camera_borders['top']
        w = self.display_surface_size[0] -(self.camera_borders['right'] + self.camera_borders['left'])
        h = self.display_surface_size[1] -(self.camera_borders['bottom'] + self.camera_borders['top'])
        self.camera_rect = pygame.Rect(l, r, w, h)

        self.mouse_speed= 0.4

        # camera control
        self.mouse_pos_down = pygame.math.Vector2(0,0)
        self.mouse_pos_up = pygame.math.Vector2(0,0)
        self.drag_flag = False

        # zoom
        self.zoom_scale = 1

        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2(0,0)
        self.internal_offset.x = self.internal_surface_size[0]//2 - self.display_surface_half_width
        self.internal_offset.y = self.internal_surface_size[1]//2 - self.display_surface_half_height
    def screen_movement_with_mouse_dragging(self, events_list):

        for event in events_list:
            # controlling zoom
            if event.type == pygame.MOUSEWHEEL:
                self.zoom_scale += event.y * 0.03
                if self.zoom_scale > 1.0 and event.y >0:
                    self.zoom_scale =1.0
                if self.zoom_scale<0.75 and event.y < 0:
                    self.zoom_scale = 0.75
            if event.type == pygame.MOUSEBUTTONDOWN:

                self.mouse_pos_down = pygame.math.Vector2(pygame.mouse.get_pos())
                self.drag_flag = True


            if self.drag_flag:
                mouse_pos_up = pygame.math.Vector2(pygame.mouse.get_pos())

                if mouse_pos_up.distance_to(self.mouse_pos_down) > 10:


                    self.offset+= (mouse_pos_up - self.mouse_pos_down) * self.mouse_speed
                    if self.offset.x < -self.internal_offset.x:
                        self.offset.x= -self.internal_offset.x
                    if self.offset.x > self.internal_surface_size[0] - self.display_surface_size[0] :
                        self.offset.x = self.internal_surface_size[0] - self.display_surface_size[0]
                    if self.offset.y < -self.internal_offset.y:
                        self.offset.y=-self.internal_offset.y
                    if self.offset.y > self.internal_surface_size[1] - self.display_surface_size[1] :
                        self.offset.y = self.internal_surface_size[1] - self.display_surface_size[1]

                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag_flag = False
                self.mouse_pos_down = mouse_pos_up

        def screen_mouse_control_with_moving(self):
            mouse = pygame.math.Vector2(pygame.mouse.get_pos())
            mouse_offset_vector = pygame.math.Vector2(0,0)

            left_border = self.camera_borders['left']
            top_border = self.camera_borders['top']
            right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
            bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

            if top_border < mouse.y < bottom_border:
                if mouse.x < left_border:
                    mouse_offset_vector.x = mouse.x - left_border
                    pygame.mouse.set_pos((left_border, mouse.y))
                if mouse.x > right_border:
                    mouse_offset_vector.x =  mouse.x - right_border
                    pygame.mouse.set_pos((right_border, mouse.y))

            elif mouse.y < top_border:
                if mouse.x < left_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)

                    pygame.mouse.set_pos((left_border, top_border))
                if mouse.x > right_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                    pygame.mouse.set_pos((right_border, top_border))


            if left_border < mouse.x < right_border:
                if mouse.y < top_border:
                    mouse_offset_vector.y = mouse.y - top_border
                    pygame.mouse.set_pos((mouse.x, top_border))
                if mouse.y > bottom_border:
                    mouse_offset_vector.y =  mouse.y - bottom_border
                    pygame.mouse.set_pos((mouse.x, bottom_border))

            elif mouse.y > bottom_border:
                if mouse.x < left_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                    pygame.mouse.set_pos((left_border, bottom_border))
                if mouse.x > right_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                    pygame.mouse.set_pos((right_border, bottom_border))
            self.offset -= mouse_offset_vector *self.mouse_speed


    def get_total_offset(self):
        return self.offset+self.internal_offset
    def get_dragging_offset(self):
        return self.offset
    def get_internal_offset(self):
        zoom_scale = self.get_zoom()
        internal_offset = pygame.math.Vector2(0,0)
        internal_offset.x = self.internal_surface_size[0]//2 - self.display_surface_half_width*(1/zoom_scale)
        internal_offset.y = self.internal_surface_size[1]//2 - self.display_surface_half_height*(1/zoom_scale)
        return internal_offset
    def get_internal_surface_scale(self):

        return self.zoom_scale * self.internal_surface_size_vector
    def get_zoom(self):
        return self.zoom_scale
        