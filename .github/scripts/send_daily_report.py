#!/usr/bin/env python3
"""
日報メール送信スクリプト

GitHub Actionsから呼び出され、直近N日分の未送信日報を検出し、
Gmailのsmtpサーバー経由でメール送信します。
送信後はfrontmatterに送信済みフラグを記録します。
"""

import os
import re
import sys
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

import yaml


def parse_frontmatter(content: str) -> tuple[Optional[dict], str]:
    """
    ファイル内容からfrontmatterを解析する

    Args:
        content: ファイルの全内容

    Returns:
        (frontmatter辞書, 本文) のタプル。frontmatterがなければ(None, content)
    """
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter or {}, body
        except yaml.YAMLError:
            return None, content

    return None, content


def update_frontmatter(content: str, updates: dict) -> str:
    """
    frontmatterを更新（なければ新規追加）

    Args:
        content: ファイルの全内容
        updates: 更新する辞書

    Returns:
        更新後のファイル内容
    """
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        frontmatter = {}

    frontmatter.update(updates)

    # frontmatterをYAML形式に変換
    yaml_content = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False
    ).strip()

    return f"---\n{yaml_content}\n---\n{body}"


def is_sent(content: str) -> bool:
    """
    日報が送信済みかどうかを判定

    Args:
        content: ファイルの全内容

    Returns:
        送信済みならTrue
    """
    frontmatter, _ = parse_frontmatter(content)

    if frontmatter is None:
        return False

    return frontmatter.get('sent', False) is True


def get_daily_report_path(date: datetime) -> Path:
    """
    日付から日報ファイルのパスを生成

    Args:
        date: 対象日付

    Returns:
        日報ファイルのパス
    """
    year = date.strftime('%Y')
    month = date.strftime('%m')
    date_str = date.strftime('%Y-%m-%d')
    return Path(f"10_daily/{year}/{month}/{date_str}.md")


def find_unsent_reports(lookback_days: int) -> list[tuple[datetime, Path]]:
    """
    直近N日分の未送信日報を検出

    Args:
        lookback_days: 何日前まで走査するか

    Returns:
        (日付, パス) のリスト（古い順）
    """
    unsent = []
    today = datetime.now()

    for i in range(lookback_days, -1, -1):  # 古い順に走査
        target_date = today - timedelta(days=i)
        path = get_daily_report_path(target_date)

        if not path.exists():
            print(f"⚠️  {target_date.strftime('%Y-%m-%d')}: ファイルなし（スキップ）")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if is_sent(content):
            print(f"✅ {target_date.strftime('%Y-%m-%d')}: 送信済み")
        else:
            print(f"📬 {target_date.strftime('%Y-%m-%d')}: 未送信 → 送信対象")
            unsent.append((target_date, path))

    return unsent


def load_daily_report(file_path: Path) -> str:
    """
    日報ファイルの内容を読み込む

    Args:
        file_path: 日報ファイルのパス

    Returns:
        ファイルの内容

    Raises:
        FileNotFoundError: ファイルが存在しない場合
    """
    if not file_path.exists():
        raise FileNotFoundError(f"日報ファイルが見つかりません: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def mark_as_sent(file_path: Path) -> None:
    """
    日報ファイルに送信済みフラグを追加

    Args:
        file_path: 日報ファイルのパス
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sent_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')
    updated_content = update_frontmatter(content, {
        'sent': True,
        'sent_at': sent_at
    })

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"   📝 送信済みフラグを記録しました")


def send_email(
    gmail_user: str,
    gmail_password: str,
    to_email: str,
    subject: str,
    body: str
) -> None:
    """
    Gmail経由でメールを送信する（1通のみ）

    Args:
        gmail_user: 送信元Gmailアドレス
        gmail_password: Gmailアプリパスワード
        to_email: 送信先メールアドレス（1件）
        subject: メールの件名
        body: メール本文

    Raises:
        smtplib.SMTPException: メール送信に失敗した場合
    """
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(0)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        print(f"      ✅ {to_email}")

    except smtplib.SMTPAuthenticationError as e:
        print(f"      ❌ 認証エラー: {to_email}", file=sys.stderr)
        raise
    except smtplib.SMTPException as e:
        print(f"      ❌ 送信エラー: {to_email}", file=sys.stderr)
        raise


def send_emails_to_multiple_recipients(
    gmail_user: str,
    gmail_password: str,
    to_emails: list[str],
    subject: str,
    body: str
) -> tuple[int, int]:
    """
    複数の送信先に個別にメールを送信する

    Args:
        gmail_user: 送信元Gmailアドレス
        gmail_password: Gmailアプリパスワード
        to_emails: 送信先メールアドレスのリスト
        subject: メールの件名
        body: メール本文

    Returns:
        (成功数, 失敗数) のタプル
    """
    success_count = 0
    failure_count = 0

    for to_email in to_emails:
        try:
            send_email(gmail_user, gmail_password, to_email, subject, body)
            success_count += 1
        except Exception:
            failure_count += 1

    return success_count, failure_count


def send_daily_report(
    date: datetime,
    file_path: Path,
    gmail_user: str,
    gmail_password: str,
    to_emails: list[str]
) -> bool:
    """
    1つの日報を送信する

    Args:
        date: 対象日付
        file_path: 日報ファイルのパス
        gmail_user: 送信元Gmailアドレス
        gmail_password: Gmailアプリパスワード
        to_emails: 送信先メールアドレスのリスト

    Returns:
        全員への送信に成功したらTrue
    """
    date_str = date.strftime('%Y-%m-%d')
    print(f"\n📮 [{date_str}] 送信中...")

    # 日報読み込み
    content = load_daily_report(file_path)
    _, body_content = parse_frontmatter(content)

    # メール本文作成
    email_body = f"""{date_str} の日報です。

─────────────────────────────

{body_content.strip()}

─────────────────────────────

"""

    # 送信
    subject = f"[日報] {date_str}"
    success_count, failure_count = send_emails_to_multiple_recipients(
        gmail_user=gmail_user,
        gmail_password=gmail_password,
        to_emails=to_emails,
        subject=subject,
        body=email_body
    )

    print(f"   📊 結果: {success_count}成功 / {failure_count}失敗")

    # 全員に送信成功した場合のみ送信済みフラグを記録
    if failure_count == 0:
        mark_as_sent(file_path)
        return True
    else:
        print(f"   ⚠️  一部失敗のため送信済みフラグは記録しません")
        return False


def main():
    """メイン処理"""
    try:
        # 環境変数の取得
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        to_emails_str = os.environ.get('MAIL_TO')
        lookback_days = int(os.environ.get('LOOKBACK_DAYS', '7'))

        # 環境変数のチェック
        missing_vars = []
        if not gmail_user:
            missing_vars.append('GMAIL_USER')
        if not gmail_password:
            missing_vars.append('GMAIL_APP_PASSWORD')
        if not to_emails_str:
            missing_vars.append('MAIL_TO')

        if missing_vars:
            print(f"❌ 必要な環境変数が設定されていません: {', '.join(missing_vars)}", file=sys.stderr)
            sys.exit(1)

        # 送信先をカンマ区切りで分割
        to_emails = [email.strip() for email in to_emails_str.split(',') if email.strip()]

        if not to_emails:
            print("❌ MAIL_TO に有効なメールアドレスが設定されていません", file=sys.stderr)
            sys.exit(1)

        print("=" * 60)
        print("📮 日報メール送信スクリプト開始")
        print("=" * 60)
        print(f"📅 走査期間: 直近 {lookback_days} 日間")
        print(f"📬 送信先: {len(to_emails)}件")
        for email in to_emails:
            print(f"   - {email}")
        print()

        # 未送信日報の検出
        print("─" * 60)
        print("🔍 未送信日報を検出中...")
        print("─" * 60)
        unsent_reports = find_unsent_reports(lookback_days)

        if not unsent_reports:
            print()
            print("=" * 60)
            print("✅ 未送信の日報はありません")
            print("=" * 60)
            return

        print()
        print(f"📬 {len(unsent_reports)}件の未送信日報を送信します")

        # 各日報を送信
        total_success = 0
        total_failure = 0

        for date, path in unsent_reports:
            if send_daily_report(date, path, gmail_user, gmail_password, to_emails):
                total_success += 1
            else:
                total_failure += 1

        # 結果サマリー
        print()
        print("=" * 60)
        print("📊 処理結果サマリー")
        print("=" * 60)
        print(f"✅ 送信成功: {total_success}件")
        if total_failure > 0:
            print(f"❌ 送信失敗: {total_failure}件")
            print("=" * 60)
            sys.exit(1)
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
