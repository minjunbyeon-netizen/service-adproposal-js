"""adproposal-js -- 광고제안서 디벨롭."""
import os
import logging
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

    from api.db import init_db, migrate_db
    init_db()
    migrate_db()

    from api.proposals import bp as proposals_bp
    from api.chat import bp as chat_bp

    app.register_blueprint(proposals_bp, url_prefix="/api/proposals")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/report")
    def report():
        return render_template("report.html")

    @app.route("/health")
    def health():
        return jsonify({"ok": True, "service": "adproposal-js"})

    @app.route("/pt")
    def pt_latest():
        """최신 PT로 리다이렉트 -- PT 발표용 단축 URL."""
        from flask import redirect
        from api.db import get_conn
        conn = get_conn()
        try:
            row = conn.execute(
                "SELECT id FROM proposals ORDER BY id DESC LIMIT 1"
            ).fetchone()
            if row:
                return redirect(f"/api/proposals/{row['id']}/export-html")
            return jsonify({"ok": False, "error": "PT 없음", "code": "NOT_FOUND"}), 404
        finally:
            conn.close()

    @app.route("/assets/<path:filename>")
    def serve_assets(filename):
        assets_dir = Path(__file__).resolve().parent / "assets"
        return send_from_directory(assets_dir, filename)

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"ok": False, "error": "잘못된 요청입니다", "code": "BAD_REQUEST"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"ok": False, "error": "찾을 수 없습니다", "code": "NOT_FOUND"}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"ok": False, "error": "파일이 너무 큽니다 (최대 50MB)", "code": "TOO_LARGE"}), 413

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"ok": False, "error": "서버 오류가 발생했습니다", "code": "INTERNAL"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 8881))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
