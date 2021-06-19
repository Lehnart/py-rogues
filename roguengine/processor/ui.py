from roguengine.component.dynamic_label import DynamicLabelComponent
from roguengine.component.gauge import GaugeComponent
from roguengine.component.label import LabelComponent
from roguengine.component.window import WindowComponent
from roguengine.esper import Processor
from roguengine.util.font import Font


class UI(Processor):

    def __init__(self, font: Font):
        super().__init__()
        self.font = font

    def process(self):

        window = self.world.get_component(WindowComponent)
        assert (len(window) == 1)
        window_surface = window[0][1].surface()

        label_components = self.world.get_component(LabelComponent)
        for _, label in label_components:
            x, y = label.get_position()
            s = label.get_label()
            self.font.draw_string(s, x, y, window_surface, label.get_font_color(), label.get_bkgd_color())

        dynamic_label_components = self.world.get_component(DynamicLabelComponent)
        for _, label in dynamic_label_components:
            x, y = label.get_position()
            s = label.get_callable()(self.world)
            self.font.draw_string(s, x, y, window_surface, label.get_font_color(), label.get_bkgd_color())

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
            self.font.draw_string(s[:w].ljust(w), x, y, window_surface, gauge.font_color, bkgd_color)
