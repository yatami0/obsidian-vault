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
    Gmail経由でメールを送信する

    Args:
        gmail_user: 送信元Gmailアドレス
        gmail_password: Gmailアプリパスワード
        to_email: 送信先メールアドレス
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
        print(f"📧 Gmail SMTPサーバーに接続中...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(0)  # デバッグ出力を無効化
            server.starttls()  # TLS暗号化を開始

            print(f"🔐 認証中...")
            server.login(gmail_user, gmail_password)

            print(f"📤 メール送信中: {to_email}")
            server.send_message(msg)

        print(f"✅ メール送信完了")
        print(f"   送信元: {gmail_user}")
        print(f"   送信先: {to_email}")
        print(f"   件名: {subject}")

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ 認証エラー: Gmail のユーザー名またはアプリパスワードが正しくありません", file=sys.stderr)
        print(f"   詳細: {e}", file=sys.stderr)
        raise
    except smtplib.SMTPException as e:
        print(f"❌ メール送信エラー: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}", file=sys.stderr)
        raise


def main():
    """メイン処理"""
    try:
        # 環境変数の取得
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        to_email = os.environ.get('MAIL_TO')
        file_path = os.environ.get('FILE_PATH')
        date = os.environ.get('DATE')

        # 環境変数のチェック
        missing_vars = []
        if not gmail_user:
            missing_vars.append('GMAIL_USER')
        if not gmail_password:
            missing_vars.append('GMAIL_APP_PASSWORD')
        if not to_email:
            missing_vars.append('MAIL_TO')
        if not file_path:
            missing_vars.append('FILE_PATH')
        if not date:
            missing_vars.append('DATE')

        if missing_vars:
            print(f"❌ 必要な環境変数が設定されていません: {', '.join(missing_vars)}", file=sys.stderr)
            sys.exit(1)

        print("=" * 60)
        print("📮 日報メール送信スクリプト開始")
        print("=" * 60)
        print(f"📅 対象日付: {date}")
        print(f"📄 ファイルパス: {file_path}")
        print()

        # 日報ファイルの読み込み
        report_content = load_daily_report(file_path)
        print()

        # メール本文の作成
        email_body = f"""本日の日報をお送りします。

─────────────────────────────

{report_content}

─────────────────────────────

※ このメールは GitHub Actions により自動送信されています。
"""

        # メールの送信
        subject = f"[日報] {date}"
        send_email(
            gmail_user=gmail_user,
            gmail_password=gmail_password,
            to_email=to_email,
            subject=subject,
            body=email_body
        )

        print()
        print("=" * 60)
        print("🎉 処理が正常に完了しました")
        print("=" * 60)

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
