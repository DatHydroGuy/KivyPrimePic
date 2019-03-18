from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from colorsys import hsv_to_rgb
from math import sin, cos, pi, atan2, sqrt
# import cProfile


# https://stackoverflow.com/a/22808285/1697183
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def fours(n):
    if n == 1:
        return[1]

    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4

    return factors + prime_factors(n)


# https://math.stackexchange.com/a/1806107/179367
def r(n):
    if n == 1:
        return 1
    s = sin(pi / n)
    return s / (s + 1)


class Root(BoxLayout):
    initial_center = Window.center  # initial window is centered on screen - keep that information
    Window.size = (1100, 1100)      # re-size window
    variation_x = Window.center[0] - initial_center[0]
    variation_y = Window.center[1] - initial_center[1]
    Window.left -= variation_x      # re-center window
    Window.top -= variation_y
    radius = min(Window.width / 4, Window.height / 4)

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.initial_draw()

    def initial_draw(self, *args):
        self.ids.floaty.clear_widgets()
        factors = [1]
        self.draw_factors(factors, Window.width / 2, Window.height / 2, self.radius, 0, False)

    def stuff(self, num_str, *args):
        self.ids.floaty.clear_widgets()
        try:
            num = max(0, int(num_str))
        except Exception:
            num = 0

        factors = list(reversed(fours(num)))
        self.ids.factors_label.text = ', '.join([str(s) for s in factors]).replace('4', '2, 2')
        self.draw_factors(factors, self.center_x, self.center_y, self.radius, 0, False)

    def draw_factors(self, factors, center_x, center_y, radius, angle, adjusted):
        if not factors:
            return

        n = factors[0]
        if n == 4 and adjusted is False:
            angle -= pi / 4
            adjusted = True  # First time we hit a 4, adjust rotation, but no adjustments after that!
        new_radius = radius * r(n)
        for i in range(n):
            f = AnimRect(i, n, new_radius, factors)
            if len(factors) == 1:
                self.ids.floaty.add_widget(f)
            f.position_widget(center_x, center_y, radius, angle)
            self.draw_factors(factors[1:], f.center_x, f.center_y, new_radius, f.angle, adjusted)


class AnimRect(Widget):
    angle = 0.0
    offset = 0

    def __init__(self, widget_num, num_widgets, radius, factors, **kwargs):
        super(AnimRect, self).__init__(**kwargs)
        self.id_num = widget_num
        self.radius = radius * 2
        self.factors = factors
        self.num_widgets = num_widgets
        self.colour = (1, 0, 0, 1)

    def position_widget(self, center_x, center_y, inscribed_circle_radius, angle):
        self.size = (2 * self.radius, 2 * self.radius)
        if self.num_widgets == 1:
            self.center_x = center_x
            self.center_y = center_y
            return
        self.offset = inscribed_circle_radius - self.radius   # Additional radius required to touch circle edge
        self.angle = angle + 2.0 * self.id_num * pi / self.num_widgets
        radius = round(inscribed_circle_radius + self.offset + 0.5)
        self.center_x = center_x + int(radius * sin(self.angle))
        self.center_y = center_y + int(radius * cos(self.angle))
        temp = self.generate_global_colour()
        self.colour = temp

    def generate_global_colour(self):
        x_off = self.center_x - Window.size[0] / 2
        y_off = self.center_y - Window.size[1] / 2
        master_angle = atan2(y_off, x_off)
        master_radius = sqrt(x_off * x_off + y_off * y_off)
        hue = master_angle / (2 * pi)
        hue = hue if 0 <= hue <= 1 else hue + 1
        temp = hsv_to_rgb(hue, 0.5 + master_radius / Window.height, 1)
        return tuple(temp + (1,))

    def position_widget_old(self):
        self.size = (2 * self.radius, 2 * self.radius)
        if self.num_widgets == 1:
            self.center_x = self.parent.center_x
            self.center_y = 15 + self.parent.center_y
            return
        self.offset = self.parent.parent.radius - self.radius   # Additional radius required to touch circle edge
        self.angle = 2.0 * self.id_num * pi / self.num_widgets
        radius = round(self.parent.parent.radius + self.offset)
        self.center_x = self.parent.center_x + int(radius * sin(self.angle))
        self.center_y = 15 + self.parent.center_y + int(radius * cos(self.angle))
        print(radius)
        print(self.radius)


class KivyPrimePicApp(App):
    # def on_start(self):
    #     self.profile = cProfile.Profile()
    #     self.profile.enable()
    #
    # def on_stop(self):
    #     self.profile.disable()
    #     self.profile.dump_stats('KivyPrimeApp.profile')
    #
    def build(self):
        return Root()


if __name__ == '__main__':
    KivyPrimePicApp().run()
