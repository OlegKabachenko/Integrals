__all__ = "Animator"

from collections import deque
from functools import partial
from kivy.animation import Animation


class Animator:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_p_widget_animation = False
        self.animation_queue = deque()

    def process_animation_queue(self):
        if self.animation_queue:
            next_animation = self.animation_queue.popleft()
            next_animation()

    def animate_widget_vertical(self, widget, f_opacity, f_height, anim_duration=0.5, on_complete_extra_action=None,
                                is_from_queue=False):
        if self.is_p_widget_animation and not is_from_queue:
            self.animation_queue.append(lambda: self.animate_widget_vertical(widget, f_opacity, f_height, anim_duration,
                                                                             on_complete_extra_action, True))
            return

        self.is_p_widget_animation = True

        animation = Animation(opacity=f_opacity, height=f_height, duration=anim_duration)
        on_complete_action = partial(self.on_animation_complete, on_complete_extra_action)
        animation.bind(on_complete=on_complete_action)
        animation.start(widget)

    def on_animation_complete(self, on_complete_extra_action, *args):
        self.is_p_widget_animation = False
        if on_complete_extra_action:
            on_complete_extra_action()
        self.process_animation_queue()

    @staticmethod
    def widget_delete(container, widget, start_height):
        widget.height = start_height
        container.remove_widget(widget)

    def animate_widget_add(self, container, widget):
        final_height = widget.height
        widget.opacity = 0
        widget.height = 0
        container.add_widget(widget)
        self.animate_widget_vertical(widget, 1, final_height, 0.5)

    def animate_widget_delete(self, container, widget):
        start_width = widget.height
        widget_delete = partial(self.widget_delete, container, widget, start_width)

        self.animate_widget_vertical(widget, 0, 0, 0.5, widget_delete)

    def animate_container_clear(self, container):
        if container.children:
            for widget in container.children:
                self.animate_widget_delete(container, widget)
