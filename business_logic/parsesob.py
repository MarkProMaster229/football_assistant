import requests
from bs4 import BeautifulSoup
import json
import os
import time


class FootballParser:
    def __init__(self, team_name, url, output_file="matches.json"):
        self.team_name = team_name
        self.url = url
        self.output_file = output_file
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.5993.0 Safari/537.36"
            )
        }
        self.expire_seconds = 24 * 60 * 60  # 24 часа

    def is_file_expired(self):
        if not os.path.exists(self.output_file):
            return True
        mtime = os.path.getmtime(self.output_file)
        return (time.time() - mtime) > self.expire_seconds

    def run(self):
        if not self.is_file_expired():
            print(f"Файл {self.output_file} ещё свежий, не обновляем.")
            return

        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        matches = []

        for article in soup.select(
            "ul.ArticleMonth-module__iqjysL3m article.ArticleCalendarLine-module__tNh6P3l9"
        ):
            tour = article.select_one(
                "div.ArticleCalendarLine-module__lDB62GZ2 span"
            ).get_text(strip=True)
            date_day = article.select_one(
                "div.ArticleCalendarLine-module__GsPDVEsn span:nth-child(1)"
            ).get_text(strip=True)
            date_month = article.select_one(
                "div.ArticleCalendarLine-module__GsPDVEsn span:nth-child(2)"
            ).get_text(strip=True)
            date_time = article.select_one(
                "div.ArticleCalendarLine-module__t1ZF4tjN span:nth-child(2)"
            ).get_text(strip=True)

            teams = article.select("div.VersusLine-module__TQtiY22F h3")
            if len(teams) == 2:
                home = teams[0].get_text(strip=True)
                away = teams[1].get_text(strip=True)
            else:
                continue

            score_div = article.select_one("div.VersusLine-module__dyCmWl4f")
            score_text = score_div.get_text(strip=True) if score_div else None

            score_home = score_away = None
            team_stats = {
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "points": 0,
            }

            if score_text:
                parts = score_text.split("-")
                if len(parts) == 2:
                    score_home = int(parts[0].strip())
                    score_away = int(parts[1].strip())

                    if self.team_name in [home, away]:
                        team_stats["played"] = 1
                        if self.team_name == home:
                            team_stats["goals_for"] = score_home
                            team_stats["goals_against"] = score_away
                            if score_home > score_away:
                                team_stats["wins"] = 1
                                team_stats["points"] = 3
                            elif score_home == score_away:
                                team_stats["draws"] = 1
                                team_stats["points"] = 1
                            else:
                                team_stats["losses"] = 1
                        else:  # self.team_name == away
                            team_stats["goals_for"] = score_away
                            team_stats["goals_against"] = score_home
                            if score_away > score_home:
                                team_stats["wins"] = 1
                                team_stats["points"] = 3
                            elif score_away == score_home:
                                team_stats["draws"] = 1
                                team_stats["points"] = 1
                            else:
                                team_stats["losses"] = 1

            matches.append(
                {
                    "tour": tour,
                    "date": f"{date_day} {date_month}",
                    "time": date_time,
                    "home": home,
                    "away": away,
                    "score": score_text,
                    "score_home": score_home,
                    "score_away": score_away,
                    "team_stats": team_stats,
                }
            )

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=4)

        print(f"Сохранили {len(matches)} матчей в {self.output_file}")

    @classmethod
    def start(cls):
        parser = cls(
            team_name="Пари НН",
            url="https://fcnn.ru/season/championship/calendar?_isBase=true&_limit=12&_page=1&_season=25-26-rpl&_type=championship&_view=month",
        )
        parser.run()
