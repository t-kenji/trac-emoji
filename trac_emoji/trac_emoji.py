"""Sample Wiki syntax extension plugin."""

import os
import pkg_resources
from genshi.builder import tag

from trac.core import *
from trac.wiki.api import IWikiSyntaxProvider
from trac.web.chrome import ITemplateProvider, \
                            add_script, add_stylesheet

from autocomplete_provider.api import IStrategyAdapter

class TracEmoji(Component):
    """
    Allows for emoji from https://github.com/arvida/emoji-cheat-sheet.com
    """
    implements(IWikiSyntaxProvider, ITemplateProvider, IStrategyAdapter)

    HTDOCS_PREFIX = 'trac_emoji'
    EMOJI_DIR = '/icons'
    STYLE = 'height: 3ex; margin-bottom: -0.5ex;'

    def __init__(self, *args, **kwargs):
        self.emojies = {}
        self.candidates = []
        icons = os.listdir(''.join([self.htdocs_loc, self.EMOJI_DIR]))
        for icon in icons:
            if icon.endswith('.png'):
                self.candidates.append(icon[:-4])
                emoji = ':%s:' % icon[:-4]
                self.emojies[emoji] = icon
        self.candidates.sort()
        super(self.__class__, self).__init__(*args, **kwargs)

    # IStrategyAdapter methods

    def add_strategy(self):
        return {
            'id': 'emoji',
            'match': '\B:([\-+\w]*)$',
            'candidates': self.candidates,
            'template': 'return \'<img src="/trac-plugin-test/chrome/trac_emoji/icons/\' + value + \'.png" style="height: 3ex; margin-bottom: -0.5ex;" alt=":\' + value + \':" title=":\' + value + \':" ></img>\' + value',
            'replace': 'return \':\' + value + \': \'',
            'index': 1
        }

    # IWikiSyntaxProvider methods

    def get_link_resolvers(self):
        return []

    def get_wiki_syntax(self):
        def create_emoji(f, match, fullmatch):
            emoji = match
            emoji_image = self._format_emoji(f, emoji)
            return emoji_image
        yield (r"(?P<emoji>:[^ ]+:)", create_emoji)

    def _format_emoji(self, formatter, emoji):
        emoji_image = self.emojies.get(emoji)
        if emoji_image is None:
            return emoji
        else:
            return tag.img(
                src=formatter.href.chrome('/%s%s/%s' %(
                    self.HTDOCS_PREFIX, self.EMOJI_DIR, emoji_image)),
                alt=emoji,
                title=emoji,
                style=self.STYLE)

    # ITemplateProvider methods
    def get_htdocs_loc(self):
        return pkg_resources.resource_filename(__name__, 'htdocs')
    htdocs_loc = property(get_htdocs_loc)

    def get_htdocs_dirs(self):
        return [(self.HTDOCS_PREFIX, self.htdocs_loc)]

    def get_templates_dirs(self):
        return []
