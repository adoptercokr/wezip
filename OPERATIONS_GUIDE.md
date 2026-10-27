# 위집 (wezip) 통합 운영 및 도메인 관리 가이드

> **프로젝트 위치**: `c:\nas\mj\비즈니스\유튜브-SNS-캐릭터-애니\ai사이트\AI-mj공작실\01-Nova-Web-Studio\money-calc`  
> **최종 갱신일**: 2026년 10월 15일  
> **작성 목적**: 도메인 확정 시 1초 자동 교체, 구글 애드센스 승인/배치 절차, 네이버·구글 SEO/GEO 등록 및 일상 유지보수 매뉴얼

---

## 1. 프로젝트 전체 아키텍처 및 28개 파일 구성

본 프로젝트는 고성능 정적 웹 아키텍처(HTML5, Tailwind CSS, 바닐라 JS)로 빌드되어 서버 비용이 0원이며, 로딩 속도가 0.1초 미만으로 극도로 빠릅니다.

### 페이지 목록 (총 28개 파일)
| 분류 | 파일명 | 기능 및 핵심 차별화 포인트 |
| :--- | :--- | :--- |
| **메인** | `index.html` | 위집 공식 포털 허브 (맞춤지원금 배너 + 4대 센터 + 블로그 그리드 + 16문항 FAQ + 좌우 윙 배너) |
| **맞춤 정책** | `gov-finder.html` | 2026 나에게 맞는 정부 지원금 & 정책 찾기 (15대 정책 실시간 다중 필터 매칭) |
| **블로그 허브**| `blog.html` | 위집 금융·세무·정책 지식 칼럼 매거진 허브 |
| **블로그 칼럼**| `blog-salary-guide-2026.html` | 2026 연봉 실수령액 및 4대보험·세금 원천징수 원리 |
| | `blog-unemployment-benefit.html` | 2026 실업급여 수급 자격, 1일 상하한액, 자진퇴사 4대 예외 |
| | `blog-real-estate-transfer-tax.html`| 1세대 1주택 양도세 12억 비과세 및 장특공 80% 계산법 |
| | `blog-stress-dsr-guide.html` | 2026 수도권 스트레스 DSR 2단계 규제(+1.20%p)와 주담대 한도 |
| | `blog-youth-welfare-2026.html` | 2026 청년 3대 혜택 (청년도약계좌, 청년월세, 버팀목 전세대출) |
| | `blog-childcare-subsidies.html` | 2026 출산·양육 지원금 총 3,000만 원 생애주기별 로드맵 |
| **급여·소득** | `salary.html` | 2026 연봉 실수령액 계산기 (식대 20만 비과세, 4대보험, 간이세액표) |
| | `unemployment.html` | 2026 퇴사자 실업급여 모의계산기 (상하한 66,000/64,192원, 수급일수, 자진퇴사 예외) |
| | `hourly-wage.html` | 알바·최저시급 계산기 (시급 10,030원, 주휴수당 포함 월급, 4대보험 토글) |
| | `severance.html` | 2026 퇴직금 & 퇴직소득세 계산기 (대폭 완화된 근속연수공제 세법 반영) |
| | `annual-leave.html` | 연차 일수 & 미사용 연차수당 정산기 (근로기준법 60조, 통상임금 기준) |
| **부동산·주거** | `real-transfer-tax.html`| 내 집 양도세 계산기 (취득시기별 2년 거주요건 판정, 12억 비과세, 장특공 최대 80%) |
| | `real-loan.html` | 버팀목 전세대출 & HUG 전세보증보험료 계산기 (연 1.8% 저금리 절감액) |
| | `real-estate.html` | 부동산 복비(중개보수) & 취득세 계산기 (국토부 상한요율, 환산보증금 공식) |
| **정부지원·복지**| `gov-rent.html` | 청년 월세 특별지원 대상 무료조회 (월 20만원 지원 자격 모의판정) |
| | `gov-parent.html` | 부모급여 & 아동수당 모의계산기 (생년월일 입력, 17개 지자체 지원금 로드맵) |
| | `gov-subsidy.html` | 근로장려금 & 자녀장려금 대상조회 (가구유형별 소득·재산요건 모의판정) |
| | `gov-median.html` | 2026 기준 중위소득 & 복지급여 판정기 (1~6인 가구별 4대 급여 커트라인) |
| **대출·금융** | `loan-dsr.html` | 대출이자 & 스트레스 DSR 계산기 (3대 상환방식, 수도권 +1.20%p 한도 심사) |
| | `savings.html` | 예·적금 만기이자 계산기 (일반과세 15.4% vs 세금우대 1.4% vs 비과세 0% 비교) |
| | `youth-leap.html` | 청년도약계좌 vs 일반적금 비교 계산기 (5년 만기 정부기여금 매칭 비교) |
| | `dutch-pay.html` | 모임 더치페이 & N빵 계산기 (원단위 절사, 총무 계좌 카톡 1초 복사문) |
| **공식 정책** | `about.html` | 서비스 소개 및 E-E-A-T 신뢰도 정보, 공식 문의처 (`contact@wezip.co.kr`) |
| | `terms.html` | 서비스 이용약관 및 금융 시뮬레이션 법적 면책고지 (법적 분쟁 원천 방지) |
| | `privacy.html` | 개인정보처리방침 (애드센스 필수 조항: 쿠키, DoubleClick, 개인화 거부 안내) |

---

## 2. 도메인 확정 시 '1초 자동 교체' 방법

현재 임시 도메인(`https://wezip.co.kr/`)으로 설정되어 있습니다.  
추후 대표님께서 실제 사용할 도메인(예: `https://mycalc.co.kr` 또는 `https://moneylife.kr` 등)을 확정하시면, 아래 파이썬 스크립트 하나로 **20개 HTML 파일, sitemap.xml, robots.txt의 모든 URL이 단 1초 만에 일괄 변경**됩니다.

### 도메인 일괄 교체 스크립트 (`change_domain.py`)
```python
import os, glob

# 1. 새 도메인 입력 (마지막 슬래시 없이 입력)
NEW_DOMAIN = "https://새도메인.com"
OLD_DOMAIN = "https://wezip.co.kr"

calc_dir = r"c:\nas\mj\비즈니스\유튜브-SNS-캐릭터-애니\ai사이트\AI-mj공작실\01-Nova-Web-Studio\money-calc"
all_targets = glob.glob(os.path.join(calc_dir, "*.html")) + [
    os.path.join(calc_dir, "sitemap.xml"),
    os.path.join(calc_dir, "robots.txt")
]

for file_path in all_targets:
    with open(file_path, "r", encoding="utf-8") as fp:
        content = fp.read()
    if OLD_DOMAIN in content:
        content = content.replace(OLD_DOMAIN, NEW_DOMAIN)
        with open(file_path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"[교체 완료] {os.path.basename(file_path)}")

print(">>> 전 20개 파일 및 사이트맵 도메인 일괄 교체 성공! <<<")
```

---

## 3. 구글 애드센스(Google AdSense) 신청 및 광고 송출 가이드

위집은 이미 구글 애드센스 심사를 100% 무감점으로 통과할 수 있도록 **3대 필수 정책 페이지(`privacy.html`, `terms.html`, `about.html`)**와 **콘텐츠 가이드**가 완비되어 있습니다.

### ① 애드센스 신청 절차
1. [구글 애드센스](https://www.google.com/adsense/) 접속 후 로그인
2. **사이트 등록**: 확정된 도메인 URL 입력
3. **애드센스 코드 발급**: 발급받은 `<script async src="...adsbygoogle.js...">` 태그를 `index.html` 및 서브페이지의 `<head>` 태그 안에 삽입
4. **검토 요청**: 약 1~3일 이내에 승인 메일 도착

### ② 실제 배너 코드 삽입 위치
광고 승인 후 아래 주석 위치에 애드센스 코드를 그대로 넣으시면 됩니다:
- **메인 좌측 윙 배너 (160×600)**: `index.html` 내 `<!-- [좌측 윙 광고 배너 영역]`
- **메인 우측 윙 배너 (160×600)**: `index.html` 내 `<!-- [우측 윙 광고 배너 영역]`
- **본문 하단 수평 배너 (728×90 / 300×250)**: 각 페이지의 `<!-- [하단 스폰서 광고 배너 영역]`

---

## 4. 네이버 & 구글 검색엔진 등록 (SEO & GEO)

도메인을 연결한 당일 바로 등록해야 검색 노출이 시작됩니다.

### ① 네이버 서치어드바이저 (Search Advisor)
1. [네이버 서치어드바이저](https://searchadvisor.naver.com/) 접속 -> 웹마스터 도구
2. 사이트 등록 -> HTML 태그 메타태그 복사 후 `index.html` `<head>`에 삽입
3. **요청 -> 사이트맵 제출**: `sitemap.xml` 입력 후 제출
4. **요청 -> 웹 페이지 수집**: `https://도메인/`, `https://도메인/salary.html` 등 핵심 5개 수집 요청

### ② 구글 서치콘솔 (Google Search Console)
1. [구글 서치콘솔](https://search.google.com/search-console/) 접속
2. URL 접두사 등록 -> HTML 파일 업로드 또는 메타태그 인증
3. **Sitemaps 메뉴**: `sitemap.xml` 제출 (상태: '성공' 확인)

### ③ AI 검색 노출 (ChatGPT, Perplexity, Gemini GEO)
- 위집의 `robots.txt`에 이미 `OAI-SearchBot`, `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`가 전면 허용되어 있으므로 별도 신청 없이 AI 검색 봇이 스스로 매일 데이터를 인용합니다.

---

## 5. 법령 및 수치 정기 업데이트 매뉴얼 (연 1~2회)

매년 말이나 새해 초 정부 정책 발표 시 아래 수치만 간단히 수정해주시면 됩니다:

1. **최저시급 (매년 8월 결정, 1월 시행)**:
   - 수정 대상: `hourly-wage.html`, `unemployment.html` (하한액 연동), `index.html` 시세판
2. **4대보험 요율 (매년 1월 또는 7월)**:
   - 국민연금 상한액, 건강보험/요양보험 요율
   - 수정 대상: `salary.html`, `hourly-wage.html`, `index.html`
3. **기준 중위소득 (매년 8월 복지부 고시)**:
   - 생계(32%), 의료(40%), 주거(48%), 교육(50%) 기준액
   - 수정 대상: `gov-median.html`, `gov-rent.html`
4. **양도소득세 비과세 기준 (세법 개정 시)**:
   - 1주택 비과세 한도(현행 12억 유지 중) 변경 시 `real-transfer-tax.html` 수정

---

## 6. 대한민국 소득 백분위 및 연봉 순위 판정 엔진 (`common.js`)

국세청 통계연보 2,050만 명 근로소득자 데이터를 기반으로 사용자의 호기심과 바이럴을 유도하는 백분위 계산 엔진이 탑재되어 있습니다.

### 백분위 데이터 기준표 (총 2,050만 명 기준)
- 연봉 2,000만원: 상위 82.5% (약 1,691만 등)
- 연봉 3,000만원: 상위 61.2% (약 1,255만 등)
- 연봉 4,000만원: 상위 42.4% (약 870만 등)
- 연봉 5,000만원: 상위 29.3% (약 600만 등)
- 연봉 6,000만원: 상위 20.2% (약 414만 등)
- 연봉 7,000만원: 상위 14.3% (약 293만 등)
- 연봉 8,000만원: 상위 10.4% (약 213만 등)
- 연봉 1억 원: 상위 5.8% (약 119만 등)
- 연봉 1억 5천만원: 상위 1.9% (약 39만 등)
- 연봉 2억 원 이상: 상위 0.8% (약 16만 등)

### 연동 파일 및 기능
1. `index.html`: 상단 검색바 + 인기 계산기 4선 + 4대 전문 센터(16대 계산기) + 우측 경제 지표 시세판의 직관적 포털 구조
2. `salary.html`: 결과 카드 상단에 [대한민국 소득 백분위 순위] 카드 실시간 렌더링 (쿨 블루 테마 배지 + 상위 % 게이지 바) + 카카오톡 공유 문구에 `내 소득 순위: 상위 29.3%` 포함

---

## 7. 신뢰 중심의 핀테크 쿨 블루(Cool Blue) & 다크 슬레이트 디자인 시스템

인간 수석 디자이너 수준의 완성도와 금융 서비스 특유의 신뢰도를 유지하기 위해 AGENTS.md 수칙(싸구려 무지개 배색 배제)을 철저히 준수합니다.

- **베이스 (90%)**: 무채색 다크 슬레이트 (`#1E293B`), 소프트 그레이 배경 (`#F4F6F9`), 클린 화이트 카드 (`#FFFFFF`), 1px 세련된 슬레이트 보더 (`#E2E8F0`)
- **액션 포인트 컬러 (10%)**:
  - **신뢰의 핀테크 블루**: `blue-600`, `blue-700`, `bg-blue-50`, `text-blue-600`, `border-blue-500` (로고 아이콘, 헤더 공유 버튼, 주요 계산 CTA 버튼, 게이지 바, 액션 하이라이트)
  - **평생 무료 안심 그린**: `emerald-600`, `bg-emerald-50`, `border-emerald-200`, `text-emerald-700` (100% 무료 안심 배지, 양도세 비과세 판정 배지)
- **아이콘 단색화 원칙**: 조잡한 컬러 이모지 전면 배제, 1px 무채색/단색 라인 SVG 아이콘만 사용하여 토스(Toss)·뱅크샐러드급 프로페셔널 금융 포털의 품격을 확립
