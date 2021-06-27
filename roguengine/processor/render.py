import pygame

from roguengine.component.sprite import VisibleSpriteComponent, InvisibleSpriteComponent
from roguengine.component.viewed import ViewedComponent
from roguengine.component.visible import VisibleComponent
from roguengine.component.window import WindowComponent
from roguengine.rogue_esper import Processor


class RenderProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        for window_entity, [window_component] in self.world.get_components(WindowComponent):
            self._draw_on_window(window_component)

    def _draw_on_window(self, window_component: WindowComponent):

        window_surface = window_component.surface()
        sprite_components = [sprite_component for _, [sprite_component, _] in self.world.get_components(VisibleSpriteComponent, VisibleComponent)]

        invisible_sprite_components = [
            sprite_component
            for ent, [sprite_component, _] in self.world.get_components(InvisibleSpriteComponent, ViewedComponent)
            if not self.world.has_component(ent, VisibleComponent)
        ]

        sprite_components.extend(invisible_sprite_components)

        sprite_components.sort(key=lambda s: s.layer())
        sprite_components = [s for s in sprite_components if s.is_shown()]
        for sprite_component in sprite_components:
            window_surface.blit(sprite_component.sprite(), sprite_component.top_left_pixel_position())

        pygame.display.flip()
        window_surface.fill((0, 0, 0))
