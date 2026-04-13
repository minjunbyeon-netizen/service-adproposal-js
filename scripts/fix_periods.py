"""create_v29.py 문자열 리터럴 안의 마침표만 제거 + 교훈 수정."""
import re

with open("scripts/create_v29.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1) 교훈 수정
content = content.replace("지혜가 실력이다", "지혜로운 가치를 배우는 대학, 지혜로운 당신을 만드는 대학")

# 2) 보호 패턴 (임시 치환)
placeholders = {}
counter = 0

def protect(m):
    global counter
    key = f"\x00EXT{counter}\x00"
    placeholders[key] = m.group(0)
    counter += 1
    return key

# 파일 확장자
content = re.sub(r"\.(jpg|jpeg|png|mp4|py|db|html|css|js|svg|json|toml|md|zip|txt)", protect, content)
# 숫자.숫자 (소수점: 96.4, 3.6, 1.25, 11.1 등)
content = re.sub(r"\d+\.\d+", protect, content)
# IP 주소 (이미 숫자.숫자로 보호됨)
# var(--xxx) 안의 내용은 . 이 없으므로 보호 불필요

# 이제 문자열 리터럴 안의 . 만 제거
# Python 소스에서 문자열 리터럴을 파싱
output = []
i = 0
n = len(content)
while i < n:
    ch = content[i]

    # 주석 (#) 처리 - 줄 끝까지 코드 취급 (그대로)
    # 문자열 시작 감지
    if ch in ("'", '"'):
        # triple quote 체크
        if content[i:i+3] in ('"""', "'''"):
            quote = content[i:i+3]
            output.append(quote)
            i += 3
            # triple quote 끝까지
            while i < n:
                if content[i:i+3] == quote:
                    output.append(quote)
                    i += 3
                    break
                elif content[i] == "\\":
                    output.append(content[i:i+2])
                    i += 2
                elif content[i] == ".":
                    pass  # 제거
                    i += 1
                else:
                    output.append(content[i])
                    i += 1
        else:
            quote = ch
            output.append(quote)
            i += 1
            while i < n:
                if content[i] == "\\":
                    output.append(content[i:i+2])
                    i += 2
                elif content[i] == quote:
                    output.append(content[i])
                    i += 1
                    break
                elif content[i] == ".":
                    pass  # 제거
                    i += 1
                elif content[i] == "\n":
                    # 줄바꿈이면 문자열 끝 (syntax error 방지)
                    output.append(content[i])
                    i += 1
                    break
                else:
                    output.append(content[i])
                    i += 1
    else:
        output.append(ch)
        i += 1

result = "".join(output)

# placeholder 복원
for key, val in placeholders.items():
    result = result.replace(key, val)

with open("scripts/create_v29.py", "w", encoding="utf-8") as f:
    f.write(result)

print("Done: periods removed from strings, 교훈 updated")


