# -*- coding: utf-8 -*-
# :Project:   SoL -- Matches printout
# :Created:   lun 13 giu 2016 11:49:26 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018 Lele Gaifax
#

from reportlab.lib import colors
from reportlab.platypus import Paragraph, TableStyle
from reportlab.platypus.tables import Table

from ..i18n import gettext

from . import caption_style, normal_style, rank_width
from .basic import TourneyPrintout
from .utils import ordinalp


class MatchesPrintout(TourneyPrintout):
    "Next turn matches."

    def __init__(self, output, locale, tourney):
        super().__init__(output, locale, tourney, 1)

    def getLitURL(self, request):
        functional_testing = request.registry.settings['desktop.version'] == 'test'
        if not request.host.startswith('localhost') or functional_testing:
            return request.route_url('lit_tourney', guid=self.tourney.guid,
                                     _query=dict(turn=self.tourney.currentturn))

    def getSubTitle(self):
        if self.tourney.finalturns:
            return gettext('Matches %s final round') % ordinalp(self.tourney.currentturn)
        else:
            return gettext('Matches %s round') % ordinalp(self.tourney.currentturn)

    def getElements(self):
        yield from super().getElements()

        phantom = gettext('Phantom')
        currentturn = self.tourney.currentturn
        turn = [(m.board,
                 m.competitor1.caption(),
                 m.competitor2.caption() if m.competitor2 else phantom)
                for m in self.tourney.matches
                if m.turn == currentturn]
        if not turn:
            return

        turn.sort()
        rows = [(gettext('#'),
                 gettext('Match'))]
        rows.extend([(board, Paragraph(c1, normal_style), Paragraph(c2, normal_style))
                     for (board, c1, c2) in turn])

        desc_width = (self.doc.width/self.columns*0.9 - rank_width) / 2
        yield Table(rows, (rank_width, desc_width, desc_width),
                    style=TableStyle([
                        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                        ('SPAN', (1, 0), (-1, 0)),
                        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
                        ('ALIGN', (-2, 1), (-1, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONT', (0, 0), (-1, 0), caption_style.fontName),
                        ('SIZE', (0, 0), (-1, 0), caption_style.fontSize),
                        ('LEADING', (0, 0), (-1, 0), caption_style.leading),
                        ('SIZE', (0, 1), (-1, -1), normal_style.fontSize),
                        ('LEADING', (0, 1), (-1, -1), normal_style.leading),
                        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)]))
