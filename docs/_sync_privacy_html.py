#!/usr/bin/env python3
"""One-off sync: PRIVACY_POLICY.md changes -> hosted HTML pages."""

from __future__ import annotations

import glob
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

OLD_DATE = "2026-04-28"
NEW_DATE = "2026-05-25"

SECTION_1_LEGAL_EN = """
          <p>Legal links:</p>
          <ul>
            <li>Terms of Use (EULA): <a href="https://addeo.github.io/clowSpeakerT/docs/">https://addeo.github.io/clowSpeakerT/docs/</a></li>
            <li>Privacy Policy (this document): <a href="https://addeo.github.io/clowSpeaker/docs/">https://addeo.github.io/clowSpeaker/docs/</a></li>
          </ul>
          <p>Auto-renewable subscriptions are sold through the Apple App Store. The subscription title, length, and price are shown in the App before you purchase.</p>
"""

SECTION_1_LEGAL_RU = """
          <p>Юридические ссылки:</p>
          <ul>
            <li>Условия использования (EULA): <a href="https://addeo.github.io/clowSpeakerT/docs/">https://addeo.github.io/clowSpeakerT/docs/</a></li>
            <li>Политика конфиденциальности (этот документ): <a href="https://addeo.github.io/clowSpeaker/docs/">https://addeo.github.io/clowSpeaker/docs/</a></li>
          </ul>
          <p>Автопродлеваемые подписки продаются через Apple App Store. Название, срок и цена подписки отображаются в Приложении до покупки.</p>
"""

SECTION_3_4_EN = """
          <h3>3.4 Third-Party AI Services (User-Selected)</h3>
          <p>The App can route Telegram message content to <strong>third-party AI bots or providers that you choose</strong> in Telegram (for example, AI bots you add or select as a destination chat). The App operator does <strong>not</strong> operate those third-party AI services.</p>
          <p><strong>What data may be sent (when you enable forwarding/routing):</strong></p>
          <ul>
            <li>message text and attachments or metadata needed to deliver the content you choose to send;</li>
            <li>context you configure in the App (for example monitored chat, destination chat, parsing prefix, role/prompt text);</li>
            <li>Telegram identifiers required for delivery (for example chat IDs, bot usernames), as handled by Telegram/TDLib.</li>
          </ul>
          <p><strong>Who receives the data:</strong></p>
          <ul>
            <li>the <strong>specific third-party bot or AI provider account you select</strong> in the App or in Telegram;</li>
            <li><strong>Telegram</strong> as the transport platform, under Telegram&#x27;s policies;</li>
            <li><strong>not</strong> the App operator&#x27;s own backend (the App does not run a server that stores your message contents).</li>
          </ul>
          <p><strong>How the App collects and sends data:</strong></p>
          <ul>
            <li>on your device from your Telegram session via TDLib/API;</li>
            <li>when <strong>you</strong> configure destinations and enable or trigger forwarding or sending flows supported by the App.</li>
          </ul>
          <p><strong>Your permission and control:</strong></p>
          <ul>
            <li>the App presents disclosures before you enable features that share content with third-party AI destinations, and you must confirm in the App;</li>
            <li>you can change or disable destinations and related settings at any time;</li>
            <li>you are responsible for reviewing each third-party bot or provider&#x27;s terms and privacy policy before sending personal or sensitive data.</li>
          </ul>
          <p><strong>Third-party protection:</strong></p>
          <ul>
            <li>third-party AI providers may process data in other countries and may not offer the same protections described in this Policy for the App operator;</li>
            <li>verify their policies before sharing personal data.</li>
          </ul>
"""

SECTION_3_4_RU = """
          <h3>3.4 Сторонние AI-сервисы (выбранные пользователем)</h3>
          <p>Приложение может направлять содержимое сообщений Telegram в <strong>сторонние AI-боты или провайдеров, которых вы выбираете</strong> в Telegram (например, AI-ботов, которых вы добавляете или выбираете как чат назначения). Оператор Приложения <strong>не</strong> управляет этими сторонними AI-сервисами.</p>
          <p><strong>Какие данные могут передаваться (при включённой переадресации/маршрутизации):</strong></p>
          <ul>
            <li>текст сообщений и вложения или метаданные, необходимые для доставки выбранного вами контента;</li>
            <li>контекст, который вы настраиваете в Приложении (например, отслеживаемый чат, чат назначения, префикс парсинга, текст роли/промпта);</li>
            <li>идентификаторы Telegram, необходимые для доставки (например, ID чатов, имена ботов), через Telegram/TDLib.</li>
          </ul>
          <p><strong>Кто получает данные:</strong></p>
          <ul>
            <li><strong>конкретный сторонний бот или AI-провайдер, которого вы выбираете</strong> в Приложении или в Telegram;</li>
            <li><strong>Telegram</strong> как платформа передачи — по политикам Telegram;</li>
            <li><strong>не</strong> собственный бэкенд оператора Приложения (Приложение не запускает сервер, хранящий содержимое ваших сообщений).</li>
          </ul>
          <p><strong>Как Приложение собирает и отправляет данные:</strong></p>
          <ul>
            <li>на вашем устройстве из сессии Telegram через TDLib/API;</li>
            <li>когда <strong>вы</strong> настраиваете назначения и включаете или инициируете переадресацию/отправку, поддерживаемую Приложением.</li>
          </ul>
          <p><strong>Ваше разрешение и контроль:</strong></p>
          <ul>
            <li>Приложение показывает раскрытие информации до включения функций, передающих контент сторонним AI-назначениям, и вы должны подтвердить это в Приложении;</li>
            <li>вы можете изменить или отключить назначения и связанные настройки в любое время;</li>
            <li>вы несёте ответственность за ознакомление с условиями и политикой конфиденциальности каждого стороннего бота или провайдера перед отправкой персональных или чувствительных данных.</li>
          </ul>
          <p><strong>Защита со стороны третьих лиц:</strong></p>
          <ul>
            <li>сторонние AI-провайдеры могут обрабатывать данные в других странах и не обеспечивать тот же уровень защиты, что описан в этой Политике для оператора Приложения;</li>
            <li>проверяйте их политики перед передачей персональных данных.</li>
          </ul>
"""

SECTION_5_EN = """
          <p><strong>No-training commitment (App operator):</strong></p>
          <p>Telegram message data processed by this app must not be used to train or fine-tune AI/ML models by the app operator.</p>
          <p>The App operator does not use Telegram message content from this App for model training or fine-tuning.</p>
          <p><strong>Third-party services:</strong></p>
          <p>If you forward or send data to third-party bots or providers (including third-party AI services on Telegram), those parties may apply their own retention, inference, or training policies. You are responsible for that transfer and for any permissions required by those services.</p>
"""

SECTION_5_RU = """
          <p><strong>Обязательство не использовать данные для обучения (оператор Приложения):</strong></p>
          <p>Данные сообщений Telegram, обрабатываемые этим приложением, не должны использоваться для обучения или дообучения AI/ML-моделей оператором приложения.</p>
          <p>Оператор Приложения не использует содержимое сообщений Telegram из этого Приложения для обучения или дообучения моделей.</p>
          <p><strong>Сторонние сервисы:</strong></p>
          <p>Если вы пересылаете или отправляете данные сторонним ботам или провайдерам (включая сторонние AI-сервисы в Telegram), эти стороны могут применять собственные правила хранения, инференса или обучения. Вы несёте ответственность за такую передачу и за любые разрешения, требуемые этими сервисами.</p>
"""

FALLBACK_NOTICE_EN = """
          <p class="policy-notice"><strong>Update {date}:</strong> Sections 1, 3.4, 5, and 7 were expanded for App Store compliance. Please read the <a href="../en/">English version</a> for the authoritative text until this translation is updated.</p>
"""

FALLBACK_NOTICE_RU = """
          <p class="policy-notice"><strong>Обновление {date}:</strong> разделы 1, 3.4, 5 и 7 расширены для соответствия требованиям App Store. Актуальный текст на английском: <a href="../en/">English version</a>.</p>
"""

LEGAL_CONSENT_EN = "your consent for optional permissions/features and for sharing with user-selected third-party AI destinations."
LEGAL_CONSENT_OLD_EN = "your consent for optional permissions/features."


def patch_file(path: str, lang: str) -> None:
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if OLD_DATE not in content and NEW_DATE not in content:
        print(f"skip (no date marker): {path}")
        return

    content = content.replace(OLD_DATE, NEW_DATE)

    is_en = lang in ("en", "root")
    is_ru = lang == "ru"

    if "Legal links:" not in content and "Юридические ссылки:" not in content:
        legal = SECTION_1_LEGAL_RU if is_ru else SECTION_1_LEGAL_EN
        content = content.replace(
            '<p><a class="contact-email" href="mailto:supp0rt.serg@yandex.com">supp0rt.serg@yandex.com</a></p>\n        </section>',
            '<p><a class="contact-email" href="mailto:supp0rt.serg@yandex.com">supp0rt.serg@yandex.com</a></p>\n' + legal + "        </section>",
            1,
        )

    marker_34 = "<h3>3.4 "
    if marker_34 not in content:
        block = SECTION_3_4_RU if is_ru else SECTION_3_4_EN
        content = re.sub(
            r"(        </section>\n        <section>\n          <h2>4\.)",
            block + r"\1",
            content,
            count=1,
        )

    if "must not be used to train or fine-tune AI/ML models by the app operator" not in content and (
        "не должны использоваться для обучения" not in content
    ):
        section_5 = SECTION_5_RU if is_ru else SECTION_5_EN
        content = re.sub(
            r"(<h2>5\.[^<]*</h2>\n)(.*?)(\n        </section>\n        <section>\n          <h2>6\.)",
            r"\1" + section_5 + r"\3",
            content,
            count=1,
            flags=re.DOTALL,
        )

    if LEGAL_CONSENT_OLD_EN in content:
        content = content.replace(LEGAL_CONSENT_OLD_EN, LEGAL_CONSENT_EN)

    notice_key = "policy-notice"
    if notice_key not in content and not is_en and not is_ru:
        notice = FALLBACK_NOTICE_EN.format(date=NEW_DATE)
        content = content.replace(
            '<p class="policy-lead">',
            notice + '          <p class="policy-lead">',
            1,
        )

    with open(path, encoding="utf-8") as f:
        if f.read() == content:
            print(f"unchanged: {path}")
            return

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"updated: {path}")


def main() -> None:
    paths = [os.path.join(ROOT, "index.html")]
    paths.extend(glob.glob(os.path.join(ROOT, "*/index.html")))
    for path in sorted(paths):
        rel = os.path.relpath(path, ROOT)
        lang = "root" if rel == "index.html" else rel.split(os.sep)[0]
        patch_file(path, lang)


if __name__ == "__main__":
    main()
