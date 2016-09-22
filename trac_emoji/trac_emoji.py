"""Sample Wiki syntax extension plugin."""

import os
import pkg_resources
from genshi.builder import tag

from trac.core import *
from trac.wiki.api import IWikiSyntaxProvider
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, \
                            add_stylesheet

from autocomplete_provider.api import IStrategyAdapter

import emojis

class TracEmoji(Component):
    """
    Allows for emoji from https://github.com/arvida/emoji-cheat-sheet.com
    """
    implements(IRequestFilter, IWikiSyntaxProvider, ITemplateProvider, IStrategyAdapter)

    HTDOCS_PREFIX = 'trac_emoji'

    # IStrategyAdapter methods

    def add_strategy(self):
        return {
            'id': 'emoji',
            'match': '\B:([\-+\w]*)$',
            'candidates': emojis.candidates,
            'template': 'return \'<i class="emoji emoji-\' + value.replace(/\+/g, \'\') + \'"></i>\' + value',
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
        if emoji[1:-1] not in emojis.candidates:
            return emoji
        else:
            return tag.i(title=emoji, class_='emoji emoji-{}'.format(emoji[1:-1].replace('+', '')))

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        return [(self.HTDOCS_PREFIX, pkg_resources.resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return []

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template is not None and template in ('ticket.html', 'bs_ticket.html',
                                                 'wiki_edit.html', 'bs_wiki_edit.html'):
            add_stylesheet(req, self.HTDOCS_PREFIX + '/css/emojis.css')
        return template, data, content_type
