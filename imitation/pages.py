from otree.api import *
from .models import Constants

class Decision(Page):
    form_model = 'player'
    form_fields = ['choice']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs_and_info'

class Results(Page):
    def vars_for_template(self):
        neighbors = self.group.get_neighbors(self.player)
        return dict(
            neighbors=neighbors,
            show_payoff=self.group.condition == '提示群',
            network_image=self.group.network_image(self.player),
        )

page_sequence = [Decision, ResultsWaitPage, Results]
