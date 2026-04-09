"""섹션 생성 + 대화형 수정 API."""
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from api.db import get_conn

bp = Blueprint("chat", __name__)
logger = logging.getLogger(__name__)


@bp.route("/sections/<int:sid>/generate", methods=["POST"])
def generate_section(sid):
    """섹션 초안 생성."""
    from services.section_writer import generate_section as gen

    conn = get_conn()
    try:
        section = conn.execute("SELECT * FROM sections WHERE id=?", (sid,)).fetchone()
        if not section:
            return jsonify({"ok": False, "error": "섹션을 찾을 수 없습니다"}), 404

        proposal = conn.execute(
            "SELECT rfp_summary FROM proposals WHERE id=?",
            (section["proposal_id"],),
        ).fetchone()
        if not proposal or not proposal["rfp_summary"]:
            return jsonify({"ok": False, "error": "RFP 분석이 완료되지 않았습니다"}), 400
    finally:
        conn.close()

    try:
        conn = get_conn()
        conn.execute(
            "UPDATE sections SET status='generating', updated_at=? WHERE id=?",
            (datetime.now().isoformat(), sid),
        )
        conn.commit()
        conn.close()

        content = gen(
            rfp_summary=proposal["rfp_summary"],
            section_title=section["title"],
            section_level=section["level"],
        )

        conn = get_conn()
        try:
            conn.execute(
                "UPDATE sections SET content=?, status='done', updated_at=? WHERE id=?",
                (content, datetime.now().isoformat(), sid),
            )
            # assistant 메시지 저장
            conn.execute(
                "INSERT INTO messages (section_id, role, content) VALUES (?, 'assistant', ?)",
                (sid, content),
            )
            conn.commit()
            return jsonify({"ok": True, "data": {"section_id": sid, "content": content}})
        finally:
            conn.close()

    except Exception as e:
        logger.error("Section generation failed: %s", e, exc_info=True)
        conn = get_conn()
        conn.execute(
            "UPDATE sections SET status='pending', updated_at=? WHERE id=?",
            (datetime.now().isoformat(), sid),
        )
        conn.commit()
        conn.close()
        return jsonify({"ok": False, "error": f"생성 실패: {str(e)[:300]}"}), 500


@bp.route("/sections/<int:sid>/message", methods=["POST"])
def post_message(sid):
    """사용자 메시지를 저장하고 AI 응답을 생성한다."""
    from services.section_writer import reply_section

    data = request.get_json()
    if not data or not (data.get("content") or "").strip():
        return jsonify({"ok": False, "error": "메시지를 입력해주세요"}), 400

    user_text = data["content"].strip()

    conn = get_conn()
    try:
        section = conn.execute("SELECT * FROM sections WHERE id=?", (sid,)).fetchone()
        if not section:
            return jsonify({"ok": False, "error": "섹션을 찾을 수 없습니다"}), 404

        proposal = conn.execute(
            "SELECT rfp_summary FROM proposals WHERE id=?",
            (section["proposal_id"],),
        ).fetchone()

        # 사용자 메시지 저장
        conn.execute(
            "INSERT INTO messages (section_id, role, content) VALUES (?, 'user', ?)",
            (sid, user_text),
        )
        conn.commit()

        # 대화 이력 조회
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE section_id=? ORDER BY id",
            (sid,),
        ).fetchall()
        history = [{"role": r["role"], "content": r["content"]} for r in rows]
    finally:
        conn.close()

    try:
        reply = reply_section(
            rfp_summary=proposal["rfp_summary"] or "",
            section_title=section["title"],
            section_content=section["content"],
            history=history,
        )

        conn = get_conn()
        try:
            # AI 응답 저장
            conn.execute(
                "INSERT INTO messages (section_id, role, content) VALUES (?, 'assistant', ?)",
                (sid, reply),
            )
            # 섹션 내용 업데이트
            conn.execute(
                "UPDATE sections SET content=?, status='done', updated_at=? WHERE id=?",
                (reply, datetime.now().isoformat(), sid),
            )
            conn.commit()
            return jsonify({"ok": True, "data": {"content": reply}})
        finally:
            conn.close()

    except Exception as e:
        logger.error("Reply failed: %s", e, exc_info=True)
        return jsonify({"ok": False, "error": f"응답 생성 실패: {str(e)[:300]}"}), 500


@bp.route("/sections/<int:sid>/messages", methods=["GET"])
def get_messages(sid):
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT role, content, created_at FROM messages WHERE section_id=? ORDER BY id",
            (sid,),
        ).fetchall()
        return jsonify({"ok": True, "data": [dict(r) for r in rows]})
    finally:
        conn.close()


@bp.route("/sections/<int:sid>", methods=["PUT"])
def update_section(sid):
    """섹션 내용 수동 편집."""
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"ok": False, "error": "content 필드가 필요합니다"}), 400

    conn = get_conn()
    try:
        conn.execute(
            "UPDATE sections SET content=?, status='done', updated_at=? WHERE id=?",
            (data["content"], datetime.now().isoformat(), sid),
        )
        conn.commit()
        return jsonify({"ok": True})
    finally:
        conn.close()
