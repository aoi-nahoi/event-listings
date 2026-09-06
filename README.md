# Event Listings

Django + HTMX で作ったローカルイベント一覧アプリです。イベントの閲覧・検索・フィルタ、作成・編集・削除、ブックマーク、お気に入りができます。

## RenderデプロイURL
https://event-listings.onrender.com

## アプリ構成

| アプリ | 役割 |
| --- | --- |
| `events_app` | イベント管理、検索・フィルタ、HTMX 部分更新、ブックマーク / お気に入り、デモデータ投入 |
| `accounts` | 会員登録、ログイン / ログアウト、プロフィール設定、パスワード変更 |
| `events_site` | Django プロジェクト設定、ルート URL、ヘルスチェック |

補助ディレクトリ:

- `tests/` — pytest
- `docs/` — 採点・デモ用メモ
- `openspec/` — 仕様・プロジェクト文脈

## 機能概要

### events_app

- 公開イベント一覧（タイトル、日付、場所、カテゴリ、主催者名）
- キーワード検索、カテゴリ / 日付フィルタ（HTMX で結果を部分更新）
- イベント作成・編集・削除（ログイン必須、作者または staff）
- 詳細ページでのブックマーク追加（HTMX）
- お気に入りの追加 / 解除
- マイページ（自分のイベント、下書き、お気に入り）
- デモデータ投入（`/seed-demo/`、何度実行しても重複しない）

### accounts

- ユーザー登録・ログイン・ログアウト
- プロフィール設定（表示名など）
- パスワード変更

### events_site

- 設定・静的ファイル / メディア配信
- `/healthz/` ヘルスチェック
- `/admin/` Django 管理画面

## データモデル

- `User` — 認証・イベント作者
- `Category` — イベント分類（Lecture, Concert など）
- `OrganizerProfile` — 主催者の表示名 / 連絡先
- `Event` — タイトル、説明、日付、場所、カテゴリ、作者、状態、ポスター画像
- `Bookmark` — イベントへのブックマーク（名前・メモ）
- `Favorite` — ユーザーごとのお気に入り

## アーキテクチャ

- UI は Django テンプレート
- 書き込みは `events_app/services.py`
- 読み取りクエリは `events_app/selectors.py`
- `views.py` はリクエスト / レスポンス処理に限定

## セットアップ

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

`http://127.0.0.1:8000/` を開きます。

ホームの **Seed demo data** でデモデータを投入できます。  
デモアカウント: `sota` / `mika` / `ren`（パスワードはいずれも `demo-pass-123`）

## 主なルート

| URL | 内容 |
| --- | --- |
| `/` | イベント一覧・検索・フィルタ |
| `/me/` | マイページ |
| `/events/new/` | イベント作成 |
| `/events/<id>/` | 詳細・ブックマーク |
| `/events/<id>/edit/` | 編集 |
| `/events/<id>/delete/` | 削除 |
| `/events/<id>/favorite/` | お気に入り切替 |
| `/partials/events/` | HTMX 用一覧 partial |
| `/seed-demo/` | デモデータ投入 |
| `/accounts/register/` | 会員登録 |
| `/accounts/login/` | ログイン |
| `/accounts/logout/` | ログアウト |
| `/accounts/settings/` | プロフィール設定 |
| `/accounts/password/change/` | パスワード変更 |
| `/healthz/` | ヘルスチェック |
| `/admin/` | 管理画面 |

## 開発コマンド

```bash
python3 -m uv run ruff check .
python3 -m uv run python manage.py check
python3 -m uv run pytest
python3 -m uv run python manage.py collectstatic --noinput
```

## デプロイ

Render（`render.yaml`）または Docker に対応しています。

```bash
# Docker 例
docker build -t event-listings .
docker run --rm -p 8000:8000 \
  -e DJANGO_DEBUG=0 \
  -e DJANGO_SECRET_KEY=change-me \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  event-listings
```

本番では `DJANGO_SECRET_KEY` と `DJANGO_ALLOWED_HOSTS` を設定し、デプロイ後に `/healthz/` を確認してください。

## 関連ドキュメント

- `docs/rubric-alignment.md` — 採点観点との対応
- `docs/project-review.md` — レビュー用まとめ
- `docs/final-demo-notes.md` — デモ手順
- `openspec/specs/` — 仕様
- `CONTRIBUTING.md` — 貢献・レビュー手順
- `AGENTS.md` — エージェント向け規約
