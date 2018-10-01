# ##
# Copyright (c) 2018, Laurent
# All rights reserved.
#
#
# ##

"""
YBot: sup ygg bot
"""

import yggscr
import supybot
import supybot.world as world

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = '1.0.9'

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.authors.unknown

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = ''

from . import config
from . import plugin
import yggscr
# from .yggscr import ygg
# from .yggscr import sbrowser
# from .yggscr import torrents
# from .yggscr import shout
# from .yggscr import link
# from .yggscr import const
from imp import reload
# In case we're being reloaded.
reload(yggscr)
# reload(ygg)
# reload(config)
# reload(plugin)
# reload(sbrowser)
# reload(torrents)
# reload(shout)
# reload(link)
# reload(const)
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
