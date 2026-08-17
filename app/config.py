"""Who the page is for and what it links to.

The operational bits (收件信箱、Calendly、活動名稱) read from env so you can
change them without touching code; the copy and the people just live here.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

try:  # optional: load .env if python-dotenv is installed
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"


@dataclass(frozen=True)
class Person:
    """Someone the visitor may have met at the booth."""

    name: str
    title: str = ""
    tagline: str = ""
    linkedin: str = ""

    @property
    def initials(self) -> str:
        return "".join(part[0] for part in self.name.split()[:2]).upper()


# 攤位上會出現的人，順序就是頁面顯示的順序
PEOPLE: list[Person] = [
    Person(
        name="Reed Giovannetti",
        title="Co-founder & CEO at DeviceNexus",
        tagline="Physical AI infra & endpoint ops | OEM Whisperer",
        linkedin="https://www.linkedin.com/in/reed-giovannetti/",
    ),
    Person(
        name="Mike Chen",
        title="FDE at DeviceNexus",
        linkedin="https://www.linkedin.com/in/mikechenyz/",
    ),
]


@dataclass(frozen=True)
class Profile:
    # 對方按下按鈕後，信會寄到這裡；cc 留空就不帶副本
    email: str = os.getenv("CONTACT_EMAIL", "reed@devicenexus.ai")
    cc_email: str = os.getenv("CONTACT_CC", "mike@devicenexus.ai")
    company: str = os.getenv("COMPANY_NAME", "DeviceNexus")
    website: str = os.getenv("COMPANY_WEBSITE", "https://devicenexus.ai")
    calendly_url: str = os.getenv("CALENDLY_URL", "https://calendly.com/ez945y/30min")
    event_name: str = os.getenv("EVENT_NAME", "台灣機器人年會")

    one_liner: str = os.getenv(
        "COMPANY_ONE_LINER",
        "我們提供跨硬體的裝置維運基礎建設，專注解決設備建置時間與安全管理的痛點。",
    )
    # 頁面上的三個記憶點，順序就是想讓對方記住的順序
    value_props: list[str] = field(
        default_factory=lambda: [
            "極速部署：刷機時間縮短至 8 到 9 分鐘",
            "OTA 更新：分批推送韌體與模型，完整支援新舊版 Jetson",
            "遠端存取：不用派人到場，就能直接連線重現問題與除錯",
        ]
    )
    people: list[Person] = field(default_factory=lambda: list(PEOPLE))


profile = Profile()
