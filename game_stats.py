import json

class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.game_active = False
        self.player = "nobody"

        self.reset_stats()


    def reset_stats(self):
        """初始化在游戏运行期间可能变化的信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.power = 0

        # 提取历史得分信息
        scorefilename = 'scores.json'
        with open(scorefilename) as f:
            self.scores_data = json.load(f)
        self.high_score = int(self.scores_data[0]['score'])
