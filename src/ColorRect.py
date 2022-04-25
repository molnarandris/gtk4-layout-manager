from gi.repository import Gtk, Gdk, Graphene

class ColorRect(Gtk.Widget):
    __gtype_name__ = 'ColorRect'

    def __init__(self, color):
        super().__init__()

        self.size = 32
        self.set_tooltip_text(color)
        self.color = Gdk.RGBA()   # depending on version Gdk.RGBA(color) works as well
        self.color.parse(color)

    def do_measure(self, orientation, for_size):
        return (self.size,self.size,-1,-1)

    def do_snapshot(self, snapshot):
        rect = Graphene.Rect().init(0, 0, self.get_width(), self.get_height())
        snapshot.append_color(self.color, rect)
