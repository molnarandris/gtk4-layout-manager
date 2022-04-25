from gi.repository import Gtk, Gdk
import math, random

class ShufflingLayoutManager(Gtk.LayoutManager):
    __gtype_name__ = 'ShufflingLayoutManager'

    n_children = 0
    position = 0
    child_pos = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._n_grid_columns = 4


    @property
    def n_grid_columns(self):
        return self._n_grid_columns

    @n_grid_columns.setter
    def n_grid_columns(self, n):
        self._n_grid_columns = n


    @classmethod
    def add_element(cls):
        cls.n_children += 1
        cls.child_pos.append(cls.n_children)

    def shuffle(self):
        for i in range(self.n_children):
            j = random.randint(0,self.n_children-1)
            self.child_pos[i], self.child_pos[j] = self.child_pos[j], self.child_pos[i]

    def set_position(self,t):
        self.position = t


    def do_measure(self, widget, orientation, for_size):
        child = widget.get_first_child()
        min_size = 0
        nat_size = 0

        while child:

            if not child.should_layout():
                continue

            child_min, child_nat, _, _ = child.measure(orientation, -1)
            min_size = max(min_size, child_min)
            nat_size = max(nat_size,child_nat)

            child = child.get_next_sibling()

        natural = math.floor(self.n_children * nat_size / math.pi + nat_size)
        minimum = math.floor(self.n_children * min_size / math.pi + min_size)

        return (minimum, natural, -1, -1)

    def do_allocate(self, widget, width, height, baseline):
        child = widget.get_first_child()
        child_width = 0
        child_height = 0
        while child:
            if not child.should_layout():
                continue

            child_req, _ = child.get_preferred_size()
            child_width = max(child_width, child_req.width)
            child_height = max(child_height, child_req.height)

            child = child.get_next_sibling()

        x0 = width/2.0  - child_width/2.0
        y0 = height/2.0 - child_height/2.0
        r = self.n_children/2.0 * child_width / math.pi
        t = self.position

        child = widget.get_first_child()
        i = 0

        while child:
            if not child.should_layout():
                continue

            child_req, _ = child.get_preferred_size()
            # The grid layout
            gx = x0 + (i % self.n_grid_columns - 2) * child_req.width
            gy = y0 + (int(i / self.n_grid_columns) - 2) * child_req.height
            # The circle layout
            a = self.child_pos[i] * (math.pi / (self.n_children / 2))
            cx = int(x0 + math.sin(a) * r )
            cy = int(y0 + math.cos(a) * r )
            # interpolation
            x = int(gx*(1-t)+ cx*t)
            y = int(gy*(1-t)+ cy*t)
            # This is weird, but works. I am not sure how Gdk.Rectangle should work
            allocation = Gdk.Rectangle()
            allocation.x = x
            allocation.y = y
            allocation.width = child_width
            allocation.height = child_height
            # Allocation
            child.size_allocate(allocation, -1)
            # The iteration
            child = child.get_next_sibling()
            i+=1

    def do_get_request_mode(self,widget):
        return Gtk.SizeRequestMode.CONSTANT_SIZE
