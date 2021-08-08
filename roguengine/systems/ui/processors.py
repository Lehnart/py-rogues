from roguengine.systems.render.events import DrawStringEvent
from roguengine.rogue_esper import Processor
from roguengine.systems.ui.components import *
from roguengine.util.font import Font


class BlinkProcessor(Processor):

    def __init__(self):
        super().__init__()

    def process(self):

        for ent, comp in self.world.get_component(BlinkingComponent):

            last_time = comp.get_last_blinking_time()
            now = time.time()
            if now > last_time + comp.get_period():
                comp.blink()


class UIProcessor(Processor):

    def __init__(self, font: Font):
        super().__init__()
        self.font = font

    def process(self):

        label_components = self.world.get_component(LabelComponent)
        for ent, label in label_components:
            x, y = label.get_position()
            s = label.get_label()

            if self.world.has_component(ent, BlinkingComponent) and self.world.component_for_entity(ent,
                                                                                                    BlinkingComponent).get_blinking_count() % 2 == 1:
                self.world.publish(DrawStringEvent(s, x, y, label.get_bkgd_color(), label.get_bkgd_color(), self.font))
            else:
                self.world.publish(DrawStringEvent(s, x, y, label.get_font_color(), label.get_bkgd_color(), self.font))

        dynamic_label_components = self.world.get_component(DynamicLabelComponent)
        for _, label in dynamic_label_components:
            x, y = label.get_position()
            s = label.get_callable()(self.world)
            self.world.publish(DrawStringEvent(s, x, y, label.get_font_color(), label.get_bkgd_color(), self.font))

        menu_components = self.world.get_component(MenuComponent)
        for _, menu in menu_components:
            labels = menu.get_labels()
            selected_index = menu.get_selected()

            for i, label in enumerate(labels):
                if selected_index is not None and i == selected_index:
                    self.world.publish(DrawStringEvent(label.s, label.px, label.py, menu.get_selected_color(), label.bkgd_color, self.font))
                else:
                    self.world.publish(DrawStringEvent(label.s, label.px, label.py, label.font_color, label.bkgd_color, self.font))

        gauge_components = self.world.get_component(GaugeComponent)
        for _, gauge in gauge_components:
            x, y = gauge.px, gauge.py
            v = gauge.value_function(self.world)
            v_max = gauge.value_max_function(self.world)
            if v_max <= 0.:
                continue

            r = v / v_max
            bkgd_color = gauge.color_threshold[-1][1]
            for v, color in gauge.color_threshold:
                if r <= v:
                    bkgd_color = color
                    break

            w = int((r * gauge.width) / self.font.get_char_width())
            s = gauge.label
            self.world.publish(DrawStringEvent(s[:w].ljust(w), x, y, gauge.font_color, bkgd_color, self.font))
