from otree.api import *
import math
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx


doc = """
成功者模倣実験アプリ
"""

class Constants(BaseConstants):
    NAME_IN_URL = 'imitation'
    PLAYERS_PER_GROUP = 20
    NUM_ROUNDS = 15
    K = 4  # 左右2人ずつが近傍

class Subsession(BaseSubsession):
    def creating_session(self):
        condition = self.session.config.get('condition', '提示群')
        for g in self.get_groups():
            g.condition = condition

class Group(BaseGroup):
    condition = models.StringField()

    def get_neighbors(self, player: 'Player'):
        players = self.get_players()
        n = len(players)
        index = player.id_in_group - 1
        offsets = [-2, -1, 1, 2]
        return [players[(index + o) % n] for o in offsets]

    def set_payoffs_and_info(self):
        for p in self.get_players():
            # 仮の利得計算: A=1ポイント, B=2ポイント
            p.payoff = 1 if p.choice == 'A' else 2

    def build_graph(self):
        G = nx.Graph()
        players = self.get_players()
        for p in players:
            G.add_node(p.id_in_group, player=p)
        n = len(players)
        for i, p in enumerate(players):
            for k in range(1, Constants.K//2 + 1):
                j = (i + k) % n
                G.add_edge(p.id_in_group, players[j].id_in_group)
                j = (i - k) % n
                G.add_edge(p.id_in_group, players[j].id_in_group)
        return G

    def network_image(self, focus_player: 'Player'):
        G = self.build_graph()
        colors = []
        labels = {}
        players = {p.id_in_group: p for p in self.get_players()}
        for node in G.nodes():
            p = players[node]
            colors.append('blue' if p.choice == 'A' else 'red')
            labels[node] = str(p.payoff) if self.condition == '提示群' else ''
        pos = nx.circular_layout(G)
        plt.figure(figsize=(4,4))
        nx.draw(G, pos, node_color=colors, with_labels=False)
        nx.draw_networkx_labels(G, pos, labels)
        nx.draw_networkx_nodes(G, pos, nodelist=[focus_player.id_in_group], node_color='green')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        return base64.b64encode(img.getvalue()).decode('utf-8')

class Player(BasePlayer):
    choice = models.StringField(
        choices=[('A', 'A行動'), ('B', 'B行動')],
        widget=widgets.RadioSelect,
    )
    payoff = models.CurrencyField()
