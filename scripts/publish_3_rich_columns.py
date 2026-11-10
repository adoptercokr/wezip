# -*- coding: utf-8 -*-
"""
publish_3_rich_columns.py
1. Overwrites blog-parental-leave-pay-250.html & blog-national-pension-early-receipt.html with deep, human-style long-form articles.
2. Generates new rich article blog-didimdol-loan-room-deduction.html.
3. Updates blog.html (updates #48 & #49, adds #50), sitemap.xml, and rss.xml.
"""

import os
import re
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TODAY = datetime.date.today().isoformat()
TODAY_DOT = TODAY.replace("-", ".")
NOW_RFC822 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%a, %d %b %Y %H:%M:%S +0900")

ARTICLES_DATA = [
    {
        "slug": "blog-parental-leave-pay-250",
        "no": 48,
        "title": "2026 육아휴직 급여 최대 250만원 인상 개편안 총정리: 사후지급금 폐지부터 6+6 부모육아휴직제 교차 수령 실전 꿀팁",
        "desc": "2026년 대폭 개편된 육아휴직 급여 총정리! 첫 3개월 월 최대 250만원, 4~6개월 200만원, 7개월 이후 160만원으로 대폭 인상되고 직장 복귀 후 받던 25% 사후지급금이 즉시 지급으로 전환된 최신 지침과 6+6 부모육아휴직제 부부 교차 수령 실전 가이드.",
        "cat": "welfare",
        "catName": "복지·지원금",
        "badge": "NEW",
        "readTime": "약 8분",
        "calcLink": "gov-parent.html",
        "calcName": "부모급여 & 아동수당 모의계산기",
        "hook_title": "월 112만원 쥐어짜던 시절은 끝, 휴직 첫 달부터 통장에 250만원이 온전히 꽂힙니다",
        "hook_p1": "임신과 출산을 앞둔 직장인 예비 부모님들이라면 요즘 한 번쯤 들어보셨을 겁니다. '육아휴직 급여가 월 250만 원까지 올랐다는데, 나도 받을 수 있을까?', '복직하고 나서야 찔끔 주던 25% 사후지급금은 정말 없어진 걸까?' 결론부터 말씀드리면, 2026년 육아휴직 제도는 역대 가장 파격적인 수준으로 전면 개편되었습니다.",
        "hook_p2": "기존에는 월 최대 150만 원 상한에 묶여 있었고, 그마저도 25%를 강제로 떼어두었다가 복직 후 6개월을 더 다녀야 돌려받았기 때문에 휴직 중 실제 통장에 꽂히는 돈은 월 112만 5천 원에 불과했습니다. 기저귀값과 분유값, 대출 이자를 감당하기엔 턱없이 부족했죠. 하지만 2026년부터는 첫 3개월 동안 통상임금의 100%(월 최대 250만 원)가 사후지급금 차감 없이 매달 100% 온전히 입금됩니다. 여기에 부부가 함께 쓰면 혜택이 곱절로 커지는 '6+6 부모육아휴직제'까지 결합하면 1년간 부부 합산 최대 3,900만 원 이상의 소득 안전망을 확보할 수 있습니다.",
        "editor_tip": "육아휴직 급여는 소득세법상 '전액 비과세'이며 건강보험료도 휴직 기간 동안 납부 유예 및 복직 시 최대 60% 감면 혜택이 주어집니다. 4대보험 공제 없는 순수 현금 통장 입금액 구조를 반드시 미리 파악하세요.",
        "content_html": """
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">1. 2026년 육아휴직 급여 개편 핵심 요약: 기간별 상한액과 지급 방식</h2>
            <p>
                고용보험법 시행령 개정으로 2026년부터 육아휴직 급여는 통상임금 반영률과 월 상한액이 기간별로 차등 지급되는 3단계 계단식 구조로 전환되었습니다. 특히 초기 3개월 동안 영아 집중 돌봄을 지원하기 위해 상한액을 기존 150만 원에서 250만 원으로 무려 100만 원(66.7%) 대폭 상향했습니다.
            </p>
            <div class="overflow-x-auto my-4">
                <table class="w-full text-xs sm:text-sm text-left border border-slate-200 rounded-xl overflow-hidden">
                    <thead class="bg-slate-100 text-slate-800 font-bold border-b border-slate-200">
                        <tr>
                            <th class="p-3">휴직 기간</th>
                            <th class="p-3">통상임금 반영률</th>
                            <th class="p-3 font-bold text-blue-600">월 지급 상한액</th>
                            <th class="p-3">실제 월 통장 입금 방식</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 font-medium">
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">1개월 ~ 3개월 (초기)</td>
                            <td class="p-3">통상임금의 100%</td>
                            <td class="p-3 font-bold text-blue-600">월 최대 250만 원</td>
                            <td class="p-3">사후지급금 공제 없이 매월 100% 전액 즉시 통장 입금</td>
                        </tr>
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">4개월 ~ 6개월 (중기)</td>
                            <td class="p-3">통상임금의 100%</td>
                            <td class="p-3 font-bold text-blue-600">월 최대 200만 원</td>
                            <td class="p-3">매월 전액 즉시 통장 입금</td>
                        </tr>
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">7개월 ~ 12개월 (후기)</td>
                            <td class="p-3">통상임금의 80%</td>
                            <td class="p-3 font-bold text-blue-600">월 최대 160만 원</td>
                            <td class="p-3">매월 전액 즉시 통장 입금 (최대 1년 수급)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <p class="text-xs text-slate-500">
                * 하한액: 최저 월 70만 원 보장 (통상임금이 낮은 근로자도 최소 월 70만 원 지급).<br>
                * 통상임금 기준: 기본급 + 고정 직책수당 등 정기적·일률적으로 지급되는 금액 (상여금, 야근수당 등 변동 수당 제외).
            </p>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">2. '사후지급금 25% 폐지'가 가계에 가져온 결정적 차이</h2>
            <p>
                그동안 육아휴직을 망설이게 만들었던 주범은 바로 '사후지급금(25%)' 제도였습니다. 복직 후 6개월 이상 계속 근무해야만 떼어둔 25%를 돌려주다 보니, 휴직 중에는 정작 가장 돈이 필요한 시기에 생활고를 겪거나 비자발적 퇴사 시 급여를 떼이는 문제가 심각했습니다.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-4">
                <div class="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2">
                    <div class="font-bold text-slate-700 text-sm">과거 지급 방식 (개편 전)</div>
                    <div class="text-slate-500 text-xs leading-relaxed">
                        • 상한액 월 150만원 기준, 휴직 중 75%(월 112.5만원)만 매달 수령.<br>
                        • 나머지 25%(월 37.5만원)는 복직 후 6개월 뒤 450만원 뭉텅이 수령.<br>
                        • <strong>문제점</strong>: 휴직 기간 동안 당장 고정 생활비와 아기 용품 지출 부족으로 적자 발생.
                    </div>
                </div>
                <div class="p-5 bg-blue-50/60 border border-blue-200 rounded-2xl space-y-2">
                    <div class="font-bold text-blue-900 text-sm">2026년 최신 방식 (현재)</div>
                    <div class="text-slate-700 text-xs leading-relaxed font-medium">
                        • 사후지급금 제도 전격 폐지! 매월 급여 100%를 해당 월에 즉시 입금.<br>
                        • 통상임금 300만원 근로자 기준: 첫 3달 250만×3 = 750만, 4~6달 200만×3 = 600만, 7~12달 160만×6 = 960만.<br>
                        • <strong>결과</strong>: 1년간 총 2,310만 원을 매달 안정적으로 수령 (기존 대비 약 510만 원 실질 소득 증가).
                    </div>
                </div>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">3. 부부 합산 최대 3,900만원! '6+6 부모육아휴직제' 실전 배분 전략</h2>
            <p>
                생후 18개월 이내의 자녀를 둔 부모가 동시에 또는 순차적으로 육아휴직을 사용하는 경우 일반 육아휴직 급여 대신 '6+6 부모육아휴직제'가 우선 적용됩니다. 이 제도는 부모 각각의 월 상한액을 첫 달 200만 원에서 시작해 매달 50만 원씩 높여 6개월 차에는 부모 1인당 최대 450만 원까지 지급합니다.
            </p>
            <div class="overflow-x-auto my-4">
                <table class="w-full text-xs sm:text-sm text-left border border-slate-200 rounded-xl overflow-hidden">
                    <thead class="bg-slate-100 text-slate-800 font-bold border-b border-slate-200">
                        <tr>
                            <th class="p-3">휴직 월차</th>
                            <th class="p-3">1인당 월 상한액</th>
                            <th class="p-3 font-bold text-blue-600">부부 합산 월 최대 수령액</th>
                            <th class="p-3">누적 수령액 (부부 합산)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 font-medium">
                        <tr><td class="p-2.5">1개월 차</td><td class="p-2.5">200만 원</td><td class="p-2.5 font-bold text-blue-600">400만 원</td><td class="p-2.5">400만 원</td></tr>
                        <tr><td class="p-2.5">2개월 차</td><td class="p-2.5">250만 원</td><td class="p-2.5 font-bold text-blue-600">500만 원</td><td class="p-2.5">900만 원</td></tr>
                        <tr><td class="p-2.5">3개월 차</td><td class="p-2.5">300만 원</td><td class="p-2.5 font-bold text-blue-600">600만 원</td><td class="p-2.5">1,500만 원</td></tr>
                        <tr><td class="p-2.5">4개월 차</td><td class="p-2.5">350만 원</td><td class="p-2.5 font-bold text-blue-600">700만 원</td><td class="p-2.5">2,200만 원</td></tr>
                        <tr><td class="p-2.5">5개월 차</td><td class="p-2.5">400만 원</td><td class="p-2.5 font-bold text-blue-600">800만 원</td><td class="p-2.5">3,000만 원</td></tr>
                        <tr><td class="p-2.5">6개월 차</td><td class="p-2.5">450만 원</td><td class="p-2.5 font-bold text-blue-600">900만 원</td><td class="p-2.5 font-extrabold text-blue-700">3,900만 원</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                <strong>실전 팁</strong>: 아빠와 엄마가 같은 달에 동시에 휴직하지 않고, 엄마가 출산휴가 후 6개월 먼저 휴직하고 아빠가 이어서 6개월을 사용하더라도 두 번째 사용자의 휴직 기간 중 두 사람 모두에게 6+6 소급 인상분이 지급됩니다. 통상임금이 높은 쪽이 나중에 사용하더라도 첫 번째 사용자의 급여가 사후 정산되어 지급되므로 걱정하지 않으셔도 됩니다.
            </p>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">4. 신청 전 90%가 놓치는 치명적인 함정 4가지</h2>
            <div class="space-y-3 my-4">
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">1. 고용보험 피보험 단위기간 180일 요건</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        휴직 개시일 이전에 피보험 단위기간(실제 보수를 지급받은 유급일수)이 합산 180일 이상이어야 합니다. 단순 재직 6개월이 아니라 주휴일 포함 유급일 기준이므로 주 5일 근로자는 약 7~8개월의 근무 이력이 필요합니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">2. 회사에 휴직 개시 30일 전 신청서 제출 의무</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        남녀고용평등법상 근로자는 휴직 개시 예정일 30일 전까지 회사에 신청서를 제출해야 합니다. 사업주는 정당한 사유 없이 육아휴직을 거부할 수 없으며 위반 시 500만 원 이하의 벌금이 부과됩니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">3. 부모급여(월 100만/50만원)와의 중복 수령 100% 가능</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        부모급여는 보건복지부의 아동 보육 수당이고, 육아휴직 급여는 고용보험의 실직/휴직 대체 급여이므로 두 제도는 전액 중복 수급이 가능합니다. 0세 아동 기준 월 최대 250만원(육아휴직) + 100만원(부모급여) = 월 350만원까지 수령할 수 있습니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">4. 휴직 기간 중 부업 및 알바 소득 발생 시 주의점</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        육아휴직 중 주 15시간 이상 일하거나 월 150만 원 이상의 근로·사업 소득이 발생하면 고용센터에 반드시 신고해야 합니다. 미신고 시 부정수급으로 판정되어 지원금 전액 환수 및 배액 징수를 당할 수 있습니다.
                    </p>
                </div>
            </div>
        """,
        "faqs": [
            ("Q. 육아휴직 급여에도 4대보험이나 근로소득세가 부과되나요?",
             "아닙니다. 고용보험법상 육아휴직 급여는 전액 비과세 소득이므로 소득세 및 지방소득세가 원천징수되지 않습니다. 또한 건강보험료는 납부유예를 신청할 수 있으며, 복직 시 직장가입자 최저보험료 수준으로 최대 60% 감면 적용을 받습니다."),
            ("Q. 육아휴직 중 자진퇴사하면 사후지급금을 못 받나요?",
             "2026년부터 사후지급금 제도 자체가 완전히 폐지되었기 때문에, 휴직 기간 동안 매월 지급받은 100% 급여는 복직 여부나 퇴사 여부와 관계없이 일체 반환하지 않아도 됩니다."),
            ("Q. 아빠도 육아휴직 1년을 온전히 다 쓸 수 있나요?",
             "네, 부모 각각 자녀 1명당 최대 1년(부부 합산 총 2년)의 육아휴직을 사용할 수 있으며, 두 사람 모두 독립적으로 육아휴직 급여 수급 자격을 인정받습니다.")
        ]
    },
    {
        "slug": "blog-national-pension-early-receipt",
        "no": 49,
        "title": "국민연금 조기수령 감액(최대 30%) 손익분기점 계산: 몇 살에 받는 것이 이득일까? 건보료 피부양자 방어 실전 전략",
        "desc": "국민연금 정규 수령 나이보다 최대 5년 일찍 받는 조기노령연금의 장단점과 평생 깎이는 감액률(연 6%, 최대 30%) 분석! 건강보험 피부양자 자격 유지(연 2,000만원 룰)와 평균 수명 기준 손익분기점 나이(76.6세) 실전 계산.",
        "cat": "salary",
        "catName": "급여·세무",
        "badge": "필독",
        "readTime": "약 8분",
        "calcLink": "salary.html",
        "calcName": "2026 연봉 실수령액 & 국민연금 계산기",
        "hook_title": "평생 30% 감액의 덫인가, 아니면 5년 먼저 받는 현명한 목돈 확보인가?",
        "hook_p1": "50대 후반에서 60대 초반에 접어든 직장인이나 은퇴 예정자분들이 요즘 모임이나 상담에서 가장 열띠게 토론하는 주제가 있습니다. '국민연금을 당겨 받을까, 아니면 제 나이 될 때까지 기다릴까?' 정규 수령 나이(만 63~65세)보다 최대 5년 일찍 받을 수 있는 '조기노령연금' 제도가 있지만, 1년 일찍 받을 때마다 매년 6%씩, 5년을 일찍 받으면 평생 원래 연금액의 30%가 깎인 70%만 지급됩니다.",
        "hook_p2": "'평생 30%가 깎인다는데 굳이 당겨 받아야 할까?' 싶다가도, '당장 은퇴해서 소득도 없는데 5년 동안 손가락만 빨고 있을 수는 없지 않나', '요즘 건강보험 피부양자 기준이 빡빡해져서 연금을 많이 받으면 건강보험료 폭탄을 맞는다던데' 하는 현실적인 걱정이 밀려옵니다. 과연 몇 살까지 살아야 제 나이에 받는 것이 이득일까요? 그리고 은퇴 후 월 수십만 원의 지역 건강보험료를 아끼기 위해 조기수령을 활용하는 절세 고수들의 전략은 무엇일까요? 오늘은 감정적인 판단이 아닌, 1원 단위까지 시뮬레이션한 손익분기점과 피부양자 방어 공식을 가감 없이 공개합니다.",
        "editor_tip": "국민연금 조기수령은 한 번 신청하면 나중에 취소하거나 정규 수령액으로 되돌릴 수 없는 '불가역적 선택'입니다. 본인의 기대수명뿐만 아니라 건강보험 피부양자 자격(연소득 2,000만 원 초과 여부)과 합산하여 입체적으로 판단해야 합니다.",
        "content_html": """
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">1. 조기노령연금 신청 자격 및 출생연도별 정규 수령 연령</h2>
            <p>
                국민연금(노령연금)은 본인의 가입 기간이 10년(120개월) 이상이어야 하며, 법정 출생연도에 따라 정규 수급 개시 연령이 단계적으로 늦춰져 있습니다. 조기노령연금은 이 정규 수급 개시 나이보다 정확히 최대 5년 전부터 본인이 신청하여 수령할 수 있습니다.
            </p>
            <div class="overflow-x-auto my-4">
                <table class="w-full text-xs sm:text-sm text-left border border-slate-200 rounded-xl overflow-hidden">
                    <thead class="bg-slate-100 text-slate-800 font-bold border-b border-slate-200">
                        <tr>
                            <th class="p-3">출생 연도</th>
                            <th class="p-3">정규 수급 개시 나이</th>
                            <th class="p-3 font-bold text-blue-600">조기 수령 가능 나이 (최대 5년 전)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 font-medium">
                        <tr><td class="p-2.5">1953년 ~ 1956년생</td><td class="p-2.5">만 61세</td><td class="p-2.5 font-bold text-blue-600">만 56세</td></tr>
                        <tr><td class="p-2.5">1957년 ~ 1960년생</td><td class="p-2.5">만 62세</td><td class="p-2.5 font-bold text-blue-600">만 57세</td></tr>
                        <tr><td class="p-2.5">1961년 ~ 1964년생</td><td class="p-2.5">만 63세</td><td class="p-2.5 font-bold text-blue-600">만 58세</td></tr>
                        <tr><td class="p-2.5">1965년 ~ 1968년생</td><td class="p-2.5">만 64세</td><td class="p-2.5 font-bold text-blue-600">만 59세</td></tr>
                        <tr><td class="p-2.5">1969년생 이후 출생자</td><td class="p-2.5 font-extrabold text-slate-900">만 65세</td><td class="p-2.5 font-extrabold text-blue-600">만 60세</td></tr>
                    </tbody>
                </table>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">2. 조기수령 기간별 평생 감액률과 수령액 비율 매트릭스</h2>
            <p>
                조기노령연금을 신청하면 1개월당 0.5%씩, 1년당 6%씩 연금액이 평생 감액됩니다. 중요한 것은 <strong>정규 수령 나이가 도달해도 원래 금액으로 회복되지 않고 깎인 비율이 평생 유지</strong>된다는 점입니다.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5 my-4">
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-700 text-sm">5년 조기 (만 60세)</div>
                    <div class="text-lg font-black text-rose-600">30% 평생 감액</div>
                    <div class="text-xs text-slate-500">원래 연금의 70%만 평생 지급</div>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-700 text-sm">3년 조기 (만 62세)</div>
                    <div class="text-lg font-black text-slate-800">18% 평생 감액</div>
                    <div class="text-xs text-slate-500">원래 연금의 82%만 평생 지급</div>
                </div>
                <div class="p-4 bg-blue-50/70 border border-blue-200 rounded-xl space-y-1">
                    <div class="font-bold text-blue-900 text-sm">정규 수급 (만 65세)</div>
                    <div class="text-lg font-black text-blue-600">0% 감액 (100% 전액)</div>
                    <div class="text-xs text-slate-500">원래 산정된 연금액 100% 온전 지급</div>
                </div>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">3. 실전 손익분기점 계산: 도대체 몇 살까지 살아야 이득일까?</h2>
            <p>
                정규 연금액이 월 100만 원(연 1,200만 원)인 가입자를 기준으로 5년 일찍 받는 조기수령(월 70만 원)과 정규 수령(월 100만 원)의 누적 수령액을 비교해 보겠습니다.
            </p>
            <div class="p-5 bg-slate-50 border border-slate-200 rounded-2xl text-xs sm:text-sm text-slate-700 leading-relaxed space-y-3 font-medium my-4">
                <p>• <strong>조기수령자(만 60세 개시)</strong>: 만 60세부터 65세까지 5년(60개월) 동안 월 70만 원씩 총 4,200만 원을 먼저 손에 쥡니다.</p>
                <p>• <strong>정규 수급자(만 65세 개시)</strong>: 만 65세부터 매월 100만 원을 받으므로, 조기수령자보다 매달 30만 원을 더 받게 됩니다.</p>
                <p>• <strong>누적 역전 계산</strong>: 정규 수급자가 앞선 4,200만 원의 격차를 따라잡으려면 4,200만 원 ÷ 월 30만 원 = 140개월(11년 8개월)이 걸립니다.</p>
                <p class="pt-2 border-t border-slate-200 text-blue-900 font-extrabold text-sm sm:text-base">
                    손익분기점 = 만 65세 + 11년 8개월 = 만 76세 8개월 (약 76.6세)!
                </p>
            </div>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                <strong>명확한 결론</strong>:<br>
                1) 만 76세 이전에 사망할 경우: 조기수령이 총 수령액 면에서 무조건 유리합니다.<br>
                2) 만 77세 이상 건강하게 장수할 경우: 정규 수령이 훨씬 유리하며, 85세 시점에는 정규 수령자가 약 3,000만 원 이상 더 많이 받게 됩니다.
            </p>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">4. 건강보험 피부양자 탈락(연 2,000만원 룰) 방어 전략</h2>
            <p>
                최근 은퇴자들 사이에서 조기수령 신청이 급증한 진짜 이유는 '건강보험료' 때문입니다. 현행 건강보험법상 국민연금 등 공적연금 소득이 연간 2,000만 원(월 166.7만 원)을 단 1원이라도 초과하면 직장인 자녀의 피부양자에서 전격 박탈되어 지역가입자로 강제 전환됩니다.
            </p>
            <div class="p-5 bg-rose-50/60 border border-rose-200 rounded-2xl text-xs sm:text-sm text-slate-700 leading-relaxed space-y-2 my-4">
                <div class="font-bold text-rose-900 text-sm">실전 사례: 원래 연금액이 월 175만 원인 은퇴자 A씨</div>
                <p>• <strong>정규 수령 시</strong>: 연 2,100만 원 수령 &rarr; 2,000만 원 기준 초과로 피부양자 즉시 박탈 &rarr; 아파트 및 자동차 재산 점수 합산되어 매달 지역건보료 약 25만 원(연 300만 원) 발생.</p>
                <p>• <strong>조기수령 시</strong>: 2년 조기수령(12% 감액)으로 월 154만 원(연 1,848만 원) 수령 &rarr; 연소득 2,000만 원 이하 유지로 피부양자 자격 철통 방어 &rarr; 건보료 0원 유지!</p>
                <p class="font-bold text-rose-800 pt-1">
                    * 연금은 연 252만 원 덜 받지만, 건보료 300만 원을 아끼므로 가계 전체로는 매년 50만 원 이상 순이익을 얻습니다.
                </p>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">5. 조기수령 전 반드시 점검해야 할 3대 주의사항</h2>
            <div class="space-y-3 my-4">
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">1. '소득 있는 업무(A값 초과)' 종사 시 연금 지급 정지</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        월평균 소득금액이 국민연금 'A값'(최근 3개년 평균 소득월액, 약 300만 원 수준)을 초과하는 근로·사업 소득이 발생하면 조기연금 지급이 해당 기간 동안 전면 중단됩니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">2. 배우자 사망 시 '유족연금 중복 조정' 시 감액 불이익</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        부부가 모두 연금을 받다가 배우자가 먼저 사망하는 경우, 본인 연금 + 유족연금 30%를 선택하게 되는데 본인 연금 자체가 30% 감액된 상태이므로 최종 합산 수령액이 낮아질 수 있습니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">3. 물가상승률 복리 효과의 축소</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        국민연금은 매년 소비자물가상승률만큼 원금이 인상됩니다. 원금 자체가 70%로 작아져 있으면 매년 붙는 물가상승분(원금×물가상승률)의 절대 금액도 작아져 20~30년 장기 생존 시 격차가 더욱 크게 벌어집니다.
                    </p>
                </div>
            </div>
        """,
        "faqs": [
            ("Q. 조기연금을 신청했다가 나중에 마음이 바뀌면 취소할 수 있나요?",
             "조기노령연금 수급권을 취득한 후에는 임의로 수령을 철회하거나 원래 금액으로 환원할 수 없습니다. 단, A값을 초과하는 소득 활동을 하거나 '지급정지 신청'을 하면 지급을 일시 정지하고 정지된 기간만큼 나중에 감액률을 다시 재조정받을 수는 있습니다."),
            ("Q. 국민연금을 오히려 늦게 받는 '연기연금'은 어떤 사람에게 유리한가요?",
             "연기연금은 1년 늦출 때마다 7.2%(최대 5년 36%)를 더 얹어줍니다. 현재 60대 초반에도 안정적인 고소득 직장에 근무하여 세금과 연금 삭감을 피하고 싶거나, 가족력이 있어 85세 이상 장수가 확실시되는 분들에게 최적입니다."),
            ("Q. 개인연금저축이나 IRP 연금 수령액도 건강보험 2,000만원 기준에 들어가나요?",
             "아닙니다. 건강보험 피부양자 소득 요건(2,000만 원)에 합산되는 연금 소득은 국민연금, 공무원연금, 사학연금, 군인연금, 별정우체국연금 등 '공적연금'뿐이며, 사적연금(IRP, 연금저축펀드, 퇴직연금)은 현재 합산되지 않습니다.")
        ]
    },
    {
        "slug": "blog-didimdol-loan-room-deduction",
        "no": 50,
        "title": "수도권 디딤돌 대출 5,500만원 방공제 의무화 규제 분석: 내 집 마련 잔금 부족 사태 방어법과 실전 자금 조달 대안",
        "desc": "국토교통부 수도권 정책모기지 긴급 규제 완벽 해설! 소액임차보증금(방공제) 5,500만원 필수 차감으로 축소된 실제 주택구입 잔금 대출 한도 계산법과 모기지신용보증(MCG) 배제 시 자금 조달 실전 대안 총정리.",
        "cat": "realestate",
        "catName": "부동산·주거",
        "badge": "특보",
        "readTime": "약 8분",
        "calcLink": "real-loan.html",
        "calcName": "버팀목·디딤돌 정책대출 비교기",
        "hook_title": "잔금 3주 전 날아온 5,500만원 한도 삭감 통보, 어떻게 메워야 계약금을 지킬 수 있을까?",
        "hook_p1": "생애 첫 내 집 마련을 꿈꾸며 청약에 당첨되었거나 수도권 중저가 아파트 매매 계약서에 도장을 찍은 실수요자분들에게 청천벽력 같은 소식이 전해졌습니다. 바로 정부의 수도권 디딤돌 대출 한도 축소 규제입니다. 가장 뼈아픈 대목은 바로 '소액임차보증금(일명 방공제)' 차감 의무화입니다.",
        "hook_p2": "기존에는 한국주택금융공사의 모기지신용보증(MCG)에 가입하면 방공제 금액을 차감하지 않고 LTV 한도(최대 70~80%)를 꽉 채워 대출을 받을 수 있었는데, 이제 수도권 아파트는 서울 기준 무려 5,500만 원, 경기 과밀억제권역 기준 4,800만 원을 무조건 대출금에서 깎고 내어주겠다는 것입니다. 당장 다음 달 잔금일인데 은행에서 '5,500만 원 덜 나옵니다'라는 통보를 받으면 어떻게 해야 할까요? 계약금을 날리지 않고 부족한 현금을 메우는 합법적인 대안은 무엇일까요? 규제 예외 대상부터 실전 자금 조달 플랜까지 꼼꼼하게 짚어드립니다.",
        "editor_tip": "신생아 특례 디딤돌 대출은 이번 방공제 의무화 규제 대상에서 전격 제외되었습니다. 본인의 대출 유형이 일반 디딤돌인지 신생아 특례인지 확인하고, 일반 디딤돌이라면 즉시 보금자리론과의 금리 및 한도 비교 시뮬레이션을 돌려보셔야 합니다.",
        "content_html": """
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">1. 디딤돌 대출 '방공제(소액임차보증금 차감)' 규제의 본질</h2>
            <p>
                주택임대차보호법에 따르면 집이 경매로 넘어갈 경우 소액임차인의 최우선변제금을 은행 대출금보다 먼저 배당해야 합니다. 은행은 이 손실을 막기 위해 방 1개당 최우선변제금만큼 대출 한도를 차감하는데, 이를 현장에서 <strong>방공제</strong>라고 부릅니다.
            </p>
            <div class="overflow-x-auto my-4">
                <table class="w-full text-xs sm:text-sm text-left border border-slate-200 rounded-xl overflow-hidden">
                    <thead class="bg-slate-100 text-slate-800 font-bold border-b border-slate-200">
                        <tr>
                            <th class="p-3">지역 구분</th>
                            <th class="p-3 font-bold text-rose-600">필수 방공제 차감액</th>
                            <th class="p-3">적용 대상 주요 지역</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 font-medium">
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">서울특별시</td>
                            <td class="p-3 font-extrabold text-rose-600 text-base">5,500만 원 차감</td>
                            <td class="p-3">서울 25개 전 자치구</td>
                        </tr>
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">수도권 과밀억제권역</td>
                            <td class="p-3 font-extrabold text-rose-600 text-base">4,800만 원 차감</td>
                            <td class="p-3">인천(일부 제외), 수원, 성남, 고양, 부천, 안양, 광명 등 및 세종·화성·용인·김포</td>
                        </tr>
                        <tr class="hover:bg-slate-50">
                            <td class="p-3 font-bold text-slate-900">지방 광역시</td>
                            <td class="p-3 font-bold text-slate-700">규제 미적용 (MCG 유지)</td>
                            <td class="p-3 text-slate-500">지방 주택 시장 침체 방지를 위해 방공제 면제 유지</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">2. 규제 적용 전후 실제 통장 수령액 및 자금 격차 비교</h2>
            <p>
                실제 서울 시내 5억 원 아파트를 매수하는 무주택 생애최초 매수자를 기준으로 규제 전후 대출금 차이를 시뮬레이션해 보겠습니다.
            </p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 my-4">
                <div class="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2">
                    <div class="font-bold text-slate-700 text-sm">규제 적용 전 (MCG 보증 가입)</div>
                    <div class="text-slate-600 text-xs leading-relaxed">
                        • 주택가격 5억원 × LTV 70% = <strong>3억 5,000만원 대출 승인</strong>.<br>
                        • 방공제 0원 (MCG 보증서로 전액 면제).<br>
                        • 매수자 준비 현금: 계약금 10%(5천만원) + 취득세 및 부대비용 등 약 7,000만원.
                    </div>
                </div>
                <div class="p-5 bg-rose-50/60 border border-rose-200 rounded-2xl space-y-2">
                    <div class="font-bold text-rose-900 text-sm">규제 적용 후 (현재 수도권 아파트)</div>
                    <div class="text-slate-700 text-xs leading-relaxed font-medium">
                        • 산출 한도 3억 5,000만원 - 서울 방공제 5,500만원 = <strong>2억 9,500만원 대출</strong>.<br>
                        • <strong>한도 축소분</strong>: 정확히 5,500만 원 부족 발생!<br>
                        • 매수자 준비 현금: 기존 7천만 원 + 부족분 5,500만 원 = <strong>총 1억 2,500만 원의 순수 현금 필요</strong>.
                    </div>
                </div>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">3. 방공제 규제에서 전격 제외되는 3대 예외 대상</h2>
            <div class="space-y-3 my-4">
                <div class="p-4 bg-blue-50/70 border border-blue-200 rounded-xl space-y-1">
                    <div class="font-bold text-blue-900 text-sm">1. 신생아 특례 디딤돌 대출 (100% 예외)</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        출산 2년 이내 가구를 위한 '신생아 특례 디딤돌 대출'은 이번 수도권 대출 한도 축소 및 방공제 규제 대상에서 전격 제외되었습니다. 기존처럼 MCG에 가입하여 방공제 차감 없이 LTV 70~80% 전액 대출이 가능합니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">2. 비수도권(지방) 소재 주택</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        부산, 대구, 대전, 광주, 울산 및 전국 도 단위 시·군 지역 주택은 가계부채 관리 강화 대상이 아니므로 기존과 동일하게 방공제 면제가 유지됩니다.
                    </p>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                    <div class="font-bold text-slate-900 text-sm">3. 규제 시행일 이전 계약금 납부 완료자</div>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        규제 시행일 이전에 매매계약을 체결하고 계약금을 송금한 사실이 금융거래 내역으로 입증되는 매수자는 종전 규정을 적용받아 방공제가 차감되지 않습니다.
                    </p>
                </div>
            </div>

            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-2 pt-6">4. 잔금일 5,500만원 부족할 때 실전 자금 조달 플랜 B</h2>
            <div class="p-5 bg-slate-50 border border-slate-200 rounded-2xl text-xs sm:text-sm text-slate-700 leading-relaxed space-y-3 font-medium my-4">
                <p>• <strong>대안 1: 한국주택금융공사 '보금자리론'으로 전환</strong>: 보금자리론은 디딤돌보다 금리가 약 0.5~1.0%p 높지만, 방공제 필수 차감 규제가 적용되지 않아 LTV 70% 전액을 그대로 수령할 수 있습니다. 한도가 급한 경우 디딤돌을 포기하고 보금자리론으로 갈아타는 것이 현명합니다.</p>
                <p>• <strong>대안 2: 신용대출 동시 실행 시 대출 순서 주의</strong>: 주택담보대출 실행일 전에 신용대출을 먼저 받으면 DSR 한도에 걸려 디딤돌 승인이 거절될 수 있습니다. 반드시 디딤돌 대출 심사가 완료된 후 잔금 당일에 맞춰 신용대출을 실행해야 합니다.</p>
                <p>• <strong>대안 3: 부모님 사적 차용증 작성</strong>: 부모님에게 5,500만 원을 빌릴 경우, 세법상 무이자 차용 한도는 원금 2억 1,700만 원까지 가능하므로 차용증을 작성하고 매달 소액이라도 원금 상환 이체 내역을 남겨 증여세 과세를 방어해야 합니다.</p>
            </div>
        """,
        "faqs": [
            ("Q. 오피스텔이나 빌라(다세대)도 디딤돌 방공제가 적용되나요?",
             "디딤돌 대출은 원칙적으로 주택법상 주택(아파트, 연립, 다세대, 단독주택)만 가능하며 업무시설인 오피스텔은 대상이 아닙니다. 빌라의 경우 이번 수도권 방공제 규제 대상에 아파트와 동일하게 포함됩니다."),
            ("Q. 생애최초 주택구입자도 방공제 차감을 피할 수 없나요?",
             "네, 안타깝게도 생애최초 특례 LTV 80%를 적용받더라도 산출된 한도에서 서울 5,500만 원, 경기 과밀 4,800만 원이 그대로 차감됩니다."),
            ("Q. 분양 아파트 잔금 대출(후취담보)도 방공제 규제를 받나요?",
             "네, 신규 분양 아파트의 입주 잔금 대출 시에도 소유권 이전등기 전까지 후취담보가 제한되거나 방공제가 적용되어 수분양자의 실질 현금 부담이 늘어납니다.")
        ]
    }
]

def render_full_article(article):
    filename = f"{article['slug']}.html"
    title = article['title']
    desc = article['desc']
    cat = article['cat']
    cat_name = article['catName']
    badge = article['badge']
    read_time = article['readTime']
    calc_link = article['calcLink']
    calc_name = article['calcName']
    hook_title = article['hook_title']
    hook_p1 = article['hook_p1']
    hook_p2 = article['hook_p2']
    editor_tip = article['editor_tip']
    content_html = article['content_html']
    faqs = article['faqs']

    # FAQ HTML
    faq_cards_html = ""
    faq_schema_items = []
    for q, a in faqs:
        faq_cards_html += f"""<div class="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                            <div class="font-bold text-slate-800 text-sm">{q}</div>
                            <div class="text-xs sm:text-sm text-slate-600 mt-1.5 leading-relaxed">{a}</div>
                        </div>"""
        faq_schema_items.append(f"""{{
          "@type": "Question",
          "name": "{q}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a}"
          }}
        }}""")

    faq_schema_str = ",\n        ".join(faq_schema_items)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2N5V6S642H"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-2N5V6S642H');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{title} | 위집 (wezip)</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://wezip.co.kr/{filename}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title} | 위집">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="https://wezip.co.kr/{filename}">
    <meta property="og:site_name" content="위집 (wezip)">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:image" content="https://wezip.co.kr/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="WE ZIP - 대한민국 생활 금융 포털">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://wezip.co.kr/og-image.png">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="manifest" href="site.webmanifest">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-5717882145510454">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5717882145510454" crossorigin="anonymous"></script>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="common.css">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{title}",
      "description": "{desc}",
      "author": {{
        "@type": "Organization",
        "name": "위집 금융편집국",
        "url": "https://wezip.co.kr/about.html"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "위집",
        "url": "https://wezip.co.kr"
      }},
      "datePublished": "{TODAY}",
      "dateModified": "{TODAY}",
      "mainEntityOfPage": "https://wezip.co.kr/{filename}"
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {faq_schema_str}
      ]
    }}
    </script>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans">

    <header class="sticky top-0 z-40 bg-[#0F172A] border-b border-slate-800 text-white select-none">
        <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center gap-8">
                <a href="index.html" class="flex items-center gap-2.5 shrink-0 group" aria-label="WE ZIP 홈으로 이동">
                    <div class="w-10 h-10 rounded-xl bg-blue-600 group-hover:bg-blue-500 flex items-center justify-center text-white shadow-sm transition">
                        <svg class="svg-icon w-5 h-5 text-white stroke-[2.2]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 9.5L12 3l9 6.5v10a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 19.5v-10z"></path>
                            <polyline points="9 21 9 12 15 12 15 21"></polyline>
                        </svg>
                    </div>
                    <div class="flex items-center gap-1.5">
                        <span class="font-black text-xl tracking-tight text-white notranslate" translate="no">WE <span class="text-blue-400">ZIP</span></span>
                        <span class="text-[11px] font-black text-emerald-300 px-2 py-0.5 bg-emerald-950/70 rounded-full border border-emerald-500 shadow-sm">100% 무료</span>
                    </div>
                </a>

                <nav class="hidden md:flex items-center gap-1 text-sm font-medium">
                    <a href="salary.html" class="px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition">급여·소득</a>
                    <a href="real-estate.html" class="px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition">부동산·취득세</a>
                    <a href="gov-finder.html" class="px-3 py-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition">정부지원금</a>
                    <a href="blog.html" class="px-3 py-2 rounded-lg text-blue-400 bg-slate-800/80 transition font-bold">금융 칼럼</a>
                </nav>
            </div>

            <div class="flex items-center gap-2">
                <a href="gov-finder.html" class="text-xs font-bold px-3 py-2 rounded-lg bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 hover:text-white transition flex items-center gap-1.5">
                    <svg class="svg-icon w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>지원금 찾기</span>
                </a>
            </div>
        </div>
    </header>

    <!-- [와이드 3단 레이아웃: 좌측 배너 + 중앙 컨텐츠 + 우측 배너] -->
    <div class="w-full max-w-[1560px] mx-auto px-2 sm:px-4 py-8 flex items-start justify-center gap-5 flex-grow">
        <!-- [좌측 스폰서 배너 광고 (데스크톱 160x600)] -->
        <aside class="hidden xl:flex flex-col items-center w-[160px] shrink-0 sticky top-20 select-none z-10" aria-label="좌측 스폰서 광고">
            <div class="w-full bg-white border border-dashed border-slate-300 rounded-2xl p-3 text-center shadow-xs min-h-[600px] flex flex-col justify-between hover:border-slate-400 transition">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">ADVERTISEMENT</span>
                <div class="my-auto py-8 text-slate-400">
                    <svg class="svg-icon w-6 h-6 mx-auto mb-2 text-slate-400" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <div class="text-xs font-bold text-slate-600">좌측 날개 배너</div>
                    <div class="text-[11px] text-slate-400 mt-1">160 × 600<br>구글 애드센스 및<br>직접 광고 스폰서</div>
                </div>
                <div class="w-full pt-2 border-t border-slate-100">
                    <span class="text-[10px] text-slate-400 font-medium block mb-1">WE ZIP 스폰서</span>
                    <a href="contact.html?type=ad" class="block w-full py-1.5 px-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-bold rounded-lg border border-blue-200 transition text-center">
                        배너 광고 문의 &rarr;
                    </a>
                </div>
            </div>
        </aside>

        <!-- [중앙 메인 컨텐츠] -->
        <main class="w-full max-w-4xl mx-auto space-y-8">
            <nav class="flex items-center gap-2 text-xs text-slate-500 font-medium">
                <a href="index.html" class="hover:text-blue-600 transition">홈</a>
                <span>&gt;</span>
                <a href="blog.html" class="hover:text-blue-600 transition">금융 칼럼</a>
                <span>&gt;</span>
                <span class="text-slate-800 font-bold">{cat_name}</span>
            </nav>

            <header class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-4">
                <div class="flex items-center gap-2">
                    <span class="text-xs font-bold px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200">{cat_name} 심층분석</span>
                    <span class="text-xs text-slate-400">읽는 시간 {read_time} · {TODAY}</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-snug">
                    {title}
                </h1>
                <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {desc}
                </p>

                <!-- 계산기 바로가기 배너 -->
                <div class="p-4 bg-blue-50/70 border border-blue-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-4">
                    <div class="flex items-center gap-2 text-xs sm:text-sm text-blue-900 font-bold">
                        <svg class="svg-icon w-4 h-4 text-blue-600 shrink-0" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line></svg>
                        <span>내 실제 예상 금액을 1초 만에 무료로 직접 계산해 보세요!</span>
                    </div>
                    <a href="{calc_link}" class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition shadow-sm shrink-0 text-center">
                        {calc_name} 바로가기 &rarr;
                    </a>
                </div>
            </header>

            <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-8 text-slate-700 leading-relaxed font-normal">
                <!-- [블로그형 스토리텔링 도입부 & 공감 해설 박스] -->
                <div class="bg-gradient-to-r from-blue-50/70 via-slate-50 to-blue-50/40 border-l-4 border-blue-600 rounded-r-2xl p-5 sm:p-7 space-y-3.5 text-slate-700 text-sm sm:text-base leading-relaxed">
                    <div class="flex items-center gap-2 font-black text-slate-900 text-base sm:text-lg">
                        <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                        <span>{hook_title}</span>
                    </div>
                    <p class="font-medium text-slate-800 leading-relaxed">
                        {hook_p1}
                    </p>
                    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
                        {hook_p2}
                    </p>
                    <div class="pt-2 border-t border-blue-100/80 flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2 text-xs font-bold text-blue-800">
                        <span>* 위집 편집국 핵심 조언:</span>
                        <span class="font-normal text-slate-600">{editor_tip}</span>
                    </div>
                </div>

                <!-- 아티클 본문 섹션들 -->
                {content_html}

                <!-- FAQ 섹션 -->
                <section class="space-y-4 border-t border-slate-100 pt-6">
                    <h2 class="text-lg sm:text-xl font-bold text-slate-900 flex items-center gap-2">
                        <span class="w-2 h-5 bg-blue-600 rounded-full inline-block"></span>
                        <span>자주 묻는 질문 (FAQ)</span>
                    </h2>
                    <div class="space-y-3">
                        {faq_cards_html}
                    </div>
                </section>

                <!-- 관련 계산기 하단 추천 배너 -->
                <section class="p-5 bg-blue-50/70 border border-blue-200 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="space-y-1 text-center sm:text-left">
                        <div class="text-xs font-bold text-blue-600 uppercase tracking-wide">WE ZIP 실시간 계산기 연동</div>
                        <div class="text-sm sm:text-base font-extrabold text-slate-900">내 실제 예상 금액을 1초 만에 확인해 보세요</div>
                        <p class="text-xs text-slate-600">2026년 최신 법정 기준이 100% 반영된 무료 시뮬레이터입니다.</p>
                    </div>
                    <a href="{calc_link}" class="w-full sm:w-auto py-2.5 px-5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm rounded-xl transition text-center shrink-0 shadow-sm">
                        {calc_name} 바로가기 &rarr;
                    </a>
                </section>
            </article>

            <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <div class="font-bold text-slate-900 text-sm">페이지 내용이 도움이 되셨나요?</div>
                    <div class="text-xs text-slate-500">지인이나 동료에게 링크를 복사하여 유용한 금융·세무 정보를 공유해 보세요.</div>
                </div>
                <button type="button" onclick="copyPageUrl(this)" class="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center gap-1.5 transition">
                    <svg class="svg-icon w-3.5 h-3.5" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                    <span>페이지 링크 복사</span>
                </button>
            </div>
        </main>

        <!-- [우측 스폰서 배너 광고 (데스크톱 160x600)] -->
        <aside class="hidden xl:flex flex-col items-center w-[160px] shrink-0 sticky top-20 select-none z-10" aria-label="우측 스폰서 광고">
            <div class="w-full bg-white border border-dashed border-slate-300 rounded-2xl p-3 text-center shadow-xs min-h-[600px] flex flex-col justify-between hover:border-slate-400 transition">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">ADVERTISEMENT</span>
                <div class="my-auto py-8 text-slate-400">
                    <svg class="svg-icon w-6 h-6 mx-auto mb-2 text-slate-400" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <div class="text-xs font-bold text-slate-600">우측 날개 배너</div>
                    <div class="text-[11px] text-slate-400 mt-1">160 × 600<br>구글 애드센스 및<br>직접 광고 스폰서</div>
                </div>
                <div class="w-full pt-2 border-t border-slate-100">
                    <span class="text-[10px] text-slate-400 font-medium block mb-1">WE ZIP 스폰서</span>
                    <a href="contact.html?type=ad" class="block w-full py-1.5 px-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-bold rounded-lg border border-blue-200 transition text-center">
                        배너 광고 문의 &rarr;
                    </a>
                </div>
            </div>
        </aside>
    </div>

    <footer class="bg-white border-t border-slate-200 mt-20 select-none">
        <div class="max-w-6xl mx-auto px-4 py-8">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-100 pb-6 text-xs text-slate-500">
                <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-blue-600 flex items-center justify-center text-white font-bold text-xs">W</div>
                    <span class="font-bold text-slate-700">위집 (wezip)</span>
                    <span class="text-slate-300">|</span>
                    <span>2026 대한민국 생활 금융 포털</span>
                </div>
                <div class="flex items-center gap-4 font-medium">
                    <a href="about.html" class="hover:text-blue-600 transition">서비스 소개</a>
                    <a href="terms.html" class="hover:text-blue-600 transition">이용약관</a>
                    <a href="privacy.html" class="hover:text-blue-600 transition font-bold text-slate-700">개인정보처리방침</a>
                </div>
            </div>
            <div class="pt-6 text-center text-xs text-slate-400 space-y-1">
                <p>본 사이트의 모든 계산 결과는 2026년 관계 법령 및 세법 기준 시뮬레이션이며, 법적 효력을 갖는 공식 증명서가 아닙니다.</p>
                <p>© 2026 wezip.co.kr. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="common.js"></script>
</body>
</html>
"""
    return html

def update_blog_html():
    blog_path = os.path.join(BASE_DIR, "blog.html")
    with open(blog_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We want:
    # no: 50 -> blog-didimdol-loan-room-deduction.html
    # no: 49 -> blog-national-pension-early-receipt.html (rich updated title/desc)
    # no: 48 -> blog-parental-leave-pay-250.html (rich updated title/desc)
    # followed by no: 47 -> blog-year-end-settlement-dual-income.html

    # Replace the existing entries for 49 and 48 if present, or add 50 on top
    didimdol = ARTICLES_DATA[2]
    pension = ARTICLES_DATA[1]
    parental = ARTICLES_DATA[0]

    new_top_block = f"""      {{
        no: 50,
        title: "{didimdol['title']}",
        desc: "{didimdol['desc']}",
        cat: "{didimdol['cat']}",
        catName: "{didimdol['catName']}",
        badge: "{didimdol['badge']}",
        date: "{TODAY_DOT}",
        readTime: "{didimdol['readTime']}",
        link: "blog-didimdol-loan-room-deduction.html"
      }},
      {{
        no: 49,
        title: "{pension['title']}",
        desc: "{pension['desc']}",
        cat: "{pension['cat']}",
        catName: "{pension['catName']}",
        badge: "{pension['badge']}",
        date: "2026.11.08",
        readTime: "{pension['readTime']}",
        link: "blog-national-pension-early-receipt.html"
      }},
      {{
        no: 48,
        title: "{parental['title']}",
        desc: "{parental['desc']}",
        cat: "{parental['cat']}",
        catName: "{parental['catName']}",
        badge: "{parental['badge']}",
        date: "2026.11.04",
        readTime: "{parental['readTime']}",
        link: "blog-parental-leave-pay-250.html"
      }},"""

    # Regex replace from 'const ARTICLES = [' to before 'no: 47'
    pattern = r'const ARTICLES = \[\s*\{[^}]*no:\s*49[^}]*\},\s*\{[^}]*no:\s*48[^}]*\},'
    if re.search(pattern, content):
        content = re.sub(pattern, f"const ARTICLES = [\n{new_top_block}", content, count=1)
    else:
        # fallback replace
        articles_marker = "const ARTICLES = ["
        content = content.replace(articles_marker, f"{articles_marker}\n{new_top_block}", 1)

    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated blog.html: set #50, #49, #48.")

def update_sitemap():
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_urls = []
    for art in ARTICLES_DATA:
        filename = f"{art['slug']}.html"
        if f"<loc>https://wezip.co.kr/{filename}</loc>" not in content:
            new_urls.append(f"""    <url>
        <loc>https://wezip.co.kr/{filename}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.80</priority>
    </url>""")

    if new_urls:
        content = content.replace("</urlset>", "\n".join(new_urls) + "\n</urlset>")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated sitemap.xml with {len(new_urls)} URLs.")

def update_rss():
    rss_path = os.path.join(BASE_DIR, "rss.xml")
    with open(rss_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_items = []
    for art in ARTICLES_DATA:
        filename = f"{art['slug']}.html"
        if f"<link>https://wezip.co.kr/{filename}</link>" not in content:
            new_items.append(f"""    <item>
      <title>{art['title']}</title>
      <link>https://wezip.co.kr/{filename}</link>
      <guid>https://wezip.co.kr/{filename}</guid>
      <description>{art['desc']}</description>
      <pubDate>{NOW_RFC822}</pubDate>
      <category>{art['catName']}</category>
    </item>""")

    if new_items:
        items_block = "\n".join(new_items)
        m = re.search(r'(<lastBuildDate>[^<]+</lastBuildDate>)', content)
        if m:
            content = content.replace(m.group(1), f"{m.group(1)}\n{items_block}")
        else:
            content = content.replace("<channel>", f"<channel>\n{items_block}")

        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated rss.xml with {len(new_items)} items.")

def main():
    print("=== Publishing Deep Human-Style Columns ===")
    for art in ARTICLES_DATA:
        filename = f"{art['slug']}.html"
        file_path = os.path.join(BASE_DIR, filename)
        html_content = render_full_article(art)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Written rich article: {filename} ({len(html_content):,} bytes)")

    update_blog_html()
    update_sitemap()
    update_rss()
    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
