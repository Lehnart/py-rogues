import pygame

from roguengine.rogue_esper import Processor
from roguengine.systems.render.components import WindowComponent, InvisibleSpriteComponent, VisibleSpriteComponent
from roguengine.systems.render.events import DrawStringEvent, UpdateSpritePositionEvent, FlipEvent
from roguengine.systems.view.components import VisibleComponent, ViewedComponent


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

        for msg in self.world.receive(UpdateSpritePositionEvent):
            sprite: VisibleSpriteComponent = self.world.component_for_entity(msg.ent, VisibleSpriteComponent)
            sprite.set_position(msg.x, msg.y)

        for msg in self.world.receive(FlipEvent):
            sprite: VisibleSpriteComponent = self.world.component_for_entity(msg.ent, VisibleSpriteComponent)
            sprite.flip()

        for msg in self.world.receive(DrawStringEvent):
            font = msg.font
            font.draw_string(msg.s, msg.x, msg.y, window_surface, msg.font_color, msg.bkgd_color)

        pygame.display.flip()
        window_surface.fill((0, 0, 0))
