"""제안서 CRUD, 파일 업로드, 마크다운 내보내기."""
import io
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from api.db import get_conn
from services.parser import extract_text_from_pdf, extract_text_from_docx

bp = Blueprint("proposals", __name__)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_FILES = 5


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("", methods=["GET"])
def list_proposals():
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, title, status, created_at FROM proposals ORDER BY id DESC"
        ).fetchall()
        return jsonify({"ok": True, "data": [dict(r) for r in rows]})
    finally:
        conn.close()


@bp.route("/upload", methods=["POST"])
def upload_files():
    title = (request.form.get("title") or "").strip()
    manual_text = (request.form.get("text") or "").strip()
    files = request.files.getlist("files[]")

    if not title:
        return jsonify({"ok": False, "error": "제목을 입력해주세요"}), 400

    if len(files) > MAX_FILES:
        return jsonify({"ok": False, "error": f"파일은 최대 {MAX_FILES}개까지 업로드 가능합니다"}), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    texts = []
    saved_paths = []

    try:
        for f in files:
            if not f.filename:
                continue
            if not _allowed_file(f.filename):
                return jsonify({"ok": False, "error": f"허용되지 않는 파일 형식: {f.filename}"}), 400

            safe_name = secure_filename(f.filename)
            filepath = UPLOAD_DIR / safe_name
            f.save(filepath)
            saved_paths.append(filepath)

            ext = safe_name.rsplit(".", 1)[1].lower()
            if ext == "pdf":
                text = extract_text_from_pdf(str(filepath))
            elif ext == "docx":
                text = extract_text_from_docx(str(filepath))
            else:
                continue
            texts.append(f"\n\n===FILE: {f.filename}===\n\n{text}")

        if manual_text:
            texts.append(f"\n\n===MANUAL INPUT===\n\n{manual_text}")

        if not texts:
            return jsonify({"ok": False, "error": "파일 또는 텍스트를 입력해주세요"}), 400

        raw_text = "".join(texts)

        conn = get_conn()
        try:
            cur = conn.execute(
                "INSERT INTO proposals (title, raw_text) VALUES (?, ?)",
                (title, raw_text),
            )
            conn.commit()
            proposal_id = cur.lastrowid
        finally:
            conn.close()

        return jsonify({"ok": True, "data": {"proposal_id": proposal_id}})

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    finally:
        for p in saved_paths:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


@bp.route("/<int:pid>", methods=["GET"])
def get_proposal(pid):
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "제안서를 찾을 수 없습니다"}), 404

        data = dict(row)
        if data.get("rfp_json"):
            data["rfp_json"] = json.loads(data["rfp_json"])
        if data.get("toc_json"):
            data["toc_json"] = json.loads(data["toc_json"])

        sections = conn.execute(
            "SELECT id, level, title, order_idx, status, content FROM sections "
            "WHERE proposal_id=? ORDER BY order_idx",
            (pid,),
        ).fetchall()
        data["sections"] = [dict(s) for s in sections]

        return jsonify({"ok": True, "data": data})
    finally:
        conn.close()


@bp.route("/<int:pid>", methods=["DELETE"])
def delete_proposal(pid):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM proposals WHERE id=?", (pid,))
        conn.commit()
        return jsonify({"ok": True})
    finally:
        conn.close()


@bp.route("/<int:pid>/analyze", methods=["POST"])
def analyze_proposal(pid):
    """RFP 교차분석 실행."""
    from services.rfp_analyzer import analyze_rfp

    conn = get_conn()
    try:
        row = conn.execute("SELECT raw_text, status FROM proposals WHERE id=?", (pid,)).fetchone()
        if not row:
            return jsonify({"ok": False, "error": "제안서를 찾을 수 없습니다"}), 404
        if not row["raw_text"]:
            return jsonify({"ok": False, "error": "업로드된 텍스트가 없습니다"}), 400
    finally:
        conn.close()

    try:
        conn = get_conn()
        conn.execute("UPDATE proposals SET status='analyzing' WHERE id=?", (pid,))
        conn.commit()
        conn.close()

        rfp_json, rfp_summary, toc_json, full_response = analyze_rfp(row["raw_text"])

        conn = get_conn()
        try:
            conn.execute(
                "UPDATE proposals SET rfp_json=?, rfp_summary=?, toc_json=?, status='ready', updated_at=? WHERE id=?",
                (json.dumps(rfp_json, ensure_ascii=False),
                 rfp_summary,
                 json.dumps(toc_json, ensure_ascii=False),
                 datetime.now().isoformat(),
                 pid),
            )

            # toc_json -> sections 테이블에 행 삽입
            conn.execute("DELETE FROM sections WHERE proposal_id=?", (pid,))
            for item in toc_json:
                conn.execute(
                    "INSERT INTO sections (proposal_id, level, title, order_idx) VALUES (?, ?, ?, ?)",
                    (pid, item["level"], item["title"], item["order_idx"]),
                )
            conn.commit()

            # 생성된 sections 조회
            sections = conn.execute(
                "SELECT id, level, title, order_idx, status FROM sections WHERE proposal_id=? ORDER BY order_idx",
                (pid,),
            ).fetchall()

            return jsonify({
                "ok": True,
                "data": {
                    "rfp_json": rfp_json,
                    "rfp_summary": rfp_summary,
                    "toc": [dict(s) for s in sections],
                    "analysis_text": full_response,
                },
            })
        finally:
            conn.close()

    except Exception as e:
        logger.error("RFP analysis failed: %s", e, exc_info=True)
        conn = get_conn()
        conn.execute("UPDATE proposals SET status='draft' WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        return jsonify({"ok": False, "error": f"분석 실패: {str(e)[:300]}"}), 500


@bp.route("/<int:pid>/sections", methods=["GET"])
def list_sections(pid):
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, level, title, order_idx, status, content FROM sections "
            "WHERE proposal_id=? ORDER BY order_idx",
            (pid,),
        ).fetchall()
        return jsonify({"ok": True, "data": [dict(r) for r in rows]})
    finally:
        conn.close()


@bp.route("/<int:pid>/export", methods=["GET"])
def export_markdown(pid):
    conn = get_conn()
    try:
        proposal = conn.execute("SELECT title FROM proposals WHERE id=?", (pid,)).fetchone()
        if not proposal:
            return jsonify({"ok": False, "error": "제안서를 찾을 수 없습니다"}), 404

        sections = conn.execute(
            "SELECT level, title, content FROM sections WHERE proposal_id=? ORDER BY order_idx",
            (pid,),
        ).fetchall()

        lines = [f"# {proposal['title']}\n"]
        for s in sections:
            prefix = "#" * min(s["level"] + 1, 4)
            lines.append(f"\n{prefix} {s['title']}\n")
            if s["content"]:
                lines.append(f"{s['content']}\n")

        md_content = "\n".join(lines)
        buf = io.BytesIO(md_content.encode("utf-8"))
        return send_file(buf, as_attachment=True, download_name="proposal.md", mimetype="text/markdown")
    finally:
        conn.close()
