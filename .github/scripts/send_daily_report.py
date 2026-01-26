#!/usr/bin/env python3
"""
日報メール送信スクリプト

GitHub Actionsから呼び出され、指定された日報ファイルを
Gmailのsmtpサーバー経由でメール送信します。
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def load_daily_report(file_path: str) -> str:
    """
    日報ファイルの内容を読み込む

    Args:
        file_path: 日報ファイルのパス

    Returns:
        ファイルの内容

    Raises:
        FileNotFoundError: ファイルが存在しない場合
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"日報ファイルが見つかりません: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✅ 日報ファイルを読み込みました: {file_path}")
    print(f"📊 ファイルサイズ: {len(content)} 文字")

    return content


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
    # メールメッセージの作成
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # 本文を追加
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        # SMTPサーバーに接続
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(0)  # デバッグ出力を無効化
            server.starttls()  # TLS暗号化を開始
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        print(f"   ✅ 送信完了: {to_email}")

    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ 認証エラー: {to_email}", file=sys.stderr)
        print(f"      詳細: {e}", file=sys.stderr)
        raise
    except smtplib.SMTPException as e:
        print(f"   ❌ 送信エラー: {to_email}", file=sys.stderr)
        print(f"      詳細: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"   ❌ 予期しないエラー: {to_email}", file=sys.stderr)
        print(f"      詳細: {e}", file=sys.stderr)
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
    print(f"📧 Gmail SMTPサーバーに接続準備...")
    print(f"📤 {len(to_emails)}件の送信先に個別送信します")
    print()

    success_count = 0
    failure_count = 0
    failed_emails = []

    for i, to_email in enumerate(to_emails, 1):
        print(f"[{i}/{len(to_emails)}] 送信中: {to_email}")
        try:
            send_email(gmail_user, gmail_password, to_email, subject, body)
            success_count += 1
        except Exception as e:
            failure_count += 1
            failed_emails.append(to_email)
            print(f"   ⚠️ スキップして次へ進みます")

    print()
    print("=" * 60)
    print(f"📊 送信結果")
    print("=" * 60)
    print(f"✅ 成功: {success_count}件")
    if failure_count > 0:
        print(f"❌ 失敗: {failure_count}件")
        print(f"   失敗した送信先: {', '.join(failed_emails)}")
    print()

    return success_count, failure_count


def main():
    """メイン処理"""
    try:
        # 環境変数の取得
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        to_emails_str = os.environ.get('MAIL_TO')
        file_path = os.environ.get('FILE_PATH')
        date = os.environ.get('DATE')

        # 環境変数のチェック
        missing_vars = []
        if not gmail_user:
            missing_vars.append('GMAIL_USER')
        if not gmail_password:
            missing_vars.append('GMAIL_APP_PASSWORD')
        if not to_emails_str:
            missing_vars.append('MAIL_TO')
        if not file_path:
            missing_vars.append('FILE_PATH')
        if not date:
            missing_vars.append('DATE')

        if missing_vars:
            print(f"❌ 必要な環境変数が設定されていません: {', '.join(missing_vars)}", file=sys.stderr)
            sys.exit(1)

        # 送信先をカンマ区切りで分割（空白を除去）
        to_emails = [email.strip() for email in to_emails_str.split(',') if email.strip()]

        if not to_emails:
            print(f"❌ MAIL_TO に有効なメールアドレスが設定されていません", file=sys.stderr)
            sys.exit(1)

        print("=" * 60)
        print("📮 日報メール送信スクリプト開始")
        print("=" * 60)
        print(f"📅 対象日付: {date}")
        print(f"📄 ファイルパス: {file_path}")
        print(f"📬 送信先: {len(to_emails)}件")
        for i, email in enumerate(to_emails, 1):
            print(f"   [{i}] {email}")
        print()

        # 日報ファイルの読み込み
        report_content = load_daily_report(file_path)
        print()

        # メール本文の作成
        email_body = f"""本日の日報です。

─────────────────────────────

{report_content}

─────────────────────────────

※ このメールは GitHub Actions により自動送信されています。
"""

        # 複数の送信先に個別送信
        subject = f"[日報] {date}"
        success_count, failure_count = send_emails_to_multiple_recipients(
            gmail_user=gmail_user,
            gmail_password=gmail_password,
            to_emails=to_emails,
            subject=subject,
            body=email_body
        )

        print("=" * 60)
        if failure_count == 0:
            print("🎉 処理が正常に完了しました")
        else:
            print(f"⚠️ 処理が完了しましたが、{failure_count}件の送信に失敗しました")
        print("=" * 60)

        # 失敗があった場合はエラーコードを返す
        if failure_count > 0:
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"\n❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
