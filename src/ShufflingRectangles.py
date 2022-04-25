from gi.repository import Gtk, GLib

from .ShufflingLayoutManager import ShufflingLayoutManager
from .ColorRect import  ColorRect

COLUMN_WIDTH = 5.0
DURATION = 0.5* GLib.TIME_SPAN_SECOND
COLORS = [ "red", "orange", "yellow", "green",
          "blue", "grey", "magenta", "lime",
          "yellow", "firebrick", "aqua", "purple",
          "tomato", "pink", "thistle", "maroon",
          "black", "white", "brown", "blueviolet",
          "chartreuse", "CadetBlue", "Coral", "DarkCyan", "GreenYellow"]

# The widget containing all the rectangles that get shuffled.
class ShufflingRectangles(Gtk.Widget):
    __gtype_name__ = 'ShufflingRectangles'


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.backwards = False
        self.start_time = None
        self.tick_id = 0
        margin = 10

        layout = ShufflingLayoutManager()
        layout.n_grid_columns = COLUMN_WIDTH
        self.set_layout_manager(layout)
        self.layout_manager = layout

        for c in COLORS:
            child = ColorRect(c)
            # add margin to the rectangles to separate them
            child.set_margin_start(margin)
            child.set_margin_end(margin)
            child.set_margin_top(margin)
            child.set_margin_bottom(margin)
            self.add_child(child)

        # Add an event controller and connect to the "pressed" event
        gesture = Gtk.GestureClick()
        gesture.connect("pressed", self.click_cb)
        self.add_controller(gesture)

    def click_cb(self,widget,n,x,y):
        print("pressed", self.tick_id)
        if self.tick_id != 0:
            return
        self.start_time = GLib.get_monotonic_time()
        self.tick_id = self.add_tick_callback(self.transition)

    def transition(self, widget, frame_clock):
        now = GLib.get_monotonic_time()
        self.queue_allocate()

        if self.backwards:
            self.layout_manager.set_position(1.0 - (now-self.start_time)/DURATION)
        else:
            self.layout_manager.set_position((now-self.start_time)/DURATION)

        if (now-self.start_time) >= DURATION:
            self.backwards = not self.backwards
            self.layout_manager.set_position(1.0 if self.backwards else 0)
            if not self.backwards:
                self.layout_manager.shuffle()
            self.tick_id = 0
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE

    def add_child(self, child):
        self.layout_manager.add_element()
        # This should be undone in the dispose method of this widget by calling
        # unparent() on each child widget. Iterate over the children by
        # get_first_child() and get_next_sibling()
        child.set_parent(self)

    # This does not get called because of a bug in pygobject...
    # https://gitlab.gnome.org/GNOME/pygobject/-/merge_requests/197
    def do_dispose(self):
        # remove all references to self from all its children
        child = self.get_first_child()
        while child:
            child.unparent()
            child = self.get_first_child()
        # and finally run dispose of the base class
        super().do_dispose()
