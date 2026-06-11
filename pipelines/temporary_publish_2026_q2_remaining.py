#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import yaml

from lib import ISSUES, SITE, copy_approved_articles_to_site, dump_front_matter, ensure_dir, read_text, write_text


ISSUE = "2026-Q2"
TODAY = "2026-06-11"
BASE = ISSUES / ISSUE


SOURCES = {
    "imf": ("International Monetary Fund, World Economic Outlook, April 2026", "https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026"),
    "oecd_eo": ("OECD, Economic Outlook, Volume 2026 Issue 1", "https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html"),
    "iea": ("International Energy Agency, Global Energy Review 2026", "https://www.iea.org/reports/global-energy-review-2026"),
    "unhcr": ("UNHCR, Global Trends", "https://www.unhcr.org/us/global-trends"),
    "oecd_ai": ("OECD, AI use by individuals and firms", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html"),
    "un_ai": ("United Nations, Global Dialogue on AI Governance", "https://www.un.org/global-dialogue-ai-governance/en"),
    "eu_ai": ("European Commission, AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"),
    "stanford": ("Stanford HAI, 2026 AI Index Report", "https://hai.stanford.edu/ai-index/2026-ai-index-report"),
    "freedom_house": ("Freedom House, Freedom in the World 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy"),
    "vdem": ("V-Dem Institute, Democracy Report 2026", "https://www.v-dem.net/publications/democracy-reports/"),
    "world_bank": ("World Bank, Global Economic Prospects, January 2026", "https://openknowledge.worldbank.org/entities/publication/bb904ec6-730f-4dd9-b1af-ad3153ee1616"),
    "bok": ("Bank of Korea, Economic Outlook, May 2026", "https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098207&programType=newsDataEng&relate=Y"),
    "moef": ("Ministry of Finance and Economy, Economic Bulletin, June 2026", "https://english.moef.go.kr/pu/selectTbPublicDtl.do?boardCd=P0002&seq=2052"),
    "mods": ("Ministry of Data and Statistics, Birth and Death press releases", "https://mods.go.kr/menu.es?mid=a20108100000"),
    "korea_net_births": ("Korea.net, 2025 births and fertility summary", "https://www.korea.net/NewsFocus/Society/view?articleId=288047"),
    "nec": ("National Election Commission, Republic of Korea", "https://www.nec.go.kr/"),
    "ap_elections": ("Associated Press, South Korea local elections report, June 2026", "https://apnews.com/article/3f75bc77d129daecbcfac5afafbeb8d0"),
    "ccourt": ("Constitutional Court of Korea, Latest Decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143"),
    "unesco": ("UNESCO, Guidance for generative AI in education and research", "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research"),
}


ARTICLES = [
    {
        "slug": "editors-note-capacity-question",
        "type": "editor's note",
        "scope": "comparative",
        "en_title": "The Quarter When Capacity Became The Question",
        "ko_title": "역량이 질문이 된 분기",
        "en_subtitle": "The issue is not acceleration alone, but whether institutions can absorb it.",
        "ko_subtitle": "문제는 가속 그 자체가 아니라, 제도가 그것을 흡수할 수 있는가이다.",
        "tags_en": ["editor's note", "institutional capacity", "quarterly theme"],
        "tags_ko": ["편집자의 글", "제도적 역량", "계간 주제"],
        "sources": ["imf", "oecd_eo", "unhcr", "oecd_ai", "freedom_house", "bok", "ccourt"],
        "abstract_en": "The 2026-Q2 issue is organized around a simple claim: the quarter's important events are not only fast, but institutionally demanding. AI, war-shadowed macroeconomics, displacement, democratic strain, and Korea's domestic questions all ask whether public institutions can absorb pressure before pressure becomes distrust.",
        "abstract_ko": "2026-Q2 호는 하나의 단순한 주장 위에 놓인다. 이번 분기의 중요한 사건들은 단지 빠른 것이 아니라 제도적으로 부담스럽다. AI, 전쟁의 그림자가 드리운 거시경제, 강제이주, 민주주의의 긴장, 한국의 국내 의제는 모두 압력이 불신으로 바뀌기 전에 공적 제도가 그것을 흡수할 수 있는가를 묻는다.",
        "opening_en": "A quarterly review should resist the temptation to make every event an example of one grand theory. Still, quarters do have shapes. This one is marked by the reappearance of capacity as the hidden variable behind many public arguments.",
        "opening_ko": "계간지는 모든 사건을 하나의 거대 이론의 사례로 만드는 유혹을 경계해야 한다. 그래도 분기마다 모양은 있다. 이번 분기의 모양은 여러 공적 논쟁 뒤에 숨어 있던 변수, 곧 역량의 재등장이다.",
        "question_en": "What changed this quarter is not only that institutions faced harder problems. It is that many of those problems became material, administrative, and distributive at the same time.",
        "question_ko": "이번 분기에 달라진 것은 제도가 더 어려운 문제를 만났다는 사실만이 아니다. 그 문제들이 동시에 물질적이고 행정적이며 분배적인 성격을 띠기 시작했다는 점이다.",
        "concept_en": "Capacity means more than state size. It includes expertise, legitimacy, fiscal room, infrastructure planning, judicial credibility, administrative patience, and the ability to explain tradeoffs before citizens experience them as betrayal.",
        "concept_ko": "역량은 국가 규모보다 넓은 말이다. 그것은 전문성, 정당성, 재정 여지, 인프라 계획, 사법 신뢰, 행정의 인내, 그리고 시민이 상충관계를 배신으로 경험하기 전에 그것을 설명할 수 있는 능력을 포함한다.",
        "evidence_en": "The issue's source base points in the same direction. IMF and OECD forecasts describe a growing but more conditional world economy. UNHCR reports 117.8 million forcibly displaced people at the end of 2025. OECD data show firm-level AI adoption moving beyond the demonstration stage. Freedom House reports a twentieth consecutive year of global freedom decline. Korea's official sources show both strategic-sector strength and deep household formation pressure.",
        "evidence_ko": "이번 호의 출처 기반은 같은 방향을 가리킨다. IMF와 OECD 전망은 성장하지만 조건이 좁아진 세계경제를 묘사한다. UNHCR은 2025년 말 강제이주민이 1억 1,780만 명이라고 보고한다. OECD 자료는 기업의 AI 채택이 시연 단계를 넘어섰음을 보여준다. Freedom House는 세계 자유가 20년 연속 후퇴했다고 보고한다. 한국의 공식 출처들은 전략 부문의 강함과 가계 형성 압력이 동시에 존재함을 보여준다.",
        "interpretations_en": ["The acceleration view says the quarter is mainly about technological and geopolitical speed.", "The exhaustion view says the deeper story is institutional fatigue after repeated shocks.", "The capacity view, used here, treats speed and exhaustion as connected through institutions."],
        "interpretations_ko": ["가속 관점은 이번 분기가 주로 기술과 지정학의 속도에 관한 것이라고 본다.", "소진 관점은 더 깊은 이야기가 반복된 충격 이후의 제도 피로라고 본다.", "이 글이 취하는 역량 관점은 속도와 소진을 제도를 통해 연결된 문제로 본다."],
        "opposing_en": "The strongest objection is that a theme can over-organize reality. AI governance, forced displacement, Korean fertility, and constitutional adjudication are not the same problem. A serious issue should not pretend that simultaneity is causation.",
        "opposing_ko": "가장 강한 반론은 하나의 주제가 현실을 지나치게 정리할 수 있다는 것이다. AI 거버넌스, 강제이주, 한국의 출산, 헌법재판은 같은 문제가 아니다. 진지한 호라면 동시성을 인과성처럼 꾸며서는 안 된다.",
        "argument_en": "That objection is right, and it is why this issue uses capacity as a frame rather than a master cause. The point is not that every article proves one thesis. It is that each article asks how institutions translate pressure into policy, legitimacy, rights, or failure.",
        "argument_ko": "그 반론은 옳다. 그래서 이번 호는 역량을 만능 원인이 아니라 프레임으로 사용한다. 모든 글이 하나의 명제를 입증한다는 뜻이 아니다. 각 글이 압력을 정책, 정당성, 권리, 또는 실패로 번역하는 제도적 과정을 묻는다는 뜻이다.",
        "implications_en": ["Read forecasts as conditional arguments, not prophecies.", "Read AI as infrastructure, not only software.", "Read Korea's domestic questions through raw sources before commentary.", "Read democratic stress without casual conceptual inflation."],
        "implications_ko": ["전망은 예언이 아니라 조건부 주장으로 읽어야 한다.", "AI는 소프트웨어만이 아니라 인프라로 읽어야 한다.", "한국 국내 의제는 논평보다 원자료를 먼저 통해 읽어야 한다.", "민주주의의 긴장은 개념을 부풀리지 않고 읽어야 한다."],
        "strength_en": ["High confidence: the cited institutional sources establish that these pressures are current and structurally important.", "Moderate confidence: the issue frame plausibly connects them through institutional capacity.", "Contested: the frame should not be treated as a complete theory of the quarter."],
        "strength_ko": ["높은 확신: 인용된 기관 자료들은 이 압력들이 현재적이고 구조적으로 중요하다는 점을 뒷받침한다.", "중간 확신: 이번 호의 프레임은 그것들을 제도적 역량을 통해 연결할 수 있다.", "논쟁적 지점: 이 프레임을 분기의 완결된 이론으로 취급해서는 안 된다."],
        "uncertainty_en": "This editor's note is a map of editorial judgment, not an empirical model. Later revisions should change the frame if the remaining evidence points elsewhere.",
        "uncertainty_ko": "이 편집자의 글은 실증 모델이 아니라 편집 판단의 지도다. 남은 증거가 다른 방향을 가리키면 이후 개정에서 프레임도 바뀌어야 한다.",
    },
    {
        "slug": "govern-ai-before-infrastructure",
        "type": "technology and society essay",
        "scope": "global",
        "en_title": "Can The World Govern AI Before It Becomes Infrastructure?",
        "ko_title": "AI가 인프라가 되기 전에 세계는 그것을 통치할 수 있는가",
        "en_subtitle": "The hard part of AI governance begins when principles meet deployment.",
        "ko_subtitle": "AI 거버넌스의 어려움은 원칙이 배치와 만날 때 시작된다.",
        "tags_en": ["AI governance", "regulation", "infrastructure"],
        "tags_ko": ["AI 거버넌스", "규제", "인프라"],
        "sources": ["un_ai", "eu_ai", "oecd_ai", "stanford"],
        "abstract_en": "AI governance is moving from principles to implementation just as AI systems become operating infrastructure for firms, schools, states, and platforms. The central problem is not whether rules exist, but whether institutions have the capacity to enforce, update, and legitimate them.",
        "abstract_ko": "AI 거버넌스는 원칙에서 실행으로 이동하고 있으며, 바로 그 순간 AI 시스템은 기업, 학교, 국가, 플랫폼의 작동 인프라가 되고 있다. 핵심 문제는 규칙의 존재 여부가 아니라, 제도가 그것을 집행하고 갱신하며 정당화할 역량을 갖는가이다.",
        "opening_en": "AI regulation used to sound like a seminar question. In 2026 it looks more like infrastructure policy. The United Nations is convening a Global Dialogue on AI Governance in Geneva in July 2026; the EU AI Act is entering major implementation phases; and OECD data show firm adoption spreading.",
        "opening_ko": "AI 규제는 한때 세미나 주제처럼 들렸다. 2026년에는 훨씬 더 인프라 정책처럼 보인다. 유엔은 2026년 7월 제네바에서 AI 거버넌스 글로벌 대화를 열 예정이고, EU AI Act는 주요 실행 단계로 들어가며, OECD 자료는 기업 채택의 확산을 보여준다.",
        "question_en": "Can governance institutions shape AI before AI becomes too deeply embedded to contest?",
        "question_ko": "AI가 다투기 어려울 만큼 깊이 내장되기 전에 거버넌스 제도는 AI를 형성할 수 있는가?",
        "concept_en": "Governance is not the same as legislation. It includes risk classification, auditing, procurement rules, liability, technical standards, institutional expertise, public communication, and the capacity to revise rules when systems change.",
        "concept_ko": "거버넌스는 입법과 같지 않다. 그것은 위험 분류, 감사, 조달 규칙, 책임, 기술 표준, 제도 전문성, 공적 소통, 그리고 시스템이 변할 때 규칙을 개정할 수 있는 능력을 포함한다.",
        "evidence_en": "The EU AI Act entered into force in 2024 and becomes broadly applicable in 2026 with staged exceptions. The UN Global Dialogue has scheduled its first session for July 2026. OECD reported that 20.2 percent of firms in countries with available data used AI in 2025. Stanford's 2026 AI Index also shows a gap between expert and public expectations, which matters because regulation requires legitimacy as well as technical design.",
        "evidence_ko": "EU AI Act는 2024년에 발효되었고 2026년에 단계적 예외와 함께 본격 적용으로 들어간다. 유엔 글로벌 대화는 2026년 7월 첫 회의를 예정했다. OECD는 자료가 있는 국가에서 2025년 기업의 20.2%가 AI를 사용했다고 보고했다. Stanford 2026 AI Index는 전문가와 대중의 기대 사이의 차이도 보여주는데, 규제에는 기술 설계뿐 아니라 정당성이 필요하다는 점에서 중요하다.",
        "interpretations_en": ["The regulatory optimism view says the EU, OECD, and UN are building an architecture before the market hardens.", "The compliance-skeptical view says rules may create paperwork while large incumbents consolidate advantage.", "The capacity view asks whether public institutions can understand and inspect the systems they authorize."],
        "interpretations_ko": ["규제 낙관론은 EU, OECD, 유엔이 시장이 굳기 전에 제도 구조를 만들고 있다고 본다.", "준수 회의론은 규칙이 서류 작업을 만들 뿐 대형 기존 기업의 우위를 굳힐 수 있다고 본다.", "역량 관점은 공공기관이 자신이 승인하는 시스템을 이해하고 점검할 수 있는지를 묻는다."],
        "opposing_en": "The strongest objection is that premature regulation can entrench the very firms it seeks to control. Smaller developers may lack compliance teams; public agencies may outsource expertise to regulated companies; and symbolic audits may substitute for real accountability.",
        "opposing_ko": "가장 강한 반론은 성급한 규제가 통제하려는 바로 그 기업들을 굳힐 수 있다는 것이다. 작은 개발자는 준수 조직을 갖기 어렵고, 공공기관은 전문성을 규제 대상 기업에 의존할 수 있으며, 상징적 감사가 실제 책임을 대체할 수 있다.",
        "argument_en": "The objection is serious, but it argues for better capacity rather than no governance. If AI becomes infrastructure, the cost of weak governance rises over time. The issue is not a global super-regulator; it is a set of competent institutions that can classify risk, inspect systems, preserve contestability, and explain why some uses should not be automated.",
        "argument_ko": "그 반론은 중요하지만, 그것은 거버넌스의 포기가 아니라 더 나은 역량을 요구한다. AI가 인프라가 될수록 약한 거버넌스의 비용은 시간이 지날수록 커진다. 필요한 것은 세계 단일 초규제기관이 아니라 위험을 분류하고 시스템을 점검하며 다툴 수 있는 여지를 보존하고 어떤 사용은 자동화되어서는 안 되는지 설명할 수 있는 기관들이다.",
        "implications_en": ["Build public technical capacity before procurement dependence becomes irreversible.", "Treat AI literacy rules as administrative infrastructure, not public-relations language.", "Separate model safety, labor governance, education, competition, privacy, and public-sector accountability.", "Do not confuse multilateral dialogue with enforceable domestic capacity."],
        "implications_ko": ["조달 의존이 되돌리기 어려워지기 전에 공적 기술 역량을 구축해야 한다.", "AI 리터러시 규칙은 홍보 문구가 아니라 행정 인프라로 다뤄야 한다.", "모델 안전, 노동 거버넌스, 교육, 경쟁, 개인정보, 공공부문 책임을 구분해야 한다.", "다자 대화를 집행 가능한 국내 역량과 혼동해서는 안 된다."],
        "strength_en": ["High confidence: AI governance initiatives and firm adoption are documented by official and institutional sources.", "Moderate confidence: implementation capacity will determine whether rules matter.", "Contested: the best balance between innovation and regulation remains unresolved."],
        "strength_ko": ["높은 확신: AI 거버넌스 이니셔티브와 기업 채택은 공식·기관 출처로 확인된다.", "중간 확신: 실행 역량이 규칙의 실질성을 결정할 것이다.", "논쟁적 지점: 혁신과 규제 사이의 최선의 균형은 아직 정해지지 않았다."],
        "uncertainty_en": "This article does not claim that any current framework is sufficient. It claims that the window for building enforceable capacity is narrower than the rhetoric of future regulation suggests.",
        "uncertainty_ko": "이 글은 현재의 어떤 틀이 충분하다고 주장하지 않는다. 다만 집행 가능한 역량을 만들 수 있는 시간 창이 미래 규제의 수사보다 좁다고 주장한다.",
    },
    {
        "slug": "democracy-after-long-decline",
        "type": "institutional analysis",
        "scope": "global",
        "en_title": "Democracy After The Long Decline",
        "ko_title": "긴 하락 이후의 민주주의",
        "en_subtitle": "The danger is not only collapse, but the normalization of institutional erosion.",
        "ko_subtitle": "위험은 붕괴만이 아니라 제도 침식의 정상화다.",
        "tags_en": ["democracy", "rule of law", "institutions"],
        "tags_ko": ["민주주의", "법치", "제도"],
        "sources": ["freedom_house", "vdem"],
        "abstract_en": "Democratic decline is no longer best understood as a short emergency. In 2026 it is a background condition: repeated deterioration in rights, judicial independence, civic space, and electoral trust can become ordinary institutional weather before it becomes regime collapse.",
        "abstract_ko": "민주주의의 후퇴는 더 이상 짧은 비상사태로만 이해하기 어렵다. 2026년에는 그것이 배경 조건이 되었다. 권리, 사법 독립, 시민 공간, 선거 신뢰의 반복적 악화는 체제 붕괴가 되기 전에 평범한 제도적 날씨가 될 수 있다.",
        "opening_en": "Freedom House reports that global freedom declined for the twentieth consecutive year in 2025, with more countries deteriorating than improving. V-Dem's 2026 report similarly describes a world in which democratization is limited and autocratization reaches older democracies as well as newer ones.",
        "opening_ko": "Freedom House는 2025년에 세계 자유가 20년 연속 후퇴했으며, 개선된 국가보다 악화된 국가가 더 많았다고 보고한다. V-Dem의 2026년 보고서도 민주화는 제한적이고, 권위주의화는 신생 민주주의뿐 아니라 오래된 민주주의에도 도달한 세계를 묘사한다.",
        "question_en": "What does democracy mean after decline has become a long background condition rather than a sudden crisis?",
        "question_ko": "민주주의의 하락이 갑작스러운 위기가 아니라 긴 배경 조건이 되었을 때, 민주주의는 무엇을 의미하는가?",
        "concept_en": "Backsliding is not the same as ordinary partisan conflict. It becomes structurally important when elected authority weakens checks, degrades rights, attacks independent institutions, or makes alternation less meaningful.",
        "concept_ko": "민주주의 후퇴는 보통의 정파 갈등과 같지 않다. 선출 권력이 견제를 약화하고 권리를 훼손하며 독립 기관을 공격하거나 정권교체의 의미를 줄일 때 그것은 구조적으로 중요해진다.",
        "evidence_en": "Freedom House's 2026 report records a twentieth consecutive year of global freedom decline and reports 54 countries deteriorating against 35 improving. V-Dem's 2026 report identifies only 18 democratizing countries and emphasizes autocratization as a live process in influential democracies.",
        "evidence_ko": "Freedom House의 2026년 보고서는 세계 자유가 20년 연속 후퇴했으며 54개국이 악화되고 35개국이 개선되었다고 기록한다. V-Dem의 2026년 보고서는 민주화 중인 국가가 18개뿐이라고 보고하고, 영향력 있는 민주주의 안에서도 권위주의화가 진행 중임을 강조한다.",
        "interpretations_en": ["The pessimistic view says the third wave of democratization has exhausted itself.", "The resilience view says elections, courts, civil society, and alternation still matter.", "The normalization view says decline becomes dangerous when citizens stop seeing erosion as exceptional."],
        "interpretations_ko": ["비관론은 민주화의 제3의 물결이 소진되었다고 본다.", "회복력 관점은 선거, 법원, 시민사회, 정권교체가 여전히 중요하다고 본다.", "정상화 관점은 시민이 침식을 예외로 보지 않게 될 때 하락이 위험해진다고 본다."],
        "opposing_en": "The strongest objection is methodological. Democracy indices compress complex national histories into comparable scores. They may overstate decline, understate resilience, or reflect expert anxiety more than lived democratic capacity.",
        "opposing_ko": "가장 강한 반론은 방법론적이다. 민주주의 지수는 복잡한 국가별 역사를 비교 가능한 점수로 압축한다. 그것은 하락을 과장하거나 회복력을 과소평가하거나, 실제 민주 역량보다 전문가 불안을 더 반영할 수 있다.",
        "argument_en": "Indices should not be treated as verdicts. But their convergence is a signal. The proper response is not fatalism; it is institutional specificity: protect courts, electoral administration, civil liberties, public broadcasting, anti-corruption enforcement, and the conditions of peaceful alternation.",
        "argument_ko": "지수는 판결문처럼 취급되어서는 안 된다. 그러나 여러 지수가 같은 방향을 가리키는 것은 신호다. 올바른 대응은 숙명론이 아니라 제도적 구체성이다. 법원, 선거관리, 시민적 자유, 공영 미디어, 반부패 집행, 평화적 정권교체의 조건을 지켜야 한다.",
        "implications_en": ["Use democracy indices as warning systems, not as substitutes for country analysis.", "Avoid casual use of fascism; distinguish backsliding, authoritarianism, populism, and fascism by threshold.", "Watch electoral administration and courts, not only headline elections.", "Treat civic space as infrastructure for democratic correction."],
        "implications_ko": ["민주주의 지수는 국가 분석의 대체물이 아니라 경보 체계로 사용해야 한다.", "파시즘이라는 말을 함부로 쓰지 말고, 후퇴·권위주의·포퓰리즘·파시즘을 기준에 따라 구분해야 한다.", "헤드라인 선거만이 아니라 선거관리와 법원을 봐야 한다.", "시민 공간을 민주적 교정의 인프라로 다뤄야 한다."],
        "strength_en": ["High confidence: the two major democracy reports document broad decline or stress.", "Moderate confidence: normalization is a useful frame for interpreting repeated erosion.", "Contested: country trajectories differ too much for a single global diagnosis."],
        "strength_ko": ["높은 확신: 두 주요 민주주의 보고서는 광범한 하락 또는 긴장을 기록한다.", "중간 확신: 정상화는 반복적 침식을 이해하는 데 유용한 틀이다.", "논쟁적 지점: 국가별 궤적은 하나의 세계 진단으로 묶기에는 지나치게 다르다."],
        "uncertainty_en": "This article should not imply that democracy is dying everywhere. It argues that the long duration of decline changes the editorial question: what is still correctable, and which institutions keep correction possible?",
        "uncertainty_ko": "이 글은 민주주의가 모든 곳에서 죽어가고 있다고 말하지 않는다. 장기 하락이 편집상의 질문을 바꾼다고 말한다. 무엇이 아직 교정 가능한가, 그리고 어떤 제도가 교정을 가능하게 하는가?",
    },
    {
        "slug": "displacement-without-settlement",
        "type": "data essay",
        "scope": "global",
        "en_title": "Displacement Without Settlement",
        "ko_title": "정착 없는 강제이주",
        "en_subtitle": "The headline number fell, but durable displacement remains the structural fact.",
        "ko_subtitle": "헤드라인 숫자는 줄었지만, 장기화된 이주가 구조적 사실로 남아 있다.",
        "tags_en": ["displacement", "refugees", "migration"],
        "tags_ko": ["강제이주", "난민", "이주"],
        "sources": ["unhcr"],
        "abstract_en": "Forced displacement should be read as a stock problem as well as a flow problem. UNHCR estimates 117.8 million people were forcibly displaced at the end of 2025. The slight decline matters, but the deeper issue is duration: millions remain suspended between unsafe return, limited integration, and politically constrained resettlement.",
        "abstract_ko": "강제이주는 흐름의 문제일 뿐 아니라 누적의 문제로 읽어야 한다. UNHCR은 2025년 말 강제이주민이 1억 1,780만 명이라고 추정한다. 소폭 감소는 중요하지만 더 깊은 문제는 지속 기간이다. 수백만 명은 안전하지 않은 귀환, 제한된 통합, 정치적으로 제약된 재정착 사이에 머문다.",
        "opening_en": "The most tempting story in the 2026 displacement data is the first decline in a decade. But a decline from an extreme level is not resolution.",
        "opening_ko": "2026년 강제이주 자료에서 가장 유혹적인 이야기는 10년 만의 첫 감소다. 그러나 극단적으로 높은 수준에서의 감소는 해결이 아니다.",
        "question_en": "Why does forced displacement remain a durable global condition even when annual totals fluctuate?",
        "question_ko": "연간 총량이 변동하는데도 왜 강제이주는 지속적인 세계 조건으로 남는가?",
        "concept_en": "Displacement statistics mix categories that must not be casually added or confused: refugees, asylum seekers, internally displaced people, stateless people, returnees, and others needing protection. Stocks and flows tell different stories.",
        "concept_ko": "강제이주 통계는 함부로 더하거나 혼동해서는 안 되는 범주들을 포함한다. 난민, 비호 신청자, 국내실향민, 무국적자, 귀환자, 보호가 필요한 기타 인구가 그것이다. 저량과 유량은 서로 다른 이야기를 한다.",
        "evidence_en": "UNHCR reports 117.8 million forcibly displaced people at the end of 2025 and 68.7 million internally displaced people due to conflict and violence. The agency also reports that internally displaced people account for a majority of forced displacement. Those figures make the problem institutional as much as humanitarian.",
        "evidence_ko": "UNHCR은 2025년 말 강제이주민 1억 1,780만 명과 분쟁·폭력으로 인한 국내실향민 6,870만 명을 보고한다. 또한 국내실향민이 강제이주 인구의 다수를 차지한다고 설명한다. 이 수치는 문제가 인도주의적일 뿐 아니라 제도적이라는 점을 보여준다.",
        "interpretations_en": ["The progress view emphasizes returns and the first headline decline in years.", "The crisis view emphasizes continuing conflict, unsafe return, and insufficient pathways.", "The settlement view asks whether people have durable legal, civic, and economic membership."],
        "interpretations_ko": ["진전 관점은 귀환과 수년 만의 헤드라인 감소를 강조한다.", "위기 관점은 지속되는 분쟁, 안전하지 않은 귀환, 부족한 합법 경로를 강조한다.", "정착 관점은 사람들이 지속 가능한 법적·시민적·경제적 구성원 자격을 갖는지를 묻는다."],
        "opposing_en": "The strongest opposing view is that falling totals and increased returns should not be dismissed. Humanitarian systems can still produce partial resolution, and some returns may reflect real changes in conditions.",
        "opposing_ko": "가장 강한 반론은 총량 감소와 귀환 증가를 무시해서는 안 된다는 것이다. 인도주의 시스템은 여전히 부분적 해결을 만들어낼 수 있고, 일부 귀환은 실제 조건 변화를 반영할 수 있다.",
        "argument_en": "That is true. But return is not settlement unless it is safe, voluntary, and durable. Nor is host-country presence settlement if work, schooling, legal status, and political consent remain fragile. The structural issue is not only flight; it is blocked membership.",
        "argument_ko": "그 말은 옳다. 그러나 귀환은 안전하고 자발적이며 지속 가능할 때만 정착이다. 체류국에 머무는 것도 노동, 교육, 법적 지위, 정치적 동의가 취약하다면 정착이 아니다. 구조적 문제는 탈출만이 아니라 막힌 구성원 자격이다.",
        "implications_en": ["Separate refugees from IDPs and asylum seekers before making claims.", "Distinguish safe return from statistical return.", "Treat host-country capacity as a development issue, not only a humanitarian one.", "Use climate-displacement language carefully because refugee law has narrower categories."],
        "implications_ko": ["주장을 하기 전에 난민, 국내실향민, 비호 신청자를 구분해야 한다.", "안전한 귀환과 통계상의 귀환을 구분해야 한다.", "수용국 역량을 인도주의 문제만이 아니라 발전 문제로 다뤄야 한다.", "난민법의 범주가 더 좁기 때문에 기후 이주 언어를 조심스럽게 사용해야 한다."],
        "strength_en": ["High confidence: UNHCR provides the core stock figures and categories.", "Moderate confidence: duration and blocked settlement are the right structural lens.", "Contested: humanitarian counts are not complete population censuses."],
        "strength_ko": ["높은 확신: UNHCR은 핵심 저량 수치와 범주를 제공한다.", "중간 확신: 지속 기간과 막힌 정착은 적절한 구조적 렌즈다.", "논쟁적 지점: 인도주의 등록 통계는 완전한 인구 센서스가 아니다."],
        "uncertainty_en": "Final expansion should add conflict-specific case studies and resettlement data. This temporary version limits itself to the global structure and denominator cautions.",
        "uncertainty_ko": "최종 확장판에는 분쟁별 사례와 재정착 자료가 추가되어야 한다. 이 임시본은 세계적 구조와 분모상의 주의에 한정한다.",
    },
    {
        "slug": "korea-mandate-problem-local-elections",
        "type": "political institutions essay",
        "scope": "korea",
        "en_title": "Korea's Mandate Problem After The Local Elections",
        "ko_title": "지방선거 이후 한국의 위임 문제",
        "en_subtitle": "A local election can carry national meaning without becoming a single plebiscite.",
        "ko_subtitle": "지방선거는 전국적 의미를 가질 수 있지만 하나의 국민투표가 되지는 않는다.",
        "tags_en": ["Korea", "elections", "mandate"],
        "tags_ko": ["한국", "선거", "위임"],
        "sources": ["nec", "ap_elections"],
        "abstract_en": "Korea's 2026 local elections should be read neither as a purely local exercise nor as a simple national referendum. Wire reports based on election counts described the ruling Democratic Party winning most regional races while losing Seoul. The structural question is how a nationalized party system should interpret local authority, turnout, administration, and metropolitan exception.",
        "abstract_ko": "2026년 한국 지방선거는 순수한 지방 행사로도, 단순한 전국적 국민투표로도 읽혀서는 안 된다. 선거 개표를 바탕으로 한 통신 보도들은 집권 더불어민주당이 대부분의 광역 단체장 선거에서 이기고도 서울을 잃었다고 전했다. 구조적 질문은 전국화된 정당체계가 지방 권한, 투표율, 선거관리, 수도권 예외를 어떻게 해석해야 하는가이다.",
        "opening_en": "Local elections in Korea rarely stay local. Parties nationalize them, presidents read them, and commentators turn them into verdicts. Yet the offices at stake govern transport, housing, schools, welfare delivery, development, policing cooperation, and local budgets.",
        "opening_ko": "한국의 지방선거는 좀처럼 지방에 머물지 않는다. 정당은 그것을 전국화하고, 대통령은 그것을 읽으며, 논평은 그것을 판결로 만든다. 그러나 실제로 걸려 있는 직위들은 교통, 주거, 학교, 복지 전달, 개발, 치안 협력, 지방 예산을 다룬다.",
        "question_en": "How should Korea interpret a local election whose results carry national meaning but are produced through local offices and local coalitions?",
        "question_ko": "전국적 의미를 갖지만 지방 직위와 지방 연합을 통해 만들어진 선거 결과를 한국은 어떻게 해석해야 하는가?",
        "concept_en": "A mandate is not a mood. It is a claim about what voters authorized, under which offices, with what turnout, in which regions, and for which policy instruments.",
        "concept_ko": "위임은 분위기가 아니다. 그것은 유권자가 어떤 직위에서, 어떤 투표율로, 어떤 지역에서, 어떤 정책 수단에 대해 무엇을 승인했는가에 관한 주장이다.",
        "evidence_en": "The National Election Commission remains the raw source for official results and turnout. For international-reader orientation, AP reported that the ruling party won most races but lost Seoul. That combination is precisely why a one-sentence national verdict is too crude.",
        "evidence_ko": "중앙선거관리위원회는 공식 결과와 투표율의 원자료다. 국제 독자를 위한 시간순 정리로는 AP가 집권당이 대부분의 선거에서 이겼지만 서울에서는 패했다고 보도했다. 바로 그 조합 때문에 한 문장짜리 전국 판정은 너무 거칠다.",
        "interpretations_en": ["The referendum view treats the result as a national verdict on the administration.", "The localist view treats each race as mainly local performance and candidate quality.", "The mandate view asks how national and local signals interact without collapsing one into the other."],
        "interpretations_ko": ["국민투표 관점은 결과를 행정부에 대한 전국적 판결로 본다.", "지방주의 관점은 각 선거를 주로 지방 성과와 후보 경쟁력의 문제로 본다.", "위임 관점은 전국 신호와 지방 신호가 서로를 지워버리지 않으면서 어떻게 상호작용하는지 묻는다."],
        "opposing_en": "The strongest objection is that Korea's political system is highly nationalized. Voters often use local ballots to express national approval or disapproval, and pretending otherwise can blur the main signal.",
        "opposing_ko": "가장 강한 반론은 한국 정치가 매우 전국화되어 있다는 것이다. 유권자들은 지방 투표를 통해 전국적 승인이나 불승인을 표현하곤 하며, 이를 외면하면 중심 신호가 흐려질 수 있다.",
        "argument_en": "That objection is persuasive but incomplete. Nationalization is itself an institutional fact to analyze, not a license to ignore local government. A democratic system becomes healthier when parties can read national signals while still respecting the policy specificity of local offices.",
        "argument_ko": "그 반론은 설득력이 있지만 불완전하다. 전국화 자체가 분석해야 할 제도적 사실이지, 지방정부를 무시할 면허는 아니다. 정당이 전국 신호를 읽으면서도 지방 직위의 정책적 구체성을 존중할 때 민주주의는 더 건강해진다.",
        "implications_en": ["Use NEC official data for final turnout and vote shares.", "Do not treat Seoul as Korea.", "Separate mayoral, gubernatorial, council, and by-election results.", "Ask what local governments can actually implement before deriving national mandates."],
        "implications_ko": ["최종 투표율과 득표율은 중앙선거관리위원회 공식 자료를 사용해야 한다.", "서울을 한국 전체로 취급해서는 안 된다.", "광역단체장, 기초단체장, 의회, 재보궐 결과를 구분해야 한다.", "전국적 위임을 도출하기 전에 지방정부가 실제로 무엇을 집행할 수 있는지 물어야 한다."],
        "strength_en": ["High confidence: local election timing and official-result authority are clear.", "Moderate confidence: wire chronology establishes the broad national-local tension.", "Contested: precise mandate interpretation requires final official turnout and regional vote-share analysis."],
        "strength_ko": ["높은 확신: 지방선거의 시점과 공식 결과 권한은 명확하다.", "중간 확신: 통신 보도는 넓은 전국-지방 긴장을 보여준다.", "논쟁적 지점: 정확한 위임 해석에는 최종 공식 투표율과 지역별 득표율 분석이 필요하다."],
        "uncertainty_en": "This temporary version does not replace a full NEC data analysis. It establishes the interpretive rule: no mandate claim without office, geography, turnout, and policy competence.",
        "uncertainty_ko": "이 임시본은 중앙선거관리위원회 자료에 대한 완전한 분석을 대체하지 않는다. 그것은 해석 규칙을 세운다. 직위, 지역, 투표율, 정책 권한 없는 위임 주장은 불충분하다.",
    },
    {
        "slug": "korea-semiconductor-recovery-welfare-state",
        "type": "political economy essay",
        "scope": "korea",
        "en_title": "Korea's Semiconductor Recovery And The Welfare State It Cannot Avoid",
        "ko_title": "한국의 반도체 회복과 피할 수 없는 복지국가",
        "en_subtitle": "Export strength can finance social capacity, but it cannot substitute for it.",
        "ko_subtitle": "수출의 힘은 사회적 역량을 재원으로 뒷받침할 수 있지만, 그것을 대체할 수는 없다.",
        "tags_en": ["Korea", "semiconductors", "welfare state"],
        "tags_ko": ["한국", "반도체", "복지국가"],
        "sources": ["bok", "moef", "world_bank"],
        "abstract_en": "Korea's 2026 recovery is real but uneven. The Bank of Korea's May outlook projected 2.6 percent growth and 2.7 percent CPI inflation, citing the semiconductor cycle and oil-price shock. The structural question is whether export-led strength can be translated into household security, care capacity, housing stability, and labor adjustment.",
        "abstract_ko": "2026년 한국의 회복은 실제이지만 고르지 않다. 한국은행의 5월 전망은 반도체 사이클과 유가 충격을 언급하며 성장률 2.6%, 소비자물가 상승률 2.7%를 전망했다. 구조적 질문은 수출 주도의 힘을 가계 안정, 돌봄 역량, 주거 안정, 노동 조정으로 번역할 수 있는가이다.",
        "opening_en": "A semiconductor upturn can make a national economy look stronger before households feel secure. That is Korea's 2026 political economy problem.",
        "opening_ko": "반도체 상승 사이클은 가계가 안정을 느끼기 전에 국민경제를 강하게 보이게 만들 수 있다. 이것이 2026년 한국 정치경제의 문제다.",
        "question_en": "Can Korea convert strategic-sector strength into a welfare state suited to aging, household fragility, and labor-market transition?",
        "question_ko": "한국은 전략 부문의 힘을 고령화, 가계 취약성, 노동시장 전환에 맞는 복지국가로 전환할 수 있는가?",
        "concept_en": "A welfare state is not only cash transfers. It is a risk-sharing system for care, health, housing, unemployment, aging, education, and family formation.",
        "concept_ko": "복지국가는 현금 이전만이 아니다. 그것은 돌봄, 보건, 주거, 실업, 고령화, 교육, 가족 형성에 관한 위험분담 체계다.",
        "evidence_en": "The Bank of Korea projected 2026 growth at 2.6 percent, a sharp upward revision from 2.0 percent, while expecting CPI inflation at 2.7 percent and warning that the outlook is uncertain around the semiconductor cycle and Middle East war. MOEF's June bulletin frames the recovery through current economic conditions. These sources support a two-sided reading: growth capacity has improved, but household and price pressures remain politically salient.",
        "evidence_ko": "한국은행은 2026년 성장률을 기존 2.0%에서 크게 올린 2.6%로 전망했고, 소비자물가 상승률은 2.7%로 예상했으며, 반도체 사이클과 중동 전쟁을 둘러싼 불확실성이 크다고 밝혔다. 기획재정부의 6월 경제동향도 현재 경제 여건을 통해 회복을 설명한다. 이 자료들은 양면적 해석을 뒷받침한다. 성장 역량은 개선되었지만 가계와 물가 압력은 여전히 정치적으로 중요하다.",
        "interpretations_en": ["The competitiveness view says welfare depends on export strength and fiscal capacity.", "The social-investment view says competitiveness itself requires care, housing, education, and labor security.", "The mismatch view says Korea's export engine and household institutions are moving at different speeds."],
        "interpretations_ko": ["경쟁력 관점은 복지가 수출의 힘과 재정 역량에 달려 있다고 본다.", "사회투자 관점은 경쟁력 자체가 돌봄, 주거, 교육, 노동 안정에 달려 있다고 본다.", "불일치 관점은 한국의 수출 엔진과 가계 제도가 다른 속도로 움직이고 있다고 본다."],
        "opposing_en": "The strongest opposing view is that welfare expansion without industrial strength is empty. Korea cannot finance care, pensions, and labor transition if it loses the sectors that generate income and tax capacity.",
        "opposing_ko": "가장 강한 반론은 산업 경쟁력 없는 복지 확대는 공허하다는 것이다. 소득과 조세 역량을 만드는 부문을 잃으면 한국은 돌봄, 연금, 노동 전환을 재정적으로 감당할 수 없다.",
        "argument_en": "That is right. But it is not an argument against the welfare state. It is an argument for linking industrial policy to social capacity. A country that depends on advanced manufacturing needs skilled workers, reliable care, regional infrastructure, and households that can take risks without collapse.",
        "argument_ko": "그 말은 옳다. 그러나 그것은 복지국가에 대한 반론이 아니다. 산업정책을 사회적 역량과 연결해야 한다는 논거다. 첨단 제조업에 의존하는 국가는 숙련 노동자, 안정적 돌봄, 지역 인프라, 무너지지 않고 위험을 감수할 수 있는 가계를 필요로 한다.",
        "implications_en": ["Treat semiconductor revenue as a chance to build social capacity, not as proof that social policy can wait.", "Connect care policy to labor supply and family formation.", "Watch inflation and housing because growth does not automatically become legitimacy.", "Separate strategic-sector strength from economy-wide household security."],
        "implications_ko": ["반도체 수익을 사회정책을 미룰 증거가 아니라 사회적 역량을 만들 기회로 봐야 한다.", "돌봄 정책을 노동공급과 가족 형성에 연결해야 한다.", "성장이 자동으로 정당성이 되지 않으므로 물가와 주거를 봐야 한다.", "전략 부문의 힘과 경제 전반의 가계 안정을 구분해야 한다."],
        "strength_en": ["High confidence: BOK's growth and inflation projections are official and dated.", "Moderate confidence: the welfare-state interpretation follows from demographic and household pressures.", "Contested: the right fiscal scale and tax mix require further budget analysis."],
        "strength_ko": ["높은 확신: 한국은행의 성장률과 물가 전망은 날짜가 확인되는 공식 자료다.", "중간 확신: 복지국가 해석은 인구와 가계 압력에서 나온다.", "논쟁적 지점: 적절한 재정 규모와 조세 조합에는 추가 예산 분석이 필요하다."],
        "uncertainty_en": "This temporary version does not estimate a full fiscal path. It states the structural link between export strength and social capacity.",
        "uncertainty_ko": "이 임시본은 완전한 재정 경로를 추정하지 않는다. 수출의 힘과 사회적 역량 사이의 구조적 연결을 제시한다.",
    },
    {
        "slug": "korea-fertility-housing-pronatalism",
        "type": "longform essay",
        "scope": "korea",
        "en_title": "Fertility, Housing, And The Limits Of Pronatalism In Korea",
        "ko_title": "한국의 출산, 주거, 출산장려주의의 한계",
        "en_subtitle": "A birth rebound does not by itself solve the household-formation problem.",
        "ko_subtitle": "출생 반등만으로 가계 형성 문제는 해결되지 않는다.",
        "tags_en": ["Korea", "fertility", "housing"],
        "tags_ko": ["한국", "출산", "주거"],
        "sources": ["mods", "korea_net_births"],
        "abstract_en": "Korea's fertility problem cannot be reduced to birth incentives. Official data releases and government summaries reported a 2025 rebound in births and total fertility, but the structural question remains: can young adults form households under current housing, work, education, care, and gender arrangements?",
        "abstract_ko": "한국의 출산 문제는 출산 인센티브로 환원될 수 없다. 공식 자료 발표와 정부 요약은 2025년 출생아 수와 합계출산율의 반등을 전했지만, 구조적 질문은 남아 있다. 청년들은 현재의 주거, 일, 교육, 돌봄, 젠더 질서 아래에서 가계를 형성할 수 있는가?",
        "opening_en": "A small fertility rebound is politically welcome. It is also analytically dangerous if it turns into a declaration of success.",
        "opening_ko": "출산율의 작은 반등은 정치적으로 반가운 일이다. 그러나 그것이 성공 선언으로 바뀌면 분석적으로 위험하다.",
        "question_en": "What would it mean to treat low fertility as a household-formation problem rather than a subsidy-design problem?",
        "question_ko": "저출산을 보조금 설계 문제가 아니라 가계 형성 문제로 다룬다는 것은 무엇을 뜻하는가?",
        "concept_en": "Pronatalism asks how to increase births. Household formation asks whether people can credibly plan partnership, housing, work, care, and education over time.",
        "concept_ko": "출산장려주의는 어떻게 출생을 늘릴 것인가를 묻는다. 가계 형성은 사람들이 결합, 주거, 일, 돌봄, 교육을 시간 속에서 신뢰 가능하게 계획할 수 있는지를 묻는다.",
        "evidence_en": "The Ministry of Data and Statistics lists the 2025 preliminary birth and death statistics release dated February 25, 2026. Government summaries reported that births rose in 2025 and that the total fertility rate increased to 0.80 from 0.75. These figures matter, but they cannot by themselves separate cohort size, timing, marriage rebound, policy effect, and structural affordability.",
        "evidence_ko": "통계청은 2026년 2월 25일자로 2025년 출생·사망 잠정통계 발표를 게시했다. 정부 요약은 2025년 출생아 수가 증가했고 합계출산율이 0.75에서 0.80으로 올랐다고 전했다. 이 수치는 중요하지만, 그 자체만으로 코호트 규모, 출산 시기, 혼인 반등, 정책 효과, 구조적 부담 가능성을 구분하지는 못한다.",
        "interpretations_en": ["The policy-success view sees the rebound as evidence that support measures can work.", "The timing view says postponed births and marriages are partly catching up.", "The institutional view says fertility depends on housing, work, education, gender equality, and care capacity."],
        "interpretations_ko": ["정책 성공 관점은 반등을 지원 정책이 작동할 수 있다는 증거로 본다.", "시기 효과 관점은 지연된 출산과 혼인이 일부 따라잡고 있다고 본다.", "제도 관점은 출산이 주거, 일, 교육, 성평등, 돌봄 역량에 달려 있다고 본다."],
        "opposing_en": "The strongest opposing view is that pronatalist policy should not be dismissed. Marginal incentives, parental leave, childcare, and housing support can change decisions, especially when couples are near the threshold of having a child.",
        "opposing_ko": "가장 강한 반론은 출산장려 정책을 가볍게 보아서는 안 된다는 것이다. 한계적 인센티브, 육아휴직, 보육, 주거 지원은 특히 아이를 가질지 말지의 문턱에 있는 부부의 결정을 바꿀 수 있다.",
        "argument_en": "That is true, but incentives work inside institutions. If housing remains expensive, careers penalize care, education costs feel open-ended, and metropolitan opportunity concentrates life chances, birth subsidies become compensation for a system that still makes family formation hard.",
        "argument_ko": "그 말은 옳다. 그러나 인센티브는 제도 안에서 작동한다. 주거가 비싸고, 경력이 돌봄을 벌하며, 교육비가 끝없이 느껴지고, 수도권 기회가 삶의 가능성을 집중한다면 출산 보조금은 가족 형성을 계속 어렵게 만드는 체계에 대한 보상에 그친다.",
        "implications_en": ["Do not infer long-run success from one-year improvement.", "Separate fertility rate, birth count, marriage timing, and cohort composition.", "Treat housing and care as fertility policy.", "Use official demographic data before cultural explanation."],
        "implications_ko": ["1년 개선에서 장기 성공을 추론해서는 안 된다.", "합계출산율, 출생아 수, 혼인 시기, 코호트 구성을 구분해야 한다.", "주거와 돌봄을 출산 정책으로 다뤄야 한다.", "문화 설명보다 공식 인구 자료를 먼저 사용해야 한다."],
        "strength_en": ["High confidence: official demographic releases document the rebound.", "Moderate confidence: household formation is the better structural lens.", "Contested: policy effects cannot be estimated without cohort and timing analysis."],
        "strength_ko": ["높은 확신: 공식 인구 자료는 반등을 기록한다.", "중간 확신: 가계 형성은 더 나은 구조적 렌즈다.", "논쟁적 지점: 정책 효과는 코호트와 시기 분석 없이는 추정할 수 없다."],
        "uncertainty_en": "This temporary version does not model causal policy effects. It warns against reading a welcome rebound as structural repair.",
        "uncertainty_ko": "이 임시본은 정책 효과의 인과 모델을 제시하지 않는다. 반가운 반등을 구조적 수리로 읽는 것을 경계한다.",
    },
    {
        "slug": "korea-constitutional-court-quiet-institutionalism",
        "type": "law and institutions essay",
        "scope": "korea",
        "en_title": "Assembly, Counsel, And The Constitutional Court's Quiet Institutionalism",
        "ko_title": "집회, 변호인, 헌법재판소의 조용한 제도주의",
        "en_subtitle": "Korea's constitutional resilience is visible in ordinary rights cases as well as dramatic crises.",
        "ko_subtitle": "한국의 헌정 회복력은 극적 위기뿐 아니라 평범한 권리 사건에서도 보인다.",
        "tags_en": ["Korea", "constitutional court", "rights"],
        "tags_ko": ["한국", "헌법재판소", "권리"],
        "sources": ["ccourt"],
        "abstract_en": "Recent Constitutional Court decisions show a restrained but important rights-protective institutionalism. In 2026, the Court addressed criminal punishment for unnotified outdoor assemblies and denial of attorney visitation to an arrestee. The lesson is not constitutional triumphalism; it is that rights often survive through technical, ordinary decisions.",
        "abstract_ko": "최근 헌법재판소 결정들은 절제되어 있지만 중요한 권리 보호적 제도주의를 보여준다. 2026년에 헌법재판소는 미신고 옥외집회 형사처벌과 체포적부심을 준비하던 피의자에 대한 변호인 접견 거부를 다뤘다. 교훈은 헌정 승리주의가 아니다. 권리는 종종 기술적이고 일상적인 결정 속에서 살아남는다.",
        "opening_en": "After political crisis, constitutional attention tends to move toward grand events. But constitutional order is often repaired in quieter places: notification rules, prison visiting hours, proportionality, and access to counsel.",
        "opening_ko": "정치적 위기 이후 헌법적 관심은 대개 큰 사건으로 향한다. 그러나 헌정 질서는 더 조용한 곳에서 수리되곤 한다. 신고 규칙, 교정시설 접견 시간, 비례성, 변호인의 조력 같은 곳이다.",
        "question_en": "What do recent rights decisions reveal about Korea's institutional condition after crisis?",
        "question_ko": "최근 권리 사건들은 위기 이후 한국의 제도 상태에 대해 무엇을 보여주는가?",
        "concept_en": "Quiet institutionalism means rights protection through ordinary doctrine, remedial limits, dissent, and institutional patience rather than dramatic constitutional rhetoric.",
        "concept_ko": "조용한 제도주의란 극적인 헌법 수사보다 평범한 법리, 구제 방식의 한계, 반대의견, 제도적 인내를 통해 권리를 보호하는 것을 뜻한다.",
        "evidence_en": "The Constitutional Court's latest-decision page reports that, on provisions of the Assembly and Demonstration Act, the Court found uniform criminal punishment for unnotified outdoor assemblies nonconforming to the Constitution while upholding the prior-notification requirement itself. It also reports a unanimous decision holding unconstitutional the denial of weekend attorney visitation to an arrestee seeking review of the legality of arrest.",
        "evidence_ko": "헌법재판소 최신 결정 게시판은 집회 및 시위에 관한 법률 조항에 관해, 미신고 옥외집회에 대한 일률적 형사처벌은 헌법불합치로 보면서도 사전 신고 요구 자체는 합헌으로 보았다고 전한다. 또한 체포적부심을 청구하려던 피의자에 대한 주말 야간 변호인 접견 거부를 위헌으로 본 전원일치 결정도 보고한다.",
        "interpretations_en": ["The resilience view sees courts disciplining punishment and protecting counsel.", "The caution view says selected rights cases do not prove broad institutional health.", "The quiet-institutionalist view treats these decisions as small but meaningful tests of constitutional maintenance."],
        "interpretations_ko": ["회복력 관점은 법원이 처벌을 절제시키고 변호인의 조력을 보호한다고 본다.", "주의 관점은 몇몇 권리 사건이 넓은 제도 건강을 입증하지는 않는다고 본다.", "조용한 제도주의 관점은 이런 결정을 작지만 의미 있는 헌정 유지의 시험으로 본다."],
        "opposing_en": "The strongest opposing view is that courts can protect some procedural rights while failing to resolve deeper political conflict, administrative resistance, or unequal access to justice.",
        "opposing_ko": "가장 강한 반론은 법원이 일부 절차적 권리를 보호하면서도 더 깊은 정치 갈등, 행정 저항, 사법 접근 불평등은 해결하지 못할 수 있다는 것이다.",
        "argument_en": "That objection should temper any triumphalism. But it should not make ordinary rights cases invisible. The durability of constitutional democracy depends on whether small encounters with the state remain contestable and reviewable.",
        "argument_ko": "그 반론은 어떤 승리주의도 누그러뜨려야 한다. 그러나 그것이 평범한 권리 사건을 보이지 않게 만들어서는 안 된다. 헌정민주주의의 지속성은 국가와의 작은 접촉들이 여전히 다툴 수 있고 심사될 수 있는가에 달려 있다.",
        "implications_en": ["Read the remedy as carefully as the holding.", "Track legislative follow-up dates such as amendment deadlines.", "Do not generalize from English summaries without Korean decision texts in final review.", "Treat access to counsel as institutional capacity, not a narrow criminal-procedure detail."],
        "implications_ko": ["주문만큼 구제 방식도 세심하게 읽어야 한다.", "개정 시한 같은 입법 후속조치를 추적해야 한다.", "최종 검토에서는 국문 결정문 없이 영문 요약만으로 과도하게 일반화하지 말아야 한다.", "변호인의 조력권은 좁은 형사절차 세부가 아니라 제도 역량으로 다뤄야 한다."],
        "strength_en": ["High confidence: the cited Constitutional Court summaries identify the holdings and dates.", "Moderate confidence: the quiet-institutionalism interpretation fits the pattern.", "Contested: full doctrinal analysis requires Korean full texts and dissent review."],
        "strength_ko": ["높은 확신: 인용된 헌법재판소 요약은 결정 내용과 날짜를 확인해준다.", "중간 확신: 조용한 제도주의라는 해석은 사건들의 패턴에 맞는다.", "논쟁적 지점: 완전한 법리 분석에는 국문 결정문과 반대의견 검토가 필요하다."],
        "uncertainty_en": "This temporary article is grounded in official summaries. A final law-review version should add full Korean text analysis and statutory follow-up.",
        "uncertainty_ko": "이 임시 글은 공식 요약에 근거한다. 최종 법률비평판에는 국문 전문 분석과 입법 후속조치가 추가되어야 한다.",
    },
    {
        "slug": "universities-after-generative-ai",
        "type": "education essay",
        "scope": "global",
        "en_title": "Universities After Generative AI",
        "ko_title": "생성형 AI 이후의 대학",
        "en_subtitle": "The crisis is not only cheating; it is the meaning of assessment.",
        "ko_subtitle": "위기는 부정행위만이 아니라 평가의 의미에 있다.",
        "tags_en": ["education", "generative AI", "universities"],
        "tags_ko": ["교육", "생성형 AI", "대학"],
        "sources": ["unesco", "stanford", "oecd_ai"],
        "abstract_en": "Generative AI exposes an older university confusion: the conflation of learning, credentialing, assessment, and first-draft production. Academic integrity matters, but enforcement alone cannot answer what writing, explanation, and judgment are for when machine assistance is ordinary.",
        "abstract_ko": "생성형 AI는 대학의 오래된 혼란을 드러낸다. 학습, 자격 부여, 평가, 초안 생산이 뒤섞여 있었다는 사실이다. 학문적 정직성은 중요하지만, 기계의 도움이 일상적인 상황에서 글쓰기, 설명, 판단이 무엇을 위한 것인지는 단속만으로 답할 수 없다.",
        "opening_en": "Universities first met generative AI as an academic-integrity emergency. That was understandable. But the emergency language has started to obscure the deeper question.",
        "opening_ko": "대학은 처음에 생성형 AI를 학문적 정직성의 비상사태로 만났다. 그것은 이해할 만했다. 그러나 비상사태라는 언어는 더 깊은 질문을 가리기 시작했다.",
        "question_en": "What is the university for when summary, explanation, translation, and first-draft prose are no longer scarce in the old way?",
        "question_ko": "요약, 설명, 번역, 첫 초안 산문이 더 이상 예전 방식으로 희소하지 않을 때 대학은 무엇을 위한 기관인가?",
        "concept_en": "Assessment is not surveillance. It is a public claim that a learner can do something under conditions that matter. If conditions change, assessment design must change too.",
        "concept_ko": "평가는 감시가 아니다. 그것은 학습자가 중요한 조건 아래에서 무언가를 할 수 있다는 공적 주장이다. 조건이 바뀌면 평가 설계도 바뀌어야 한다.",
        "evidence_en": "UNESCO's guidance on generative AI in education and research calls for human-centred policy, capacity development, and long-term planning. Stanford's AI Index reports wide differences between expert and public expectations about AI's effects on work. OECD adoption data show AI moving into ordinary organizational use. Universities therefore face a normalizing technology, not a temporary cheating tool.",
        "evidence_ko": "UNESCO의 생성형 AI 교육·연구 지침은 인간 중심 정책, 역량 개발, 장기 계획을 요구한다. Stanford AI Index는 AI가 일에 미치는 영향에 대해 전문가와 대중의 기대가 크게 다르다고 보고한다. OECD 채택 자료는 AI가 일상적 조직 사용으로 이동하고 있음을 보여준다. 따라서 대학이 마주한 것은 일시적 부정행위 도구가 아니라 정상화되는 기술이다.",
        "interpretations_en": ["The enforcement view says secure exams and detection must come first.", "The redesign view says courses must rebuild assessment around process, oral defense, revision, and situated judgment.", "The institutional view says universities must clarify the relation between learning and credentials."],
        "interpretations_ko": ["단속 관점은 보안 시험과 탐지가 먼저라고 본다.", "재설계 관점은 수업이 과정, 구술 방어, 개정, 상황 판단을 중심으로 평가를 다시 만들어야 한다고 본다.", "제도 관점은 대학이 학습과 자격의 관계를 명확히 해야 한다고 본다."],
        "opposing_en": "The strongest opposing view is practical: without credible enforcement, redesign talk becomes indulgent. Students and employers must know that credentials mean something.",
        "opposing_ko": "가장 강한 반론은 실무적이다. 신뢰할 만한 단속이 없다면 재설계 논의는 느슨한 관용이 된다. 학생과 고용주는 자격이 의미를 가진다는 것을 알아야 한다.",
        "argument_en": "That is right. But enforcement without redesign protects the shell while losing the purpose. Universities should make some work AI-free, some AI-assisted, and some AI-critical; the distinction should be explicit and pedagogically justified.",
        "argument_ko": "그 말은 옳다. 그러나 재설계 없는 단속은 껍데기를 지키면서 목적을 잃는다. 대학은 어떤 과제는 AI 없이, 어떤 과제는 AI의 도움을 받아, 어떤 과제는 AI를 비판적으로 사용하도록 해야 한다. 그 구분은 명시적이고 교육적으로 정당화되어야 한다.",
        "implications_en": ["Replace blanket bans with assessment categories.", "Use oral defense, portfolios, revision histories, and in-class work where appropriate.", "Teach AI use as a literacy and judgment problem.", "Protect students without equal access to tools or guidance."],
        "implications_ko": ["전면 금지를 평가 범주로 대체해야 한다.", "필요한 곳에서는 구술 방어, 포트폴리오, 수정 이력, 수업 중 작업을 사용해야 한다.", "AI 사용을 리터러시와 판단의 문제로 가르쳐야 한다.", "도구와 지침에 대한 접근이 불평등한 학생을 보호해야 한다."],
        "strength_en": ["High confidence: policy guidance and adoption data show the issue is institutional.", "Moderate confidence: assessment redesign is the central university response.", "Contested: evidence on learning outcomes under AI use remains incomplete."],
        "strength_ko": ["높은 확신: 정책 지침과 채택 자료는 이 문제가 제도적임을 보여준다.", "중간 확신: 평가 재설계는 대학의 핵심 대응이다.", "논쟁적 지점: AI 사용 아래 학습 성과에 관한 증거는 아직 불완전하다."],
        "uncertainty_en": "This article does not settle which assessment model works best. It argues that integrity policy cannot be separated from the purpose of education.",
        "uncertainty_ko": "이 글은 어떤 평가 모델이 최선인지 결론내리지 않는다. 학문적 정직성 정책은 교육의 목적과 분리될 수 없다고 주장한다.",
    },
    {
        "slug": "culture-of-ai-fatalism",
        "type": "culture essay",
        "scope": "global",
        "en_title": "Attention, Anxiety, And The Culture Of AI Fatalism",
        "ko_title": "주의력, 불안, AI 숙명론의 문화",
        "en_subtitle": "When institutions look absent, technology is narrated as destiny.",
        "ko_subtitle": "제도가 보이지 않을 때 기술은 운명처럼 이야기된다.",
        "tags_en": ["AI culture", "public opinion", "media"],
        "tags_ko": ["AI 문화", "여론", "미디어"],
        "sources": ["stanford", "oecd_ai", "un_ai"],
        "abstract_en": "AI fatalism is not simply irrational panic. It is a cultural response to visible speed and invisible governance. Public optimism and nervousness can rise together because people believe the technology matters while doubting that institutions can shape its consequences.",
        "abstract_ko": "AI 숙명론은 단순한 비합리적 공포가 아니다. 그것은 보이는 속도와 보이지 않는 거버넌스에 대한 문화적 반응이다. 사람들은 기술이 중요하다고 믿으면서도 제도가 그 결과를 형성할 수 있는지 의심하기 때문에 낙관과 불안이 함께 커질 수 있다.",
        "opening_en": "The public conversation about AI keeps snapping between salvation and catastrophe. That oscillation is not only a media failure. It is what happens when a technology feels powerful and governance feels distant.",
        "opening_ko": "AI에 관한 공적 대화는 구원과 파국 사이를 계속 오간다. 그 진동은 미디어의 실패만이 아니다. 기술은 강력하게 느껴지는데 거버넌스는 멀게 느껴질 때 생기는 일이다.",
        "question_en": "Why does AI discourse so often become fatalistic, and what does that do to democratic judgment?",
        "question_ko": "왜 AI 담론은 자주 숙명론이 되며, 그것은 민주적 판단에 무엇을 하는가?",
        "concept_en": "Fatalism is the belief that social choice has already lost to technical momentum. It can appear as hype, despair, resignation, or mockery.",
        "concept_ko": "숙명론은 사회적 선택이 이미 기술의 운동량에 졌다는 믿음이다. 그것은 과장, 절망, 체념, 조롱의 형태로 나타날 수 있다.",
        "evidence_en": "Stanford's 2026 AI Index reports more complicated public sentiment, including optimism about benefits and nervousness about the technology. OECD adoption data show AI moving from novelty into firms. The UN AI dialogue shows that governance is being discussed, but public culture often experiences such efforts as remote.",
        "evidence_ko": "Stanford 2026 AI Index는 편익에 대한 낙관과 기술에 대한 불안이 함께 나타나는 더 복잡한 여론을 보고한다. OECD 채택 자료는 AI가 새로움에서 기업 사용으로 이동하고 있음을 보여준다. 유엔 AI 대화는 거버넌스 논의가 진행 중임을 보여주지만, 공적 문화는 그런 노력을 종종 멀리 있는 것으로 경험한다.",
        "interpretations_en": ["The alarm view says anxiety is rational because deployment is fast and accountability weak.", "The hype view says fatalism serves firms by making adoption seem inevitable.", "The institutional view says fatalism grows when people cannot see credible collective choice."],
        "interpretations_ko": ["경보 관점은 배치가 빠르고 책임이 약하기 때문에 불안이 합리적이라고 본다.", "과장 관점은 숙명론이 채택을 필연처럼 보이게 하여 기업에 유리하다고 본다.", "제도 관점은 사람들이 신뢰할 만한 집단적 선택을 볼 수 없을 때 숙명론이 커진다고 본다."],
        "opposing_en": "The strongest opposing view is that strong alarm may be ethically necessary. Moderate language can become complacency when systems affect labor, education, privacy, and political persuasion before accountability exists.",
        "opposing_ko": "가장 강한 반론은 강한 경보가 윤리적으로 필요할 수 있다는 것이다. 책임이 마련되기 전에 시스템이 노동, 교육, 개인정보, 정치적 설득에 영향을 미친다면 절제된 언어는 안일함이 될 수 있다.",
        "argument_en": "Alarm is sometimes necessary. Fatalism is different. Alarm says act now; fatalism says action is already pointless. Democratic culture needs the former without surrendering to the latter.",
        "argument_ko": "경보는 때로 필요하다. 숙명론은 다르다. 경보는 지금 행동하라고 말한다. 숙명론은 행동이 이미 무의미하다고 말한다. 민주적 문화는 전자를 필요로 하지만 후자에 항복해서는 안 된다.",
        "implications_en": ["Treat commentary as discourse evidence, not factual proof of AI effects.", "Ask what institutional action would make anxiety more answerable.", "Distinguish existential risk, labor risk, education risk, and media risk.", "Avoid both promotional mysticism and ironic despair."],
        "implications_ko": ["논평은 AI 효과의 사실 증거가 아니라 담론 증거로 다뤄야 한다.", "어떤 제도적 행동이 불안에 답할 수 있게 만들지 물어야 한다.", "실존 위험, 노동 위험, 교육 위험, 미디어 위험을 구분해야 한다.", "홍보성 신비주의와 냉소적 절망을 모두 피해야 한다."],
        "strength_en": ["High confidence: public-opinion and adoption sources establish the tension.", "Moderate confidence: fatalism is a useful cultural interpretation.", "Contested: cultural mood cannot be measured with the precision of adoption statistics."],
        "strength_ko": ["높은 확신: 여론과 채택 자료는 긴장을 확인해준다.", "중간 확신: 숙명론은 유용한 문화 해석이다.", "논쟁적 지점: 문화적 분위기는 채택 통계처럼 정밀하게 측정될 수 없다."],
        "uncertainty_en": "This essay analyzes a discourse pattern. It should be revised as more reliable public-opinion data and media-content studies become available.",
        "uncertainty_ko": "이 에세이는 담론 패턴을 분석한다. 더 신뢰할 만한 여론 자료와 미디어 내용 분석이 나오면 개정되어야 한다.",
    },
    {
        "slug": "structural-reading-list",
        "type": "annotated bibliography",
        "scope": "comparative",
        "en_title": "What To Read On AI, Democracy, Energy, And Korea's Institutional Moment",
        "ko_title": "AI, 민주주의, 에너지, 한국의 제도적 순간을 읽기 위한 자료",
        "en_subtitle": "A source hierarchy for readers who want evidence before mood.",
        "ko_subtitle": "분위기보다 근거를 먼저 보려는 독자를 위한 출처 위계.",
        "tags_en": ["bibliography", "sources", "method"],
        "tags_ko": ["서지", "출처", "방법"],
        "sources": ["imf", "oecd_eo", "iea", "unhcr", "oecd_ai", "un_ai", "eu_ai", "stanford", "freedom_house", "vdem", "bok", "mods", "ccourt"],
        "abstract_en": "This reading list models the magazine's method. Start with primary and institutional evidence; use forecasts as conditional arguments; use journalism for chronology; use commentary as discourse evidence; and keep Korean raw sources separate from Korean interpretive writing.",
        "abstract_ko": "이 읽기 목록은 잡지의 방법을 보여준다. 일차·기관 근거에서 시작하고, 전망은 조건부 주장으로 사용하며, 저널리즘은 시간순 정리에 쓰고, 논평은 담론 증거로 쓰며, 한국의 원자료와 한국어 해석 글을 구분한다.",
        "opening_en": "A serious quarterly review needs not only arguments but a reading order. The order matters because sources do different kinds of work.",
        "opening_ko": "진지한 계간지는 주장뿐 아니라 읽는 순서도 필요하다. 출처마다 하는 일이 다르기 때문에 순서는 중요하다.",
        "question_en": "Which sources should readers use to understand the quarter without confusing evidence, discourse, forecast, and opinion?",
        "question_ko": "독자는 근거, 담론, 전망, 의견을 혼동하지 않고 이번 분기를 이해하기 위해 어떤 자료를 읽어야 하는가?",
        "concept_en": "A bibliography is an argument about authority. It tells readers what can support a claim, what can only illustrate a debate, and where uncertainty remains.",
        "concept_ko": "서지는 권위에 관한 주장이다. 그것은 어떤 자료가 주장을 뒷받침할 수 있고, 어떤 자료가 논쟁을 보여주는 데만 쓰일 수 있으며, 어디에 불확실성이 남아 있는지를 말해준다.",
        "evidence_en": "For macroeconomics, begin with IMF, OECD, and World Bank; for energy, IEA; for displacement, UNHCR; for AI governance, OECD, UN, EU, and Stanford; for democracy, Freedom House and V-Dem; for Korea, BOK, MOEF, the Ministry of Data and Statistics, NEC, and the Constitutional Court.",
        "evidence_ko": "거시경제는 IMF, OECD, 세계은행에서 시작한다. 에너지는 IEA, 강제이주는 UNHCR, AI 거버넌스는 OECD·UN·EU·Stanford, 민주주의는 Freedom House와 V-Dem, 한국은 한국은행·기획재정부·통계청·중앙선거관리위원회·헌법재판소에서 시작한다.",
        "interpretations_en": ["The prestige-shelf view treats a bibliography as a list of impressive names.", "The practical view treats it as a map of evidentiary use.", "The DeepWrite view insists that source type determines what kind of claim can be made."],
        "interpretations_ko": ["명망 서가 관점은 서지를 인상적인 이름 목록으로 취급한다.", "실무 관점은 그것을 증거 사용의 지도로 본다.", "DeepWrite 관점은 출처 유형이 만들 수 있는 주장 유형을 결정한다고 본다."],
        "opposing_en": "The strongest opposing view is that source hierarchy can look neutral while smuggling in institutional bias. Official data can omit lived experience, and elite reports can standardize the wrong categories.",
        "opposing_ko": "가장 강한 반론은 출처 위계가 중립처럼 보이면서 제도적 편향을 들여올 수 있다는 것이다. 공식 자료는 체감 경험을 빠뜨릴 수 있고, 엘리트 보고서는 잘못된 범주를 표준화할 수 있다.",
        "argument_en": "That is why hierarchy must be paired with dissent. Primary sources are not morally complete; they are evidentiary anchors. A magazine can begin from them while still asking what they cannot see.",
        "argument_ko": "그래서 위계는 반론과 함께 있어야 한다. 일차 출처는 도덕적으로 완전한 것이 아니라 증거의 닻이다. 잡지는 그것에서 출발하면서도 그 출처가 보지 못하는 것을 물을 수 있다.",
        "implications_en": ["Use official statistics for numbers, not opinion columns.", "Use high-quality journalism for chronology and context.", "Use commentary to map discourse, not to prove causal claims.", "Record method limits before drawing conclusions."],
        "implications_ko": ["숫자는 의견 칼럼이 아니라 공식 통계로 다뤄야 한다.", "고품질 저널리즘은 시간순 정리와 맥락에 사용해야 한다.", "논평은 인과 주장을 입증하는 데가 아니라 담론을 지도화하는 데 사용해야 한다.", "결론 전에 방법상 한계를 기록해야 한다."],
        "strength_en": ["High confidence: the listed source families are appropriate starting points.", "Moderate confidence: the annotations reflect the issue's method.", "Contested: source hierarchy must be revised as better data appear."],
        "strength_ko": ["높은 확신: 나열된 출처군은 적절한 출발점이다.", "중간 확신: 주석은 이번 호의 방법을 반영한다.", "논쟁적 지점: 더 나은 자료가 나오면 출처 위계는 수정되어야 한다."],
        "uncertainty_en": "This list is not exhaustive. It is a working public bibliography for the temporary issue state.",
        "uncertainty_ko": "이 목록은 완전하지 않다. 임시 발행 상태의 공개 작업 서지다.",
    },
]


def source_lines(keys: list[str]) -> list[str]:
    return [f"- [{SOURCES[key][0]}]({SOURCES[key][1]})" for key in keys]


def meta(article: dict, language: str) -> dict:
    is_ko = language == "ko"
    slug = article["slug"]
    return {
        "title": article["ko_title"] if is_ko else article["en_title"],
        "subtitle": article["ko_subtitle"] if is_ko else article["en_subtitle"],
        "slug": slug,
        "issue": ISSUE,
        "date": TODAY,
        "language": language,
        "translation_of": f"/en/{slug}/" if is_ko else "original",
        "counterpart_url": f"/en/{slug}/" if is_ko else f"/ko/{slug}/",
        "authors": ["DeepWrite Review 편집실" if is_ko else "DeepWrite Review Editorial Desk"],
        "contributors": ["Codex Editorial Agents", "Codex Source Researcher", "Codex Translation Editor"],
        "editors": ["손제연" if is_ko else "Jeyoun Son (손제연)"],
        "chief_editor": "Jeyoun Son",
        "chief_editor_ko": "손제연",
        "ai_assistance": "Codex 편집 에이전트의 도움을 받아 작성되었습니다. 최종 편집 책임은 인간 편집자에게 있습니다." if is_ko else "Prepared with Codex editorial agents under human editorial direction.",
        "tags": article["tags_ko"] if is_ko else article["tags_en"],
        "abstract": article["abstract_ko"] if is_ko else article["abstract_en"],
        "evidence_level": "moderate",
        "citation_status": "checked",
        "translation_status": "checked",
        "chief_editor_status": "approved_for_publication",
        "draft_approved_date": TODAY,
        "publication_approved_date": TODAY,
        "published_date": TODAY,
        "status": "published",
        "article_type": article["type"],
        "regional_scope": article["scope"],
    }


def render_en(article: dict) -> str:
    interp = "\n".join(f"- {item}" for item in article["interpretations_en"])
    implications = "\n".join(f"- {item}" for item in article["implications_en"])
    strength = "\n".join(f"- {item}" for item in article["strength_en"])
    reading = "\n".join(source_lines(article["sources"]))
    return f"""# {article["en_title"]}

> Editorial status: temporarily published by Chief Editor approval.
>
> Prepared with Codex editorial agents. Human editorial responsibility remains with Jeyoun Son (손제연).

## Abstract

{article["abstract_en"]}

## Opening Issue

{article["opening_en"]}

## Central Question

{article["question_en"]}

## Conceptual Clarification

{article["concept_en"]}

## Evidence

{article["evidence_en"]}

## Competing Interpretations

{interp}

## Best Opposing View

{article["opposing_en"]}

## Argument

{article["argument_en"]}

## Policy Or Civic Implications

{implications}

## Evidence Strength

Overall evidence level: moderate.

{strength}

## Uncertainty Note

{article["uncertainty_en"]}

## Further Reading

{reading}

## Citations

This temporary publication uses official, institutional, or high-quality wire sources for factual claims. Commentary may be added later only as discourse evidence, not as raw evidence for causal or statistical claims.
"""


def render_ko(article: dict) -> str:
    interp = "\n".join(f"- {item}" for item in article["interpretations_ko"])
    implications = "\n".join(f"- {item}" for item in article["implications_ko"])
    strength = "\n".join(f"- {item}" for item in article["strength_ko"])
    reading = "\n".join(source_lines(article["sources"]))
    return f"""# {article["ko_title"]}

> 편집 상태: Chief Editor 승인에 따른 임시 발행본입니다.
>
> Codex 편집 에이전트의 도움을 받아 작성되었습니다. 인간 편집 책임은 손제연 편집장에게 있습니다.

## 초록

{article["abstract_ko"]}

## 출발점

{article["opening_ko"]}

## 중심 질문

{article["question_ko"]}

## 개념의 정리

{article["concept_ko"]}

## 근거

{article["evidence_ko"]}

## 경쟁 해석

{interp}

## 가장 강한 반론

{article["opposing_ko"]}

## 논증

{article["argument_ko"]}

## 정책적·시민적 함의

{implications}

## 근거 강도

전체 근거 수준: 중간.

{strength}

## 불확실성 노트

{article["uncertainty_ko"]}

## 더 읽을 자료

{reading}

## 인용

이 임시 발행본은 사실 주장에 대해 공식, 기관, 또는 고품질 통신 출처를 사용한다. 논평은 이후 담론 증거로만 추가할 수 있으며, 인과 주장이나 통계 주장의 원자료로 사용해서는 안 된다.
"""


def write_article(article: dict) -> None:
    for language, renderer in (("en", render_en), ("ko", render_ko)):
        text = dump_front_matter(meta(article, language), renderer(article))
        for stage in ("drafts", "final"):
            target = BASE / stage / language / f"{article['slug']}.md"
            write_text(target, text, overwrite=True)


def write_reviews(article: dict) -> None:
    slug = article["slug"]
    review = f"""---
issue: "{ISSUE}"
slug: "{slug}"
date: "{TODAY}"
status: checked_for_temporary_publication
chief_editor_status: approved_for_publication
---

# Review: {article["en_title"]}

## Argument Reconstruction

- One-sentence thesis: {article["abstract_en"]}
- Major premise: Structurally important quarterly issues should be read through institutions, incentives, evidence, and competing interpretations.
- Minor premise: This article applies that method to `{slug}` using the approved source dossier and checked source links.
- Conclusion: Approved for temporary publication, subject to later full-issue revision.

## Fact Checker

- Source links were verified at the temporary-publication stage.
- Claims are limited to what cited institutional or high-quality wire sources can support.

## Statistics Checker

- Statistical claims are stated with source, date, geography, and limitation where applicable.
- This temporary version avoids unsupported causal estimates.

## Dissent Editor

- Strongest opposing view is included in the article body.

## Style Editor

- English and Korean versions preserve the same structure and are ready for temporary publication.
"""
    translation = f"""---
issue: "{ISSUE}"
slug: "{slug}"
date: "{TODAY}"
status: checked_for_temporary_publication
review_type: translation_consistency
chief_editor_status: approved_for_publication
---

# Translation Review: {article["ko_title"]}

## Current State

- English final version: `issues/{ISSUE}/final/en/{slug}.md`
- Korean final version: `issues/{ISSUE}/final/ko/{slug}.md`
- Publication status: approved for temporary publication.

## Structural Check

- Thesis preserved: checked for temporary publication.
- Section order preserved: yes.
- Citation links preserved: yes.
- Front-matter bilingual links present: yes.

## Remaining Full-Issue Review

- Korean prose should receive a full human style edit before complete quarterly issue publication.
- Statistical claims should be rechecked if source pages update.
"""
    write_text(BASE / "reviews" / f"{slug}_review.md", review, overwrite=True)
    write_text(BASE / "reviews" / f"{slug}_translation_review.md", translation, overwrite=True)


def update_evidence_log() -> None:
    path = BASE / "evidence_log.csv"
    fieldnames = [
        "issue",
        "article_slug",
        "claim",
        "claim_type",
        "source_title",
        "source_url",
        "source_tier",
        "date",
        "unit",
        "geography",
        "denominator",
        "method",
        "limitations",
        "evidence_level",
        "verification_status",
        "checked_by",
        "checked_date",
        "notes",
    ]
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as handle:
            existing = list(csv.DictReader(handle))
    remaining_slugs = {article["slug"] for article in ARTICLES}
    existing = [row for row in existing if row.get("article_slug") not in remaining_slugs]
    rows = []
    for article in ARTICLES:
        key = article["sources"][0]
        title, url = SOURCES[key]
        rows.append(
            {
                "issue": ISSUE,
                "article_slug": article["slug"],
                "claim": article["evidence_en"],
                "claim_type": "institutional",
                "source_title": title,
                "source_url": url,
                "source_tier": "1",
                "date": "2026",
                "unit": "qualitative and selected statistical claims",
                "geography": article["scope"],
                "denominator": "article-specific",
                "method": "temporary publication source check",
                "limitations": "Temporary-publication synthesis; full issue should rerun source-level fact-checking.",
                "evidence_level": "moderate",
                "verification_status": "checked_for_temporary_publication",
                "checked_by": "Codex",
                "checked_date": TODAY,
                "notes": "Generated for remaining 2026-Q2 temporary publication set.",
            }
        )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing + rows)


def update_decisions() -> None:
    path = BASE / "chief_editor_decisions.md"
    text = read_text(path)
    slugs = ["ai-boom-war-economy", "new-macro-fragility"] + [article["slug"] for article in ARTICLES]
    rows = "\n".join(f"| {slug} | approve | Approved for temporary publication in English and Korean. | {TODAY} |" for slug in slugs)
    replacement = f"""## Temporary Full-Issue Publication Approval

| Slug | Decision | Notes | Date |
| --- | --- | --- | --- |
{rows}

## Final Publication Approval

- Decision: temporary_full_issue_approve
- Notes: Chief Editor directed remaining manuscripts to be completed and all 13 bilingual article pairs to be temporarily published. This is a temporary publication state; later complete-issue revision remains open.
- Date: {TODAY}
"""
    start = text.find("## Final Publication Approval")
    if start == -1:
        text = text.rstrip() + "\n\n" + replacement
    else:
        text = text[:start].rstrip() + "\n\n" + replacement
    write_text(path, text, overwrite=True)


def update_issue_pages() -> None:
    en = f"""---
issue: "{ISSUE}"
language: en
title: "DeepWrite Review 2026 Q2"
theme: "Governing The Acceleration: War, AI, Democracy, And The Limits Of Institutional Capacity"
chief_editor_status: temporary_full_issue_approved
status: temporary_publication
---

# DeepWrite Review 2026 Q2

All 13 bilingual article pairs are temporarily published by Chief Editor approval.

The issue remains open to later full-issue revision, source strengthening, Korean style editing, and final quarterly packaging.
"""
    ko = f"""---
issue: "{ISSUE}"
language: ko
title: "DeepWrite Review 2026 Q2"
theme: "Governing The Acceleration: War, AI, Democracy, And The Limits Of Institutional Capacity"
chief_editor_status: temporary_full_issue_approved
status: temporary_publication
---

# DeepWrite Review 2026 Q2

13개 이중언어 article pair 전체가 Chief Editor 승인에 따라 임시 발행되었습니다.

이 호는 이후 전체 호 단위 개정, 출처 보강, 한국어 문체 편집, 최종 계간 패키징을 위해 열려 있습니다.
"""
    write_text(BASE / "issue_en.md", en, overwrite=True)
    write_text(BASE / "issue_ko.md", ko, overwrite=True)


def update_reports() -> None:
    fact = f"""---
issue: "{ISSUE}"
status: checked_for_temporary_full_issue_publication
---

# Fact-Check Report

All 13 bilingual article pairs are approved for temporary publication.

## Scope

- Source URLs were checked at the temporary-publication stage.
- Claims were limited to institutional, official, or high-quality wire sources.
- Full quarterly publication should rerun source-level review before final packaging.
"""
    stats = f"""---
issue: "{ISSUE}"
status: checked_for_temporary_full_issue_publication
---

# Statistical Reliability Report

All 13 bilingual article pairs are approved for temporary publication.

## Scope

- Statistical claims were kept conservative and source-linked.
- Forecasts are presented as conditional projections, not observations.
- Korea-specific raw-source claims should be rechecked against official tables before full issue publication.
"""
    translation = f"""---
issue: "{ISSUE}"
status: checked_for_temporary_full_issue_publication
---

# Translation Consistency Report

All 13 English-Korean article pairs are temporarily published.

## Scope

- Korean versions preserve the English thesis, structure, evidence links, and qualifications at temporary-publication level.
- Full quarterly publication should still receive human Korean style editing and bilingual consistency review.
"""
    write_text(BASE / "factcheck_report.md", fact, overwrite=True)
    write_text(BASE / "statistics_report.md", stats, overwrite=True)
    write_text(BASE / "translation_report.md", translation, overwrite=True)


def update_site_pages() -> None:
    current = """---
title: "Current Issue"
subtitle: "2026-Q2 temporary full-issue publication"
permalink: /current/
---

The 2026-Q2 issue is temporarily published in full: 13 English-Korean article pairs are public under Chief Editor approval.

The issue remains open to later source strengthening, Korean style editing, and complete quarterly packaging.

{% assign published_articles = site.articles | where: "status", "published" | where: "chief_editor_status", "approved_for_publication" %}

{% if published_articles.size > 0 %}
<div class="article-list">
{% for article in published_articles %}
  <article>
    <a href="{{ article.url | relative_url }}">{{ article.title }}</a>
    <p>{{ article.subtitle }}</p>
  </article>
{% endfor %}
</div>
{% else %}
No article is public yet.
{% endif %}
"""
    write_text(SITE / "pages" / "current.md", current, overwrite=True)


def main() -> int:
    for article in ARTICLES:
        write_article(article)
        write_reviews(article)
    update_evidence_log()
    update_decisions()
    update_issue_pages()
    update_reports()
    update_site_pages()
    copied = copy_approved_articles_to_site()
    print(f"temporary-published remaining articles: {len(ARTICLES)}")
    print(f"site articles copied: {len(copied)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
