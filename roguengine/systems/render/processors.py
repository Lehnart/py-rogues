import datetime

import pygame

from roguengine.rogue_esper import Processor
from roguengine.systems.render.components import WindowComponent, InvisibleSpriteComponent, VisibleSpriteComponent
from roguengine.systems.render.events import DrawStringEvent, UpdateSpritePositionEvent, FlipEvent, MoveSpriteEvent, CreateSpriteEvent, SetSpriteEvent
from roguengine.systems.view.tools import has_been_viewed, is_visible

FRAME_PER_SECONDS = 60


class RenderProcessor(Processor):

    def __init__(self):
        super().__init__()
        self.last_time_drawn = datetime.datetime.now()

    def process(self):

        for msg in self.world.receive(MoveSpriteEvent):
            sprite: VisibleSpriteComponent = self.world.component_for_entity(msg.ent, VisibleSpriteComponent)
            sprite.move(msg.dx, msg.dy)

        for msg in self.world.receive(UpdateSpritePositionEvent):
            sprite: VisibleSpriteComponent = self.world.component_for_entity(msg.ent, VisibleSpriteComponent)
            sprite.set_position(msg.x, msg.y)

        for msg in self.world.receive(FlipEvent):
            sprite: VisibleSpriteComponent = self.world.component_for_entity(msg.ent, VisibleSpriteComponent)
            sprite.flip()

        for msg in self.world.receive(CreateSpriteEvent):
            ent = msg.ent
            if not msg.is_invisible:
                sprite_comp = VisibleSpriteComponent(msg.px, msg.py, msg.sprite, msg.layer)
            else:
                sprite_comp = InvisibleSpriteComponent(msg.px, msg.py, msg.sprite, msg.layer)
            self.world.add_component(ent, sprite_comp)

        for msg in self.world.receive(SetSpriteEvent):
            ent = msg.ent
            if not msg.is_invisible and self.world.has_component(ent, VisibleSpriteComponent):
                visible_sprite = self.world.component_for_entity(ent, VisibleSpriteComponent)
                px, py = visible_sprite.top_left_pixel_position()
                layer = visible_sprite.layer()
                self.world.remove_component(ent, VisibleSpriteComponent)
                sprite_comp = VisibleSpriteComponent(
                    px,
                    py,
                    msg.sprite,
                    layer
                )
                self.world.add_component(ent, sprite_comp)

            elif self.world.has_component(ent, InvisibleSpriteComponent):
                invisible_sprite = self.world.component_for_entity(ent, InvisibleSpriteComponent)
                px, py = invisible_sprite.top_left_pixel_position()
                layer = invisible_sprite.layer()
                self.world.remove_component(ent, InvisibleSpriteComponent)
                sprite_comp = InvisibleSpriteComponent(
                    px,
                    py,
                    msg.sprite,
                    layer
                )
                self.world.add_component(ent, sprite_comp)

        for window_entity, [window_component] in self.world.get_components(WindowComponent):
            self._draw_on_window(window_component)

    def _draw_on_window(self, window_component: WindowComponent):

        if datetime.datetime.now() - self.last_time_drawn < datetime.timedelta(seconds=1. / FRAME_PER_SECONDS):
            return
        self.last_time_drawn = datetime.datetime.now()

        window_surface = window_component.surface()
        sprite_components = [
            sprite_component
            for sprite_ent, [sprite_component] in self.world.get_components(VisibleSpriteComponent)
            if is_visible(self.world, sprite_ent)
        ]

        invisible_sprite_components = [
            sprite_component
            for sprite_ent, [sprite_component] in self.world.get_components(InvisibleSpriteComponent)
            if has_been_viewed(self.world, sprite_ent) and not is_visible(self.world, sprite_ent)
        ]

        sprite_components.extend(invisible_sprite_components)

        sprite_components.sort(key=lambda s: s.layer())
        sprite_components = [s for s in sprite_components if s.is_shown()]
        for sprite_component in sprite_components:
            window_surface.blit(sprite_component.sprite(), sprite_component.top_left_pixel_position())

        for msg in self.world.receive(DrawStringEvent):
            font = msg.font
            font.draw_string(msg.s, msg.x, msg.y, window_surface, msg.font_color, msg.bkgd_color)

        pygame.display.flip()
        window_surface.fill((0, 0, 0))
