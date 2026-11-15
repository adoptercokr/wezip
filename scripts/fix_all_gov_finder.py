import re
from pathlib import Path

ROOT = Path(r"01-Nova-Web-Studio\money-calc")
gov_file = ROOT / "gov-finder.html"
content = gov_file.read_text(encoding="utf-8")

print("Original length:", len(content))

# Step 1: Remove all duplicate static catalog sections between '<!-- 섹션 3-2:' and '<!-- 섹션 4: FAQ -->'
first_sec_marker = "        <!-- 섹션 3-2:"
faq_marker = "            <!-- 섹션 4: FAQ -->"

if first_sec_marker in content and faq_marker in content:
    idx_first = content.find(first_sec_marker)
    idx_faq = content.find(faq_marker)
    content = content[:idx_first] + content[idx_faq:]
    print("Removed duplicate static catalog blocks successfully.")
else:
    print("WARNING: Could not find section markers for deduplication.")

# Step 2: Ensure all 100 policies have explicit category
# Let's check policies array
# Specifically, we know policies with id small_biz_electricity and durunuri should be business,
# and any policy without category should be personal.
# We can do this in JS parsing or regex on the policy definitions.

# Let's inspect where POLICIES array is defined
array_start = content.find("const POLICIES = [")
array_end = content.find("];\n", array_start)
if array_end == -1:
    array_end = content.find("];", array_start)

policies_str = content[array_start:array_end+2]

# In policies_str, for each object:
# If it has id: 'small_biz_electricity' or id: 'durunuri', ensure category: 'business'
# If it does not have category:, add category: 'personal', right after id: '...'

def fix_policy_object(m):
    obj_text = m.group(0)
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", obj_text)
    if not id_m:
        return obj_text
    p_id = id_m.group(1)
    
    if "category:" in obj_text:
        # If it's small_biz_electricity or durunuri, make sure it's business
        if p_id in ("small_biz_electricity", "durunuri"):
            obj_text = re.sub(r"category:\s*['\"][^'\"]+['\"]", "category: 'business'", obj_text)
        return obj_text
    else:
        # Add category
        cat = "business" if p_id in ("small_biz_electricity", "durunuri") else "personal"
        # insert category right after id: '...'
        obj_text = re.sub(r"(id:\s*['\"][^'\"]+['\"],)", rf"\1\n            category: '{cat}',", obj_text, count=1)
        return obj_text

# Policy object pattern
# Match from { id: ... to next }, or end of array
obj_pattern = re.compile(r"\{\s*id:\s*['\"][^'\"]+['\"][\s\S]*?\n        \}")
new_policies_str = obj_pattern.sub(fix_policy_object, policies_str)

content = content[:array_start] + new_policies_str + content[array_end+2:]
print("Updated policy categories.")

# Step 3: Replace outdated hero and subtitle text
replacements = [
    (
        "개인 복지 35종 &amp; 소상공인 25종 등 60대 지원금 DB",
        "개인 복지 55종 &amp; 소상공인 45종 등 100대 지원금 DB"
    ),
    (
        "60대 핵심 지원금(개인·가구 복지 35종 및 소상공인·자영업자 특화 지원금 25종)",
        "100대 핵심 지원금(개인·가구 복지 55종 및 소상공인·자영업자 특화 지원금 45종)"
    ),
    (
        "<span>전체 지원금 (100건)</span>",
        '<span>전체 지원금 (<span id="tabCountAll">100건</span>)</span>'
    ),
    (
        '<span class="text-blue-900 font-extrabold">소상공인·사업자 지원금 (25건)</span>',
        '<span class="text-blue-900 font-extrabold">소상공인·사업자 지원금 (<span id="tabCountBiz">45건</span>)</span>'
    ),
    (
        '<span>개인·가구 지원금 (35건)</span>',
        '<span>개인·가구 지원금 (<span id="tabCountPersonal">55건</span>)</span>'
    ),
    (
        "실시간 60대 지원금 검색",
        "실시간 100대 지원금 검색"
    ),
    (
        "전체 60개 지원금 DB",
        "전체 100개 지원금 DB"
    ),
    (
        "const isBizPolicy = p.category === 'business' || p.id === 'small_biz_electricity' || p.id === 'durunuri';",
        "const isBizPolicy = p.category === 'business';"
    ),
    (
        "// 3. 사업자 탭이면 10대 소상공인 정책 100% 노출",
        "// 3. 사업자 탭이면 45대 소상공인 정책 100% 노출"
    )
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:40]} -> {new[:40]}")
    else:
        print(f"Notice: pattern not found: {old[:40]}")

# Step 4: Inject syncTabCounts() into JavaScript
sync_fn = """
        // 대분류 탭 건수 동적 실시간 바인딩
        function syncTabCounts() {
            const total = POLICIES.length;
            const biz = POLICIES.filter(p => p.category === 'business').length;
            const personal = POLICIES.filter(p => p.category === 'personal').length;
            const elAll = document.getElementById('tabCountAll');
            const elBiz = document.getElementById('tabCountBiz');
            const elPersonal = document.getElementById('tabCountPersonal');
            if (elAll) elAll.textContent = `${total}건`;
            if (elBiz) elBiz.textContent = `${biz}건`;
            if (elPersonal) elPersonal.textContent = `${personal}건`;
        }
"""

if "function syncTabCounts()" not in content:
    # insert before runPolicyMatch
    content = content.replace("function runPolicyMatch() {", sync_fn + "\n        function runPolicyMatch() {")
    # also call syncTabCounts() inside DOMContentLoaded
    content = content.replace("runPolicyMatch();", "syncTabCounts();\n            runPolicyMatch();", 1)
    print("Injected syncTabCounts() and called on init.")

gov_file.write_text(content, encoding="utf-8")
print("Saved gov-finder.html. New length:", len(content))
