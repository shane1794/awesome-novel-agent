# Theme registration form

> Phase 2: Show it to the author when choosing a topic. The sequence of `GENRES` is
> consistent with `tools/init.py` (1-24), and the number can be used directly for
> `--genre <number>`. Each entry points to the example file under
> `knowledge/genre-example/`, including style_blueprint, genre_config, genre_taboos,
> prompt_segment, story_arc_templates.

| Number | Subject | id | Description |
|------|------|----|------|
| 1 | Eastern xianxia (immortal cultivation) | `xianxia` | Cultivation of immortality, Taoism, cultivation and other xianxia elements |
| 2 | Traditional xuanhuan (Eastern fantasy) | `xuanhuan` | Traditional xuanhuan such as the counterattack of losers and the rebirth of the strong, the world of high martial arts and the alien continent |
| 3 | Urban category | `urban` | Modern urban base category, subcategory variants cover differentiated fields |
| 4 | Urban romance | `urban-romance` | Urban romance, love |
| 5 | Urban Daily | `urban-daily` | Urban emotions, real life and other urban articles |
| 6 | Urban Farming | `urban-farming` | Urban literature such as rebirth era, workplace business war, farming construction, etc. |
| 7 | Urban wild idea | `urban-brained` | Male-oriented urban wild idea with golden finger system |
| 8 | Urban Cultivation | `urban-cultivation` | Urban literature with Cultivation as the power system |
| 9 | Urban Gaowu | `urban-high-martial` | Urban overhead, everyone has a training system, spiritual energy recovery, etc. |
| 10 | The God of War live-in son-in-law | `war-god` | The urban god of war, the king of war |
| 11 | Western Fantasy | `western-fantasy` | A Western world background, including magic, fighting spirit, arcane and other fantasy elements |
| 12 | Ancient Style Strategy | `ancient-politics` | Ancient court, strategy, struggle for hegemony, etc. |
| 13 | History Category | `historical` | History Literature Base Category, subcategory variants cover differentiated fields |
| 14 | Ancient history | `historical-ancient` | Mainly focusing on farming, court, resourcefulness, hegemony, imperial examination, etc., non-systematic historical text without golden finger |
| 15 | History wild idea | `historical-brained` | Wild idea goes to history, usually with golden finger |
| 16 | Anti-Japanese War Spy | `anti-japanese-war` | Male-oriented novel about military warfare and espionage during the Anti-Japanese War |
| 17 | Science fiction apocalypse | `scifi-apocalypse` | Apocalypse, zombies, interstellar, mecha, future technology, etc. |
| 18 | Suspense criminal investigation | `suspense-crime` | male-oriented detective, suspense, reasoning |
| 19 | Suspense and supernatural | `suspense-paranormal` | male-oriented detective, suspense, horror, Feng Shui and thaumaturgy, etc. |
| 20 | Suspenseful wild idea | `suspense-brained` | Wild idea-oriented suspenseful supernatural, crime-solving adventure genre, as well as weird recovery, thriller games, rules and strange stories, etc. |
| 21 | Game Sports | `game-sports` | Online games, competitions, sports and immersive games or world gamification |
| 22 | Animation derivatives | `anime-derivative` | Games, animation and other two-dimensional fan works |
| 23 | Derived class | `derivative` | Derived class base class, shared by corpus |
| 24 | male-oriented derivatives | `male-derivative` | film and television drama male-oriented fan fiction |

> The number corresponds one-to-one with `tools/init.py --genre <number>`;
> `xuanhuan-brained` is a variant of the traditional xuanhuan corpus (`xuanhuan.md`)
> and is not in the independent numbering list.
