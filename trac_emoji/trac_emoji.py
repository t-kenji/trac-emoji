# -*- coding: utf-8 -*-
"""Sample Wiki syntax extension plugin."""

import os
import pkg_resources
from genshi.builder import tag

from trac.core import *
from trac.wiki.api import IWikiSyntaxProvider
from trac.web.api import IRequestFilter
from trac.web.chrome import (
    ITemplateProvider, add_stylesheet,
)

from tracautocomplete.api import IWikiAutocompleteProvider

import emojis

class TracEmoji(Component):
    """
    Allows for emoji from https://github.com/arvida/emoji-cheat-sheet.com
    """
    implements(IRequestFilter,
               IWikiSyntaxProvider,
               ITemplateProvider,
               IWikiAutocompleteProvider)

    HTDOCS_PREFIX = 'trac_emoji'

    # IWikiAutocompleteProvider methods

    def add_strategy(self):
        return {
            'id': 'emoji',
            'match': '\B:([\-+\w]*)$',
            'source': emojis.source,
            'template': '''
                return '<i class="emoji"><img src="{}/chrome/{}/img/emojis.png" class="emoji emoji-' + item.value.replace(/\+/g, '') + '" /></i> ' + item.value
                '''.format(self.env.href(), self.HTDOCS_PREFIX),
            'replace': 'return ":" + item.value + ": "',
            'index': 1,
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
        if emoji[1:-1] not in emojis.source:
            return emoji
        else:
            return tag.i(tag.img(src=formatter.href.chrome('/{}/img/emojis.png'.format(self.HTDOCS_PREFIX)),
                                 class_='emoji emoji-{}'.format(emoji[1:-1].replace('+', '')),
                                 alt=emoji,
                                 title=emoji),
                         class_='emoji')

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        return [(self.HTDOCS_PREFIX, pkg_resources.resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return []

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template in ('ticket.html',
                        'wiki_view.html', 'wiki_edit.html',
                        'fullblog_view.html', 'fullblog_edit.html',):
            add_stylesheet(req, self.HTDOCS_PREFIX + '/css/emojis.css')
        return template, data, content_type
