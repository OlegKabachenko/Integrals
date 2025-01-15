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
        else:
            self.is_p_widget_animation = False

    def animate_widget_vertical(self, widget, f_opacity, f_height, anim_duration=0.5, on_complete_extra_action=None,
                                before_extra_action=None, is_from_queue=False):
        if self.is_p_widget_animation and not is_from_queue:
            self.animation_queue.append(
                lambda: self.animate_widget_vertical(widget, f_opacity, f_height, anim_duration,
                                                     on_complete_extra_action, before_extra_action, True))
            return

        self.is_p_widget_animation = True

        if before_extra_action:
            before_extra_action()

        animation = Animation(opacity=f_opacity, height=f_height, duration=anim_duration)
        on_complete_action = partial(self.on_animation_complete, on_complete_extra_action)
        animation.bind(on_complete=on_complete_action)
        animation.start(widget)

    def on_animation_complete(self, on_complete_extra_action, *args):
        if on_complete_extra_action:
            on_complete_extra_action()
        self.process_animation_queue()

    @staticmethod
    def prepare_widget_for_add(container, widget):
        widget.opacity = 0
        widget.height = 0
        container.add_widget(widget)

    def animate_widget_add(self, container, widget, anim_duration=0.5, on_complete_extra_action=None,
                           is_from_queue=False):
        if self.is_p_widget_animation and not is_from_queue:
            self.animation_queue.append(
                lambda: self.animate_widget_add(container, widget, anim_duration, on_complete_extra_action, True))
            return

        final_height = widget.height
        before_action = partial(self.prepare_widget_for_add, container, widget)
        self.animate_widget_vertical(widget, 1, final_height, anim_duration, on_complete_extra_action, before_action,
                                     is_from_queue=is_from_queue)

    @staticmethod
    def remove_widget_post_animation (container, widget, initial_height):
        # Restore the widget's original height to preserve its initial size.
        # This is important for future re-adding, ensuring the widget's height is not lost.
        widget.height = initial_height
        container.remove_widget(widget)

    def animate_widget_delete(self, container, widget, anim_duration, is_from_queue=False):
        initial_height = widget.height
        after_delete = partial(self.remove_widget_post_animation , container, widget, initial_height)

        self.animate_widget_vertical(widget, 0, 0, anim_duration, after_delete, is_from_queue=is_from_queue)

    def animate_container_clear(self, container, anim_duration=0.5, is_from_queue=False):
        if self.is_p_widget_animation and not is_from_queue:
            self.animation_queue.append(
                lambda: self.animate_container_clear(container, anim_duration, True))
            return

        if container.children:
            for i, widget in enumerate(container.children):
                if i == 0:
                    # The first widget is deleted immediately
                    self.animate_widget_delete(container, widget, anim_duration, is_from_queue=is_from_queue)
                else:
                    # For all other widgets, add their deletion animation to the start of the queue.
                    # This ensures that the first widget will be deleted first and subsequent widgets will follow immediately.
                    self.animation_queue.insert(0 + (i - 1),
                                                lambda: self.animate_widget_delete(container, widget, anim_duration,
                                                                                   is_from_queue=True))

        else:
            self.process_animation_queue()
