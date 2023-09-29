# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
#from qtile_extras.widget import StatusNotifier
import colors

# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/scripts/qtile_autostart'])

home         = os.path.expanduser('~')
mod          = "mod4"              # Sets mod key to SUPER/WINDOWS
alacritty    = 'alacritty --config-file ' + home + '/.config/alacritty/alacritty.yml'
myBrowser    = "brave" # My browser of choice
terminal     = home + '/.config/qtile/scripts/qtile_term'
music_player = home + '/.config/qtile/scripts/qtile_music'
color_picker = home + '/.config/qtile/scripts/qtile_colorpicker'
brightness   = home + '/.config/qtile/scripts/qtile_brightness'
volume       = home + '/.config/qtile/scripts/qtile_volume'
screenshot   = home + '/.config/qtile/scripts/qtile_screenshot'
notify_cmd   = 'dunstify -u low -h string:x-dunst-stack-tag:qtileconfig'

# A list of available commands that can be bound to keys can be found
# at https://docs.qtile.org/en/latest/manual/config/lazy.html
keys = [

    Key(
		["mod1"], "F1", 
		lazy.spawn("dm-run"), 
		desc="Run application launcher"
	),
    # The essential    
    Key(
		[mod], "Return", 
		lazy.spawn(terminal), 
		desc="Launch terminal with qtile configs"
	),
    Key(
		[mod, "shift"], "Return", 
		lazy.spawn(terminal + ' --float'), 
		desc="Launch floating terminal with qtile configs"
	),
    Key(
		[mod, "mod1"], "Return", 
		lazy.spawn(terminal + ' --full'), 
		desc="Launch fullscreen terminal with qtile configs"
	),

    Key([mod, "shift"], "q", lazy.spawn("dm-logout"), desc="Logout menu"),


    Key(
		[], "XF86MonBrightnessUp", 
		lazy.spawn(brightness + ' --inc'),
		desc="Increase display brightness"	
	),
    Key(
		[], "XF86MonBrightnessDown", 
		lazy.spawn(brightness + ' --dec'),
		desc="Decrease display brightness"	
	),

    Key(
		[], "XF86AudioRaiseVolume", 
		lazy.spawn(volume + ' --inc'),
		desc="Raise speaker volume"	
	),
    Key(
		[], "XF86AudioLowerVolume", 
		lazy.spawn(volume + ' --dec'),
		desc="Lower speaker volume"	
	),
    Key(
		[], "XF86AudioMute", 
		lazy.spawn(volume + ' --toggle'),
		desc="Toggle mute"	
	),
    Key(
		[], "XF86AudioMicMute", 
		lazy.spawn(volume + ' --toggle-mic'),
		desc="Toggle mute for mic"
	),

    Key(
		[], "XF86AudioNext", 
		lazy.spawn("playerctl next"),
		desc="Next track"
	),
    Key(
		[], "XF86AudioPrev", 
		lazy.spawn("playerctl previous"),
		desc="Previous track"
	),
    Key(
		[], "XF86AudioPlay", 
		lazy.spawn("playerctl play-pause"),
		desc="Toggle play/pause"
	),
    Key(
		[], "XF86AudioStop", 
		lazy.spawn("playerctl stop"),
		desc="Stop playing"
	),

    Key(
		[mod], "c", 
		lazy.window.kill(), 
		desc="Kill focused window"
	),
    Key(
		[mod], "q", 
		lazy.window.kill(), 
		desc="Kill focused window"
	),

    Key(
		[mod, "control"], "r", 
		lazy.reload_config(),
		lazy.spawn(notify_cmd + ' "Configuration Reloaded!"'),
		desc="Reload the config"
	),
    Key(
		[mod, "control"], "s", 
		lazy.restart(), 
		lazy.spawn(notify_cmd + ' "Restarting Qtile..."'),
		desc="Restart Qtile"
	),
    Key(
		[mod, "control"], "q", 
		lazy.shutdown(), 
		lazy.spawn(notify_cmd + ' "Exiting Qtile..."'),
		desc="Shutdown Qtile"
	),

    # Switch between windows
    Key(
		[mod], "Left", 
		lazy.layout.left(), 
		desc="Move focus to left"
	),
    Key(
		[mod], "Right",
		lazy.layout.right(), 
		desc="Move focus to right"
	),
    Key(
		[mod], "Down", 
		lazy.layout.down(), 
		desc="Move focus down"
	),
    Key(
		[mod], "Up",
		lazy.layout.up(), 
		desc="Move focus up"
	),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "space", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right. 
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod], "t", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),

    Key(
		[mod, "shift"], "Left", 
		lazy.layout.shuffle_left(), 
		desc="Move window to the left"
	),
    Key(
		[mod, "shift"], "Right",
		lazy.layout.shuffle_right(), 
		desc="Move window to the right"
	),
    Key(
		[mod, "shift"], "Down", 
		lazy.layout.shuffle_down(), 
		desc="Move window down"
	),
    Key(
		[mod, "shift"], "Up",
		lazy.layout.shuffle_up(), 
		desc="Move window up"
	),

    Key(
		[mod, "control"], "Left", 
		lazy.layout.grow_left(), 
		desc="Grow window to the left"
	),
    Key(
		[mod, "control"], "Right", 
		lazy.layout.grow_right(), 
		desc="Grow window to the right"
	),
    Key(
		[mod, "control"], "Down", 
		lazy.layout.grow_down(), 
		desc="Grow window down"
	),
    Key(
		[mod, "control"], "Up", 
		lazy.layout.grow_up(), 
		desc="Grow window up"
	),
    Key(
		[mod, "control"], "Return", 
		lazy.layout.normalize(), 
		desc="Reset all window sizes"
	),

    Key(
		[mod, "mod1"], "Right", 
		lazy.screen.next_group(), 
		desc="Move to the group on the right"
	),
    Key(
		[mod, "mod1"], "Left", 
		lazy.screen.prev_group(), 
		desc="Move to the group on the left"
	),
    # Back-n-forth groups
    Key(
		[mod], "b", 
		lazy.screen.toggle_group(), 
		desc="Move to the last visited group"
	),

	# Change focus to other window
    Key(
		[mod], "Tab", 
		lazy.layout.next(), 
		desc="Move window focus to other window"
	),

    # Toggle between different layouts as defined below
    Key(
		[mod, "shift"], "space", 
		lazy.next_layout(), 
		desc="Toggle between layouts"
	),

	# Increase the space for master window at the expense of slave windows
    Key(
		[mod], "equal", 
		lazy.layout.increase_ratio(), 
		desc="Increase the space for master window"
	),

	# Decrease the space for master window in the advantage of slave windows
    Key(
		[mod], "minus", 
		lazy.layout.decrease_ratio(), 
		desc="Decrease the space for master window"
	),

    # Toggle between split and unsplit sides of stack.
    Key(
        [mod, "shift"], "s",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

	# Modes: Reize
    KeyChord([mod, "shift"], "r", [
        Key([], "Left", lazy.layout.grow_left()),
        Key([], "Right", lazy.layout.grow_right()),
        Key([], "Down", lazy.layout.grow_down()),
        Key([], "Up", lazy.layout.grow_up())],
        mode=True,
        name="Resize"
    ),

	# Modes: Layouts
    KeyChord([mod, "shift"], "l", [
        Key([], "Left", lazy.prev_layout()),
        Key([], "Right", lazy.next_layout())],
        mode=True,
        name="Layouts"
    ),


    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),
    
    # An example of using the extension 'CommandSet' to give 
    # a list of commands that can be executed in dmenu style.
    Key([mod], 'z', lazy.run_extension(extension.CommandSet(
        commands={
            'play/pause': '[ $(mocp -i | wc -l) -lt 2 ] && mocp -p || mocp -G',
            'next': 'mocp -f',
            'previous': 'mocp -r',
            'quit': 'mocp -x',
            'open': 'urxvt -e mocp',
            'shuffle': 'mocp -t shuffle',
            'repeat': 'mocp -t repeat',
            },
        pre_commands=['[ $(mocp -i | wc -l) -lt 1 ] && mocp -S'],
        ))),
    

    # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord([mod], "p", [
        Key([], "h", lazy.spawn("dm-hub"), desc='List all dmscripts'),
        Key([], "a", lazy.spawn("dm-sounds"), desc='Choose ambient sound'),
        Key([], "b", lazy.spawn("dm-setbg"), desc='Set background'),
        Key([], "c", lazy.spawn("dtos-colorscheme"), desc='Choose color scheme'),
        Key([], "e", lazy.spawn("dm-confedit"), desc='Choose a config file to edit'),
        Key([], "i", lazy.spawn("dm-maim"), desc='Take a screenshot'),
        Key([], "k", lazy.spawn("dm-kill"), desc='Kill processes '),
        Key([], "m", lazy.spawn("dm-man"), desc='View manpages'),
        Key([], "n", lazy.spawn("dm-note"), desc='Store and copy notes'),
        Key([], "o", lazy.spawn("dm-bookman"), desc='Browser bookmarks'),
        Key([], "p", lazy.spawn("passmenu -p \"Pass: \""), desc='Logout menu'),
        Key([], "q", lazy.spawn("dm-logout"), desc='Logout menu'),
        Key([], "r", lazy.spawn("dm-radio"), desc='Listen to online radio'),
        Key([], "s", lazy.spawn("dm-websearch"), desc='Search various engines'),
        Key([], "t", lazy.spawn("dm-translate"), desc='Translate text')
    ])

]
groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]

#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX",]
group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9",]
#group_labels = ["", "", "", "", "", "", "", "", "",]


group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.
# There 10 colorschemes available to choose from:
#
# colors = colors.DoomOne
# colors = colors.Dracula
# colors = colors.GruvboxDark
# colors = colors.MonokaiPro
# colors = colors.Nord
# colors = colors.OceanicNext
# colors = colors.Palenight
# colors = colors.SolarizedDark
# colors = colors.SolarizedLight
# colors = colors.TomorrowNight
#
# It is best not manually change the colorscheme; instead run 'dtos-colorscheme'
# which is set to 'MOD + p c'

colors = colors.Girhub

### LAYOUTS ###
# Some settings that I use on almost every layout, which saves us
# from having to type these out for each individual layout.
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": colors[8],
                "border_normal": colors[0]
                }


var_bg_color = '#2e3440'
var_active_bg_color = '#81A1C1'
var_active_fg_color = '#2e3440'
var_inactive_bg_color = '#3d4555'
var_inactive_fg_color = '#D8DEE9'
var_urgent_bg_color = '#BF616A'
var_urgent_fg_color = '#D8DEE9'
var_section_fg_color = '#EBCB8B'
var_active_color = '#81A1C1'
var_normal_color = '#3d4555'
var_border_width = 2
var_margin = [5,5,5,5]
var_gap_top = 45
var_gap_bottom = 5
var_gap_left = 5
var_gap_right = 5
var_font_name = 'JetBrainsMono Nerd Font'


layouts = [
	# Extension of the Stack layout
    layout.Columns(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_on_single=False,
		border_width=var_border_width,
		fair=False,
		grow_amount=10,
		insert_position=0,
		margin=var_margin,
		margin_on_single=None,
		num_columns=2,
		split=True,
		wrap_focus_columns=True,
		wrap_focus_rows=True,
		wrap_focus_stacks=True
	),

	# Layout inspired by bspwm
    layout.Bsp(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_on_single=False,
		border_width=var_border_width,
		fair=True,
		grow_amount=10,
		lower_right=True,
		margin=var_margin,
		margin_on_single=None,
		ratio=1.6,
		wrap_clients=False
    ),

	# This layout divides the screen into a matrix of equally sized cells and places one window in each cell.
    layout.Matrix(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,    
		columns=2,
		margin=var_margin
    ),

	# Maximized layout
    layout.Max(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,    
		margin=0
    ),

	# Emulate the behavior of XMonad's default tiling scheme.
    layout.MonadTall(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		margin=12,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='after_current',
		ratio=0.5,
		single_border_width=None,
		single_margin=None
    ),

	# Emulate the behavior of XMonad's ThreeColumns layout.
    layout.MonadThreeCol(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		main_centered=True,
		margin=12,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='top',
		ratio=0.5,
		single_border_width=None,
		single_margin=None    
    ),

	# Emulate the behavior of XMonad's horizontal tiling scheme.
    layout.MonadWide(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		margin=12,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='after_current',
		ratio=0.5,
		single_border_width=None,
		single_margin=None    
    ),

	# Tries to tile all windows in the width/height ratio passed in
    layout.RatioTile(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		fancy=False,
		margin=var_margin,
		ratio=1.618,
		ratio_increment=0.1
    ),

	# This layout cuts piece of screen_rect and places a single window on that piece, and delegates other window placement to other layout
    layout.Slice(
		match=None,
		side='left',
		width=256
    ),

	# A mathematical layout, Renders windows in a spiral form by splitting the screen based on a selected ratio.
    layout.Spiral(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		clockwise=True,
		main_pane='left',
		main_pane_ratio=None,
		margin=0,
		new_client_position='top',
		ratio=0.6180469715698392,
		ratio_increment=0.1
    ),
    
	# A layout composed of stacks of windows
    layout.Stack(
		autosplit=False,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		fair=False,
		margin=var_margin,
		num_stacks=2
    ),

	# A layout with two stacks of windows dividing the screen
    layout.Tile(
		add_after_last=False,
		add_on_top=True,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_on_single=False,
		border_width=var_border_width,
		expand=True,
		margin=var_margin,
		margin_on_single=None,
		master_length=1,
		master_match=None,
		max_ratio=0.85,
		min_ratio=0.15,
		ratio=0.618,
		ratio_increment=0.05,
		shift_windows=False
    ),


	# Tiling layout that works nice on vertically mounted monitors
    layout.VerticalTile(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		margin=var_margin
    ),

	# A layout with single active windows, and few other previews at the right
    layout.Zoomy(
		columnwidth=300,
		margin=var_margin,
		property_big='1.0',
		property_name='ZOOM',
		property_small='0.1'
    ),

	# Floating layout, which does nothing with windows but handles focus order
    layout.Floating(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		fullscreen_border_width=0,
		max_border_width=0
	)
]


# Some settings that I use on almost every widget, which saves us
# from having to type these out for each individual widget.
widget_defaults = dict(
    font="Jetbrains Mono Bold",
    fontsize = 12,
    padding = 2,
    padding_x = 4,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [

        widget.GroupBox(
                 fontsize = 11,
                 margin_y = 3,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 3,
                 borderwidth = 3,
                 active = colors[8],
                 inactive = colors[1],
                 font = "Jetbrains Mono Bold",
                 rounded = False,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = colors[7],
                 this_screen_border = colors [4],
                 other_current_screen_border = colors[7],
                 other_screen_border = colors[4],
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.CurrentLayoutIcon(
                 # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                 foreground = colors[1],
                 padding = 0,
                 scale = 0.5
                 ),
        widget.CurrentLayout(
                 foreground = colors[1],
                 padding = 5
                 ),
        widget.TextBox(
                 text = '|',
                 font = "Ubuntu Mono",
                 foreground = colors[1],
                 padding = 2,
                 fontsize = 14
                 ),
        widget.WindowName(
                 foreground = colors[6],
                 max_chars = 40
                 ),

        widget.Mpris2(
                 format = "{xesam:title} - ({xesam:artist})",
                 playing_text = " #  {track}",
                 paused_text  = " # {track}",
                 width = 200,
                 scroll_delay = 5,
                 scroll_interval = 0.25,
                 scroll_step = 15,   
                 foreground = colors[7],            
                 **widget_defaults
                 ),  
        widget.Spacer(length = 8),   
        



        widget.GenPollText(
                 update_interval = 300,
                 func = lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 foreground = colors[3],
                 fmt = ' ❤ {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[3],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.CPU(
                 format = ' ▓ Cpu: {load_percent}%',
                 foreground = colors[4],
                 decorations=[
                     BorderDecoration(
                         colour = colors[4],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Memory(
                 foreground = colors[8],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(alacritty + ' -e htop')},
                 format = '{MemUsed: .0f}{mm}',
                 fmt = ' 🖥 Mem: {} used',
                 decorations=[
                     BorderDecoration(
                         colour = colors[8],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.DF(
                 update_interval = 60,
                 foreground = colors[5],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(alacritty + ' -e df')},
                 partition = '/',
                 #format = '[{p}] {uf}{m} ({r:.0f}%)',
                 format = '{uf}{m} free',
                 fmt = ' 🖴 Disk: {}',
                 visible_on_warn = False,
                 decorations=[
                     BorderDecoration(
                         colour = colors[5],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),

        widget.Battery(
                  update_interval = 10,
                  fontsize = 12,
                  foreground = colors[8],
                  notify_below = 15,
                  fmt = 'Batt: {}'
                  

                 ),

        widget.Spacer(length = 8),

        widget.Volume(
                 foreground = colors[7],
                 fmt = ' 🕫 Vol: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[7],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),  

          
        widget.Spacer(length = 8),
        widget.Clock(
                 foreground = colors[6],
                 format = " ⏱ %a, %b %d - %I:%M %P",
                 decorations=[
                     BorderDecoration(
                         colour = colors[6],
                         border_width = [0, 0, 0, 0],
                     )
                 ],
                 ),
        widget.Spacer(length = 8),
        widget.Systray(padding = 3),
        widget.Spacer(length = 8),

        ]
    return widgets_list

# Monitor 1 will display ALL widgets in widgets_list. It is important that this
# is the only monitor that displays all widgets because the systray widget will
# crash if you try to run multiple instances of it.
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1 

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[22:24]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(title="pinentry"),          # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


