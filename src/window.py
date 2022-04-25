# window.py
#
# Copyright 2022 Andras Molnar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk
from .ShufflingRectangles import ShufflingRectangles
from .ColorRect import ColorRect

@Gtk.Template(resource_path='/com/github/molnarandris/gtk4_layoutmanager/window.ui')
class Gtk4LayoutmanagerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'Gtk4LayoutmanagerWindow'

    shuffle = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'gtk4_layoutmanager'
        self.props.version = "0.1.0"
        self.props.authors = ['Andras Molnar']
        self.props.copyright = '(C) 2021 Andras Molnar'
        self.props.logo_icon_name = 'com.github.molnarandris.gtk4_layoutmanager'
        self.set_transient_for(parent)
