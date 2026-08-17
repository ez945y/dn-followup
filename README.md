# 會後 Follow-up 頁

一個很小的 FastAPI 服務：把「在台灣機器人年會遇到的人」導到一頁上，
上面有一封**已經幫他擬好、寄給我們的信**。他可以在頁面上直接改，
按一下就跳到 Gmail 開好的草稿，確認後由他自己送出。
同一頁也可以直接約 30 分鐘的會議。

流程是：**他看草稿 → 改成自己的狀況 → 跳 Gmail → 他自己寄給我們**。
我們這邊不寄信、不存資料、沒有資料庫。

```
app/config.py            攤位上的人（Reed / Mike + LinkedIn）、Calendly 連結、公司介紹
app/main.py              兩個頁面路由 + Jinja2
templates/page.html.j2   對方看到的那一頁
templates/draft.subject.j2  信件主旨草稿
templates/draft.body.j2     信件內文草稿（用「對方的口氣」寫，因為是他要寄的）
```

## 跑起來

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打開 http://127.0.0.1:8000/ 就看得到。

## 一條網址所有人共用

會場上不知道會遇到誰，所以頁面刻意不帶任何人的名字：抬頭是「很高興在會場遇到您」，
信末留 `[您的姓名]` / `[公司名稱]` 讓對方自己填。
一個 QR code 印在名片或攤位背板上就能用，事後補訊息也是給同一條連結。

`/draft` 會用純文字回同一份草稿，方便你自己校字。

## 上線：GitHub Pages

頁面在使用者打開時沒有任何伺服器邏輯（內容都來自 `config.py`，按鈕是純 JS），
所以可以直接輸出成一個靜態檔給 GitHub Pages 服務，不用養一台機器。

```bash
python3 build.py     # 產生 docs/index.html
git add -A && git commit -m "update page" && git push
```

GitHub 上到 **Settings → Pages → Source: Deploy from a branch → `main` / `docs`**，
一兩分鐘後就會有網址。

> **改完 `config.py` 或 `templates/` 一定要重跑 `python3 build.py` 再 push**，
> 不然線上還是舊的。本機用 `uvicorn` 預覽、要上線才 build。

## 三顆按鈕

- **在 Gmail 開啟並寄出** — 另開 Gmail 的 compose（`mail.google.com/mail/?view=cm`），
  收件人、主旨、內文都填好了。信**不會**自動送出，一定要他自己按送出。
- **用我自己的郵件軟體** — 同樣內容走 `mailto:`，給不用 Gmail 的人。
- **複製內容** — 複製主旨 + 內文，貼到哪都行。

按下按鈕時抓的是頁面上當下的文字，所以他改過的版本會一起帶過去。

## 要改的東西

| 想改什麼 | 改哪裡 |
| --- | --- |
| 攤位上的人：名字、職稱、LinkedIn | `app/config.py` 的 `PEOPLE`（想加第三個人就再 append 一個 `Person`） |
| 收件信箱、Calendly、活動名稱、公司一句話、三個記憶點 | `app/config.py` 的 `Profile`（或 `.env`，見 `.env.example`） |
| 信的內容、語氣 | `templates/draft.body.j2`、`draft.subject.j2` |
| 頁面排版、文案 | `templates/page.html.j2` |

要英文版就複製一份 `draft.*.j2` 改成英文，在 `main.py` 依 `?lang=` 選檔名即可。

## 上線前要確認

- **`CONTACT_EMAIL` 目前預設是 `reed@devicenexus.ai`，這是我猜的，請先確認再分享出去** ——
  這是對方按下按鈕後信會寄到的地方，寫錯信就掉了。
- Mike 的職稱目前是空的（`PEOPLE` 裡的 `title=""`），補上去才會顯示。
- Calendly `https://calendly.com/ez945y/30min` 已確認可以被 iframe 嵌入（`x-frame-options: ALLOWALL`）。
- 部署時記得掛 HTTPS；頁面有 `noindex`，不會被搜尋引擎收錄。
