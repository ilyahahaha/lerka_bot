from typing import Any, Dict

from schemas.bgu import BguCompetitionGroup
from schemas.isu import IsuCompetitionGroup


def get_default_message(name: str, state_data: Dict[str, Any] | None = None) -> str:
    isu_leaderboard = state_data.get("isu") if state_data else None
    istu_leaderboard = state_data.get("istu") if state_data else None
    # bgu_leaderboard = state_data.get("bg") if state_data else None

    message = (
        f"👋 <b>Привет,</b> {name}."
        + "\n\n"
        + "✅ Я создан помочь Лерке мониторить результаты по поступлению в ВУЗы Иркутска."
        + "\n\n"
        + "<b>Текущие результаты:</b>"
        + "\n\n"
        + "1️⃣ <b>ИГУ: </b>"
        + f"\n{isu_leaderboard if isu_leaderboard else '❌ <i>Нет данных</i>'}\n\n"
        + "2️⃣ <b>ИРНИТУ: </b>"
        + f"\n{istu_leaderboard if istu_leaderboard else '❌ <i>Нет данных</i>'}\n\n"
        # + "3️⃣ <b>БГУ: </b>"
        # + f"\n{bgu_leaderboard if bgu_leaderboard else '❌ <i>Нет данных</i>'}"
    )

    return message


def build_leaderboard(
    results: list[IsuCompetitionGroup | IsuCompetitionGroup | BguCompetitionGroup],
) -> str | None:
    message = []

    if any(x is None for x in results):
        return None

    for result in results:
        text_string = f"<code>🏆 {result.group} -</code> {result.place} место"
        message.append(text_string)

    return "\n".join(message)
