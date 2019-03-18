# ##
# Copyright (c) 2018-2019, Laurent
# All rights reserved.
#
#
# ##

"""
YBot: sup ygg bot
"""

import supybot
import supybot.world as world

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = '1.2.18'

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.authors.unknown

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = ''

from . import config
from . import plugin
from yggscr import ylogging
from yggscr import link
from yggscr import const
from yggscr import sbrowser
from yggscr import ygg
from yggscr import shout
from yggscr import torrents

from imp import reload
# In case we're being reloaded.
reload(plugin)
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!
reload(ylogging)
reload(link)
reload(const)
reload(sbrowser)
reload(ygg)
reload(shout)
reload(torrents)

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
