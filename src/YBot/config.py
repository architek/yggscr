###
# Copyright (c) 2018-2019, Laurent
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('YBot')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('YBot', True)


ybot = conf.registerPlugin('YBot')
shout = conf.registerGroup(ybot,'shout')
conf.registerGlobalValue(ybot.shout, 'fmt',
        registry.String('{time} {fuser} : {message}', _("""Shout format( time, fuser, user, group, message)""")))
conf.registerGlobalValue(ybot.shout, 'rate_err',
        registry.PositiveInteger(30, _("""Error rate limit""")))
cred = conf.registerGroup(ybot,'cred')
conf.registerGlobalValue(ybot.cred, 'user',
        registry.String('', _("""Ygg user name."""), private=True))
conf.registerGlobalValue(ybot.cred, 'pass',
        registry.String('', _("""Ygg password (stored unencrypted)."""), private=True))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
