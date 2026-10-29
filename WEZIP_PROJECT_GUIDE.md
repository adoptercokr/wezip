# 위집 (wezip.co.kr) 전체 작업 및 복원·운영 가이드

> **최종 갱신일:** 2026년 10월 28일  
> **프로젝트 성격:** 대한민국 No.1 공익형 생활금융·세무·지원금 마이크로 계산기 및 지식 포털  
> **도메인:** [https://wezip.co.kr](https://wezip.co.kr) (www.wezip.co.kr)  
> **로컬 저장소 경로:** `C:\nas\mj\비즈니스\유튜브-SNS-캐릭터-애니\ai사이트\AI-mj공작실\01-Nova-Web-Studio\money-calc`  
> **원격 Git 저장소:** `https://github.com/adoptercokr/wezip.git` (브랜치: `main`)

---

## 1. 인프라 및 도메인 / 배포 구조

### 1) 도메인 및 DNS 설정
- **도메인 등록처:** 도메인클럽 (domainclub.kr)
- **네임서버(NS):**
  - 1차: `ns1.ibrain.kr` (221.143.43.39)
  - 2차: `ns2.ibrain.kr` (162.159.24.151)
- **DNS 레코드 설정:**
  - `wezip.co.kr` (루트) -> A 레코드 `216.198.79.1`
  - `www.wezip.co.kr` -> CNAME `cname.vercel-dns.com` 또는 A 레코드 `216.198.79.1`

### 2) 호스팅 및 Vercel 배포 원칙 (필독 절대 규칙)
- **절대 금지:** Windows CMD / PowerShell 터미널에서 `npx vercel deploy` 등 Vercel CLI 명령어를 직접 실행하지 말 것 (빌드 정체 및 UNKNOWN 오류 발생).
- **표준 배포:** 코드를 수정하거나 추가한 후에는 **반드시 원격 GitHub 저장소(`main` 브랜치)로 Push**(`git add .`, `git commit`, `git push origin main`)할 것. GitHub Push 감지 시 Vercel 클라우드가 자동 감지하여 15초 이내에 실시간 무중단 배포(Auto Deploy)를 수행함.

---

## 2. 전체 사이트 페이지 아키텍처 (총 198개 HTML 파일)

위집 포털은 100% 정적 HTML + Tailwind CSS + Vanilla JS로 빌드되어 서버 비용 0원, 최고 속도의 응답성 및 강력한 검색엔진 최적화(SEO)를 달성하고 있습니다.

### 1) 메인 및 핵심 허브 (3개)
- `index.html`: 포털 메인 홈 (핵심 계산기 그리드, FAQPage 구조화 데이터, 실시간 공지)
- `blog.html`: 46개 금융·세무 전문 지식 칼럼 게시판 (동적 검색, 카테고리 필터, 페이지네이션)
- `gov-finder.html`: 맞춤형 정부지원금·복지 혜택 탐색기

### 2) 14대 금융·생활 마이크로 계산기
1. `salary.html`: 연봉 계산기 (2026년 4대보험 요율 및 간이세액표 기반 월 실수령액 산출)
2. `hourly-wage.html`: 알바·최저시급 계산기 (2026년 최저시급 10,030원, 주휴수당 자동 산정)
3. `unemployment.html`: 퇴사자 실업급여 계산기 (1일 상한액 66,000원, 하한액 64,192원)
4. `severance.html`: 퇴직금 계산기 (3개월 평균임금, 연차수당/상여금 반영, IRP 절세율)
5. `annual-leave.html`: 연차 일수 및 미사용 연차수당 계산기 (근로기준법 제60조 기준)
6. `real-transfer-tax.html`: 1세대 1주택 12억 비과세 양도소득세 & 장특공(최대 80%) 계산기
7. `real-loan.html`: 버팀목 전세대출 한도 & HUG 전세보증금 반환보증 심사 조회기
8. `real-estate.html`: 부동산 중개수수료(복비) 및 취득세 감면 계산기
9. `gov-rent.html`: 청년월세 특별지원(월 20만/연 240만) 대상 자격조회기
10. `gov-parent.html`: 2026 출산 부모급여(0세 100만, 1세 50만) & 아동수당 계산기
11. `gov-subsidy.html`: 근로장려금(최대 360만) 및 자녀장려금(100만) 모의계산기
12. `gov-median.html`: 2026 기준 중위소득(4인 가구 609만원) 및 4대 복지급여 기준 조회기
13. `loan-dsr.html`: 대출이자 & 스트레스 DSR 2단계(+1.20%p) 한도 축소 계산기
14. `savings.html`: 예·적금 만기이자 및 15.4% 이자소득세 비과세 비교 계산기
15. `youth-leap.html`: 청년도약계좌 5년 5,000만원 만기금 & 정부 기여금 매칭 조회기
16. `dutch-pay.html`: 더치페이 N빵 정산기 (비음주자 분리, 10원 단위 절사)

### 3) 46대 금융·세무 전문 칼럼 (`blog-*.html`)
모든 칼럼에는 **① 클릭을 부르는 후킹(Hooking) 제목, ② 블로그형 공감 스토리텔링 도입부 카드, ③ 실전 시뮬레이션 표, ④ 실무 꿀팁, ⑤ 핵심 FAQ, ⑥ 좌우 160×600 날개 광고 배너**가 탑재되어 있습니다.

| 번호 | 파일명 | 칼럼 후킹 제목 |
| :---: | :--- | :--- |
| 1 | `blog-annual-leave-allowance.html` | 안 쓰면 그대로 소멸? 2026 연차수당 100% 다 챙겨 받는 통상임금 계산법과 미지급 대처 요령 |
| 2 | `blog-capital-gains-tax-multi-home-owner.html` | 하루 차이로 수천만원 세금 폭탄? 다주택자 양도세 중과 배제 유예와 일시적 1가구 2주택 3년 매도 꿀팁 |
| 3 | `blog-childcare-subsidies.html` | 아이 낳으면 통장에 총 3,000만원? 2026 출산·양육 지원금 놓치면 손해보는 0~7세 신청 총정리 |
| 4 | `blog-compound-interest-rule-of-72.html` | 내 돈이 2배로 불어나는 정확한 시점은? 1초 만에 계산하는 복리의 마법과 72의 법칙 |
| 5 | `blog-comprehensive-income-tax-brackets.html` | 월급 외 1원만 더 벌어도 세금 폭탄? 2026 종합소득세 8단계 세율표와 모르면 털리는 절세 치트키 |
| 6 | `blog-credit-loan-vs-minus-account.html` | 신용대출 vs 마이너스통장, 이자 100만원 아끼는 선택은? 직장인이 무조건 알아야 할 실전 비교 |
| 7 | `blog-credit-score-improvement-tips.html` | 신용카드 이렇게 쓰면 점수 뚝뚝 떨어진다? 900점 이상 1등급 만드는 신용점수 급상승 비법 |
| 8 | `blog-deposit-interest-tax.html` | 이자 15.4% 세금 떼이면 남는 게 없다? 예·적금 만기 이자 1원도 안 떼이는 비과세 3대 비법 |
| 9 | `blog-diaper-formula-milk-voucher.html` | 매달 기저귀·분윳값 최대 20만원 국가지원! 영아 부모라면 무조건 신청해야 할 바우처 총정리 |
| 10 | `blog-dutch-pay-culture-split-bill.html` | 모임 회식 후 돈 때문에 정떨어지지 않는 법: 술 안 마신 사람 빼고 1초 만에 끝내는 스마트 N빵 공식 |
| 11 | `blog-earned-income-tax-credit.html` | 최대 360만원 현금 환급 잭팟! 2026 근로장려금 맞벌이·단독가구 신청 자격 1분 체크 |
| 12 | `blog-energy-voucher-application.html` | 난방비·전기세 고지서 보고 기겁했다면? 연 최대 수십만원 공짜 차감되는 에너지바우처 신청법 |
| 13 | `blog-first-home-buyer-tax.html` | 생애 첫 내 집 마련 취득세 200만원 전액 면제받는 법! 신생아 특례 디딤돌 초저금리 합체 전략 |
| 14 | `blog-freelancer-3-3-tax-return.html` | 3.3% 떼인 내 돈 수십만원 돌려받는 법: 삼쩜삼 수수료 아끼는 홈택스 셀프 환급 완벽 가이드 |
| 15 | `blog-gift-tax-deduction-limits.html` | 부모 자식 간 계좌이체 국세청에 다 걸린다? 증여세 0원으로 합법 이체하는 차용증·비과세 특효약 |
| 16 | `blog-health-insurance-skin-dependent.html` | 건강보험 피부양자 박탈되면 월 20만원 폭탄! 과표 5.4억·연소득 2,000만원 방어 전략 |
| 17 | `blog-holding-tax-comprehensive-real-estate.html` | 단 하루 차이로 1년 치 보유세 독박 쓴다? 6월 1일 과세기준일 잔금일 밀당 실전 전략 |
| 18 | `blog-hourly-wage-2026.html` | 최저시급 1만원 시대! 주휴수당 안 주면 불법? 2026 알바생·사장님 필수 월급 계산 팩트체크 |
| 19 | `blog-housing-subscription-points.html` | 청약통장 월 10만원 넣으면 영원히 당첨 불가? 25만원 상향 개편과 신혼·신생아 특공 당첨 치트키 |
| 20 | `blog-infertility-treatment-support.html` | 소득 상관없이 누구나 최대 110만원 지원! 2026 난임시술비 무제한 국가지원 혜택 200% 받는 법 |
| 21 | `blog-interest-rate-cut-demand-right.html` | 은행에 전화 한 통으로 대출이자 월 10만원 깎는 법: 금리인하요구권 승인 꿀팁과 거절 시 반격법 |
| 22 | `blog-irp-pension-savings-tax-deduction.html` | 연말정산 148.5만원 꽁돈 환급받는 연금저축 vs IRP 황금 비율! 중도인출 함정 피하는 법 |
| 23 | `blog-jeonse-lease-protection-act.html` | 집주인이 내가 들어와 살 테니 나가라 할 때 대처법! 계약갱신청구권 5% 상한과 손해배상 청구 비법 |
| 24 | `blog-jeonse-scam-prevention-checklist.html` | 피 같은 전세보증금 통째로 날리지 않으려면? 등기부등본 을구 근저당과 HUG 반환보증 5대 체크리스트 |
| 25 | `blog-jeonse-to-monthly-rent-conversion.html` | 집주인이 월세 올린다면 무조건 따져봐야 할 공식! 전월세 전환율 법정 상한과 손익 계산법 |
| 26 | `blog-job-change-salary-negotiation.html` | 이직할 때 연봉 20% 더 땡기는 실전 협상법: 원천징수 영끌 계산부터 처우협의 계약서 꿀팁 |
| 27 | `blog-k-pass-transportation-card-guide.html` | 매달 교통비 5만원씩 꼬박꼬박 돌려받는 K-패스 환급법! 출퇴근 직장인·청년 필수 신청 가이드 |
| 28 | `blog-median-income-welfare.html` | 내가 정부지원금 받을 수 있을까? 2026 기준 중위소득 표와 1인·4인가구 맞춤 복지급여 커트라인 |
| 29 | `blog-national-pension-reform.html` | 내 국민연금 나중에 진짜 받을 수 있을까? 2026 보험료율 인상 개혁안과 예상 수령액 팩트체크 |
| 30 | `blog-officetel-vs-apartment-tax.html` | 오피스텔 샀다가 아파트 청약·양도세 다 날린다? 주거용 오피스텔 세금 함정과 취득세 4.6% 실전 분석 |
| 31 | `blog-overseas-stock-capital-gains-tax.html` | 서학개미 수익 났다고 좋아하다 22% 세금 폭탄? 250만원 공제와 마이너스 종목 손익통산 절세 비법 |
| 32 | `blog-overtime-pay-calculation.html` | 야근하고 주말 출근했는데 수당 제대로 받았을까? 1.5배~2배 야근·휴일근로수당 통상임금 계산법 |
| 33 | `blog-real-estate-brokerage-fee-standard.html` | 부동산 계약할 때 복비 그대로 다 주면 호구? 법정 중개수수료 상한 요율표와 협상 꿀팁 |
| 34 | `blog-real-estate-transfer-tax.html` | 내 집 팔 때 세금 0원 만드는 법: 1세대 1주택 비과세 12억 기준과 수천만원 아끼는 장특공 80% 공식 |
| 35 | `blog-salary-guide-2026.html` | 연봉 5,000만원 실수령액이 고작 이 정도? 2026 4대보험·소득세 공제 후 통장 입금액 완벽 해부 |
| 36 | `blog-severance-intermediate-settlement.html` | 급전 필요할 때 내 퇴직금 미리 땡겨 받을 수 있을까? 법적으로 인정되는 중간정산 6대 사유와 서류 |
| 37 | `blog-severance-pay-guide.html` | 퇴사할 때 퇴직금 10원도 안 떼이고 다 받는 법! 평균임금 계산 공식과 IRP 절세 30% 감면 꿀팁 |
| 38 | `blog-single-parent-welfare-benefits.html` | 혼자 아이 키우는 부모라면 매달 21만원 지원! 2026 한부모가정 복지급여 자격 조건과 신청 총정리 |
| 39 | `blog-stress-dsr-guide.html` | 스트레스 DSR 2단계로 내 대출 5,000만원 깎였다? 수도권 주담대 한도 축소 방어하는 3대 전략 |
| 40 | `blog-tax-reform-2026-guide.html` | 2026 세법개정안 핵심 총정리: 종부세 14억·월세공제 1,200만·근로장려금 360만 실생활 절세 총력전 |
| 41 | `blog-telecom-fee-discount-welfare.html` | 부모님 핸드폰 요금 매달 33,500원 공짜 할인! 114 전화 한 통으로 끝내는 취약계층 통신비 감면 |
| 42 | `blog-unemployment-benefit.html` | 자진퇴사해도 실업급여 받을 수 있다? 2026 실업급여 1일 66,000원 수급 자격과 4대 예외 조건 |
| 43 | `blog-weekly-holiday-allowance-part-time.html` | 주 15시간 알바생 주휴수당 못 받으면 100% 임금체불? 쪼개기 알바 분쟁과 법적 계산법 완벽 해설 |
| 44 | `blog-year-end-tax-settlement-guide.html` | 13월의 월급 120만원 더 돌려받는 1급 비밀! 연말정산 카드·의료비·연금 소득공제 황금 비율 |
| 45 | `blog-youth-tomorrow-savings-account.html` | 월 10만원 넣고 3년 뒤 1,440만원 타는 법! 정부가 원금 3배 얹어주는 청년내일저축계좌 총정리 |
| 46 | `blog-youth-welfare-2026.html` | 청년이라면 정부가 주는 수백만원 놓치지 마세요! 2026 청년 3대 국가지원금(도약·월세·버팀목) 총정리 |

### 4) 프로그래머틱 SEO 전용 랜딩페이지 (129개)
- **연봉 구간별 69개 페이지 (`salary-*.html`):** `salary-2400.html` (연봉 2,400만원)부터 `salary-20000.html` (연봉 2억원)까지 100만원~1,000만원 단위 완벽 세분화.
- **부동산 세금 및 정부복지 60개 페이지 (`tax-*.html`, `subsidy-*.html`):** 생애최초 주택가액별 취득세, 다주택 중과세, 전세사기 예방 등 롱테일 키워드 100% 점유.

### 5) 공통 정책 및 고객지원 (4개)
- `about.html`: 서비스 소개 및 편집 원칙
- `terms.html`: 이용약관 및 법적 면책
- `privacy.html`: 개인정보처리방침
- `contact.html`: 고객센터 & 광고 문의 접수처 (2-Tab 분리형 초간편 폼)

---

## 3. 핵심 시스템 세부 규격

### 1) 고객센터 및 광고 문의 시스템 (`contact.html`)
- **2단 탭 구조:** `일반 문의` 탭과 `광고 문의` 탭으로 분리하여 원클릭 즉시 전환 (`switchInquiryTab`)
- **URL 파라미터 연동:**
  - `contact.html`: 기본 일반 문의 탭 활성화 (상단 네비게이션 '문의하기' 단일 링크)
  - `contact.html?type=ad`: 광고 문의 탭 즉시 자동 활성화 (푸터 및 우측 스폰서 배너 연동)
- **초간단 폼 필드:**
  - **일반 문의:** 제목(`genTitle`, 내용 바로 위), 회신 연락처/이메일(`genContact`), 문의 내용(`genMessage`)
  - **광고 문의:** 제목(`adTitle`, 내용 바로 위), 업체명/성함(`adCompany`), 회신 연락처/이메일(`adContact`), 문의 내용(`adMessage`)
- **이메일 보안 및 메일 출처 3중 각인 식별:**
  - 관리자 수신 이메일(`joykorea7@gmail.com`)이 화면에 절대 노출되지 않음 (Base64 암호화 전송)
  - **애니맵 등 타 사이트와 명확한 구분:** 메일함 발신자명(`name: [위집 wezip.co.kr]`), 메일 제목(`_subject: [위집 wezip.co.kr] ...`), 본문 1행(`사이트출처: 위집 (wezip.co.kr)`)에 출처가 3중으로 굵게 각인되어 수신 메일함에서 즉시 판별 가능
  - 상대방이 이메일 입력 시 `_replyto`가 자동 지정되어 메일함에서 클릭 한 번으로 바로 답장 가능
  - **외부 서버 일시 장애 시 세이프가드:** FormSubmit 521 등 서버 오류 감지 시 작성 내용이 보존된 채 원클릭 이메일 앱 발송(`mailto:joykorea7@gmail.com`) 및 클립보드 복사 카드 자동 노출
  - 페이지 리로드 없이 1초 만에 비동기 전송 후 접수 완료 토스트 및 확인 카드 표출

### 2) 실시간 방문자 카운터 시스템 (`api/counter.js` & `common.js`)
- **원리 및 크로스 브라우징 완전 동기화:**
  - Vercel 서버리스 함수(`api/counter.js`)를 구축하여 서버단에서 `hits.sh` 중앙 카운터를 직접 조회
  - 브라우저 CORS 차단 문제 및 개별 브라우저별 `localStorage` 격리 현상을 원천 해결
  - 크롬, 엣지, 사파리, 네이버 웨일, 모바일 브라우저 등 **어떤 기기나 브라우저에서 접속하더라도 동일한 중앙 카운트가 100% 실시간 동기화**
  - 당일 방문 캐시(`wezip_counter_today`, `wezip_counter_total`)를 적용하여 페이지 이동 시 깜빡임(flickering) 방지
- **표기 형식:**
  - `오늘 방문 18 | 전체 방문 148 · 26년 10월 27일부터`
  - 불필요한 기술 용어 `(PV)` 완전 제거
  - 서비스 시작 기준일(`26년 10월 27일부터`) 명시

### 3) 수익화 및 광고 영역 규격
- **구글 애드센스:**
  - 게시자 ID: `ca-pub-5717882145510454` (전체 HTML `<head>`에 메타태그 및 비동기 스크립트 삽입 완료)
  - `ads.txt` 루트 파일: `google.com, pub-5717882145510454, DIRECT, f08c47fec0942fa0`
- **데스크톱 와이드 3단 레이아웃:**
  - 최대 너비 1560px (`max-w-[1560px]`)
  - 좌측 & 우측 160×600 스카이스크래퍼 배너 (`sticky top-20`)
  - 배너 하단에 `배너 광고 문의 →` 링크(`contact.html?type=ad`) 배치

### 4) 검색엔진 등록 및 색인 규격
- **네이버 서치어드바이저:**
  - 소유권 확인 메타: `<meta name="naver-site-verification" content="4b1f13ae8ec3adff4aa7557dcd9772168cb34ab9" />`
  - 사이트맵: `https://wezip.co.kr/sitemap.xml` (총 198개 URL 수집 완료)
  - RSS: `https://wezip.co.kr/rss.xml` (초경량 15개 최신 칼럼 유지, 500 오류 방지)
- **구글 서치콘솔:**
  - 소유권 확인 메타: `<meta name="google-site-verification" content="rG_dAHCcKAuP0DmIaLVp9EMR-RvnwceWg_-WmMwQCR4" />`
  - URL 접두어 속성 `https://wezip.co.kr/` 등록 및 사이트맵 제출 성공
- **다음(Daum / 카카오) 웹마스터도구:**
  - 인증 방식: robots.txt 하단 인증키 기입
  - 인증 코드: `#DaumWebMasterTool:742ccc120c16a4ff031a8e1d8971d975e5fe0e655e361ff24f28b17b870faabc:7v7Co2KibzUex4fH7zWmNA==`
  - robots.txt 배포 완료

---

## 4. 주간 무인 자동화 시스템 (Sidecar Automation)

- **설정 파일 위치:** `C:\Users\mj\.gemini\config\sidecars\wezip-weekly-seo-updater\sidecar.json`
- **실행 주기:** **매주 일요일 밤 10:00 (Asia/Seoul)** (`CRON_TZ=Asia/Seoul 0 22 * * 0`)
- **수행 파이프라인:**
  1. 최신 세법 개정안, 복지 지원금 인상, 부동산 대출 규제(DSR) 웹 검색
  2. 기존 14대 계산기 요율표(4대보험, 간이세액표, 중위소득 등) 변경사항 검토
  3. 실시간 고수익 검색어 기반 금융 칼럼 2~3편 자동 집필 (디자인 수칙 준수)
  4. `sitemap.xml`, `rss.xml`, `blog.html` 자동 갱신
  5. 사이트 전수 검증(`verify_all_pages.py`) 실행
  6. Git Commit 및 `origin main` Push 자동 수행 &rarr; Vercel 실시간 배포

---

## 5. 검증 및 배포 체크리스트 (작업 시 필수 실행)

코드를 수정하거나 신규 페이지를 추가한 경우, 반드시 아래 순서를 엄수해야 합니다.

```bash
# 1. 작업 디렉토리 이동
cd "c:\nas\mj\비즈니스\유튜브-SNS-캐릭터-애니\ai사이트\AI-mj공작실\01-Nova-Web-Studio\money-calc"

# 2. 198개 전 페이지 HTML 무결성 검사 (오류 0건 필수)
python verify_all_pages.py

# 3. 변경 사항 확인
git status

# 4. GitHub main 브랜치 커밋 및 푸시 (Vercel 자동 배포 트리거)
git add .
git commit -m "작업 내용 요약"
git push origin main

# 5. 실시간 배포 확인 (5~10초 후 HTTP 200 확인)
curl.exe -sIL https://wezip.co.kr
```

---

## 6. Anti-AI Cliché 디자인 절대 수칙 (MJ 대표님 지침)
- **아이콘 단색화 & 절제:** 조잡한 컬러 이모지(🎨, 💰, 📈, 🚀 등) 사용 절대 금지. 오직 1px 얇은 단색 라인형 SVG 아이콘만 필수 위치에 한해 사용할 것.
- **모노크롬 + 쿨블루 포인트:** 화이트(#FFFFFF), 고급스러운 그레이(#F8FAFC, #E2E8F0, #1E293B)를 90% 이상 베이스로 삼고, 포인트 컬러는 오직 쿨블루(#2563EB) 1개만 절제하여 사용할 것.
- **데이터 보존 절대 원칙:** 기존 데이터나 칼럼, 계산기 코드를 임의로 삭제하거나 축약하지 말 것. 항상 추가/보강 방식으로 전개할 것.
