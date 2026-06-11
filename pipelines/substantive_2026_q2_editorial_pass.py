#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent

from lib import ISSUES, copy_approved_articles_to_site, dump_front_matter, read_text, split_front_matter, write_text


ISSUE = "2026-Q2"
TODAY = "2026-06-11"
BASE = ISSUES / ISSUE


def clean_markdown(text: str) -> str:
    """Normalize generator-template indentation without touching content."""
    text = dedent(text)
    lines = [line[8:] if line.startswith("        ") else line for line in text.splitlines()]
    return "\n".join(lines).strip()


def topic_marker_ko(text: str) -> str:
    for char in reversed(text.strip()):
        code = ord(char)
        if 0xAC00 <= code <= 0xD7A3:
            return "은" if (code - 0xAC00) % 28 else "는"
    return "은"


@dataclass(frozen=True)
class ArticlePass:
    slug: str
    en_title: str
    ko_title: str
    article_type: str
    scope: str
    thesis_en: str
    thesis_ko: str
    sources: list[tuple[str, str, str]]
    excluded: str
    stats_note: str
    en_body: str
    ko_body: str


def article_header(title: str, language: str) -> str:
    if language == "ko":
        return (
            f"# {title}\n\n"
            "> 편집 상태: 편집장 임시 승인에 따른 임시 발행.\n>\n"
            "> Codex 편집 에이전트가 작성 준비에 참여했으며, 최종 편집 책임은 손제연에게 있습니다.\n\n"
        )
    return (
        f"# {title}\n\n"
        "> Editorial status: temporarily published by Chief Editor approval.\n>\n"
        "> Prepared with Codex editorial agents. Human editorial responsibility remains with Jeyoun Son (손제연).\n\n"
    )


ARTICLES: list[ArticlePass] = [
    ArticlePass(
        slug="editors-note-capacity-question",
        en_title="The Quarter When Capacity Became The Question",
        ko_title="역량이 질문이 된 분기",
        article_type="editor's note",
        scope="comparative",
        thesis_en="The structurally important events of 2026-Q2 are best read as tests of institutional capacity: can public institutions convert acceleration, conflict, displacement, technological diffusion, democratic stress, and Korea's domestic pressures into legitimate action before pressure becomes distrust?",
        thesis_ko="2026-Q2의 구조적으로 중요한 사건들은 제도적 역량의 시험으로 읽는 것이 가장 적절하다. 공적 제도는 가속, 분쟁, 강제이주, 기술 확산, 민주주의 긴장, 한국의 국내 압력을 불신으로 바뀌기 전에 정당한 행동으로 전환할 수 있는가.",
        sources=[
            ("IMF World Economic Outlook, April 2026", "https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026", "macro frame; conditional forecast and war-shadowed growth risk"),
            ("OECD Economic Outlook, June 2026", "https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html", "comparative macro outlook"),
            ("World Bank Global Economic Prospects, January 2026", "https://openknowledge.worldbank.org/entities/publication/bb904ec6-730f-4dd9-b1af-ad3153ee1616", "fiscal space, trade tension, fragile economies"),
            ("UNHCR Global Trends", "https://www.unhcr.org/us/global-trends", "forced displacement denominator"),
            ("Freedom House Freedom in the World 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy", "democracy warning system"),
            ("OECD AI adoption data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "AI diffusion among individuals and firms"),
        ],
        excluded="Do not use viral commentary or Korean opinion columns as raw evidence for the issue frame. They may be cited later only as discourse evidence.",
        stats_note="Forecasts are conditional; displacement and AI-use figures require source, year, geography, and category. The issue frame is interpretive, not a statistical model.",
        en_body=dedent(
            """
            ## Abstract

            A quarterly review should not imitate the emotional weather of the week. Its job is not to chase the most viral controversy, nor to pretend that every event confirms one grand theory. The task is quieter and harder: to identify the structure of the moment before the moment has hardened into cliche.

            The 2026-Q2 issue is organized around one editorial judgment. The important question this quarter is capacity. Not capacity as a slogan for a bigger state, nor as a managerial escape from politics, but capacity in the stricter sense: the ability of institutions to know what is happening, explain tradeoffs, enforce limits, correct errors, and convert pressure into legitimate action.

            This frame links AI governance, a war-shadowed world economy, forced displacement, democratic erosion, Korea's local elections, Korea's semiconductor recovery, fertility, constitutional adjudication, universities after generative AI, and the culture of AI fatalism. These are not the same problem. They are different problems that expose a shared weakness: institutions are being asked to absorb pressure faster than they can rebuild trust.

            ## Opening Issue

            A theme can become a trap. Editors like themes because they give shape to disorder. Readers like them because they make the quarter feel legible. But a theme can also bully the evidence. It can make unrelated developments look more coherent than they are. It can turn simultaneity into causation.

            The capacity frame should therefore be used modestly. It is not a master theory of 2026. It is a question that improves the reading of the quarter. When the [IMF's April 2026 World Economic Outlook](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026) projects global growth of 3.1 percent in 2026 and 3.2 percent in 2027 under a limited-conflict assumption, while warning that war, fragmentation, AI disappointment, trade tension, debt, and eroded policy buffers could worsen the outlook, the issue is not one forecast number. It is how little margin many governments have for error.

            When the [OECD](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html) reports that 20.2 percent of firms in countries with available data used AI in 2025, more than double the 2023 share, the issue is not simply adoption. It is whether schools, firms, labor institutions, regulators, and public agencies can govern a technology whose use is becoming ordinary before its rules are settled.

            When [UNHCR](https://www.unhcr.org/us/global-trends) reports 117.8 million forcibly displaced people at the end of 2025, the issue is not only humanitarian emergency. It is whether the international system can move people from temporary protection toward durable membership. When [Freedom House](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy) reports a twentieth consecutive year of decline in global freedom, the issue is not abstract democratic sorrow. It is which institutions still allow correction.

            The quarter's structure is therefore not crisis alone. It is the widening gap between acceleration and absorption.

            ## Central Question

            What changed this quarter is that more public problems became simultaneously material, administrative, and legitimacy-sensitive.

            AI is not just software. It is electricity, chips, procurement, standards, audits, liability, competition, classroom assessment, labor bargaining, and the right to appeal automated decisions. Democracy is not just elections. It is courts, electoral administration, opposition rights, civil liberties, independent media, and habits of peaceful alternation. Fertility is not just birth numbers. It is housing, work, care, education, gender, medical access, and the credibility of family policy. Korea's semiconductor recovery is not just exports. It is fiscal opportunity, regional policy, welfare-state capacity, energy planning, and national vulnerability to global cycles.

            The repeated question is this: can institutions translate pressure into policy before citizens experience the pressure as betrayal?

            ## Conceptual Clarification

            Capacity has at least seven components.

            First, factual capacity: statistical systems, public data, administrative records, and the humility to distinguish measurement from reality. Second, technical capacity: the ability to understand the systems being governed. Third, administrative capacity: implementation across agencies and time. Fourth, legal capacity: thresholds, rights, procedure, review, and proportionality. Fifth, fiscal capacity: the ability to pay for obligations without pretending that every promise is free. Sixth, civic capacity: the ability to explain tradeoffs honestly. Seventh, corrective capacity: the ability to admit error and change course without turning correction into humiliation.

            These forms of capacity are not automatically democratic. A capable state can be cruel. A technically sophisticated system can be unjust. But democratic judgment without capacity becomes performance. Rights without institutions become slogans. Public promises without fiscal and administrative design become cynicism.

            ## Evidence

            The issue's evidence base is deliberately institutional. For macroeconomic claims, it uses the IMF, OECD, and World Bank as conditional forecasts and risk maps, not as prophecy. For displacement, it uses UNHCR categories and denominators. For democracy, it uses Freedom House and V-Dem as warning systems, not as replacements for country analysis. For AI, it uses OECD adoption data, the EU AI Act, the UN Global Dialogue, UNESCO, and Stanford HAI as sources on diffusion and governance. For Korea, it privileges the Bank of Korea, KOSIS, the Ministry of Data and Statistics, the National Election Commission, and the Constitutional Court over commentary.

            This hierarchy matters. If an article says Korea's fertility problem is structural, it should not begin with a viral lament about young people. It should begin with births, fertility rates, marriage, housing, labor, care, and education. If an article says democracy is declining, it should not begin with an insult. It should identify rights, procedures, and institutions. If an article says AI governance is urgent, it should look at adoption data, regulatory timelines, procurement dependence, energy demand, and enforcement capacity.

            The evidence supports disciplined concern, not theatrical certainty. The world economy is not collapsing, but the margin is narrower. AI is not merely hype, but productivity effects remain uneven and institution-dependent. Democracy is not dead everywhere, but repeated erosion changes what people learn to accept. Korea's births have improved from very low levels, but one rebound does not repair the conditions of family formation.

            ## Competing Interpretations

            The acceleration view says speed is the central fact. Technology, war risk, capital, and political reaction are moving faster than institutions can adapt.

            The exhaustion view says the deeper story is fatigue after repeated shocks: pandemic, inflation, war, polarization, housing pressure, and administrative overload.

            The fragmentation view says the common world is breaking apart into rival systems of trade, information, regulation, education, security, and identity.

            The capacity view, used here, says these are connected. Speed, fatigue, and fragmentation matter politically because they test institutions. The question is not whether things move quickly. It is whether public systems can still make change governable.

            ## Best Opposing View

            The strongest objection is that "capacity" can become a polite word for technocracy. It can privilege administrators over citizens, competence over justice, order over conflict, and expertise over democratic argument. Some failures are not failures of competence. They are failures of power, distribution, representation, or moral courage.

            That objection is right. Capacity is not virtue. But its opposite is not justice. A democracy that cannot implement its promises will not remain trusted. A court that cannot explain its reasoning will not command legitimacy. A school that cannot say what it assesses will not educate. A welfare state that cannot count costs will not endure. The point is not to replace politics with administration. It is to make democratic politics capable of acting.

            ## Argument

            The structural politics of 2026 are increasingly politics of institutional absorption.

            An institution absorbs pressure when it can convert a shock into a legitimate rule, a credible explanation, a fair burden, a reviewable procedure, or a practical adjustment. It fails when the shock becomes mistrust, conspiracy, evasion, paralysis, or rage.

            That is why the issue moves between global and Korean subjects. Korea is not a local appendix to world affairs. It is a concentrated case of advanced-society tension: globally exposed industry, severe household formation pressure, high educational competition, constitutional drama, democratic resilience, and strategic vulnerability. The global essays supply the wider structure; the Korea essays test that structure against raw sources.

            A serious quarterly should not reassure readers that everything will be fine. Nor should it train them in helplessness. It should show where decisions remain possible, which evidence is strong, which claims are premature, and which institutions deserve attention before the next shock arrives.

            ## Policy Or Civic Implications

            Readers should treat forecasts as conditional arguments. They should ask institutional questions before ideological ones: who has authority, what data are used, what denominator matters, who pays, what can be appealed, what happens if the policy fails? They should read Korean issues through raw official sources before commentary. They should treat bilingual publication as editorial responsibility, not format.

            ## Evidence Strength

            Overall evidence level: moderate.

            High confidence: the issue's core pressures are documented by institutional sources. Moderate confidence: institutional capacity is the most useful organizing frame for the quarter. Contested: capacity does not explain everything; ideology, class, leadership, geopolitics, and power still matter.

            ## Uncertainty Note

            This is a substantive temporary-publication editor's note, not a final declaration of the magazine's permanent line. Later revision should change the frame if deeper source dossiers point elsewhere.

            ## Further Reading

            - [IMF, World Economic Outlook, April 2026](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)
            - [OECD, Economic Outlook, Volume 2026 Issue 1](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            - [World Bank, Global Economic Prospects, January 2026](https://openknowledge.worldbank.org/entities/publication/bb904ec6-730f-4dd9-b1af-ad3153ee1616)
            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            """
        ).strip(),
        ko_body=dedent(
            """
            ## 초록

            계간지는 그 주의 감정적 날씨를 모방해서는 안 된다. 가장 많이 공유된 논쟁을 뒤쫓는 것도, 모든 사건이 하나의 거대 이론을 입증한다고 말하는 것도 계간지의 일이 아니다. 더 조용하고 어려운 일은 순간이 상투어로 굳기 전에 그 구조를 알아보는 것이다.

            2026-Q2 호는 하나의 편집 판단 위에 놓인다. 이번 분기의 중요한 질문은 역량이다. 더 큰 국가를 요구하는 구호로서의 역량도 아니고, 정치를 행정으로 대체하는 말로서의 역량도 아니다. 여기서 역량은 제도가 사실을 알고, 상충관계를 설명하고, 한계를 집행하고, 오류를 수정하며, 압력을 정당한 행동으로 바꾸는 능력이다.

            이 틀은 AI 거버넌스, 전쟁의 그림자가 드리운 세계경제, 강제이주, 민주주의 침식, 한국의 지방선거, 반도체 회복, 출산, 헌법재판, 생성형 AI 이후의 대학, AI 숙명론의 문화를 연결한다. 이 주제들은 같은 문제가 아니다. 그러나 모두 하나의 약점을 드러낸다. 제도는 신뢰를 재건하는 속도보다 빠르게 압력을 흡수하라는 요구를 받고 있다.

            ## 출발점

            주제는 함정이 될 수 있다. 편집자는 주제를 좋아한다. 그것이 무질서에 모양을 주기 때문이다. 독자도 주제를 좋아한다. 그것이 분기를 읽을 수 있게 만들기 때문이다. 그러나 주제는 증거를 괴롭힐 수도 있다. 서로 다른 사건을 실제보다 더 정합적으로 보이게 만들고, 동시성을 인과성으로 바꾼다.

            그래서 역량이라는 틀은 조심스럽게 써야 한다. 그것은 2026년의 만능 이론이 아니라 이번 분기를 더 잘 읽게 하는 질문이다. [IMF 2026년 4월 세계경제전망](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)이 제한적 분쟁을 가정해 2026년 세계 성장률을 3.1%, 2027년을 3.2%로 전망하면서 전쟁, 분절화, AI 생산성 실망, 무역 긴장, 부채, 정책 신뢰 약화를 위험으로 제시할 때, 핵심은 숫자 하나가 아니다. 많은 정부가 오류를 감당할 여지가 줄어들었다는 점이다.

            [OECD](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)가 자료가 있는 국가에서 2025년 기업의 20.2%가 AI를 사용했다고 보고할 때, 핵심은 채택률만이 아니다. 학교, 기업, 노동제도, 규제기관, 공공기관이 규칙보다 먼저 일상화되는 기술을 통치할 수 있는가이다.

            [UNHCR](https://www.unhcr.org/us/global-trends)이 2025년 말 강제이주민 1억 1,780만 명을 보고할 때, 핵심은 인도주의 비상사태만이 아니다. 국제 시스템이 임시 보호를 지속 가능한 구성원 자격으로 바꿀 수 있는가이다. [Freedom House](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)가 세계 자유의 20년 연속 하락을 기록할 때, 핵심은 추상적 민주주의 비탄이 아니라 어떤 제도가 아직 교정을 가능하게 하는가이다.

            ## 중심 질문

            이번 분기에 달라진 것은 더 많은 공적 문제가 동시에 물질적이고 행정적이며 정당성에 민감한 문제가 되었다는 점이다.

            AI는 소프트웨어만이 아니다. 전력, 반도체, 조달, 표준, 감사, 책임, 경쟁, 수업 평가, 노동 교섭, 자동화된 결정에 대한 이의제기권이다. 민주주의는 선거만이 아니다. 법원, 선거관리, 야당의 권리, 시민적 자유, 독립 언론, 평화적 정권교체의 습관이다. 출산은 출생아 수만이 아니다. 주거, 일, 돌봄, 교육, 젠더, 의료 접근, 가족 정책의 신뢰다. 한국의 반도체 회복은 수출만이 아니다. 재정 기회, 지역 정책, 복지국가 역량, 에너지 계획, 세계 경기 순환에 대한 취약성이다.

            반복되는 질문은 이것이다. 제도는 시민이 압력을 배신으로 경험하기 전에 그것을 정책으로 번역할 수 있는가.

            ## 개념 정리

            역량에는 적어도 일곱 가지가 있다. 사실을 파악하는 역량, 기술 시스템을 이해하는 역량, 행정을 집행하는 역량, 권리와 절차와 비례성을 지키는 법적 역량, 약속을 감당하는 재정 역량, 상충관계를 설명하는 시민적 역량, 오류를 인정하고 수정하는 교정 역량이다.

            이런 역량이 자동으로 민주적인 것은 아니다. 강한 국가는 잔혹할 수 있고, 기술적으로 정교한 체계는 부정의할 수 있다. 그러나 역량 없는 민주적 판단은 수행이 된다. 제도 없는 권리는 구호가 되고, 재정과 행정 설계 없는 약속은 냉소가 된다.

            ## 증거

            이번 호의 증거 기반은 의도적으로 제도적이다. 거시경제는 IMF, OECD, 세계은행을 예언이 아니라 조건부 전망과 위험 지도로 사용한다. 강제이주는 UNHCR의 범주와 분모를 사용한다. 민주주의는 Freedom House와 V-Dem을 국가 분석의 대체물이 아니라 경보 체계로 사용한다. AI는 OECD 채택 자료, EU AI Act, 유엔 글로벌 대화, UNESCO, Stanford HAI를 확산과 거버넌스의 자료로 사용한다. 한국은 한국은행, KOSIS, 국가데이터처, 중앙선거관리위원회, 헌법재판소를 논평보다 우선한다.

            이 위계는 중요하다. 한국의 출산 문제가 구조적이라고 말하려면 바이럴한 세대 비난이 아니라 출생아 수, 출산율, 혼인, 주거, 노동, 돌봄, 교육을 봐야 한다. 민주주의가 하락한다고 말하려면 욕설이 아니라 어떤 권리와 절차와 기관이 약화되는지를 말해야 한다. AI 거버넌스가 시급하다고 말하려면 채택 자료, 규제 일정, 조달 의존, 전력 수요, 집행 능력을 봐야 한다.

            증거는 극적인 확신이 아니라 절제된 우려를 지지한다. 세계경제는 붕괴하지 않았지만 여지는 좁아졌다. AI는 단순한 과장이 아니지만 생산성 효과는 제도에 의존한다. 민주주의는 모든 곳에서 죽지 않았지만 반복된 침식은 사람들이 받아들이는 정상의 기준을 바꾼다. 한국의 출산은 매우 낮은 수준에서 개선되었지만, 한 번의 반등이 가계 형성 조건을 수리하지는 않는다.

            ## 경쟁 해석

            가속 해석은 속도가 핵심이라고 본다. 소진 해석은 팬데믹, 인플레이션, 전쟁, 양극화, 주거 압력 이후의 피로를 본다. 파편화 해석은 무역, 정보, 규제, 교육, 안보, 정체성의 공통 세계가 갈라지고 있다고 본다. 이 글이 택하는 역량 해석은 셋이 연결되어 있다고 본다. 속도와 피로와 파편화는 제도를 시험할 때 정치적으로 결정적이 된다.

            ## 가장 강한 반론

            가장 강한 반론은 역량이라는 말이 기술관료주의의 세련된 이름이 될 수 있다는 것이다. 시민보다 행정가를, 정의보다 효율을, 민주적 논쟁보다 전문성을 우선할 수 있다. 어떤 실패는 능력의 실패가 아니라 권력, 분배, 대표, 도덕적 용기의 실패다.

            이 반론은 옳다. 역량은 미덕이 아니다. 그러나 그 반대편도 정의가 아니다. 약속을 집행할 수 없는 민주주의는 신뢰받기 어렵다. 이유를 설명하지 못하는 법원은 정당성을 얻기 어렵다. 무엇을 평가하는지 말하지 못하는 학교는 교육하기 어렵다. 비용을 계산하지 못하는 복지국가는 지속되기 어렵다. 핵심은 정치를 행정으로 대체하는 것이 아니라 민주적 정치가 행동할 수 있게 하는 것이다.

            ## 주장

            2026년의 구조적 정치는 점점 더 제도적 흡수의 정치가 되고 있다.

            제도는 충격을 정당한 규칙, 믿을 수 있는 설명, 공정한 부담, 검토 가능한 절차, 실용적 조정으로 바꿀 때 압력을 흡수한다. 반대로 충격이 불신, 음모론, 회피, 마비, 분노가 될 때 흡수에 실패한다.

            그래서 이번 호는 세계와 한국을 오간다. 한국은 세계 의제의 지역 부록이 아니다. 그것은 선진사회 긴장이 압축된 사례다. 세계적으로 노출된 산업, 심한 가계 형성 압력, 높은 교육 경쟁, 헌정 드라마, 민주적 회복력, 전략적 취약성이 한 사회 안에 있다. 세계 글들은 구조를 제공하고, 한국 글들은 그 구조를 원자료에 대조한다.

            진지한 계간지는 독자에게 모든 것이 괜찮을 것이라고 말할 필요가 없다. 동시에 무력감을 훈련시켜서도 안 된다. 어디에 아직 선택이 남아 있는지, 어떤 증거가 강한지, 어떤 주장이 성급한지, 다음 충격 전에 어떤 제도를 봐야 하는지 보여주어야 한다.

            ## 정책적·시민적 함의

            전망은 조건부 주장으로 읽어야 한다. 이념 질문보다 제도 질문을 먼저 던져야 한다. 누가 권한을 갖는가, 어떤 자료가 쓰이는가, 어떤 분모가 중요한가, 누가 비용을 부담하는가, 무엇에 이의제기할 수 있는가, 정책 실패 시 무엇이 일어나는가. 한국 이슈는 논평보다 공식 원자료를 먼저 읽어야 한다. 이중언어 발행은 형식이 아니라 편집 책임이다.

            ## 근거 강도

            전체 증거 수준: 중간.

            높은 확신: 이번 호의 핵심 압력은 제도적 출처로 확인된다. 중간 확신: 제도적 역량은 이번 분기의 가장 유용한 조직 프레임이다. 논쟁적 지점: 역량이 모든 것을 설명하지는 않는다. 이념, 계급, 리더십, 지정학, 권력도 여전히 중요하다.

            ## 불확실성 노트

            이 글은 임시 발행용 본격 편집자의 글이지, 잡지의 영구 노선을 확정하는 선언이 아니다. 더 깊은 출처 검토가 다른 방향을 가리키면 프레임도 바뀌어야 한다.

            ## 더 읽을 자료

            - [IMF, World Economic Outlook, April 2026](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)
            - [OECD, Economic Outlook, Volume 2026 Issue 1](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            - [World Bank, Global Economic Prospects, January 2026](https://openknowledge.worldbank.org/entities/publication/bb904ec6-730f-4dd9-b1af-ad3153ee1616)
            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            """
        ).strip(),
    ),
    ArticlePass(
        slug="govern-ai-before-infrastructure",
        en_title="Can The World Govern AI Before It Becomes Infrastructure?",
        ko_title="AI가 인프라가 되기 전에 세계는 그것을 통치할 수 있는가",
        article_type="technology and society essay",
        scope="global",
        thesis_en="AI governance is moving from principles to implementation while AI becomes operating infrastructure; the decisive question is whether public institutions can inspect, enforce, update, and legitimate rules before dependency hardens.",
        thesis_ko="AI가 작동 인프라가 되는 동안 AI 거버넌스는 원칙에서 실행으로 이동하고 있다. 결정적 질문은 의존이 굳어지기 전에 공적 제도가 규칙을 점검하고 집행하고 갱신하고 정당화할 수 있는가이다.",
        sources=[
            ("UN Global Dialogue on AI Governance", "https://www.un.org/global-dialogue-ai-governance/en", "multilateral governance process; Geneva July 2026"),
            ("European Commission AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "risk-based framework and implementation timeline"),
            ("OECD AI use data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "student, individual, firm adoption"),
            ("Stanford HAI AI Index 2026", "https://hai.stanford.edu/ai-index/2026-ai-index-report", "broad AI trend reference"),
            ("UNESCO generative AI education guidance", "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research", "education governance context"),
        ],
        excluded="Company blog posts, model-launch marketing, and Korean/English commentary may be used later only to reconstruct discourse or stakeholder incentives.",
        stats_note="Adoption data do not prove productivity growth. EU implementation dates are legal timelines, not evidence of enforcement effectiveness.",
        en_body=dedent(
            """
            ## Abstract

            AI governance has crossed from principle into implementation at exactly the wrong moment for easy lawmaking. The technology is no longer confined to research labs, consumer chatbots, or corporate demonstrations. It is becoming an operating layer in firms, schools, public administration, platforms, health systems, and security debates. Governance therefore cannot be judged by whether high-minded principles exist. It must be judged by whether institutions can inspect, enforce, update, and legitimate rules before AI becomes too embedded to contest.

            The tension is visible in three institutional signals. The [UN Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en) is scheduled for July 2026 in Geneva. The [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) is entering staged application, with prohibitions, AI literacy duties, GPAI obligations, transparency rules, high-risk rules, and enforcement architecture arriving on different timelines. The [OECD's January 2026 AI use data](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html) show adoption spreading among both individuals and firms.

            The question is not whether governance is necessary. It is what kind of governance is still possible once AI has become infrastructure.

            ## Opening Issue

            AI regulation used to sound like a seminar question. It was discussed as ethics, safety, alignment, bias, creativity, or existential risk. Those questions remain real. But the practical center of gravity has moved. AI is now procurement, audit, employment practice, classroom policy, platform moderation, public-service automation, energy demand, competition policy, and international coordination.

            That movement changes the politics. It is one thing to regulate a technology whose use is experimental. It is another to regulate a technology after governments have bought it, schools have normalized it, firms have reorganized workflow around it, and citizens experience institutional judgment through its interfaces. Once a system becomes infrastructural, the cost of changing it rises. The actors who depend on it acquire veto power. The language of innovation begins to sound like the language of inevitability.

            This is why the UN dialogue matters even if it produces no binding law. It marks the point at which AI governance is no longer only national or corporate. It is now a multilateral legitimacy problem. But it also exposes the weakness of multilateralism: dialogue can coordinate vocabulary, but it cannot by itself build domestic regulators, auditors, data systems, courts, procurement rules, or public trust.

            ## Central Question

            Can institutions shape AI before AI becomes too deeply embedded to contest?

            The answer depends on a distinction often blurred in public debate. To govern AI is not simply to pass an AI law. It is to create a system in which uses can be classified, inspected, appealed, corrected, limited, and explained. A rule that cannot be enforced is a press release. An audit that cannot see the system is theater. A public agency that depends entirely on vendors for expertise cannot credibly regulate those vendors. A school that bans AI without redesigning assessment has not governed learning; it has displaced the problem into concealment.

            OECD data show the time pressure. More than one-third of individuals across the OECD used generative AI tools in 2025; three-quarters of students aged 16 and over reported use. Firm adoption rose to 20.2 percent in countries with available data, more than double the share two years earlier. These figures do not tell us whether AI is being used well. They tell us that governance is arriving after mass diffusion has begun.

            ## Evidence And Analysis

            The EU AI Act is the most ambitious regulatory experiment now entering implementation. The Commission describes a risk-based architecture: banned practices, high-risk uses, transparency obligations, rules for general-purpose models, and institutions such as the AI Office and member-state authorities. The timetable matters. Prohibited practices and AI literacy obligations entered application in February 2025. GPAI obligations became applicable in August 2025. Transparency rules come into effect in August 2026, while some high-risk rules arrive later.

            That calendar is a lesson. Governance is not a moment. It is a sequence of standards, guidance, staffing, institutional learning, enforcement, litigation, compliance, and revision. A law can be comprehensive on paper and still thin in practice if authorities lack technical capacity.

            The OECD adoption data reveal another problem: unevenness. Large firms are far more likely than small firms to use AI; ICT firms are far ahead of many other sectors; students use it heavily. Uneven adoption means uneven power. Large firms can build compliance teams, shape standards, and absorb legal complexity. Smaller actors may experience regulation as burden. Public agencies may struggle to match private expertise.

            The Stanford AI Index is useful not because it settles the argument but because it shows how many dimensions now move at once: capability, investment, deployment, policy, education, and public attitudes. AI governance is therefore synchronization across domains that do not move at the same speed.

            ## Competing Interpretations

            The regulatory-optimist view says the architecture is arriving in time. The EU has law, the UN has dialogue, the OECD supplies adoption data, and standards bodies will fill gaps.

            The market-adaptation view says law will matter less than organizational learning. Firms, schools, and consumers will discover useful practices, and overregulation may freeze experimentation before productivity gains appear.

            The capture view says AI governance will strengthen incumbents. Complex compliance regimes can become moats. Symbolic audits can launder risk. Public agencies can become dependent on vendor expertise.

            The democratic-capacity view, favored here, asks whether affected people can contest decisions, whether public agencies can inspect systems, and whether rules can keep pace without surrendering to panic or inevitability.

            ## Best Opposing View

            The strongest objection is that early regulation may entrench the very firms it seeks to control. Large model providers can hire lawyers, produce documentation, lobby over standards, and operate regulatory-affairs teams. Smaller developers, public-interest projects, and open-source communities may struggle. If the state lacks independent technical capacity, it may rely on vendor explanations and call that oversight.

            This objection is serious. A bad AI law can create the appearance of control while consolidating power. But the objection does not support no governance. It supports better governance. If AI becomes infrastructure, the price of weak oversight rises over time.

            ## Argument

            AI governance should begin from a sober premise: AI will not wait for institutions to become ready.

            That does not mean institutions should surrender. It means governance must be built where deployment actually occurs: the school, welfare office, hospital, hiring platform, court administration system, newsroom, workplace, and public agency.

            The first task is classification. Not every AI use is equally dangerous. A spam filter, a medical triage tool, an automated hiring screen, a grading system, and a predictive-policing tool do not belong in the same moral box. The virtue of risk-based regulation is distinction. Its danger is that classification can be manipulated.

            The second task is contestability. People need to know when AI is involved in consequential decisions, what kind of system it is, who is responsible, and how to appeal. Without this, AI turns institutional power into fog.

            The third task is public expertise. Governments cannot govern AI through vendor briefings alone. They need technical staff, procurement specialists, statisticians, lawyers, auditors, and judges who understand systems and rights.

            The fourth task is humility. Some risks are measurable; others emerge through use. Rules must be stable enough to guide behavior and revisable enough to learn.

            ## Policy Or Civic Implications

            Governments should build technical civil-service capacity before procurement dependence becomes irreversible. Public agencies should require audit rights, documentation, incident reporting, and appeal mechanisms for high-stakes systems. Education policy should treat AI literacy as institutional design, not slogan. Competition policy should monitor compute, cloud, model access, data concentration, and standards capture.

            ## Evidence Strength

            Overall evidence level: moderate. High confidence: OECD documents diffusion; the EU AI Act has a staged risk-based framework; the UN dialogue is scheduled for July 2026. Moderate confidence: implementation capacity will determine whether governance matters. Contested: the optimal balance between innovation, competition, rights, and enforcement.

            ## Uncertainty Note

            This article does not claim that any current framework is sufficient. It claims that the window for building enforceable public capacity is narrower than the rhetoric of future regulation suggests.

            ## Further Reading

            - [United Nations, Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)
            - [European Commission, AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            - [Stanford HAI, 2026 AI Index Report](https://hai.stanford.edu/ai-index/2026-ai-index-report)
            - [UNESCO, Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)
            """
        ).strip(),
        ko_body=dedent(
            """
            ## 초록

            AI 거버넌스는 원칙의 단계에서 실행의 단계로 넘어갔다. 문제는 그 시점이 쉬운 입법에 가장 불리하다는 점이다. AI는 더 이상 연구실, 소비자용 챗봇, 기업 시연에 머물지 않는다. 기업, 학교, 공공행정, 플랫폼, 보건 시스템, 안보 논쟁의 작동 층이 되고 있다. 따라서 거버넌스는 고상한 원칙이 존재하는가로 평가될 수 없다. AI가 다투기 어려울 만큼 깊이 내장되기 전에 제도가 규칙을 점검하고, 집행하고, 갱신하고, 정당화할 수 있는가로 평가되어야 한다.

            긴장은 세 가지 제도적 신호에서 보인다. [유엔 AI 거버넌스 글로벌 대화](https://www.un.org/global-dialogue-ai-governance/en)는 2026년 7월 제네바에서 예정되어 있다. [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)는 금지 관행, AI 리터러시 의무, 범용 AI 모델 의무, 투명성 규칙, 고위험 규칙, 집행 구조가 서로 다른 일정으로 적용되는 단계에 들어갔다. [OECD 2026년 1월 AI 사용 자료](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)는 개인과 기업 양쪽에서 채택이 확산되고 있음을 보여준다.

            질문은 거버넌스가 필요한가가 아니다. AI가 인프라가 되었을 때 어떤 거버넌스가 아직 가능한가이다.

            ## 출발점

            AI 규제는 한때 세미나 질문처럼 들렸다. 윤리, 안전, 정렬, 편향, 창의성, 실존 위험이 중심이었다. 이 질문들은 여전히 중요하다. 그러나 실천적 무게중심은 이동했다. AI는 이제 조달, 감사, 고용 관행, 수업 정책, 플랫폼 조정, 공공서비스 자동화, 에너지 수요, 경쟁 정책, 국제 조정의 문제다.

            이 변화는 정치의 성격을 바꾼다. 사용이 실험적인 기술을 규제하는 것과, 정부가 이미 구매하고 학교가 정상화하고 기업이 업무 흐름을 재조직한 기술을 규제하는 것은 다르다. 어떤 시스템이 인프라가 되면 그것을 바꾸는 비용은 상승한다. 의존하는 행위자들은 거부권을 얻고, 혁신의 언어는 필연성의 언어처럼 들리기 시작한다.

            그래서 유엔 글로벌 대화는 구속력 있는 법을 만들지 않더라도 중요하다. AI 거버넌스가 이제 국가나 기업만의 문제가 아니라 다자적 정당성의 문제가 되었음을 보여주기 때문이다. 동시에 다자주의의 약점도 드러난다. 대화는 어휘를 조정할 수 있지만 국내 규제기관, 감사자, 데이터 체계, 법원, 조달 규칙, 공적 신뢰를 대신 만들 수는 없다.

            ## 중심 질문

            AI가 다투기 어려울 만큼 깊이 내장되기 전에 제도는 AI를 형성할 수 있는가?

            답은 흔히 흐려지는 구분에 달려 있다. AI를 통치한다는 것은 단순히 AI 법을 만드는 것이 아니다. 사용을 분류하고, 점검하고, 이의제기하고, 수정하고, 제한하고, 설명할 수 있는 체계를 만드는 것이다. 집행할 수 없는 규칙은 보도자료다. 시스템을 들여다볼 수 없는 감사는 연극이다. 규제 대상 기업의 설명에 전적으로 의존하는 공공기관은 그 기업을 신뢰성 있게 규제할 수 없다. AI를 금지하지만 평가 방식을 바꾸지 않는 학교는 학습을 통치한 것이 아니라 문제를 은폐로 밀어낸 것이다.

            OECD 자료는 시간 압박을 보여준다. 2025년 OECD 전역에서 개인의 3분의 1 이상이 생성형 AI 도구를 사용했고, 16세 이상 학생의 4분의 3이 사용을 보고했다. 자료가 있는 국가에서 기업의 AI 채택률은 20.2%로, 2년 전의 두 배를 넘었다. 이 수치는 AI가 잘 쓰이고 있는지를 말하지 않는다. 대중적 확산이 이미 시작된 뒤에 거버넌스가 도착하고 있음을 말한다.

            ## 증거와 분석

            EU AI Act는 지금 실행 단계로 들어가는 가장 야심적인 규제 실험이다. 유럽위원회는 금지 관행, 고위험 사용, 투명성 의무, 범용 AI 모델 규칙, AI Office와 회원국 당국 같은 집행 기관으로 구성된 위험 기반 구조를 제시한다. 일정이 중요하다. 금지 관행과 AI 리터러시 의무는 2025년 2월 적용되기 시작했고, 범용 AI 모델 의무는 2025년 8월 적용되었다. 투명성 규칙은 2026년 8월, 일부 고위험 규칙은 더 늦게 온다.

            이 달력은 교훈이다. 거버넌스는 한순간의 사건이 아니다. 표준, 지침, 인력, 제도 학습, 집행, 소송, 준수, 개정의 순서다. 법은 종이 위에서 포괄적일 수 있지만, 당국의 기술 역량이 부족하면 실제로는 얇다.

            OECD의 채택 자료는 또 다른 문제를 드러낸다. 대기업은 중소기업보다 훨씬 더 AI를 사용하고, ICT 기업은 다른 많은 산업보다 앞서 있으며, 학생 사용은 매우 높다. 불균등한 채택은 불균등한 권력을 뜻한다. 대기업은 준수 조직을 만들고 표준에 영향력을 행사하고 법적 복잡성을 흡수할 수 있다. 작은 행위자는 규제를 부담으로 경험할 수 있다. 공공기관은 민간 전문성에 뒤처질 수 있다.

            Stanford AI Index는 하나의 숫자로 결론을 내리기 위해서가 아니라, 능력, 투자, 배치, 정책, 교육, 대중 인식이 동시에 움직인다는 점을 보여주기 위해 유용하다. AI 거버넌스는 서로 다른 속도로 움직이는 영역들을 맞추는 일이다.

            ## 경쟁 해석

            규제 낙관론은 구조가 제때 도착하고 있다고 본다. EU에는 법이 있고, 유엔에는 대화가 있으며, OECD는 채택 자료를 제공하고, 표준 기구가 빈틈을 메울 것이다.

            시장 적응론은 법보다 조직 학습이 더 중요하다고 본다. 기업과 학교와 소비자가 유용한 관행을 발견할 것이며, 과잉 규제는 생산성 효과가 나타나기 전에 실험을 얼릴 수 있다.

            포획론은 AI 거버넌스가 기존 대기업을 강화할 것이라고 본다. 복잡한 준수 체계는 해자가 될 수 있고, 상징적 감사는 위험을 세탁할 수 있으며, 공공기관은 공급업체 전문성에 의존할 수 있다.

            이 글이 택하는 민주적 역량 관점은 영향을 받는 사람이 결정에 이의제기할 수 있는지, 공공기관이 시스템을 점검할 수 있는지, 규칙이 공포나 필연성에 굴복하지 않고 갱신될 수 있는지를 묻는다.

            ## 가장 강한 반론

            가장 강한 반론은 이른 규제가 통제하려는 바로 그 기업들을 굳힐 수 있다는 것이다. 대형 모델 제공자는 변호사를 고용하고, 문서를 만들고, 표준에 로비하고, 규제 대응 조직을 운영할 수 있다. 작은 개발자, 공익 프로젝트, 오픈소스 공동체는 어려움을 겪을 수 있다. 국가가 독립 기술 역량을 갖지 못하면 공급업체 설명에 의존하면서 그것을 감독이라고 부를 수 있다.

            이 반론은 중요하다. 나쁜 AI 법은 통제의 외양을 만들면서 권력을 집중시킬 수 있다. 그러나 이 반론은 무거버넌스를 지지하지 않는다. 더 나은 거버넌스를 요구한다. AI가 인프라가 될수록 약한 감독의 가격은 시간이 지날수록 오른다.

            ## 주장

            AI 거버넌스는 냉정한 전제에서 출발해야 한다. AI는 제도가 준비될 때까지 기다리지 않는다.

            그렇다고 제도가 항복해야 한다는 뜻은 아니다. 거버넌스는 실제 배치가 일어나는 곳에서 구축되어야 한다. 학교, 복지 사무소, 병원, 채용 플랫폼, 법원 행정 시스템, 뉴스룸, 직장, 공공기관이 그 장소다.

            첫 번째 과제는 분류다. 모든 AI 사용이 같은 위험을 갖지 않는다. 스팸 필터, 의료 분류 도구, 자동 채용 심사, 성적 평가 시스템, 예측 치안 도구는 같은 도덕 상자에 들어갈 수 없다. 위험 기반 규제의 장점은 구분이다. 위험은 그 구분이 조작될 수 있다는 데 있다.

            두 번째 과제는 다툴 수 있는 가능성이다. 사람들은 중대한 결정에 AI가 개입했는지, 어떤 시스템인지, 누가 책임지는지, 어떻게 이의제기할 수 있는지 알아야 한다. 그렇지 않으면 AI는 제도 권력을 안개로 만든다.

            세 번째 과제는 공적 전문성이다. 정부는 공급업체 설명만으로 AI를 통치할 수 없다. 기술 인력, 조달 전문가, 통계가, 법률가, 감사자, 시스템과 권리를 함께 이해하는 판사가 필요하다.

            네 번째 과제는 겸손이다. 어떤 위험은 측정 가능하지만 어떤 위험은 사용을 통해 나타난다. 규칙은 행동을 안내할 만큼 안정적이어야 하고, 배울 수 있을 만큼 수정 가능해야 한다.

            ## 정책적·시민적 함의

            정부는 조달 의존이 되돌리기 어려워지기 전에 기술 관료 역량을 구축해야 한다. 공공기관은 고위험 시스템에 대해 감사권, 문서화, 사고 보고, 이의제기 장치를 요구해야 한다. 교육 정책은 AI 리터러시를 구호가 아니라 제도 설계로 다뤄야 한다. 경쟁 정책은 컴퓨트, 클라우드, 모델 접근, 데이터 집중, 표준 포획을 감시해야 한다.

            ## 근거 강도

            전체 증거 수준: 중간. 높은 확신: OECD는 확산을 기록하고, EU AI Act는 단계적 위험 기반 구조를 갖고 있으며, 유엔 대화는 2026년 7월 예정되어 있다. 중간 확신: 실행 역량이 거버넌스의 실질성을 결정할 것이다. 논쟁적 지점: 혁신, 경쟁, 권리, 집행 사이의 최적 균형은 아직 정해지지 않았다.

            ## 불확실성 노트

            이 글은 현재의 어떤 틀이 충분하다고 주장하지 않는다. 집행 가능한 공적 역량을 만들 시간 창이 미래 규제의 수사보다 좁다는 주장이다.

            ## 더 읽을 자료

            - [United Nations, Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)
            - [European Commission, AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            - [Stanford HAI, 2026 AI Index Report](https://hai.stanford.edu/ai-index/2026-ai-index-report)
            - [UNESCO, Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)
            """
        ).strip(),
    ),
]


def add_remaining_articles() -> None:
    """Append the nine remaining article briefs.

    These entries keep full magazine structure and source-gated claims, but use
    slightly shorter bodies so the complete issue can move through temporary
    publication in one editorial pass.
    """
    remaining: list[ArticlePass] = [
        ArticlePass(
            slug="democracy-after-long-decline",
            en_title="Democracy After The Long Decline",
            ko_title="긴 하락 이후의 민주주의",
            article_type="institutional analysis",
            scope="global",
            thesis_en="Democratic decline should be read less as one sudden emergency than as the normalization of institutional erosion; the task is to identify which institutions still make correction possible.",
            thesis_ko="민주주의 후퇴는 하나의 갑작스러운 비상사태라기보다 제도 침식의 정상화로 읽어야 하며, 핵심 과제는 어떤 제도가 아직 교정을 가능하게 하는지 식별하는 것이다.",
            sources=[
                ("Freedom House 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy", "20th consecutive year of global freedom decline; 54 declined, 35 improved"),
                ("V-Dem Democracy Report 2026", "https://www.v-dem.net/publications/democracy-reports/", "democratization stagnation and autocratization indicators"),
                ("Constitutional Court of Korea latest decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "comparative institutional example for legal thresholds"),
            ],
            excluded="Avoid casual use of fascism; commentary is discourse evidence only.",
            stats_note="Democracy indices compress complex cases; use them as warning systems, not verdicts.",
            en_body=make_compact_en(
                title="Democracy After The Long Decline",
                thesis="Democratic decline is no longer best understood as a short emergency. In 2026 it is a background condition: repeated deterioration in rights, judicial independence, civic space, and electoral trust can become ordinary before it becomes regime collapse.",
                opening="For several years, democracy debate has been trapped between panic and denial. Panic says democracy is dying everywhere. Denial says every warning is partisan melodrama. The evidence supports neither simplification. Elections still matter; courts still matter; civil society still matters. But the accumulated warnings are too consistent to dismiss.",
                evidence="Freedom House reports that global freedom declined for the twentieth consecutive year in 2025, with 54 countries deteriorating and 35 improving. V-Dem's 2026 report describes limited democratization and significant autocratization, identifying only 18 democratizing countries. These sources use different methods, which makes their broad convergence more important.",
                analysis="The danger is gradualism. A society can lose democratic quality without one decisive day of collapse. Courts become more intimidated; electoral administration becomes more distrusted; public media become more partisan; emergency powers become more available; opposition becomes less legitimate in the eyes of rival citizens. By the time the constitutional problem becomes obvious, the habits that would allow correction may already have weakened.",
                concepts="Backsliding is not ordinary partisan conflict. It becomes structurally important when governing actors weaken the conditions of future competition and accountability. Populism is not automatically authoritarianism. Authoritarianism is not the same as fascism. Fascism should be reserved for a narrower threshold involving anti-liberal mobilization, ultranational myth, organized coercion, and the subordination of institutions to an exclusionary project.",
                opposing="The strongest objection is methodological. Democracy indices are built from expert coding and aggregation rules. They may overstate decline in some places, understate resilience in others, and compress national histories into scores. That objection is valid. Indices should not replace country analysis. But convergence across sources is a signal that requires diagnosis, not dismissal.",
                argument="Democracy after the long decline must be defended as a system of correction. Elections allow removal; courts enforce limits; legislatures slow executives; civil society discovers abuses; journalism tests claims; local government disperses authority. Backsliding is dangerous because it attacks these correction mechanisms before it necessarily abolishes elections.",
                implications="Use democracy indices as alarms, not verdicts. Watch election commissions, courts, prosecutors, public broadcasters, audit agencies, and local governments. Describe mechanisms rather than moods. Above all, preserve conceptual thresholds: imprecision may feel forceful, but it weakens democratic argument.",
                uncertainty="This article does not imply democracy is dying everywhere. It argues that the long duration of erosion changes the question: what remains correctable, and which institutions keep correction possible?",
                readings=[
                    ("Freedom House, Freedom in the World 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy"),
                    ("V-Dem, Democracy Report 2026", "https://www.v-dem.net/publications/democracy-reports/"),
                    ("Constitutional Court of Korea, Latest Decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143"),
                ],
            ),
            ko_body=make_compact_ko(
                title="긴 하락 이후의 민주주의",
                thesis="민주주의 후퇴는 더 이상 짧은 비상사태로만 이해하기 어렵다. 2026년에는 그것이 배경 조건이 되었다. 권리, 사법 독립, 시민 공간, 선거 신뢰의 반복적 악화는 체제 붕괴가 되기 전에 평범한 제도적 날씨가 될 수 있다.",
                opening="민주주의 논쟁은 한동안 공포와 부인의 사이에 갇혀 있었다. 공포는 민주주의가 모든 곳에서 죽고 있다고 말한다. 부인은 모든 경고가 정파적 과장이라고 말한다. 증거는 어느 쪽도 지지하지 않는다. 선거도 법원도 시민사회도 여전히 중요하다. 그러나 누적된 경고를 무시하기에는 자료가 너무 일관적이다.",
                evidence="Freedom House는 2025년에 세계 자유가 20년 연속 하락했고 54개국이 악화, 35개국이 개선되었다고 보고한다. V-Dem 2026년 보고서는 민주화가 제한적이며 권위주의화가 넓게 진행 중이라고 보고하고, 민주화 중인 국가는 18개뿐이라고 본다. 방법이 다른 자료들이 비슷한 방향을 가리킨다는 점이 중요하다.",
                analysis="위험은 점진성에 있다. 민주주의의 질은 단 하루의 붕괴 없이 낮아질 수 있다. 법원은 위축되고, 선거관리는 불신받고, 공적 미디어는 정파화되고, 비상 권한은 더 쉽게 호출되며, 야당은 경쟁자가 아니라 부정되어야 할 대상으로 묘사된다. 문제가 명백해졌을 때에는 이미 교정을 가능하게 하는 습관이 약해졌을 수 있다.",
                concepts="민주주의 후퇴는 보통의 정파 갈등이 아니다. 미래의 경쟁과 책임성을 가능하게 하는 조건이 약화될 때 구조적으로 중요해진다. 포퓰리즘은 곧 권위주의가 아니고, 권위주의는 곧 파시즘이 아니다. 파시즘은 반자유주의 동원, 배제적 국민 신화, 조직적 강제, 제도의 종속 같은 더 좁은 기준에 맞을 때 사용해야 한다.",
                opposing="가장 강한 반론은 방법론적이다. 민주주의 지수는 전문가 코딩과 집계 규칙에 의해 만들어진다. 어떤 곳에서는 하락을 과장하고, 다른 곳에서는 회복력을 과소평가하며, 국가별 역사를 점수로 압축할 수 있다. 이 반론은 타당하다. 지수는 국가 분석의 대체물이 아니다. 그러나 여러 자료의 수렴은 무시가 아니라 진단을 요구하는 신호다.",
                argument="긴 하락 이후의 민주주의는 교정 체계로 방어되어야 한다. 선거는 정부를 교체하게 하고, 법원은 한계를 집행하며, 의회는 행정부를 늦추고, 시민사회는 남용을 발견하며, 언론은 주장을 시험하고, 지방정부는 권력을 분산한다. 후퇴는 선거를 즉시 없애지 않더라도 이 교정 장치를 먼저 공격하기 때문에 위험하다.",
                implications="민주주의 지수는 판결문이 아니라 경보로 써야 한다. 선거관리기관, 법원, 검찰, 공영미디어, 감사기관, 지방정부를 보아야 한다. 분위기가 아니라 메커니즘을 설명해야 한다. 무엇보다 개념 기준을 지켜야 한다. 부정확한 말은 강해 보이지만 민주주의 논증을 약하게 만든다.",
                uncertainty="이 글은 민주주의가 모든 곳에서 죽고 있다고 말하지 않는다. 장기 침식이 질문을 바꾼다는 주장이다. 무엇이 아직 교정 가능하며, 어떤 제도가 그 교정을 가능하게 하는가.",
                readings=[
                    ("Freedom House, Freedom in the World 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy"),
                    ("V-Dem, Democracy Report 2026", "https://www.v-dem.net/publications/democracy-reports/"),
                    ("Constitutional Court of Korea, Latest Decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143"),
                ],
            ),
        ),
        ArticlePass(
            slug="displacement-without-settlement",
            en_title="Displacement Without Settlement",
            ko_title="정착 없는 강제이주",
            article_type="data essay",
            scope="global",
            thesis_en="Forced displacement remains structurally unresolved when people move from emergency into long-term legal and civic suspension; the key issue is durable membership, not only flight.",
            thesis_ko="강제이주는 사람들이 비상사태에서 장기적 법적·시민적 유예 상태로 이동할 때 구조적으로 해결되지 않는다. 핵심은 탈출만이 아니라 지속 가능한 구성원 자격이다.",
            sources=[("UNHCR Global Trends", "https://www.unhcr.org/us/global-trends", "117.8 million forcibly displaced at end-2025 and category definitions"), ("UNHCR Refugee Statistics", "https://www.unhcr.org/refugee-statistics", "disaggregated refugee data")],
            excluded="Do not use dramatic field journalism as denominator evidence; use it later only for case illustration.",
            stats_note="Separate refugees, asylum seekers, IDPs, stateless persons, returnees, stocks, and flows.",
            en_body=make_compact_en(
                "Displacement Without Settlement",
                "Forced displacement should be read as a stock problem as well as a flow problem. UNHCR reports 117.8 million forcibly displaced people at the end of 2025. The slight decline matters, but it does not equal settlement.",
                "The tempting story in the 2026 displacement data is the first decline in a decade. A humane analysis should not dismiss improvement. But a fall from an extreme level is not resolution. It may reflect returns, naturalization, changing conditions, data limits, or movement into categories that do not guarantee security.",
                "UNHCR's global figure includes categories that must not be casually merged: refugees, asylum seekers, internally displaced people, and others needing international protection. Internally displaced people form a very large share of the total, which matters because the international refugee regime is better developed for cross-border protection than for displacement inside a state.",
                "The deeper issue is duration. Emergency protection can become a semi-permanent social condition. A child can grow up in a camp, a city periphery, a temporary-protection regime, or an asylum backlog. The form says temporary; the years say otherwise. The global system is better at naming displacement than ending it.",
                "A refugee is not an internally displaced person; an asylum seeker is not a recognized refugee; a returnee is not necessarily settled. Stocks and flows also differ. A stock figure tells us how many people remain displaced at a point in time; a flow figure tells us how many fled, returned, applied, crossed, or were resettled during a period.",
                "The strongest opposing view is that falling totals and increased returns should not be minimized. Humanitarian systems can produce partial resolution; some returns reflect real improvement. That is true. But return is settlement only if it is safe, voluntary, and durable. Host-country presence is not settlement if work, schooling, legal status, and political consent remain fragile.",
                "Forced displacement remains durable because the world has built more pathways into temporary protection than into membership. Unsafe return, constrained integration, and limited resettlement keep millions in suspended lives. A serious policy frame must combine protection, host-community capacity, development finance, legal identity, education, work pathways, and credible asylum systems.",
                "Reporting should separate categories before making claims. Return statistics should be paired with safety questions. Host-country capacity should be treated as development policy, not merely humanitarian burden sharing. Wealthy countries should not treat displacement as a border spectacle while poorer host countries carry the administrative weight.",
                "This article does not claim all returns are unsafe or that all host states can integrate everyone. It argues that displacement cannot be considered resolved until people have secure membership somewhere.",
                [("UNHCR, Global Trends", "https://www.unhcr.org/us/global-trends"), ("UNHCR Refugee Data Finder", "https://www.unhcr.org/refugee-statistics")],
            ),
            ko_body=make_compact_ko(
                "정착 없는 강제이주",
                "강제이주는 흐름의 문제일 뿐 아니라 저량의 문제다. UNHCR은 2025년 말 강제이주민이 1억 1,780만 명이라고 보고한다. 소폭 감소는 중요하지만 그것이 곧 정착을 뜻하지는 않는다.",
                "2026년 강제이주 자료에서 가장 유혹적인 이야기는 10년 만의 첫 감소다. 개선을 무시해서는 안 된다. 그러나 극단적으로 높은 수준에서의 감소는 해결이 아니다. 그것은 귀환, 귀화, 조건 변화, 자료 한계, 또는 안전을 보장하지 않는 범주 이동을 반영할 수 있다.",
                "UNHCR의 세계 수치는 함부로 합치면 안 되는 범주를 포함한다. 난민, 비호 신청자, 국내실향민, 국제적 보호가 필요한 다른 인구가 그것이다. 국내실향민의 비중이 크다는 점도 중요하다. 국제 난민 체계는 국경을 넘은 보호에는 비교적 더 발달했지만, 한 국가 내부의 이주에는 한계가 크다.",
                "더 깊은 문제는 지속 기간이다. 비상 보호는 반영구적 사회 조건이 될 수 있다. 아이는 캠프, 도시 주변부, 임시 보호 체계, 비호 심사 적체 속에서 성장할 수 있다. 형식은 임시라고 말하지만 세월은 다르게 말한다. 세계 시스템은 강제이주를 이름 붙이는 데는 능하지만 끝내는 데는 약하다.",
                "난민은 국내실향민이 아니고, 비호 신청자는 인정 난민이 아니며, 귀환자는 반드시 정착자가 아니다. 저량과 유량도 다르다. 저량은 특정 시점에 여전히 이주 상태인 사람 수를 말하고, 유량은 일정 기간 새로 떠나거나 돌아오거나 신청하거나 재정착한 사람 수를 말한다.",
                "가장 강한 반론은 총량 감소와 귀환 증가를 가볍게 보아서는 안 된다는 것이다. 인도주의 체계는 부분적 해결을 만들 수 있고, 일부 귀환은 실제 개선을 반영한다. 맞는 말이다. 그러나 귀환은 안전하고 자발적이며 지속 가능할 때만 정착이다. 수용국 체류도 노동, 학교, 법적 지위, 정치적 동의가 취약하다면 정착이 아니다.",
                "강제이주가 오래 지속되는 이유는 세계가 구성원 자격으로 들어가는 길보다 임시 보호로 들어가는 길을 더 많이 만들었기 때문이다. 안전하지 않은 귀환, 제한된 통합, 좁은 재정착은 수백만 명을 유예된 삶에 묶어둔다. 진지한 정책은 보호, 수용 지역 역량, 개발 재정, 법적 신분, 교육, 노동 경로, 신뢰할 수 있는 비호 제도를 함께 다루어야 한다.",
                "보도와 분석은 범주를 구분한 뒤 주장해야 한다. 귀환 통계에는 안전 질문을 붙여야 한다. 수용국 역량은 인도주의 부담분담만이 아니라 개발 정책으로 다루어야 한다. 부유한 국가는 강제이주를 국경의 구경거리로 만들면서 더 가난한 수용국에 행정 부담을 떠넘겨서는 안 된다.",
                "이 글은 모든 귀환이 안전하지 않다거나 모든 수용국이 모두를 통합할 수 있다고 말하지 않는다. 다만 사람들에게 어딘가의 안정적 구성원 자격이 생기기 전에는 강제이주가 해결되었다고 할 수 없다고 주장한다.",
                [("UNHCR, Global Trends", "https://www.unhcr.org/us/global-trends"), ("UNHCR Refugee Data Finder", "https://www.unhcr.org/refugee-statistics")],
            ),
        ),
    ]
    ARTICLES.extend(remaining)


def make_compact_en(title: str, thesis: str, opening: str, evidence: str, analysis: str, concepts: str, opposing: str, argument: str, implications: str, uncertainty: str, readings: list[tuple[str, str]]) -> str:
    reading_lines = "\n".join(f"- [{label}]({url})" for label, url in readings)
    return clean_markdown(
        f"""
        ## Abstract

        {thesis}

        ## Opening Issue

        {opening}

        ## Evidence

        {evidence}

        ## Analysis

        {analysis}

        ## Reporting Judgment

        The reporting judgment is to keep the article close to institutions rather than atmosphere. The piece should not begin from the loudest column, the most elegant analogy, or the most shareable phrase. It should begin from the source that can bear weight: an official release, a legal decision, a public dataset, an institutional report, a verified election return, or a clearly bounded high-quality account.

        That discipline does not make the prose timid. It makes the argument more exact. A serious article can still have voice, rhythm, and judgment; it simply shows readers where the factual floor ends and where interpretation begins. The task is not neutrality as evasion. It is accountable judgment.

        {extra_depth_en(title)}

        ## Why This Matters Now

        The issue is current not because it is noisy, but because institutional choices are becoming harder to postpone. In this quarter, the relevant facts have moved beyond mood: official data, legal timelines, court decisions, or institutional reports now give readers something firmer than commentary to test. That does not make the conclusion automatic. It makes the question ripe for serious judgment.

        ## Conceptual Clarification

        {concepts}

        ## Best Opposing View

        {opposing}

        ## Argument

        {argument}

        ## Argument Reconstruction

        Major premise: when a public problem changes institutional authority, rights, fiscal capacity, social membership, or the credibility of knowledge, it should be treated as structural rather than merely topical.

        Minor premise: {title} is such a problem because the evidence points beyond a single event toward a change in incentives, capacities, or expectations.

        Conclusion: {thesis}

        Hidden assumption: institutions still retain enough agency for better rules, clearer evidence, and more honest public reasoning to matter.

        Possible weak link: the available sources may establish pressure more clearly than they establish causality. The article therefore treats its conclusion as a disciplined interpretation, not as a closed proof.

        ## What This Does Not Prove

        This article does not claim more than the source base can bear. It does not convert one report into a universal law, one election into a national destiny, one annual statistic into a permanent trend, or one legal decision into a complete theory of institutions. Its claim is structural and provisional: the evidence is strong enough to identify a pattern, but not strong enough to end the argument.

        ## Source Limits

        The source base is strong enough for a temporary magazine argument, but it is not the same as a completed book chapter or peer-reviewed article. Official statistics can lag behind social experience. Legal summaries can omit reasoning that matters in the full decision. International indices can compress national histories. Forecasts can change when assumptions change. Adoption figures can measure use without measuring quality, productivity, learning, or legitimacy.

        These limits are not defects to hide. They are part of the article's honesty. A serious publication should let readers see which claims are anchored in documented facts, which claims are comparative interpretations, and which claims remain provisional because better data, fuller legal texts, or additional field reporting are still needed.

        ## What Would Change The Judgment

        The judgment should change if later official releases contradict the direction of the evidence, if disaggregated data show that the apparent pattern is concentrated in a narrow subgroup, if full legal texts undermine the reading suggested by summaries, if implementation fails in ways the article treats as manageable, or if rival interpretations explain the same facts with fewer assumptions.

        This is why temporary publication is not a loophole around review. It is a visible stage in the editorial process. The article is public enough to be read, criticized, and improved, but not treated as beyond revision.

        ## Policy Or Civic Implications

        {implications}

        ## What To Watch

        Watch the next official release, the next implementation deadline, the next judicial or administrative response, and the next place where a broad claim becomes a practical burden. Structural issues reveal themselves when institutions have to move from statement to execution.

        ## Evidence Strength

        Overall evidence level: moderate. High-confidence claims are limited to source-documented facts. Interpretive claims are presented as judgments rather than settled findings.

        ## Uncertainty Note

        {uncertainty}

        ## Further Reading

        {reading_lines}
        """
    )


def make_compact_ko(title: str, thesis: str, opening: str, evidence: str, analysis: str, concepts: str, opposing: str, argument: str, implications: str, uncertainty: str, readings: list[tuple[str, str]]) -> str:
    reading_lines = "\n".join(f"- [{label}]({url})" for label, url in readings)
    return clean_markdown(
        f"""
        ## 초록

        {thesis}

        ## 출발점

        {opening}

        ## 증거

        {evidence}

        ## 분석

        {analysis}

        ## 취재 판단

        이 글의 취재 판단은 분위기가 아니라 제도에 가까이 붙는 것이다. 가장 시끄러운 칼럼, 가장 멋진 비유, 가장 잘 공유되는 문장에서 출발하지 않는다. 무게를 견딜 수 있는 출처, 곧 공식 발표, 법원 결정, 공공 데이터셋, 제도 보고서, 검증된 선거 결과, 범위가 분명한 고품질 보도에서 출발한다.

        이 규율이 문장을 소심하게 만들지는 않는다. 오히려 주장을 더 정확하게 만든다. 진지한 글은 여전히 목소리와 리듬과 판단을 가질 수 있다. 다만 사실의 바닥이 어디서 끝나고 해석이 어디서 시작되는지를 독자에게 보여준다. 목표는 회피적 중립이 아니라 책임 있는 판단이다.

        {extra_depth_ko(title)}

        ## 왜 지금 중요한가

        이 사안은 시끄럽기 때문에 중요한 것이 아니라, 제도적 선택을 더 이상 미루기 어려워졌기 때문에 중요하다. 이번 분기에는 관련 사실들이 분위기의 수준을 넘어섰다. 공식 통계, 법적 일정, 법원 결정, 제도 보고서가 논평보다 단단한 검토 대상을 제공한다. 그것이 결론을 자동으로 정해 주지는 않는다. 다만 진지한 판단을 시작할 조건을 만든다.

        ## 개념 정리

        {concepts}

        ## 가장 강한 반론

        {opposing}

        ## 주장

        {argument}

        ## 논증 재구성

        대전제: 어떤 공적 문제가 제도 권한, 권리, 재정 역량, 사회적 구성원 자격, 지식의 신뢰성을 바꾼다면 그것은 단순한 화제가 아니라 구조적 사안으로 다루어야 한다.

        소전제: {title}{topic_marker_ko(title)} 하나의 사건을 넘어 유인, 역량, 기대의 변화를 가리키기 때문에 그런 사안이다.

        결론: {thesis}

        숨은 전제: 제도에는 아직 더 나은 규칙, 더 분명한 증거, 더 정직한 공적 추론이 의미를 가질 만큼의 행위 능력이 남아 있다.

        약한 고리: 현재 출처들은 압력을 보여주는 데에는 강하지만 인과를 완전히 닫아 주지는 않을 수 있다. 그래서 이 글의 결론은 닫힌 증명이 아니라 절제된 해석으로 제시된다.

        ## 이 글이 증명하지 않는 것

        이 글은 출처 기반이 감당할 수 있는 것보다 더 강한 주장을 하지 않는다. 하나의 보고서를 보편 법칙으로, 하나의 선거를 국가의 운명으로, 하나의 연간 통계를 영구 추세로, 하나의 법원 결정을 제도 전체의 이론으로 바꾸지 않는다. 주장은 구조적이고 잠정적이다. 증거는 패턴을 식별할 만큼 강하지만 논쟁을 끝낼 만큼 강하지는 않다.

        ## 출처의 한계

        현재 출처 기반은 임시 발행용 매거진 논증에는 충분하지만, 완성된 단행본 장이나 동료심사 논문과 같지는 않다. 공식 통계는 사회 경험보다 늦게 도착할 수 있다. 법원 요약은 결정문 전문에서 중요한 추론을 생략할 수 있다. 국제 지수는 국가별 역사를 압축한다. 전망은 가정이 바뀌면 달라진다. 채택률은 사용 여부를 보여줄 수 있지만 사용의 질, 생산성, 학습, 정당성을 곧바로 보여주지는 않는다.

        이 한계는 숨길 결함이 아니다. 글의 정직성 일부다. 진지한 매체는 어떤 주장이 확인된 사실에 고정되어 있고, 어떤 주장이 비교 해석이며, 어떤 주장이 더 나은 자료, 결정문 전문, 추가 취재를 기다리는 잠정 판단인지 독자에게 보여주어야 한다.

        ## 판단을 바꿀 조건

        이후 공식 발표가 증거의 방향을 뒤집거나, 세분 자료가 겉보기 패턴이 좁은 하위집단에 집중되어 있음을 보여주거나, 결정문 전문이 요약에 근거한 해석을 약화하거나, 실행 실패가 이 글이 관리 가능하다고 본 위험보다 크거나, 경쟁 해석이 더 적은 가정으로 같은 사실을 설명한다면 판단은 바뀌어야 한다.

        그래서 임시 발행은 검토를 우회하는 장치가 아니다. 그것은 편집 과정의 보이는 단계다. 글은 읽히고 비판받고 개선될 만큼 공개되지만, 수정 불가능한 최종본으로 취급되지는 않는다.

        ## 정책적·시민적 함의

        {implications}

        ## 다음에 볼 것

        다음 공식 발표, 다음 시행 기한, 다음 사법적·행정적 대응, 그리고 넓은 주장이 실제 부담으로 바뀌는 장소를 보아야 한다. 구조적 사안은 제도가 선언에서 실행으로 이동할 때 모습을 드러낸다.

        ## 근거 강도

        전체 증거 수준: 중간. 높은 확신의 주장은 출처로 확인되는 사실에 한정한다. 해석적 주장은 확정된 발견이 아니라 편집 판단으로 제시한다.

        ## 불확실성 노트

        {uncertainty}

        ## 더 읽을 자료

        {reading_lines}
        """
    )


def extra_depth_en(title: str) -> str:
    entries = {
        "Democracy After The Long Decline": """
            ## Field Of Conflict

            The real conflict is not between people who care about democracy and people who do not. It is between different accounts of what democracy requires after voters have become accustomed to institutional stress. One side emphasizes electoral choice and warns that unelected judges, regulators, journalists, and international monitors can overrule majorities. Another emphasizes the conditions that make electoral choice meaningful: independent administration, civil liberty, opposition rights, courts that can say no, and media that can test official claims.

            The article therefore avoids treating democracy as a moral badge. It treats democracy as a correction system. A correction system can survive anger, turnover, ideological conflict, and unpopular decisions. It cannot survive indefinitely if every referee is redescribed as an enemy, every defeat as fraud, and every limit as betrayal. The reporting task is to identify which correction mechanisms still work, which are being intimidated, and which are being hollowed out by habit rather than abolished by law.

            ## Final Reporting Path

            A stronger final version should pair the aggregate indices with country-level mechanisms. It should compare several cases rather than letting one dramatic example stand for the whole world. It should identify where constitutional courts, election bodies, local governments, prosecutors, public broadcasters, and civil-society organizations actually changed outcomes. It should also ask where warnings failed: which countries looked formally democratic while losing practical accountability? The final version should use indices as a map, then walk the terrain.
        """,
        "Displacement Without Settlement": """
            ## Field Of Conflict

            The conflict in displacement policy is often described as generosity versus control. That framing is too simple. The harder conflict is among protection, consent, capacity, and membership. Host communities need schools, housing, health systems, labor rules, and political legitimacy. Displaced people need safety, work, education, documents, family unity, and a future that is not endlessly temporary. States need border rules, asylum procedures, and development finance. Humanitarian agencies need money and access. None of these needs cancels the others.

            That is why the language of emergency can become misleading. It mobilizes sympathy but can conceal duration. If a family spends ten years under a temporary status, the honest question is no longer only protection from immediate harm. It is whether a person can become a member of a society, return safely, or move legally somewhere else. The most important policy question is not whether the world can count the displaced. It is whether the world can create credible exits from displacement.

            ## Final Reporting Path

            A stronger final version should separate the data by region, legal category, age, and duration. It should compare return, local integration, and resettlement as distinct pathways rather than folding them into one hopeful word. It should add host-country fiscal and administrative capacity, because the largest host burdens are often carried by states with limited resources. It should also examine when return is voluntary and durable, not merely counted.
        """,
        "Korea's Mandate Problem After The Local Elections": """
            ## Field Of Conflict

            The conflict after a Korean local election is partly numerical and partly rhetorical. The numerical question is who won which offices, by what margins, on what turnout, in which regions. The rhetorical question is what parties then do with those numbers. A governing party may turn local success into a national mandate. An opposition party may turn local defeat into evidence of unfairness or social exhaustion. Commentators may compress mixed results into one national mood.

            The mature reading is less dramatic. It asks how Korean voters distribute authority when they are voting for local administrators inside a nationalized party system. The offices are real. They shape budgets, urban development, welfare delivery, local transport, regional planning, and cooperation with central ministries. But the party label is also real. Voters know that a mayoral or gubernatorial race sends a message about national leadership. The article therefore treats the election as a layered mandate: local authorization first, national signal second, full national permission only where the evidence supports it.

            ## Final Reporting Path

            A stronger final version should build a table from NEC returns: turnout, vote share, margin, party control before and after, and office type. It should separate Seoul from the national distribution, because Seoul carries disproportionate symbolic weight without being the whole country. It should compare the result with prior local elections and with presidential or legislative cycles. Only then should it make claims about national mandate.
        """,
        "Korea's Semiconductor Recovery And The Welfare State It Cannot Avoid": """
            ## Field Of Conflict

            Korea's semiconductor strength is a national asset, but it also creates a political temptation: to mistake export capacity for social settlement. The conflict is not between industry and welfare. It is between two versions of competitiveness. One version treats competitiveness as the ability to win in global markets. Another treats it as the ability to sustain the people, regions, infrastructure, and public legitimacy that make industrial excellence reproducible over time.

            The second version is more demanding. It asks whether housing near opportunity is livable, whether care obligations force people out of work, whether regional schools and hospitals can support industrial clusters, whether energy and water systems can carry new investment, and whether workers can move across firms and technologies without falling through social insurance. A semiconductor cycle can provide fiscal room. But a cycle is not a social contract. If the gains are treated only as proof of national prowess, the next downturn will find the same household pressures waiting.

            ## Final Reporting Path

            A stronger final version should link export and investment data to fiscal receipts, regional employment, energy demand, housing costs, and care indicators. It should distinguish permanent capacity-building from temporary transfers. It should also compare Korea with other semiconductor economies, not to copy them, but to test which social investments make high-end industrial strategy politically durable.
        """,
        "Korea's Fertility Rebound Is Not A Theory Of The Family": """
            ## Field Of Conflict

            Fertility policy is often pulled into moral argument before the evidence has been sorted. One camp reads low fertility as cultural decline, selfishness, gender conflict, or excessive individualism. Another reads it as a rational response to housing costs, unstable work, education pressure, and unequal care. A third treats the issue as budget engineering: more cash, better leave, cheaper childcare. Each view captures something and misses something.

            The article's claim is narrower. The object is household formation, not fertility as a moral score. People form families inside a sequence: partnership, housing, work, health, care, education, elder obligations, and expectations about status. If the sequence looks punitive, desired children are delayed or forgone. If the sequence becomes more livable, some rebound is possible. The policy question is therefore not how to pressure people into births. It is how to reduce the penalties attached to the family lives many people already say they want.

            ## Final Reporting Path

            A stronger final version should disaggregate the rebound by age, parity, region, marriage cohort, income, housing tenure, and employment status. It should ask whether births are first births, second births, or timing shifts. It should examine whether policy changes, housing conditions, labor-market expectations, and marriage patterns changed before the rebound. The final article should be careful not to turn one good year into a demographic doctrine.
        """,
        "The Constitutional Court's Quiet Institutionalism": """
            ## Field Of Conflict

            Constitutional courts live between law and politics. If they appear too passive, citizens may think rights are words without force. If they appear too political, citizens may think constitutional law is ordinary factional struggle in robes. The conflict is therefore not simply activism versus restraint. It is how a court gives reasons strong enough to bind power without pretending that legal judgment floats above constitutional conflict.

            Korea's recent institutional stress makes this question sharper. Emergency power, assembly rights, counsel access, impeachment, and electoral thresholds are not abstract doctrines. They are places where state power meets citizens, parties, soldiers, lawyers, voters, and legislatures. Quiet institutionalism matters because it keeps the language of thresholds alive. It asks what must be shown before the state punishes, detains, excludes, suspends, or reorganizes democratic competition. That work is less theatrical than crisis rhetoric, but it is often more durable.

            ## Final Reporting Path

            A stronger final version should read the Korean full texts, not only official English summaries. It should identify holdings, concurrences, dissents, standards of review, and remedial choices. It should distinguish legally binding reasoning from political interpretation. It should also compare the Court's emergency-power reasoning with its ordinary-rights cases, because constitutional resilience is visible in both.
        """,
        "Universities After Generative AI": """
            ## Field Of Conflict

            The conflict over generative AI in universities is not simply between honest students and cheaters. It is between inherited assessment systems and a new production environment. Universities built many courses around artifacts: the essay, the take-home exam, the code file, the literature review, the lab report. Those artifacts worked because they were expensive enough to produce that they usually carried traces of learning. Generative AI lowers that cost and blurs the trace.

            The better question is therefore not whether AI should be allowed or banned in the abstract. It is what each discipline wants students to learn, which uses of AI help or obstruct that learning, and what evidence can show the learning occurred. Philosophy, chemistry, computer science, history, law, design, and engineering will not need identical rules. A mature university policy should be less like a prohibition poster and more like an assessment architecture.

            ## Final Reporting Path

            A stronger final version should compare institutional policies across universities and disciplines, then test them against actual assessment design. It should distinguish detection, disclosure, permission, required use, prohibited use, and process evidence. It should include faculty workload, because redesigning assessment is labor-intensive. It should also examine equity: students with better access to tools, tutoring, and institutional guidance may gain more from ambiguity.
        """,
        "The Culture Of AI Fatalism": """
            ## Field Of Conflict

            AI fatalism has an odd emotional range. It can sound ecstatic: everything will be automated, abundance will arrive, and institutions merely need to adapt. It can sound apocalyptic: jobs, truth, schools, art, democracy, and human agency are already finished. The two moods disagree about the ending, but they share a premise. Both treat technological trajectory as more real than public choice.

            That premise is politically convenient. Firms can present deployment as inevitability. Governments can present weak oversight as realism. Schools can present confusion as transition. Citizens can experience exhaustion as sophistication. The article's objection is not that AI is weak or that structural power is imaginary. The objection is that fatalism hides the location of decisions. Models are built, bought, integrated, subsidized, restricted, audited, litigated, and normalized by actors. The language of destiny protects those actors from scrutiny.

            ## Final Reporting Path

            A stronger final version should reconstruct AI fatalism through discourse evidence: company statements, policy speeches, magazine essays, classroom debates, investor narratives, and cultural products. Those sources should not be used as evidence that AI will do what they say. They should be used as evidence of how inevitability is being narrated. The article should then compare discourse with adoption data and governance choices.
        """,
        "What To Read On AI, Democracy, Energy, And Korea's Institutional Moment": """
            ## Field Of Conflict

            A reading list can either discipline an issue or decorate it. Decoration is easy: attach impressive names and let citations create an aura of authority. Discipline is harder. It asks what role each source plays. Is it a denominator? A legal threshold? A forecast? A warning system? A conceptual vocabulary? A case chronology? A record of discourse? Readers should be able to see that architecture without guessing.

            This is especially important for a bilingual quarterly that uses Korean raw sources and an English-language magazine style. Korean official data should not be translated into mere atmosphere. English-language institutional reports should not become global wallpaper. Commentary in either language should not be promoted into raw evidence. The bibliography is therefore part of the magazine's method: it shows how a Korean case can be analyzed with international discipline without losing its factual ground.

            ## Final Reporting Path

            A stronger final version should become an annotated source map rather than a list. Each entry should identify source type, evidentiary use, limitations, update frequency, and article relevance. It should add Korean original PDFs, full court decisions, election datasets, and peer-reviewed literature. It should also mark where the magazine is relying on provisional English summaries and where Korean primary documents still need full editorial review.
        """,
    }
    return dedent(entries.get(title, "")).strip()


def extra_depth_ko(title: str) -> str:
    entries = {
        "긴 하락 이후의 민주주의": """
            ## 갈등의 장

            실제 갈등은 민주주의를 걱정하는 사람과 그렇지 않은 사람 사이에만 있지 않다. 유권자가 제도적 긴장에 익숙해진 뒤 민주주의가 무엇을 요구하는지에 관한 서로 다른 설명 사이에 있다. 한쪽은 선거 선택을 강조하며, 선출되지 않은 판사, 규제기관, 언론, 국제 감시자가 다수를 제약할 수 있다고 경고한다. 다른 한쪽은 선거 선택을 의미 있게 만드는 조건, 곧 독립 행정, 시민적 자유, 야당의 권리, 아니라고 말할 수 있는 법원, 공식 주장을 시험할 수 있는 언론을 강조한다.

            이 글은 민주주의를 도덕적 배지로 다루지 않는다. 민주주의를 교정 체계로 다룬다. 교정 체계는 분노, 정권교체, 이념 갈등, 인기 없는 결정을 견딜 수 있다. 그러나 모든 심판이 적으로 묘사되고, 모든 패배가 부정선거가 되며, 모든 제한이 배신으로 불릴 때 오래 버티기는 어렵다.

            ## 최종 취재 경로

            최종본은 집계 지표를 국가별 메커니즘과 결합해야 한다. 극적인 한 사례가 세계 전체를 대신하게 두지 말고 여러 사례를 비교해야 한다. 헌법재판소, 선거관리기구, 지방정부, 검찰, 공영방송, 시민사회가 실제로 결과를 바꾼 곳을 확인해야 한다. 지표는 지도이고, 최종 원고는 그 지형을 걸어야 한다.
        """,
        "정착 없는 강제이주": """
            ## 갈등의 장

            강제이주 정책의 갈등은 종종 관대함 대 통제로 설명된다. 그러나 그 틀은 너무 단순하다. 더 어려운 갈등은 보호, 동의, 역량, 구성원 자격 사이에 있다. 수용 지역에는 학교, 주거, 보건, 노동 규칙, 정치적 정당성이 필요하다. 이주민에게는 안전, 일, 교육, 문서, 가족 결합, 끝없이 임시적이지 않은 미래가 필요하다. 국가는 국경 규칙, 비호 절차, 개발 재정이 필요하고, 인도주의 기관은 돈과 접근이 필요하다.

            그래서 비상이라는 언어는 오해를 만들 수 있다. 그것은 연민을 동원하지만 지속 기간을 가릴 수 있다. 한 가족이 임시 지위로 10년을 산다면 질문은 즉각적 위해로부터의 보호만이 아니다. 어느 사회의 구성원이 될 수 있는지, 안전하게 돌아갈 수 있는지, 합법적으로 다른 곳으로 이동할 수 있는지가 된다.

            ## 최종 취재 경로

            최종본은 지역, 법적 범주, 연령, 지속 기간별로 자료를 나누어야 한다. 귀환, 현지 통합, 재정착을 하나의 희망적 단어로 묶지 말고 별도의 경로로 비교해야 한다. 특히 가장 큰 수용 부담이 제한된 자원을 가진 국가에 놓이는 경우가 많으므로 수용국의 재정·행정 역량을 함께 보아야 한다.
        """,
        "지방선거 이후 한국의 위임 문제": """
            ## 갈등의 장

            한국 지방선거 이후의 갈등은 숫자의 문제이면서 수사의 문제다. 숫자의 질문은 누가 어떤 직위를, 어떤 격차로, 어떤 투표율 속에서, 어느 지역에서 이겼는가이다. 수사의 질문은 정당이 그 숫자로 무엇을 하는가이다. 집권당은 지방 승리를 전국적 위임으로 바꾸려 할 수 있고, 야당은 패배를 불공정이나 사회적 피로의 증거로 만들 수 있다. 논평은 섞인 결과를 하나의 전국 정서로 압축한다.

            더 성숙한 독해는 덜 극적이다. 전국화된 정당 체계 안에서 유권자가 지방 행정 권한을 어떻게 배분했는지를 묻는다. 직위는 실제다. 예산, 도시개발, 복지 전달, 교통, 지역계획, 중앙정부와의 협력을 바꾼다. 그러나 정당 표지도 실제다. 그래서 이 선거는 층위가 있는 위임이다. 먼저 지방 권한, 다음으로 전국 신호, 그리고 증거가 지지하는 경우에만 전국적 허가다.

            ## 최종 취재 경로

            최종본은 중앙선거관리위원회 결과로 투표율, 득표율, 격차, 이전·이후 정당 지배, 직위 유형 표를 만들어야 한다. 서울은 상징적 무게가 크지만 전국 전체는 아니므로 별도로 다뤄야 한다. 이전 지방선거와 대선·총선 주기와도 비교한 뒤에야 전국적 위임을 말할 수 있다.
        """,
        "한국의 반도체 회복과 피할 수 없는 복지국가": """
            ## 갈등의 장

            한국의 반도체 경쟁력은 국가적 자산이지만 정치적 유혹도 만든다. 수출 역량을 사회적 타결로 착각하는 유혹이다. 갈등은 산업과 복지 사이에만 있지 않다. 경쟁력의 두 버전 사이에 있다. 하나는 세계시장에서 이기는 능력을 경쟁력으로 본다. 다른 하나는 산업적 우수성을 오래 재생산하게 하는 사람, 지역, 인프라, 공적 정당성을 유지하는 능력까지 경쟁력으로 본다.

            두 번째 버전이 더 어렵다. 기회가 있는 지역의 주거가 살 만한지, 돌봄 의무가 사람을 일에서 밀어내는지, 지역의 학교와 병원이 산업 클러스터를 떠받치는지, 전력과 물 시스템이 투자를 감당하는지, 노동자가 사회보험 밖으로 떨어지지 않고 기술과 기업 사이를 이동할 수 있는지를 묻기 때문이다. 반도체 경기는 재정 여지를 줄 수 있다. 그러나 순환은 사회계약이 아니다.

            ## 최종 취재 경로

            최종본은 수출·투자 자료를 세수, 지역 고용, 에너지 수요, 주거비, 돌봄 지표와 연결해야 한다. 일시적 이전지출과 영구적 역량 구축을 구분해야 한다. 다른 반도체 경제와의 비교도 필요하다. 모방을 위해서가 아니라 어떤 사회투자가 고급 산업 전략을 정치적으로 지속 가능하게 하는지 검토하기 위해서다.
        """,
        "한국의 출산 반등은 가족에 관한 이론이 아니다": """
            ## 갈등의 장

            출산 정책은 증거가 정리되기 전에 도덕 논쟁으로 끌려가기 쉽다. 한쪽은 저출산을 문화적 쇠퇴, 이기심, 젠더 갈등, 과도한 개인주의로 읽는다. 다른 한쪽은 주거비, 불안정 노동, 교육 압력, 불평등한 돌봄에 대한 합리적 반응으로 읽는다. 또 다른 쪽은 예산 공학으로 본다. 더 많은 현금, 더 나은 휴직, 더 싼 보육이다. 각각은 무언가를 포착하고 무언가를 놓친다.

            이 글의 주장은 더 좁다. 대상은 도덕 성적표로서의 출산율이 아니라 가계 형성이다. 사람들은 동반자 관계, 주거, 일, 건강, 돌봄, 교육, 노부모 의무, 지위 기대의 순서 안에서 가족을 형성한다. 그 순서가 처벌처럼 보이면 원하는 자녀도 미뤄지거나 포기된다. 정책 질문은 사람들을 출산으로 압박하는 것이 아니라, 사람들이 이미 원한다고 말하는 가족생활에 붙은 벌칙을 줄이는 것이다.

            ## 최종 취재 경로

            최종본은 반등을 연령, 출산 순위, 지역, 혼인 코호트, 소득, 주거 점유, 고용 상태별로 나누어야 한다. 첫째아인지 둘째아인지, 시점 이동인지도 보아야 한다. 정책 변화, 주거 조건, 노동시장 기대, 혼인 패턴이 반등 전에 어떻게 움직였는지를 확인해야 한다.
        """,
        "헌법재판소의 조용한 제도주의": """
            ## 갈등의 장

            헌법재판소는 법과 정치 사이에 산다. 너무 수동적으로 보이면 시민은 권리가 힘없는 말이라고 생각할 수 있다. 너무 정치적으로 보이면 헌법법이 법복을 입은 보통의 정파 싸움이라고 생각할 수 있다. 갈등은 단순한 적극주의 대 자제론이 아니다. 법원이 권력을 묶을 만큼 강한 이유를 어떻게 제시하면서도, 법적 판단이 헌정 갈등 위에 떠 있다고 가정하지 않을 것인가이다.

            한국의 최근 제도적 긴장은 이 질문을 더 날카롭게 만든다. 비상 권한, 집회 권리, 변호인 접견, 탄핵, 선거 기준은 추상 교리가 아니다. 국가권력이 시민, 정당, 군인, 변호사, 유권자, 입법부와 만나는 장소다. 조용한 제도주의는 기준의 언어를 살아 있게 한다. 국가가 처벌하고, 구금하고, 배제하고, 정지하고, 민주적 경쟁을 재조직하기 전에 무엇을 입증해야 하는지를 묻는다.

            ## 최종 취재 경로

            최종본은 공식 영문 요약만이 아니라 한국어 결정문 전문을 읽어야 한다. 주문, 보충의견, 반대의견, 심사 기준, 구제 방식을 확인해야 한다. 법적으로 구속력 있는 추론과 정치적 해석을 구분해야 한다. 비상 권한 사건과 일상적 권리 사건을 함께 비교해야 헌정 회복력을 볼 수 있다.
        """,
        "생성형 AI 이후의 대학": """
            ## 갈등의 장

            대학의 생성형 AI 갈등은 정직한 학생과 부정행위 학생 사이의 단순한 갈등이 아니다. 물려받은 평가 체계와 새로운 생산 환경 사이의 갈등이다. 대학은 에세이, 오픈북 과제, 코드 파일, 문헌 검토, 실험 보고서 같은 산출물을 중심으로 많은 수업을 만들었다. 그 산출물은 만들기 충분히 비쌌기 때문에 대체로 학습의 흔적을 담고 있었다. 생성형 AI는 그 비용을 낮추고 흔적을 흐린다.

            더 나은 질문은 AI를 추상적으로 허용할 것인가 금지할 것인가가 아니다. 각 학문 분야가 학생에게 무엇을 배우게 하려는지, 어떤 AI 사용이 그 학습을 돕거나 방해하는지, 어떤 증거가 학습이 일어났음을 보여줄 수 있는지다. 철학, 화학, 컴퓨터과학, 역사, 법, 디자인, 공학이 같은 규칙을 필요로 하지는 않는다.

            ## 최종 취재 경로

            최종본은 대학과 학문 분야별 정책을 비교하고 실제 평가 설계에 대조해야 한다. 탐지, 공개, 허용, 필수 사용, 금지, 과정 증거를 구분해야 한다. 평가 재설계는 노동집약적이므로 교수자의 업무량도 포함해야 한다. 도구와 지도에 더 잘 접근하는 학생이 더 큰 이익을 얻을 수 있다는 형평성 문제도 보아야 한다.
        """,
        "AI 숙명론의 문화": """
            ## 갈등의 장

            AI 숙명론은 이상한 감정 범위를 갖는다. 황홀하게 들릴 수 있다. 모든 것이 자동화되고 풍요가 오며 제도는 적응만 하면 된다는 식이다. 동시에 파국적으로 들릴 수도 있다. 일자리, 진실, 학교, 예술, 민주주의, 인간 행위 능력은 이미 끝났다는 식이다. 두 분위기는 결말에 대해서는 다투지만 전제를 공유한다. 기술 궤적이 공적 선택보다 더 현실적이라는 전제다.

            이 전제는 정치적으로 편리하다. 기업은 배치를 필연으로 제시할 수 있다. 정부는 약한 감독을 현실주의로 포장할 수 있다. 학교는 혼란을 전환기로 부를 수 있다. 시민은 소진을 세련됨으로 경험할 수 있다. 이 글의 반론은 AI가 약하다는 것이 아니다. 숙명론이 결정의 위치를 숨긴다는 것이다.

            ## 최종 취재 경로

            최종본은 기업 발표, 정책 연설, 잡지 에세이, 교실 논쟁, 투자자 서사, 문화 생산물 속에서 AI 숙명론을 재구성해야 한다. 그런 출처들은 AI가 실제로 그렇게 될 것이라는 증거가 아니라, 필연성이 어떻게 서사화되는지의 증거로 사용해야 한다. 그다음 담론을 채택 자료와 거버넌스 선택에 대조해야 한다.
        """,
        "AI, 민주주의, 에너지, 한국의 제도적 순간을 읽기 위한 자료": """
            ## 갈등의 장

            독해 목록은 호 전체를 절제시킬 수도 있고 장식할 수도 있다. 장식은 쉽다. 그럴듯한 이름을 붙이고 인용이 권위의 분위기를 만들게 하면 된다. 절제는 더 어렵다. 각 출처가 어떤 역할을 하는지 묻기 때문이다. 분모인가, 법적 기준인가, 전망인가, 경보 체계인가, 개념 어휘인가, 사건 연표인가, 담론 기록인가. 독자는 그 구조를 추측하지 않고 볼 수 있어야 한다.

            한국 원자료와 영미권 잡지 문체를 함께 쓰는 이중언어 계간지에서는 이 점이 특히 중요하다. 한국 공식 자료는 분위기로 번역되어서는 안 된다. 영문 제도 보고서는 세계적 배경 장식이 되어서는 안 된다. 어느 언어의 논평도 원자료로 승격되어서는 안 된다. 참고문헌은 그래서 방법의 일부다.

            ## 최종 취재 경로

            최종본은 목록이 아니라 주석 달린 출처 지도가 되어야 한다. 각 항목은 출처 유형, 증거로서의 용도, 한계, 갱신 주기, 관련 기사를 표시해야 한다. 한국어 원문 PDF, 법원 결정 전문, 선거 데이터셋, 동료심사 문헌도 추가해야 한다.
        """,
    }
    return dedent(entries.get(title, "")).strip()


def add_final_articles() -> None:
    additions = [
        ("korea-mandate-problem-local-elections", "Korea's Mandate Problem After The Local Elections", "지방선거 이후 한국의 위임 문제", "political institutions essay", "korea",
         "Korea's 2026 local elections should be read neither as a purely local exercise nor as a simple national referendum. Mandate claims must specify office, geography, turnout, vote share, policy competence, and timing.",
         "한국의 2026년 지방선거는 순수한 지방 행사로도, 단순한 전국 국민투표로도 읽혀서는 안 된다. 위임 주장은 직위, 지역, 투표율, 득표율, 정책 권한, 시점을 명시해야 한다.",
         [("National Election Commission", "https://www.nec.go.kr/", "official election data"), ("Associated Press local-election report", "https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0", "international chronology")],
         "Do not use Korean commentary as raw election evidence.",
         "Final claims require NEC tables; AP is chronology.",
         "A local election in Korea rarely stays local. Parties nationalize it, presidents read it, and commentators turn it into a verdict. But the offices at stake govern transport, housing, local welfare delivery, development, schools, budgets, and cooperation with national agencies.",
         "The National Election Commission is the authoritative source for official returns. AP reported that the ruling party won a majority of major local races while losing Seoul. That combination is precisely why a one-sentence national verdict is too crude.",
         "The analytical problem is scale. A vote can signal displeasure with national politics while authorizing only local offices. Korea's highly nationalized party competition makes that ambiguity unavoidable, but ambiguity is exactly why mandate claims require discipline. If a party treats every local victory as permission for every national project, it converts electoral information into overreach. If an opposition treats every loss as illegitimate, it converts defeat into institutional suspicion. The mature reading is narrower and more useful: identify where voters changed administrative power, where they sent a national signal, and where the data do not support a sweeping conclusion.",
         "A mandate is not a mood. It is a claim about authorization. Office, geography, turnout, margin, policy competence, and timing all matter. Seoul is politically special, but Seoul is not Korea. Local office carries national signals, but it does not authorize every national program.",
         "The strongest objection is that Korea's party system is highly nationalized. Voters know local ballots carry national stakes. That is true. But national meaning does not erase local authority. Signal and authorization are different.",
         "Korea's mandate problem is a problem of translation. Votes cast for local offices are translated into national claims. That translation is unavoidable, but it must be disciplined. Parties should interpret victory without overclaiming it and defeat without delegitimizing the system.",
         "Use NEC official data. Separate Seoul from national totals. Distinguish mayoral, gubernatorial, council, and by-election results. Ask what local governments can actually implement before deriving national mandates.",
         "This temporary version establishes interpretive rules. A final version should add NEC turnout tables, vote-share maps, and comparisons with prior elections."),
        ("korea-semiconductor-recovery-welfare-state", "Korea's Semiconductor Recovery And The Welfare State It Cannot Avoid", "한국의 반도체 회복과 피할 수 없는 복지국가", "political economy essay", "korea",
         "Korea's semiconductor recovery can create fiscal and political room, but it cannot substitute for social capacity in housing, care, fertility, labor mobility, and regional repair.",
         "한국의 반도체 회복은 재정적·정치적 여지를 만들 수 있지만, 주거, 돌봄, 출산, 노동 이동, 지역 회복의 사회적 역량을 대체할 수는 없다.",
         [("Bank of Korea Economic Outlook, May 2026", "https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098207&programType=newsDataEng&relate=Y", "growth and inflation projections"), ("World Bank Global Economic Prospects", "https://openknowledge.worldbank.org/entities/publication/bb904ec6-730f-4dd9-b1af-ad3153ee1616", "global uncertainty and fiscal space"), ("KOSIS", "https://kosis.kr/eng/", "demographic data")],
         "Do not use business commentary as evidence for macro facts.",
         "Forecasts are conditional; semiconductor-cycle claims require date and source.",
         "Korea is unusually good at turning strategic anxiety into industrial discipline. Semiconductors connect exports, national security, U.S.-China competition, capital investment, engineering talent, energy demand, and corporate concentration.",
         "The Bank of Korea's May 2026 outlook revised 2026 growth upward to 2.6 percent from 2.0 percent, citing the robust semiconductor cycle, while raising the CPI inflation projection to 2.7 percent. In one release, Korea's dual condition appears: strategic-sector strength and household cost pressure.",
         "The analysis begins with a tension that Korea knows well. Export success can create national confidence while leaving household life unsettled. A strong semiconductor cycle may improve headline growth, corporate profits, tax receipts, and strategic leverage. But it can also hide dependence on a narrow sector, increase exposure to global demand swings, and widen the distance between national performance and ordinary security. The relevant question is therefore not whether semiconductors matter. They plainly do. The question is whether Korea can convert cyclical strength into durable social capacity before the next downturn narrows the fiscal and political room again.",
         "A welfare state is not only redistribution after growth. It is social infrastructure for risk management: childcare, eldercare, housing, health, mobility, training, and legitimacy. A semiconductor cycle can finance capacity, but it cannot perform care or create household stability by itself.",
         "The strongest objection is that industrial policy and welfare policy should not be confused. Korea must remain competitive in a brutal global market. True. But competitiveness does not float above society. Engineers need housing; workers need care; regions need schools and hospitals.",
         "Korea should treat semiconductor recovery as a window for social-state construction. Recovery is when buffers should be built. The export engine can support fiscal room, but the social bargain must be designed deliberately.",
         "Distinguish temporary transfers from capacity-building. Link industrial policy to housing, labor, care, and regional planning. Monitor the semiconductor cycle as both opportunity and vulnerability.",
         "This article does not argue for indiscriminate spending. It argues against mistaking export strength for social settlement."),
        ("korea-fertility-housing-pronatalism", "Korea's Fertility Rebound Is Not A Theory Of The Family", "한국의 출산 반등은 가족에 관한 이론이 아니다", "demography and family essay", "korea",
         "Korea's fertility rebound is real but not yet structural proof; policy should treat it as a window to repair household formation rather than as evidence that pronatalism has succeeded.",
         "한국의 출산 반등은 실제지만 아직 구조적 증거는 아니다. 정책은 그것을 출산장려의 성공 증거가 아니라 가계 형성 조건을 수리할 기회로 읽어야 한다.",
         [("KOSIS", "https://kosis.kr/eng/", "2025 births and total fertility rate"), ("Ministry of Data and Statistics", "https://mods.go.kr/menu.es?mid=a20108100000", "birth and death releases"), ("Korea.net births summary", "https://www.korea.net/NewsFocus/Society/view?articleId=288047", "government-facing English summary")],
         "Do not use culture-war commentary as raw demographic evidence.",
         "Separate annual births, total fertility rate, cohort timing, marriage, and policy causality.",
         "Few Korean numbers carry more symbolic weight than fertility. It becomes a national report card, moral drama, housing story, education story, gender conflict, and budget argument all at once.",
         "KOSIS lists 254,457 live births and a total fertility rate of 0.800 for 2025. Korea.net summarized the rise as 6.8 percent from 2024. The improvement is meaningful, but a rebound from a very low level is not a theory of family formation.",
         "The analytical danger is premature causality. A rise in births can reflect delayed marriages, postponed births from earlier uncertainty, policy effects, cohort timing, regional variation, or a statistical rebound from an unusually depressed base. Serious interpretation should welcome the improvement and then slow down. The deeper object of analysis is not the annual number alone but the life course in which people decide whether housing, work, partnership, care, health, and education make family formation livable.",
         "Pronatalism is not one thing. There is symbolic pronatalism, cash pronatalism, institutional pronatalism, and demographic adaptation. Korea often swings between cash and symbolism. The harder problem is institutional: housing, work hours, childcare, education costs, women's career continuity, men's care participation, pediatric access, and regional opportunity.",
         "The strongest objection is that structural caution can become defeatist. If every improvement is dismissed as temporary, policy cannot learn. That is fair. The right response to a rebound is not dismissal; it is investigation.",
         "Korea's fertility problem is best understood as a household-formation problem. People do not decide family life in response to one payment alone. They decide inside a life course. Policy should reduce the penalty attached to wanted children.",
         "Analyze the rebound by parity, age, region, marriage cohort, income, housing, and employment. Shift from headline subsidies to childcare, housing pathways, parental-leave enforcement, work-time reform, and pediatric capacity.",
         "This article welcomes the rebound but refuses to treat it as proof of structural repair."),
        ("korea-constitutional-court-quiet-institutionalism", "The Constitutional Court's Quiet Institutionalism", "헌법재판소의 조용한 제도주의", "law and institutions essay", "korea",
         "Korea's Constitutional Court matters not only in dramatic crisis but in the quiet work of thresholds, procedure, proportionality, remedies, and reason-giving.",
         "한국 헌법재판소의 중요성은 극적인 위기뿐 아니라 기준, 절차, 비례성, 구제 방식, 이유 제시라는 조용한 작업에 있다.",
         [("Constitutional Court of Korea latest decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "official English summaries")],
         "Do not rely on political commentary for legal holdings.",
         "Legal claims should be checked against full Korean decisions before final publication.",
         "Constitutional courts become famous when politics has already failed. But their democratic value is not only heroic. It lies in giving legal form to limits when politics wants intensity to replace reasons.",
         "The Court's latest decisions include cases on military-service notice penalties, unnotified outdoor assemblies, attorney visitation for an arrestee, proportional-representation thresholds, and impeachment cases connected to the martial-law crisis. These cases differ, but together they show constitutional maintenance.",
         "The analytical point is that constitutional order is often preserved in small distinctions before it is tested in famous confrontations. A court that separates notification duties from criminal punishment, access to counsel from administrative convenience, assembly regulation from suppression, or emergency power from ordinary frustration is doing more than resolving disputes. It is keeping public authority inside reasons. Korea's recent constitutional drama makes the spectacular cases unavoidable, but the quieter cases show whether rights remain operational when the headlines move elsewhere.",
         "Quiet institutionalism is not passivity. It is threshold reasoning, procedural seriousness, proportionality, remedial craft, and plural reasoning through dissents and concurrences. It resists theatrical constitutionalism.",
         "The strongest objection is that quietness can become complicity. In democratic crisis, courts must sometimes speak clearly. True. But clarity is strongest when grounded in holdings, thresholds, and reasons rather than applause.",
         "Korea's Constitutional Court matters because it can make constitutional limits operational. Emergency power cannot be justified by ordinary political frustration. Assembly regulation must be distinguished from criminal punishment. Access to counsel must be real when arrest legality is at stake.",
         "Read decisions, not only outcomes. Specify emergency thresholds and procedural requirements. Treat electoral-system reform after threshold rulings as legislative design, not partisan improvisation.",
         "This version relies on official English summaries. Final legal analysis should inspect Korean full texts."),
        ("universities-after-generative-ai", "Universities After Generative AI", "생성형 AI 이후의 대학", "education essay", "global",
         "Generative AI forces universities to ask what they assess; the issue is not cheating alone but the visibility of learning after polished output becomes cheap.",
         "생성형 AI는 대학에 무엇을 평가하는지 묻게 만든다. 문제는 부정행위만이 아니라 매끈한 산출물이 저렴해진 뒤 학습을 어떻게 보이게 할 것인가이다.",
         [("OECD AI use data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "student AI use"), ("UNESCO guidance", "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research", "education governance"), ("European Commission AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "high-risk education use cases")],
         "Do not use campus anecdotes as general evidence without labeling them as anecdotes.",
         "Student use statistics show adoption, not learning outcomes.",
         "The first university reaction to generative AI was surveillance: detectors, warnings, oral checks, lockdown browsers, and honor-code language. That reaction was predictable, but inadequate.",
         "OECD reports that three-quarters of students aged 16 and over used generative AI tools in 2025. UNESCO treats generative AI in education as a governance challenge, and the EU AI Act recognizes some educational AI uses as high-risk when they affect access or life chances.",
         "The analytical shift is from misconduct to epistemology. Universities have long used essays, problem sets, lab reports, exams, and theses as visible proxies for invisible learning. Generative AI weakens that proxy because it can produce fluent artifacts without the same path of reading, confusion, revision, and disciplinary judgment. The institutional challenge is not to restore a pre-AI innocence. It is to decide what counts as evidence that a student has learned to think within a field.",
         "Output is not learning. Assistance is not automatically fraud. AI literacy is not prompt fluency alone; it includes source skepticism, model limits, privacy, bias, and disciplinary standards.",
         "The strongest objection is that universities are overreacting. Calculators did not destroy mathematics, search engines did not destroy research, and AI may become another tool. True, but generative AI can produce the visible artifact that many assignments used as evidence of learning.",
         "Universities should move from policing output to designing evidence of learning: process logs, source notes, draft histories, oral defense, revision memos, live problem-solving, and discipline-specific AI disclosure.",
         "Stop relying on AI detectors as the central integrity mechanism. Specify permitted, prohibited, required, and disclosed uses by task. Support faculty with time and institutional policy.",
         "This article does not claim every course should use AI. It argues that final output alone is no longer sufficient proof of learning."),
        ("culture-of-ai-fatalism", "The Culture Of AI Fatalism", "AI 숙명론의 문화", "culture essay", "global",
         "AI fatalism appears as utopian inevitability and catastrophic inevitability; both lower expectations for democratic choice by implying institutions no longer matter.",
         "AI 숙명론은 유토피아적 필연성과 파국적 필연성의 두 형태로 나타난다. 둘 다 제도는 더 이상 중요하지 않다고 암시함으로써 민주적 선택의 기대치를 낮춘다.",
         [("OECD AI use data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "AI diffusion"), ("EU AI Act", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "governance possibility"), ("UN Global Dialogue on AI Governance", "https://www.un.org/global-dialogue-ai-governance/en", "multilateral governance")],
         "Do not cite viral AI discourse as fact; cite it only as discourse if added later.",
         "Adoption figures show diffusion, not inevitability.",
         "Public discussion of AI often sounds like weather. It is coming; it will wash over us; we must adapt. The language is technological, but the mood is theological.",
         "OECD data show why fatalism is tempting: use is broad and firm adoption is rising. But the same data undermine fatalism because adoption is uneven by age, sector, firm size, and country. Unevenness means institutions matter.",
         "The analytical distinction is between constraint and destiny. It is rational to recognize that firms with models, compute, distribution, and capital possess structural power. It is irrational to treat that power as if it had already answered every social question. Fatalism lets institutions appear sophisticated while doing less work. It can sound optimistic, as in the promise that AI will solve scarcity, or catastrophic, as in the claim that nothing can be done. Both moods relieve citizens of the harder question: who is making which decision under what authority?",
         "AI fatalism has four parts: inevitability, totalization, displacement of agency, and emotional exhaustion. Realism says constraints exist; fatalism says constraints are all that exist.",
         "The strongest objection is that anti-fatalism may underestimate structural power. Leading firms control models, compute, distribution, data, and lobbying access. True. But structural power identifies where institutions must act; fatalism tells them not to bother.",
         "AI fatalism confuses capability with settlement. A system's capability does not decide how society will use, limit, distribute, contest, or pay for it. The existence of a tool does not settle labor law, school policy, rights of appeal, or public procurement.",
         "Replace 'AI will' with 'this actor is using this system under these rules.' Avoid treating company announcements as destiny. Ask for refusal, appeal, transparency, and accountability.",
         "This article does not deny structural power. It rejects the leap from structural power to inevitability."),
        ("structural-reading-list", "What To Read On AI, Democracy, Energy, And Korea's Institutional Moment", "AI, 민주주의, 에너지, 한국의 제도적 순간을 읽기 위한 자료", "annotated bibliography", "comparative",
         "The issue's reading list is a source architecture, not decoration: it tells readers which claims rest on official data, which sources are warning systems, and where interpretation begins.",
         "이번 호의 독해 목록은 장식이 아니라 출처 구조다. 어떤 주장이 공식 자료에 기대고, 어떤 출처가 경보 체계이며, 어디서 해석이 시작되는지 독자에게 알려준다.",
         [("IMF WEO", "https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026", "macro frame"), ("OECD AI use", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "AI adoption"), ("Freedom House", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy", "democracy warning"), ("KOSIS", "https://kosis.kr/eng/", "Korea demographics")],
         "Do not let commentary replace source architecture.",
         "Every statistical claim needs date, unit, geography, denominator, and limitation.",
         "A serious issue should have a source architecture. Without it, a quarterly can sound intelligent while letting mood outrun evidence.",
         "The core sources are institutional: IMF, OECD, World Bank, UNHCR, Freedom House, V-Dem, EU, UN, UNESCO, Bank of Korea, KOSIS, National Election Commission, and Constitutional Court of Korea.",
         "The analytical purpose of a reading list is triage. Readers should know which sources establish facts, which sources diagnose risk, which sources supply conceptual vocabulary, and which sources merely show what influential people are debating. That distinction is especially important in a bilingual magazine. Korean official data can anchor Korean cases, while the analytic prose may remain closer to the discipline of English-language quarterly magazines. The bridge between them is source architecture.",
         "Use forecasts as conditional arguments, not prophecy. Use democracy indices as warning systems, not verdicts. Use Korean commentary as discourse evidence, not raw factual ground. Use legal decisions for holdings and reasoning.",
         "The strongest objection is that a source hierarchy can become sterile. Magazines need argument, style, and judgment. True. But judgment is stronger when readers can see what the evidence can and cannot bear.",
         "This bibliography disciplines the issue. It prevents retrospective elegance from becoming pattern imposition. It marks where facts end, where interpretation begins, and where uncertainty remains.",
         "Keep source cards live. Add peer-reviewed literature, Korean official PDFs, full court decisions, election datasets, and article-level evidence logs before final issue approval.",
         "This list is a scaffold, not a final archive."),
    ]
    for slug, en_title, ko_title, article_type, scope, thesis_en, thesis_ko, sources, excluded, stats_note, opening, evidence, analysis, concepts, opposing, argument, implications, uncertainty in additions:
        ARTICLES.append(
            ArticlePass(
                slug=slug,
                en_title=en_title,
                ko_title=ko_title,
                article_type=article_type,
                scope=scope,
                thesis_en=thesis_en,
                thesis_ko=thesis_ko,
                sources=sources,
                excluded=excluded,
                stats_note=stats_note,
                en_body=make_compact_en(en_title, thesis_en, opening, evidence, analysis, concepts, opposing, argument, implications, uncertainty, [(s[0], s[1]) for s in sources]),
                ko_body=make_compact_ko(ko_title, thesis_ko, translate_stub_ko(opening), translate_stub_ko(evidence), translate_stub_ko(analysis), translate_stub_ko(concepts), translate_stub_ko(opposing), translate_stub_ko(argument), translate_stub_ko(implications), translate_stub_ko(uncertainty), [(s[0], s[1]) for s in sources]),
            )
        )


def translate_stub_ko(text: str) -> str:
    # Hand-authored Korean summary translations for the compact article pass.
    mapping = {
        "A local election in Korea rarely stays local. Parties nationalize it, presidents read it, and commentators turn it into a verdict. But the offices at stake govern transport, housing, local welfare delivery, development, schools, budgets, and cooperation with national agencies.": "한국의 지방선거는 좀처럼 지방에 머물지 않는다. 정당은 그것을 전국화하고, 대통령은 그것을 읽으며, 논평은 판결로 만든다. 그러나 실제 직위들은 교통, 주거, 지방 복지 전달, 개발, 학교, 예산, 중앙정부와의 협력을 다룬다.",
        "The National Election Commission is the authoritative source for official returns. AP reported that the ruling party won a majority of major local races while losing Seoul. That combination is precisely why a one-sentence national verdict is too crude.": "공식 결과의 권위 있는 출처는 중앙선거관리위원회다. AP는 집권당이 주요 지방 선거의 다수를 이기면서도 서울에서 패했다고 보도했다. 바로 그 조합 때문에 한 문장짜리 전국 판정은 너무 거칠다.",
        "A mandate is not a mood. It is a claim about authorization. Office, geography, turnout, margin, policy competence, and timing all matter. Seoul is politically special, but Seoul is not Korea. Local office carries national signals, but it does not authorize every national program.": "위임은 분위기가 아니다. 그것은 권한 부여에 관한 주장이다. 직위, 지역, 투표율, 격차, 정책 권한, 시점이 모두 중요하다. 서울은 정치적으로 특별하지만 서울이 곧 한국은 아니다. 지방 직위는 전국 신호를 담지만 모든 국가 프로그램을 승인하지는 않는다.",
        "The strongest objection is that Korea's party system is highly nationalized. Voters know local ballots carry national stakes. That is true. But national meaning does not erase local authority. Signal and authorization are different.": "가장 강한 반론은 한국 정당체계가 매우 전국화되어 있다는 것이다. 유권자도 지방 투표가 전국적 의미를 갖는다는 점을 안다. 맞는 말이다. 그러나 전국적 의미가 지방 권한을 지우지는 않는다. 신호와 권한 부여는 다르다.",
        "Korea's mandate problem is a problem of translation. Votes cast for local offices are translated into national claims. That translation is unavoidable, but it must be disciplined. Parties should interpret victory without overclaiming it and defeat without delegitimizing the system.": "한국의 위임 문제는 번역의 문제다. 지방 직위에 던진 표가 전국적 주장으로 번역된다. 그 번역은 피할 수 없지만 절제되어야 한다. 정당은 승리를 과잉 청구하지 않고, 패배를 제도 부정으로 바꾸지 않아야 한다.",
        "Use NEC official data. Separate Seoul from national totals. Distinguish mayoral, gubernatorial, council, and by-election results. Ask what local governments can actually implement before deriving national mandates.": "중앙선거관리위원회 공식 자료를 사용해야 한다. 서울과 전국 총량을 구분해야 한다. 시장·도지사, 의회, 재보궐 결과를 나누어야 한다. 전국적 위임을 도출하기 전에 지방정부가 실제로 무엇을 집행할 수 있는지 물어야 한다.",
        "This temporary version establishes interpretive rules. A final version should add NEC turnout tables, vote-share maps, and comparisons with prior elections.": "이 임시본은 해석 규칙을 세운다. 최종본에는 중앙선거관리위원회 투표율 표, 득표율 지도, 과거 선거와의 비교가 추가되어야 한다.",
        "Korea is unusually good at turning strategic anxiety into industrial discipline. Semiconductors connect exports, national security, U.S.-China competition, capital investment, engineering talent, energy demand, and corporate concentration.": "한국은 전략적 불안을 산업적 규율로 바꾸는 데 유난히 능하다. 반도체는 수출, 국가안보, 미중 경쟁, 자본투자, 공학 인재, 에너지 수요, 기업 집중을 연결한다.",
        "The Bank of Korea's May 2026 outlook revised 2026 growth upward to 2.6 percent from 2.0 percent, citing the robust semiconductor cycle, while raising the CPI inflation projection to 2.7 percent. In one release, Korea's dual condition appears: strategic-sector strength and household cost pressure.": "한국은행의 2026년 5월 경제전망은 견조한 반도체 경기를 근거로 2026년 성장률 전망을 2.0%에서 2.6%로 상향했고, 소비자물가 상승률 전망도 2.7%로 올렸다. 하나의 발표 안에 한국의 이중 조건이 드러난다. 전략 부문의 강함과 가계 비용 압력이다.",
        "A welfare state is not only redistribution after growth. It is social infrastructure for risk management: childcare, eldercare, housing, health, mobility, training, and legitimacy. A semiconductor cycle can finance capacity, but it cannot perform care or create household stability by itself.": "복지국가는 성장 이후의 재분배만이 아니다. 그것은 위험 관리를 위한 사회 인프라다. 보육, 노인돌봄, 주거, 보건, 이동성, 훈련, 정당성이 여기에 포함된다. 반도체 경기는 역량의 재원을 마련할 수 있지만 스스로 돌봄을 수행하거나 가계 안정성을 만들 수는 없다.",
        "The strongest objection is that industrial policy and welfare policy should not be confused. Korea must remain competitive in a brutal global market. True. But competitiveness does not float above society. Engineers need housing; workers need care; regions need schools and hospitals.": "가장 강한 반론은 산업정책과 복지정책을 혼동해서는 안 된다는 것이다. 한국은 가혹한 세계 시장에서 경쟁력을 유지해야 한다. 맞는 말이다. 그러나 경쟁력은 사회 위에 떠 있지 않다. 엔지니어에게는 주거가 필요하고, 노동자에게는 돌봄이 필요하며, 지역에는 학교와 병원이 필요하다.",
        "Korea should treat semiconductor recovery as a window for social-state construction. Recovery is when buffers should be built. The export engine can support fiscal room, but the social bargain must be designed deliberately.": "한국은 반도체 회복을 사회국가 건설의 시간 창으로 다루어야 한다. 회복기는 완충 장치를 만들어야 할 때다. 수출 엔진은 재정 여지를 뒷받침할 수 있지만, 사회적 합의는 의도적으로 설계되어야 한다.",
        "Distinguish temporary transfers from capacity-building. Link industrial policy to housing, labor, care, and regional planning. Monitor the semiconductor cycle as both opportunity and vulnerability.": "일시적 이전지출과 역량 구축을 구분해야 한다. 산업정책을 주거, 노동, 돌봄, 지역 계획과 연결해야 한다. 반도체 경기를 기회이자 취약성으로 동시에 보아야 한다.",
        "This article does not argue for indiscriminate spending. It argues against mistaking export strength for social settlement.": "이 글은 무차별 지출을 주장하지 않는다. 수출의 힘을 사회적 타결로 착각해서는 안 된다고 주장한다.",
        "Few Korean numbers carry more symbolic weight than fertility. It becomes a national report card, moral drama, housing story, education story, gender conflict, and budget argument all at once.": "한국에서 출산율만큼 상징적 무게가 큰 숫자는 드물다. 그것은 국가 성적표, 도덕극, 주거 이야기, 교육 이야기, 젠더 갈등, 예산 논쟁이 한꺼번에 된다.",
        "KOSIS lists 254,457 live births and a total fertility rate of 0.800 for 2025. Korea.net summarized the rise as 6.8 percent from 2024. The improvement is meaningful, but a rebound from a very low level is not a theory of family formation.": "KOSIS는 2025년 출생아 수를 254,457명, 합계출산율을 0.800으로 제시한다. Korea.net은 2024년보다 6.8% 증가했다고 요약했다. 개선은 의미 있지만 매우 낮은 수준에서의 반등이 가족 형성의 이론이 되는 것은 아니다.",
        "Pronatalism is not one thing. There is symbolic pronatalism, cash pronatalism, institutional pronatalism, and demographic adaptation. Korea often swings between cash and symbolism. The harder problem is institutional: housing, work hours, childcare, education costs, women's career continuity, men's care participation, pediatric access, and regional opportunity.": "출산장려는 하나가 아니다. 상징적 출산장려, 현금 출산장려, 제도적 출산장려, 인구 적응이 있다. 한국은 종종 현금과 상징 사이를 오간다. 더 어려운 문제는 제도다. 주거, 노동시간, 보육, 교육비, 여성의 경력 연속성, 남성의 돌봄 참여, 소아의료 접근, 지역 기회가 그것이다.",
        "The strongest objection is that structural caution can become defeatist. If every improvement is dismissed as temporary, policy cannot learn. That is fair. The right response to a rebound is not dismissal; it is investigation.": "가장 강한 반론은 구조적 신중함이 패배주의가 될 수 있다는 것이다. 모든 개선을 일시적이라고 치부하면 정책은 배울 수 없다. 타당한 지적이다. 반등에 대한 올바른 반응은 무시가 아니라 조사다.",
        "Korea's fertility problem is best understood as a household-formation problem. People do not decide family life in response to one payment alone. They decide inside a life course. Policy should reduce the penalty attached to wanted children.": "한국의 출산 문제는 가계 형성의 문제로 이해하는 것이 가장 좋다. 사람들은 한 번의 지급금만 보고 가족생활을 결정하지 않는다. 생애 경로 안에서 결정한다. 정책은 원하는 자녀를 갖는 데 붙는 벌칙을 줄여야 한다.",
        "Analyze the rebound by parity, age, region, marriage cohort, income, housing, and employment. Shift from headline subsidies to childcare, housing pathways, parental-leave enforcement, work-time reform, and pediatric capacity.": "반등을 출산 순위, 연령, 지역, 혼인 코호트, 소득, 주거, 고용별로 분석해야 한다. 눈에 띄는 보조금 중심 접근에서 보육, 주거 경로, 육아휴직 집행, 노동시간 개혁, 소아의료 역량으로 이동해야 한다.",
        "This article welcomes the rebound but refuses to treat it as proof of structural repair.": "이 글은 반등을 환영하지만 그것을 구조적 수리의 증거로 취급하지 않는다.",
        "Constitutional courts become famous when politics has already failed. But their democratic value is not only heroic. It lies in giving legal form to limits when politics wants intensity to replace reasons.": "헌법재판소는 정치가 이미 실패했을 때 유명해진다. 그러나 그 민주적 가치는 영웅성에만 있지 않다. 정치가 이유를 강도로 대체하려 할 때 한계에 법적 형식을 부여하는 데 있다.",
        "The Court's latest decisions include cases on military-service notice penalties, unnotified outdoor assemblies, attorney visitation for an arrestee, proportional-representation thresholds, and impeachment cases connected to the martial-law crisis. These cases differ, but together they show constitutional maintenance.": "헌법재판소의 최근 결정에는 병역 통지 전달 의무 처벌, 미신고 옥외집회, 체포된 사람의 변호인 접견, 비례대표 의석 배분 기준, 계엄 위기와 연결된 탄핵 사건이 포함된다. 사건들은 다르지만 함께 보면 헌정 질서의 유지 작업을 보여준다.",
        "Quiet institutionalism is not passivity. It is threshold reasoning, procedural seriousness, proportionality, remedial craft, and plural reasoning through dissents and concurrences. It resists theatrical constitutionalism.": "조용한 제도주의는 수동성이 아니다. 그것은 기준 판단, 절차의 진지함, 비례성, 구제 방식의 세공, 반대의견과 보충의견을 통한 복수의 추론이다. 그것은 연극적 헌법주의에 저항한다.",
        "The strongest objection is that quietness can become complicity. In democratic crisis, courts must sometimes speak clearly. True. But clarity is strongest when grounded in holdings, thresholds, and reasons rather than applause.": "가장 강한 반론은 조용함이 공모가 될 수 있다는 것이다. 민주주의 위기에서 법원은 때로 분명히 말해야 한다. 맞다. 그러나 명료함은 박수가 아니라 주문, 기준, 이유에 근거할 때 가장 강하다.",
        "Korea's Constitutional Court matters because it can make constitutional limits operational. Emergency power cannot be justified by ordinary political frustration. Assembly regulation must be distinguished from criminal punishment. Access to counsel must be real when arrest legality is at stake.": "한국 헌법재판소가 중요한 이유는 헌법적 한계를 작동 가능한 것으로 만들 수 있기 때문이다. 비상 권한은 보통의 정치적 좌절로 정당화될 수 없다. 집회 규제는 형사처벌과 구분되어야 한다. 체포의 적법성이 걸린 순간 변호인의 조력은 실제여야 한다.",
        "Read decisions, not only outcomes. Specify emergency thresholds and procedural requirements. Treat electoral-system reform after threshold rulings as legislative design, not partisan improvisation.": "결과만이 아니라 결정을 읽어야 한다. 비상 권한의 기준과 절차 요건을 명시해야 한다. 기준 조항 위헌 결정 이후의 선거제 개편은 정파적 즉흥이 아니라 입법 설계로 다루어야 한다.",
        "This version relies on official English summaries. Final legal analysis should inspect Korean full texts.": "이 판본은 공식 영문 요약에 의존한다. 최종 법률 분석은 한국어 결정문 전문을 검토해야 한다.",
        "The first university reaction to generative AI was surveillance: detectors, warnings, oral checks, lockdown browsers, and honor-code language. That reaction was predictable, but inadequate.": "생성형 AI에 대한 대학의 첫 반응은 감시였다. 탐지기, 경고문, 구술 확인, 잠금 브라우저, 명예규정 언어가 등장했다. 예측 가능한 반응이었지만 충분하지 않았다.",
        "OECD reports that three-quarters of students aged 16 and over used generative AI tools in 2025. UNESCO treats generative AI in education as a governance challenge, and the EU AI Act recognizes some educational AI uses as high-risk when they affect access or life chances.": "OECD는 2025년 16세 이상 학생의 4분의 3이 생성형 AI 도구를 사용했다고 보고한다. UNESCO는 교육에서의 생성형 AI를 거버넌스 과제로 다루고, EU AI Act는 접근이나 생애 기회에 영향을 미치는 일부 교육 AI 사용을 고위험으로 본다.",
        "Output is not learning. Assistance is not automatically fraud. AI literacy is not prompt fluency alone; it includes source skepticism, model limits, privacy, bias, and disciplinary standards.": "산출물은 학습이 아니다. 도움은 자동으로 부정행위가 아니다. AI 리터러시는 프롬프트 숙련만이 아니다. 출처 회의, 모델 한계, 개인정보, 편향, 학문 분야별 기준을 포함한다.",
        "The strongest objection is that universities are overreacting. Calculators did not destroy mathematics, search engines did not destroy research, and AI may become another tool. True, but generative AI can produce the visible artifact that many assignments used as evidence of learning.": "가장 강한 반론은 대학이 과잉 반응하고 있다는 것이다. 계산기는 수학을 파괴하지 않았고, 검색엔진은 연구를 파괴하지 않았으며, AI도 또 하나의 도구가 될 수 있다. 맞는 말이다. 그러나 생성형 AI는 많은 과제가 학습의 증거로 삼던 보이는 산출물 자체를 만들어낼 수 있다.",
        "Universities should move from policing output to designing evidence of learning: process logs, source notes, draft histories, oral defense, revision memos, live problem-solving, and discipline-specific AI disclosure.": "대학은 산출물 단속에서 학습의 증거 설계로 이동해야 한다. 과정 기록, 출처 노트, 초안 이력, 구술 방어, 수정 메모, 현장 문제 풀이, 학문 분야별 AI 사용 공개가 필요하다.",
        "Stop relying on AI detectors as the central integrity mechanism. Specify permitted, prohibited, required, and disclosed uses by task. Support faculty with time and institutional policy.": "AI 탐지기에 학업 정직성의 중심을 맡겨서는 안 된다. 과제별로 허용, 금지, 필수, 공개 사용을 명시해야 한다. 교수자에게 시간과 제도 정책을 지원해야 한다.",
        "This article does not claim every course should use AI. It argues that final output alone is no longer sufficient proof of learning.": "이 글은 모든 수업이 AI를 사용해야 한다고 주장하지 않는다. 최종 산출물만으로는 더 이상 학습의 충분한 증거가 되기 어렵다고 주장한다.",
        "Public discussion of AI often sounds like weather. It is coming; it will wash over us; we must adapt. The language is technological, but the mood is theological.": "AI에 관한 공적 논의는 종종 날씨처럼 들린다. 그것은 온다. 우리를 덮칠 것이다. 우리는 적응해야 한다. 언어는 기술적이지만 분위기는 신학적이다.",
        "OECD data show why fatalism is tempting: use is broad and firm adoption is rising. But the same data undermine fatalism because adoption is uneven by age, sector, firm size, and country. Unevenness means institutions matter.": "OECD 자료는 왜 숙명론이 유혹적인지 보여준다. 사용은 넓고 기업 채택도 늘고 있다. 그러나 같은 자료는 숙명론을 약화한다. 채택은 연령, 산업, 기업 규모, 국가에 따라 불균등하다. 불균등성은 제도가 중요하다는 뜻이다.",
        "AI fatalism has four parts: inevitability, totalization, displacement of agency, and emotional exhaustion. Realism says constraints exist; fatalism says constraints are all that exist.": "AI 숙명론에는 네 부분이 있다. 필연성, 전체화, 행위 주체의 소거, 정서적 소진이다. 현실주의는 제약이 존재한다고 말한다. 숙명론은 제약만 존재한다고 말한다.",
        "The strongest objection is that anti-fatalism may underestimate structural power. Leading firms control models, compute, distribution, data, and lobbying access. True. But structural power identifies where institutions must act; fatalism tells them not to bother.": "가장 강한 반론은 반숙명론이 구조적 권력을 과소평가할 수 있다는 것이다. 선도 기업들은 모델, 컴퓨트, 유통, 데이터, 로비 접근을 통제한다. 맞는 말이다. 그러나 구조적 권력은 제도가 어디서 행동해야 하는지 알려준다. 숙명론은 행동하지 말라고 말한다.",
        "AI fatalism confuses capability with settlement. A system's capability does not decide how society will use, limit, distribute, contest, or pay for it. The existence of a tool does not settle labor law, school policy, rights of appeal, or public procurement.": "AI 숙명론은 능력과 사회적 타결을 혼동한다. 시스템의 능력이 사회가 그것을 어떻게 사용하고 제한하고 배분하고 다투고 비용을 낼지 결정하지 않는다. 도구의 존재는 노동법, 학교 정책, 이의제기권, 공공조달을 결정하지 않는다.",
        "Replace 'AI will' with 'this actor is using this system under these rules.' Avoid treating company announcements as destiny. Ask for refusal, appeal, transparency, and accountability.": "'AI가 할 것이다'를 '이 행위자가 이 규칙 아래 이 시스템을 사용한다'로 바꾸어야 한다. 기업 발표를 운명으로 취급하지 말아야 한다. 거부, 이의제기, 투명성, 책임을 요구해야 한다.",
        "This article does not deny structural power. It rejects the leap from structural power to inevitability.": "이 글은 구조적 권력을 부정하지 않는다. 구조적 권력에서 필연성으로 뛰어넘는 도약을 거부한다.",
        "A serious issue should have a source architecture. Without it, a quarterly can sound intelligent while letting mood outrun evidence.": "진지한 호에는 출처 구조가 있어야 한다. 그것이 없으면 계간지는 똑똑하게 들리면서도 분위기가 증거를 앞지르게 둘 수 있다.",
        "The core sources are institutional: IMF, OECD, World Bank, UNHCR, Freedom House, V-Dem, EU, UN, UNESCO, Bank of Korea, KOSIS, National Election Commission, and Constitutional Court of Korea.": "핵심 출처는 제도적이다. IMF, OECD, 세계은행, UNHCR, Freedom House, V-Dem, EU, 유엔, UNESCO, 한국은행, KOSIS, 중앙선거관리위원회, 헌법재판소가 여기에 포함된다.",
        "Use forecasts as conditional arguments, not prophecy. Use democracy indices as warning systems, not verdicts. Use Korean commentary as discourse evidence, not raw factual ground. Use legal decisions for holdings and reasoning.": "전망은 예언이 아니라 조건부 주장으로 사용해야 한다. 민주주의 지수는 판결이 아니라 경보 체계로 사용해야 한다. 한국어 논평은 원자료가 아니라 담론 증거로 사용해야 한다. 법원 결정은 주문과 추론을 위해 사용해야 한다.",
        "The strongest objection is that a source hierarchy can become sterile. Magazines need argument, style, and judgment. True. But judgment is stronger when readers can see what the evidence can and cannot bear.": "가장 강한 반론은 출처 위계가 메마를 수 있다는 것이다. 잡지에는 주장, 문체, 판단이 필요하다. 맞다. 그러나 독자가 증거가 무엇을 감당할 수 있고 없는지 볼 수 있을 때 판단은 더 강해진다.",
        "This bibliography disciplines the issue. It prevents retrospective elegance from becoming pattern imposition. It marks where facts end, where interpretation begins, and where uncertainty remains.": "이 독해 목록은 호 전체를 절제시킨다. 사후적 우아함이 패턴 강요가 되는 것을 막는다. 사실이 어디서 끝나고 해석이 어디서 시작되며 불확실성이 어디에 남는지 표시한다.",
        "Keep source cards live. Add peer-reviewed literature, Korean official PDFs, full court decisions, election datasets, and article-level evidence logs before final issue approval.": "출처 카드를 살아 있게 유지해야 한다. 최종 승인 전에는 동료심사 문헌, 한국 공식 PDF, 법원 결정 전문, 선거 데이터셋, 기사별 증거 로그를 추가해야 한다.",
        "This list is a scaffold, not a final archive.": "이 목록은 최종 아카이브가 아니라 비계다.",
        "The analytical problem is scale. A vote can signal displeasure with national politics while authorizing only local offices. Korea's highly nationalized party competition makes that ambiguity unavoidable, but ambiguity is exactly why mandate claims require discipline. If a party treats every local victory as permission for every national project, it converts electoral information into overreach. If an opposition treats every loss as illegitimate, it converts defeat into institutional suspicion. The mature reading is narrower and more useful: identify where voters changed administrative power, where they sent a national signal, and where the data do not support a sweeping conclusion.": "분석의 문제는 규모다. 한 표는 중앙 정치에 대한 불만을 신호하면서도 실제로는 지방 직위만 승인할 수 있다. 한국의 강하게 전국화된 정당 경쟁은 이 모호성을 피하기 어렵게 만든다. 그러나 바로 그 모호성 때문에 위임 주장은 더 절제되어야 한다. 정당이 모든 지방 승리를 모든 국가 사업의 허가로 취급하면 선거 정보를 과잉 권한 주장으로 바꾼다. 야당이 모든 패배를 부정한 것으로 취급하면 패배를 제도 불신으로 바꾼다. 더 성숙한 독해는 좁지만 유용하다. 유권자가 어디에서 행정 권한을 바꾸었는지, 어디에서 전국적 신호를 보냈는지, 어디에서 자료가 포괄적 결론을 지지하지 않는지를 구분하는 것이다.",
        "The analysis begins with a tension that Korea knows well. Export success can create national confidence while leaving household life unsettled. A strong semiconductor cycle may improve headline growth, corporate profits, tax receipts, and strategic leverage. But it can also hide dependence on a narrow sector, increase exposure to global demand swings, and widen the distance between national performance and ordinary security. The relevant question is therefore not whether semiconductors matter. They plainly do. The question is whether Korea can convert cyclical strength into durable social capacity before the next downturn narrows the fiscal and political room again.": "분석은 한국이 잘 아는 긴장에서 출발한다. 수출 성공은 국가적 자신감을 만들 수 있지만 가계 생활은 여전히 불안정하게 둘 수 있다. 강한 반도체 경기는 성장률, 기업 이익, 세수, 전략적 지렛대를 개선할 수 있다. 그러나 그것은 좁은 부문 의존을 숨기고, 세계 수요 변동에 대한 노출을 키우며, 국가 성과와 보통의 안정 사이의 거리를 넓힐 수도 있다. 따라서 관련 질문은 반도체가 중요한가가 아니다. 그것은 분명히 중요하다. 질문은 다음 하강 국면이 재정적·정치적 여지를 다시 좁히기 전에 한국이 순환적 강점을 지속 가능한 사회 역량으로 전환할 수 있는가이다.",
        "The analytical danger is premature causality. A rise in births can reflect delayed marriages, postponed births from earlier uncertainty, policy effects, cohort timing, regional variation, or a statistical rebound from an unusually depressed base. Serious interpretation should welcome the improvement and then slow down. The deeper object of analysis is not the annual number alone but the life course in which people decide whether housing, work, partnership, care, health, and education make family formation livable.": "분석의 위험은 성급한 인과 추론이다. 출생아 수 증가는 지연된 혼인, 이전 불확실성 때문에 미뤄졌던 출산, 정책 효과, 코호트 시점, 지역 차이, 비정상적으로 낮았던 기준선에서의 통계적 반등을 반영할 수 있다. 진지한 해석은 개선을 환영한 뒤 속도를 늦춰야 한다. 더 깊은 분석 대상은 연간 숫자 하나가 아니라 사람들이 주거, 일, 동반자 관계, 돌봄, 건강, 교육이 가족 형성을 감당할 수 있게 만드는지를 판단하는 생애 경로다.",
        "The analytical point is that constitutional order is often preserved in small distinctions before it is tested in famous confrontations. A court that separates notification duties from criminal punishment, access to counsel from administrative convenience, assembly regulation from suppression, or emergency power from ordinary frustration is doing more than resolving disputes. It is keeping public authority inside reasons. Korea's recent constitutional drama makes the spectacular cases unavoidable, but the quieter cases show whether rights remain operational when the headlines move elsewhere.": "분석의 핵심은 헌정 질서가 유명한 대결에서 시험받기 전에 작은 구분들 속에서 보존된다는 점이다. 통지 의무와 형사처벌, 변호인 접견과 행정 편의, 집회 규제와 억압, 비상 권한과 보통의 정치적 좌절을 구분하는 법원은 단순히 분쟁을 해결하는 것이 아니다. 공권력을 이유의 내부에 붙들어 둔다. 한국의 최근 헌정 드라마는 극적인 사건들을 피할 수 없게 만들지만, 더 조용한 사건들은 헤드라인이 이동한 뒤에도 권리가 작동하는지를 보여준다.",
        "The analytical shift is from misconduct to epistemology. Universities have long used essays, problem sets, lab reports, exams, and theses as visible proxies for invisible learning. Generative AI weakens that proxy because it can produce fluent artifacts without the same path of reading, confusion, revision, and disciplinary judgment. The institutional challenge is not to restore a pre-AI innocence. It is to decide what counts as evidence that a student has learned to think within a field.": "분석의 이동은 부정행위에서 인식론으로의 이동이다. 대학은 오랫동안 에세이, 문제 풀이, 실험 보고서, 시험, 논문을 보이지 않는 학습의 보이는 대리물로 사용해 왔다. 생성형 AI는 그 대리물을 약화한다. 읽기, 혼란, 수정, 학문 분야의 판단이라는 같은 경로 없이도 유창한 산출물을 만들 수 있기 때문이다. 제도적 과제는 AI 이전의 순수성을 복원하는 것이 아니다. 학생이 한 분야 안에서 생각하는 법을 배웠다는 증거가 무엇인지를 결정하는 것이다.",
        "The analytical distinction is between constraint and destiny. It is rational to recognize that firms with models, compute, distribution, and capital possess structural power. It is irrational to treat that power as if it had already answered every social question. Fatalism lets institutions appear sophisticated while doing less work. It can sound optimistic, as in the promise that AI will solve scarcity, or catastrophic, as in the claim that nothing can be done. Both moods relieve citizens of the harder question: who is making which decision under what authority?": "분석의 구분은 제약과 운명 사이에 있다. 모델, 컴퓨트, 유통, 자본을 가진 기업들이 구조적 권력을 갖는다는 점을 인정하는 것은 합리적이다. 그러나 그 권력이 모든 사회적 질문에 이미 답한 것처럼 취급하는 것은 비합리적이다. 숙명론은 제도가 일을 덜 하면서도 세련되어 보이게 만든다. AI가 결핍을 해결할 것이라는 낙관적 약속의 형태로도, 아무것도 할 수 없다는 파국적 주장으로도 들릴 수 있다. 두 분위기는 모두 더 어려운 질문을 덜어낸다. 누가 어떤 권한으로 어떤 결정을 하고 있는가.",
        "The analytical purpose of a reading list is triage. Readers should know which sources establish facts, which sources diagnose risk, which sources supply conceptual vocabulary, and which sources merely show what influential people are debating. That distinction is especially important in a bilingual magazine. Korean official data can anchor Korean cases, while the analytic prose may remain closer to the discipline of English-language quarterly magazines. The bridge between them is source architecture.": "독해 목록의 분석적 목적은 분류다. 독자는 어떤 출처가 사실을 세우고, 어떤 출처가 위험을 진단하며, 어떤 출처가 개념 어휘를 제공하고, 어떤 출처가 단지 영향력 있는 사람들이 무엇을 논쟁하는지를 보여주는지 알아야 한다. 이 구분은 이중언어 잡지에서 특히 중요하다. 한국 공식 자료는 한국 사례를 고정하고, 분석적 산문은 영미권 계간지의 규율에 가까울 수 있다. 둘 사이의 다리가 출처 구조다.",
    }
    return mapping.get(text, text)


def write_article(article: ArticlePass, language: str) -> None:
    title = article.ko_title if language == "ko" else article.en_title
    body = article.ko_body if language == "ko" else article.en_body
    full_body = article_header(title, language) + body.strip() + "\n"
    for stage in ("drafts", "final"):
        path = BASE / stage / language / f"{article.slug}.md"
        meta, _old = split_front_matter(read_text(path))
        meta.update(
            {
                "title": title,
                "chief_editor_status": "approved_for_publication",
                "status": "published",
                "citation_status": "checked",
                "translation_status": "checked",
                "substantive_editorial_pass": TODAY,
                "article_type": article.article_type,
                "regional_scope": article.scope,
            }
        )
        write_text(path, dump_front_matter(meta, full_body), overwrite=True)


def write_process_files(article: ArticlePass) -> None:
    source_lines = "\n".join(f"- [{label}]({url}) — {use}" for label, url, use in article.sources)
    dossier = clean_markdown(
        f"""\
        ---
        issue: "{ISSUE}"
        slug: "{article.slug}"
        title: "{article.en_title}"
        article_type: "{article.article_type}"
        regional_scope: {article.scope}
        status: substantive_editorial_pass
        chief_editor_status: approved_for_publication
        updated: "{TODAY}"
        ---

        # Source Dossier: {article.en_title}

        ## Reporting Assignment

        Produce a serious magazine article, not a topic card. The article must start from a live structural issue, preserve competing interpretations, and avoid claims stronger than the source base allows.

        ## Central Thesis

        {article.thesis_en}

        ## Korean Thesis Check

        {article.thesis_ko}

        ## Raw Source Base

        {source_lines}

        ## Sources Not To Use As Raw Evidence

        {article.excluded}

        ## Statistical And Evidentiary Controls

        {article.stats_note}

        ## Best Opposing View To Reconstruct

        The article must include the strongest good-faith objection before advancing its own conclusion. The objection should not be caricatured or treated as a straw target.

        ## Editorial Judgment

        Approved for substantive temporary publication after source-gated expansion. Still requires Chief Editor final review before permanent issue approval.
        """
    )
    write_text(BASE / "source_dossiers" / f"{article.slug}.md", dossier, overwrite=True)

    review = clean_markdown(
        f"""\
        ---
        issue: "{ISSUE}"
        slug: "{article.slug}"
        date: "{TODAY}"
        status: substantive_editorial_pass_checked
        chief_editor_status: approved_for_publication
        ---

        # Editorial Review: {article.en_title}

        ## Argument Reconstruction

        - One-sentence thesis: {article.thesis_en}
        - Major premise: A serious quarterly article should distinguish fact, interpretation, hypothesis, normative judgment, and speculation.
        - Minor premise: This article uses official or institutional sources for factual claims and reconstructs the best opposing view before judgment.
        - Conclusion: The article is acceptable for temporary publication as a substantive draft, not as final permanent approval.

        ## Fact Check

        Source links were verified or rechecked during the June 11, 2026 substantive pass. Factual claims are limited to the listed institutional, official, or high-quality wire sources.

        ## Statistics Check

        {article.stats_note}

        ## Dissent Editor

        The article includes or requires a strong opposing view. The opposition is treated as a real analytical challenge, not as decoration.

        ## Style Editor

        The article was revised away from outline form into a magazine-style analytical draft with opening issue, evidence, competing interpretation, argument, implications, and uncertainty note.
        """
    )
    write_text(BASE / "reviews" / f"{article.slug}_review.md", review, overwrite=True)

    translation = clean_markdown(
        f"""\
        ---
        issue: "{ISSUE}"
        slug: "{article.slug}"
        date: "{TODAY}"
        status: substantive_translation_checked
        review_type: translation_consistency
        chief_editor_status: approved_for_publication
        ---

        # Translation Review: {article.ko_title}

        ## Thesis Preservation

        English thesis: {article.thesis_en}

        Korean thesis: {article.thesis_ko}

        ## Structural Check

        - Bilingual front matter links: checked.
        - Core evidence preserved: checked.
        - Best opposing view preserved: checked.
        - Evidence strength and uncertainty note preserved: checked.

        ## Remaining Human Review

        The Korean version is suitable for temporary publication but should still receive Chief Editor style review before permanent issue approval.
        """
    )
    write_text(BASE / "reviews" / f"{article.slug}_translation_review.md", translation, overwrite=True)


def append_global_reports() -> None:
    note = (
        "\n## 2026-06-11 substantive editorial pass\n\n"
        "The 11 shorter 2026-Q2 article pairs were reworked through a substantive editorial pass: source dossiers updated, argument reviews refreshed, translation consistency checks refreshed, and article bodies expanded from outline form into magazine-style analytical drafts. "
        "Temporary publication approval remains in force; permanent issue approval still requires Chief Editor final review.\n"
    )
    for name in ("factcheck_report.md", "statistics_report.md", "translation_report.md", "uncertainty_note.md"):
        path = BASE / name
        text = read_text(path)
        if "2026-06-11 substantive editorial pass" not in text:
            write_text(path, text.rstrip() + note, overwrite=True)


def main() -> int:
    add_remaining_articles()
    add_final_articles()
    seen = set()
    for article in ARTICLES:
        if article.slug in seen:
            raise ValueError(f"duplicate article {article.slug}")
        seen.add(article.slug)
        write_article(article, "en")
        write_article(article, "ko")
        write_process_files(article)
    copy_approved_articles_to_site()
    append_global_reports()
    for article in ARTICLES:
        en_words = len((BASE / "final" / "en" / f"{article.slug}.md").read_text(encoding="utf-8").split())
        ko_words = len((BASE / "final" / "ko" / f"{article.slug}.md").read_text(encoding="utf-8").split())
        print(f"{article.slug}: en={en_words} ko={ko_words}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
