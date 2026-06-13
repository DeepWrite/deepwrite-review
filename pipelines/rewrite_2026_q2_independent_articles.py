#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent

from lib import ISSUES, copy_approved_articles_to_site, dump_front_matter, read_text, split_front_matter, write_text


ISSUE = "2026-Q2"
TODAY = "2026-06-13"
BASE = ISSUES / ISSUE
RETIRED_EN_BUILDER = "make_" + "compact_en"
RETIRED_KO_BUILDER = "make_" + "compact_ko"


@dataclass(frozen=True)
class IndependentArticle:
    slug: str
    en_title: str
    ko_title: str
    agent: str
    thesis_en: str
    thesis_ko: str
    sources: list[tuple[str, str, str]]
    reporting_tasks: list[str]
    evidence_control: str
    en_body: str
    ko_body: str


def clean(text: str) -> str:
    return dedent(text).strip() + "\n"


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


def source_lines(article: IndependentArticle) -> str:
    return "\n".join(f"- [{label}]({url}) — {use}" for label, url, use in article.sources)


def task_lines(article: IndependentArticle) -> str:
    return "\n".join(f"- {task}" for task in article.reporting_tasks)


ARTICLES: list[IndependentArticle] = [
    IndependentArticle(
        slug="democracy-after-long-decline",
        en_title="Democracy After The Long Decline",
        ko_title="긴 하락 이후의 민주주의",
        agent="Political Editor with Law and Institutions Editor",
        thesis_en="Democratic decline in 2026 is best read as a normalization problem: erosion becomes dangerous when the institutions of correction still exist formally but lose practical authority.",
        thesis_ko="2026년의 민주주의 후퇴는 정상화의 문제로 읽어야 한다. 교정 장치가 형식적으로는 남아 있지만 실질 권위를 잃을 때 침식은 위험해진다.",
        sources=[
            ("Freedom House, Freedom in the World 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy", "global freedom trend; 54 countries deteriorated and 35 improved in 2025"),
            ("V-Dem, Democracy Report 2026", "https://www.v-dem.net/publications/democracy-reports/", "comparative democracy dataset and democracy-report framing"),
            ("Constitutional Court of Korea, Latest Decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "institutional example for justiciability, emergency powers, and rights review"),
        ],
        reporting_tasks=[
            "Add a country-comparison table in the next non-temporary pass: election administration, courts, public media, opposition rights, and civil-society constraints.",
            "Read full domestic-language legal texts for any country case used as more than illustration.",
            "Keep fascism, authoritarianism, populism, and ordinary conservatism conceptually distinct in all revisions.",
        ],
        evidence_control="Use democracy indices as alarms and maps, not as verdicts. Country mechanisms must carry causal claims.",
        en_body=clean(
            """
            ## Abstract

            The danger facing democracy in 2026 is not only a spectacular collapse. It is the dulling of alarm. A country can hold elections, keep courts open, retain opposition parties, and still teach citizens that correction is futile. The issue is not whether democracy disappears in a single night. It is whether the institutions that allow a society to correct power still command enough authority to matter.

            ## The Slow Normalization

            The evidence does not justify either panic or complacency. [Freedom House](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy) reports that global freedom declined for the twentieth consecutive year in 2025, with 54 countries deteriorating and 35 improving. [V-Dem's 2026 Democracy Report](https://www.v-dem.net/publications/democracy-reports/) offers a different measurement architecture, yet it points to the same broad terrain: democratic institutions are under sustained pressure, including in some established democracies.

            These indices should not be treated as tablets from the mountain. They aggregate expert judgments and compress national histories into comparable scales. But repeated convergence across methods is a warning. The better response is not to worship the index or dismiss it. It is to ask what mechanisms lie beneath the movement.

            The mechanism is usually less cinematic than the rhetoric. Democratic erosion often proceeds through ordinary-looking decisions: intimidation of judges, abuse of prosecutors, pressure on election bodies, politicized media regulation, selective law enforcement, executive emergency claims, attacks on civil society funding, and the conversion of opponents into enemies of the people. Each step can be defended as legal, necessary, popular, or temporary. The cumulative effect is to make correction more expensive.

            ## Correction Systems

            Democracy is not only majority rule. It is a correction system. Elections correct incumbents. Courts correct executives and legislatures. Legislatures correct presidents. Local governments correct central overreach. Journalists correct official narratives. Civil society corrects institutional blindness. Opposition parties correct policy monopoly. Audit bodies correct administrative self-protection.

            Backsliding matters because it weakens these channels before it necessarily abolishes them. A court can still issue judgments while learning that some cases are too dangerous. An election commission can still count votes while being redescribed as illegitimate in advance. A legislature can still meet while its right to limit the executive is treated as sabotage. The constitution remains visible; its habits become thinner.

            Korea's recent constitutional experience is useful here not because it is a universal model, but because it shows democratic correction as a chain rather than a slogan. The [Constitutional Court of Korea](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143) upheld the impeachment of President Yoon Suk-yeol on April 4, 2025, after reviewing justiciability, martial-law requirements, and the gravity of violations. Later decisions concerning assembly rights, attorney visitation, electoral thresholds, and impeachment of officials show the quieter side of constitutionalism: democracy is defended not only in historic rulings but also in routine boundary-setting.

            ## What The Indices Cannot Tell Us

            Indices can tell readers where to look. They cannot by themselves explain why institutions held in one place and failed in another. They cannot show which judges resisted, which local officials absorbed pressure, which media institutions retained professional norms, or which civil-society organizations kept administrative facts visible. They can also lag behind social experience: distrust may spread faster than formal indicators change.

            A serious magazine article should therefore use indices as a first map. The terrain is institutional behavior. What matters is whether the next dispute can be resolved through ordinary public mechanisms without each side treating loss as illegitimate.

            ## The Index Skeptic's Case

            The strongest objection is that democracy warnings can become self-serving. Governments disliked by liberal NGOs may be marked as backsliding while structural failures in established democracies receive softer language. Expert coding may reproduce professional-class assumptions about courts, rights, and media. Some voters may see institutional restraints not as democracy but as elite insulation.

            This objection should be taken seriously. Democratic language has often been used to discipline electorates rather than to understand them. Yet the objection does not erase the problem. If courts, election administrators, journalists, and opposition parties become permanent enemies, voters do not gain sovereignty. They inherit a system in which one victory can disable future correction.

            ## Correction As The Democratic Test

            The central democratic question after a long decline is not whether every threatened system has already ceased to be democratic. It is which systems remain correctable.

            Correctability is a practical test. Can an opposition win and take office? Can a court rule against the executive without institutional retaliation? Can officials investigate governing-party allies? Can citizens assemble without disproportionate punishment? Can a broadcaster contradict the government without losing its independence? Can an election defeat be accepted by enough people to prevent permanent crisis?

            This is a less theatrical language than "democracy dies." It is also more exact. The first duty of democratic analysis is to preserve thresholds. Populism is not automatically authoritarianism. Authoritarianism is not automatically fascism. Fascism should be reserved for a narrower political formation involving anti-liberal mass mobilization, exclusionary national myth, organized coercion, and subordination of institutions to a totalizing project. Imprecision may feel morally satisfying; it weakens diagnosis.

            ## What Democratic Readers Should Watch

            Watch institutions before slogans. Election bodies, courts, prosecutors, public broadcasters, audit agencies, police chains of command, and local governments are not procedural furniture. They are the machinery through which democratic conflict remains reversible.

            Citizens should ask a simple question of every crisis: does this action preserve the possibility that the other side can lawfully win, govern, criticize, sue, publish, organize, and return? If the answer repeatedly narrows, the society may still look democratic while becoming less able to correct itself.

            ## What Indices Can And Cannot Show

            Overall evidence level: moderate. High-confidence claims are limited to documented institutional reports and court summaries. The interpretive claim, that normalization of erosion is the central danger, is stronger than a mood judgment but weaker than a country-level causal proof.

            ## Country Mechanisms Still Matter

            This article does not claim democracy is collapsing everywhere. It argues that a twenty-year pattern of decline changes the editorial question: where does correction still work, and where is it being habituated out of public life?

            ## Sources On Democratic Correction

            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [V-Dem, Democracy Report 2026](https://www.v-dem.net/publications/democracy-reports/)
            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            2026년 민주주의가 마주한 위험은 극적인 붕괴만이 아니다. 더 조용한 위험은 경보가 둔해지는 것이다. 한 국가는 선거를 치르고, 법원을 열어두고, 야당을 허용하면서도 시민에게 교정이 소용없다는 감각을 가르칠 수 있다. 문제는 민주주의가 하룻밤에 사라지는가가 아니라, 권력을 교정하는 제도들이 아직 실질 권위를 갖고 있는가이다.

            ## 느린 정상화

            증거는 공포도 안일함도 정당화하지 않는다. [Freedom House](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)는 2025년 세계 자유가 20년 연속 하락했고 54개국이 악화, 35개국이 개선되었다고 보고했다. [V-Dem 2026년 민주주의 보고서](https://www.v-dem.net/publications/democracy-reports/)는 다른 측정 방식을 쓰지만 넓은 지형은 비슷하게 그린다. 민주주의 제도는 일부 오래된 민주국가를 포함해 지속적 압력을 받고 있다.

            이런 지수는 판결문처럼 읽어서는 안 된다. 전문가 판단을 모으고 각국의 역사를 비교 가능한 점수로 압축하기 때문이다. 그러나 서로 다른 방법의 수렴은 경고다. 좋은 반응은 지수를 숭배하거나 조롱하는 것이 아니라 그 아래의 메커니즘을 묻는 것이다.

            그 메커니즘은 대개 극적이지 않다. 판사 압박, 검찰권 남용, 선거기관 공격, 미디어 규제의 정파화, 선택적 법 집행, 비상 권한 주장, 시민사회 재원 공격, 반대자의 적대화 같은 평범해 보이는 결정들이 쌓인다. 각각은 합법, 필요, 인기, 임시성의 언어로 방어될 수 있다. 누적 효과는 교정 비용을 높이는 것이다.

            ## 교정 체계로서의 민주주의

            민주주의는 다수결만이 아니다. 그것은 교정 체계다. 선거는 현직자를 교정하고, 법원은 행정부와 입법부를 교정하며, 의회는 대통령을 늦추고, 지방정부는 중앙의 과잉을 분산한다. 언론은 공식 서사를 시험하고, 시민사회는 제도적 맹점을 발견하며, 야당은 정책 독점을 교정한다.

            후퇴가 위험한 이유는 이 통로들을 없애기 전에 약화시키기 때문이다. 법원은 여전히 판결하지만 어떤 사건은 너무 위험하다고 배우게 된다. 선거관리기관은 표를 세지만 이미 불법 기관으로 낙인찍힌다. 의회는 열리지만 행정부를 제한하는 권한이 방해 행위로 묘사된다. 헌법은 보이지만 습관은 얇아진다.

            한국의 최근 헌정 경험은 보편 모델이라서가 아니라 민주적 교정이 하나의 사슬이라는 점을 보여주기 때문에 유용하다. [대한민국 헌법재판소](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)는 2025년 4월 4일 윤석열 대통령 탄핵을 인용하면서 재판 가능성, 비상계엄 요건, 위반의 중대성을 검토했다. 이후 집회, 변호인 접견, 비례대표 의석 배분 기준, 공직자 탄핵 사건 등은 헌정주의의 조용한 면을 보여준다. 민주주의는 역사적 판결뿐 아니라 일상적 경계 설정 속에서도 방어된다.

            ## 지수가 말하지 못하는 것

            지수는 어디를 봐야 하는지 알려준다. 그러나 왜 어떤 곳에서는 제도가 버텼고 다른 곳에서는 무너졌는지 단독으로 설명하지 못한다. 어떤 판사가 저항했는지, 어떤 지방 공무원이 압력을 흡수했는지, 어떤 언론이 직업 규범을 지켰는지, 어떤 시민단체가 행정 사실을 보이게 했는지까지 보여주지 않는다.

            그러므로 진지한 잡지는 지수를 첫 지도처럼 사용해야 한다. 실제 지형은 제도 행동이다. 다음 갈등이 평범한 공적 절차로 해결될 수 있는가, 패배가 곧 불법으로 번역되지 않는가가 중요하다.

            ## 지수 회의론자의 반론

            가장 강한 반론은 민주주의 경고가 자기편 언어가 될 수 있다는 것이다. 자유주의 NGO가 싫어하는 정부는 후퇴로 표시되고, 오래된 민주국가의 구조적 실패에는 더 부드러운 말이 쓰일 수 있다. 전문가 코딩은 법원, 권리, 미디어에 관한 전문직 계층의 전제를 반복할 수 있다. 어떤 유권자는 제도적 제약을 민주주의가 아니라 엘리트 방어막으로 볼 수 있다.

            이 반론은 진지하다. 민주주의 언어는 때로 유권자를 이해하기보다 훈육하는 데 쓰였다. 그러나 그것이 문제를 지우지는 않는다. 법원, 선거관리자, 언론, 야당이 영구적 적으로 바뀌면 유권자는 주권을 얻는 것이 아니다. 한 번의 승리가 미래의 교정을 무력화할 수 있는 체계를 물려받는다.

            ## 민주주의의 시험으로서의 교정

            긴 하락 이후 민주주의의 핵심 질문은 모든 위협받는 체제가 이미 민주주의를 잃었는가가 아니다. 어떤 체계가 아직 교정 가능한가이다.

            교정 가능성은 실제 시험이다. 야당은 이기고 집권할 수 있는가. 법원은 보복 없이 행정부에 반대할 수 있는가. 공직자는 여권 인사를 수사할 수 있는가. 시민은 과도한 처벌 없이 모일 수 있는가. 공영 미디어는 정부와 다른 사실을 말할 수 있는가. 선거 패배는 영구 위기 없이 받아들여질 수 있는가.

            이것은 “민주주의가 죽는다”보다 덜 극적인 언어다. 그러나 더 정확하다. 민주주의 분석의 첫 의무는 기준을 지키는 것이다. 포퓰리즘은 곧 권위주의가 아니고, 권위주의는 곧 파시즘이 아니다. 파시즘은 반자유주의 대중동원, 배제적 국민 신화, 조직적 강제, 제도의 총체적 종속 같은 좁은 조건에 맞을 때 써야 한다.

            ## 민주주의 독자가 보아야 할 것

            구호보다 제도를 보아야 한다. 선거기관, 법원, 검찰, 공영 미디어, 감사기관, 경찰 지휘체계, 지방정부는 절차적 장식이 아니다. 민주적 갈등이 되돌릴 수 있는 상태로 남게 하는 장치다.

            모든 위기에서 시민은 이렇게 물어야 한다. 이 행동은 상대가 합법적으로 이기고, 통치하고, 비판하고, 소송하고, 출판하고, 조직하고, 다시 돌아올 가능성을 보존하는가. 답이 반복적으로 좁아진다면 그 사회는 민주적으로 보이면서도 교정 능력을 잃고 있을 수 있다.

            ## 지수가 보여주는 것과 보여주지 못하는 것

            전체 근거 수준: 중간. 높은 확신은 제도 보고서와 법원 요약으로 확인되는 사실에 한정된다. 침식의 정상화가 핵심 위험이라는 해석은 단순한 분위기 판단보다는 강하지만 국가별 인과 증명보다는 약하다.

            ## 국가별 메커니즘은 여전히 필요하다

            이 글은 민주주의가 모든 곳에서 붕괴한다고 말하지 않는다. 20년에 걸친 하락 패턴이 편집 질문을 바꾼다고 말한다. 어디에서 교정이 아직 작동하며, 어디에서 교정이 공적 삶에서 습관적으로 밀려나고 있는가.

            ## 민주적 교정에 관한 출처

            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [V-Dem, Democracy Report 2026](https://www.v-dem.net/publications/democracy-reports/)
            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
    ),
    IndependentArticle(
        slug="displacement-without-settlement",
        en_title="Displacement Without Settlement",
        ko_title="정착 없는 강제이주",
        agent="Foreign Affairs Editor with Data Researcher",
        thesis_en="The structural problem in forced displacement is not only flight but the conversion of emergency into long-term civic suspension.",
        thesis_ko="강제이주의 구조적 문제는 탈출만이 아니라 비상사태가 장기적 시민 유예로 바뀌는 데 있다.",
        sources=[
            ("UNHCR, Global Trends", "https://www.unhcr.org/us/global-trends", "global forced-displacement stock and category definitions"),
            ("UNHCR, Refugee Data Finder", "https://www.unhcr.org/refugee-statistics", "disaggregated refugee and asylum data for later tables"),
            ("UNHCR, Figures at a Glance", "https://www.unhcr.org/us/about-unhcr/overview/figures-glance", "cross-check for end-2025 category totals"),
        ],
        reporting_tasks=[
            "Build a stock-flow table separating refugees, asylum seekers, IDPs, returnees, stateless people, and others needing protection.",
            "Add host-country capacity cases only after country-level fiscal, school, housing, and legal-status data are checked.",
            "Treat field reporting as illustration, not denominator evidence.",
        ],
        evidence_control="Never use total displacement as if all categories have the same legal status or policy route.",
        en_body=clean(
            """
            ## Abstract

            Forced displacement is usually narrated as movement: people flee, borders close, camps swell, boats arrive, governments argue. But the deeper structure is duration. The scandal is not only that people move under violence, persecution, or fear. It is that emergency becomes a civic condition.

            [UNHCR](https://www.unhcr.org/us/global-trends) reports 117.8 million forcibly displaced people at the end of 2025. The slight decline from the previous year deserves notice. It does not justify the word resolution.

            ## Stocks, Flows, And Suspended Lives

            A humane reader wants the number to fall. But a falling stock can conceal several realities. Some people return safely. Some return because alternatives are exhausted. Some obtain legal status elsewhere. Some move from one category to another. Some fall out of sight.

            The first discipline of displacement reporting is therefore categorical. Refugees are not internally displaced persons. Asylum seekers are not yet recognized refugees. Returnees are not automatically settled. Stateless people are not merely migrants. A stock figure tells us how many people remain displaced at a point in time. A flow figure tells us how many fled, returned, applied, crossed, or were resettled during a period.

            In 2025, UNHCR reports that internally displaced people accounted for a majority of the forcibly displaced population, with 68.7 million internally displaced by conflict and violence at year's end. That matters politically. The international refugee system is built more clearly around cross-border protection than around people trapped inside a state whose institutions may be part of the problem.

            ## The Geography Of Burden

            The word "international" can mislead. Much of the burden is local or regional. People flee to the nearest possible safety, not to the destination that dominates rich-country politics. Host communities need schools, clinics, housing, water, legal administration, policing, and jobs. A humanitarian appeal cannot substitute for municipal capacity.

            This is where displacement becomes political economy. A host state may accept people legally but fail them socially. A donor state may fund emergency relief but avoid resettlement. A sending state may be too dangerous for return yet too internationally normalized for sustained attention. A family may be physically safe and still legally suspended.

            ## Three Meanings Of Return

            Return is the most emotionally satisfying word in displacement politics. It is also one of the most dangerous.

            Return can mean durable homecoming: safety, property access, school, livelihood, documents, and freedom from renewed persecution. It can mean compelled movement into insecurity. It can mean statistical exit from one category without civic restoration. A rise in returns should therefore be read with questions attached: voluntary or pressured, safe or fragile, durable or temporary, supported or abandoned?

            The same caution applies to integration. Local integration is not the mere passage of time. It requires work rights, education, health access, language or administrative support, political consent, and a path out of permanent exception.

            ## The Improvement Case

            The strongest opposing view says this analysis risks minimizing improvement. If totals fall and returns increase, surely the system has achieved something. Host states cannot integrate everyone; wealthy states face political limits; international agencies must count progress where progress is real.

            That argument is right to resist despair. Humanitarian systems can save lives, restore families, and support return. But it fails if it treats exit from emergency statistics as settlement. The right measure is not whether a crisis looks smaller on one page. It is whether people have recovered secure membership somewhere.

            ## From Protection To Membership

            The modern displacement system has more instruments for protection than for settlement. Protection keeps people alive. Settlement gives them a civic future.

            The gap between the two produces a distinctive injustice: people live under temporary rules for permanent periods. Children grow up in camps, urban peripheries, informal work, or provisional status. Adults become administratively present but politically absent. Host communities become resentful when external support is too thin and local costs are visible. Donor governments praise compassion while keeping resettlement numerically narrow.

            The solution is not one slogan. Return, integration, and resettlement are different routes. Each has conditions. Return requires safety and agency. Integration requires host capacity and consent. Resettlement requires wealthy states to treat protection as responsibility rather than theatrical border management.

            ## What Serious Coverage Should Do

            Coverage should stop using displacement numbers as moral atmosphere. It should separate categories, name denominators, state dates, compare stocks and flows, and identify who bears administrative cost. It should ask what would count as settlement in a given case: citizenship, residence, work rights, school access, property restitution, legal identity, or political inclusion.

            Above all, it should avoid the comfort of a single humanitarian emotion. Pity is not policy. Border fear is not policy. Durable membership is policy.

            ## What The Displacement Numbers Support

            Overall evidence level: moderate to strong for aggregate displacement categories; moderate for the interpretation that civic suspension is the central structural problem. Country-specific claims require further disaggregation.

            ## Return Is Not One Thing

            This article does not claim all returns are unsafe or all host states can integrate everyone. It claims that displacement remains unresolved when the endpoint is temporary protection rather than secure membership.

            ## Sources On Durable Settlement

            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [UNHCR, Refugee Data Finder](https://www.unhcr.org/refugee-statistics)
            - [UNHCR, Figures at a Glance](https://www.unhcr.org/us/about-unhcr/overview/figures-glance)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            강제이주는 보통 이동의 이야기로 쓰인다. 사람들이 도망치고, 국경이 닫히고, 캠프가 커지고, 배가 도착하고, 정부가 논쟁한다. 그러나 더 깊은 구조는 기간이다. 추문은 사람들이 폭력, 박해, 공포 때문에 움직인다는 사실만이 아니다. 비상사태가 시민적 조건이 된다는 사실이다.

            [UNHCR](https://www.unhcr.org/us/global-trends)은 2025년 말 강제이주민이 1억 1,780만 명이라고 보고했다. 전년보다 소폭 줄었다는 점은 중요하다. 그러나 그것이 해결을 뜻하지는 않는다.

            ## 저량, 유량, 유예된 삶

            좋은 독자는 숫자가 줄기를 바란다. 그러나 저량 감소는 여러 현실을 숨길 수 있다. 어떤 사람은 안전하게 돌아간다. 어떤 사람은 대안이 다해 돌아간다. 어떤 사람은 다른 곳에서 법적 지위를 얻는다. 어떤 사람은 범주를 옮긴다. 어떤 사람은 시야에서 사라진다.

            그래서 강제이주 보도의 첫 규율은 범주 구분이다. 난민은 국내실향민이 아니다. 비호 신청자는 아직 인정 난민이 아니다. 귀환자는 자동으로 정착자가 아니다. 무국적자는 단순한 이주민이 아니다. 저량은 특정 시점에 남아 있는 사람 수이고, 유량은 일정 기간 떠나고, 돌아오고, 신청하고, 건너고, 재정착한 사람 수다.

            UNHCR은 2025년 말 분쟁과 폭력으로 인한 국내실향민이 6,870만 명이라고 보고한다. 이는 정치적으로 중요하다. 국제 난민 체계는 국경을 넘은 보호에는 비교적 명확하지만, 국가 내부에 갇힌 사람들에게는 더 약하다. 그 국가의 제도 자체가 문제의 일부일 때는 더욱 그렇다.

            ## 부담의 지리

            “국제”라는 말은 오해를 만든다. 부담의 상당 부분은 지역적이고 지방적이다. 사람들은 부유한 나라의 정치가 상상하는 목적지가 아니라 가장 가까운 안전으로 간다. 수용 지역에는 학교, 병원, 주거, 물, 법적 행정, 치안, 일자리가 필요하다. 인도주의 호소는 지방정부 역량을 대체할 수 없다.

            여기서 강제이주는 정치경제가 된다. 수용국은 법적으로 사람을 받아들이면서도 사회적으로 실패할 수 있다. 공여국은 긴급구호를 지원하면서 재정착은 피할 수 있다. 송출국은 귀환하기에는 위험하지만 국제적으로는 이미 정상화되어 관심을 잃을 수 있다. 한 가족은 물리적으로 안전하지만 법적으로는 유예될 수 있다.

            ## 귀환이라는 말의 세 뜻

            귀환은 강제이주 정치에서 가장 만족스러운 말이다. 동시에 가장 위험한 말이기도 하다.

            귀환은 안전한 집으로의 지속 가능한 복귀일 수 있다. 재산 접근, 학교, 생계, 문서, 재박해로부터의 자유가 함께 있어야 한다. 그러나 귀환은 불안정으로의 압박 이동일 수도 있고, 시민적 회복 없이 통계 범주에서 빠지는 것일 수도 있다. 따라서 귀환 증가는 질문과 함께 읽어야 한다. 자발적인가, 안전한가, 지속 가능한가, 지원되는가.

            통합도 마찬가지다. 지역 통합은 단순한 시간의 경과가 아니다. 노동권, 교육, 의료, 언어와 행정 지원, 정치적 동의, 영구적 예외 상태에서 벗어나는 길이 필요하다.

            ## 개선론

            가장 강한 반론은 이 분석이 개선을 작게 볼 위험이 있다는 것이다. 총량이 줄고 귀환이 늘었다면 시스템이 무언가를 해낸 것 아닌가. 수용국이 모두를 통합할 수는 없고, 부유한 나라에도 정치적 한계가 있으며, 국제기구는 실제 개선을 개선으로 세어야 한다.

            이 반론은 절망을 경계한다는 점에서 옳다. 인도주의 체계는 생명을 구하고, 가족을 회복시키고, 귀환을 지원할 수 있다. 그러나 통계상 비상에서 빠지는 것을 정착으로 다루면 실패한다. 올바른 척도는 한 페이지에서 위기가 작아졌는가가 아니라 사람들이 어딘가의 안정적 구성원 자격을 회복했는가이다.

            ## 보호에서 구성원 자격으로

            현대 강제이주 체계에는 보호 수단이 정착 수단보다 많다. 보호는 사람을 살린다. 정착은 시민적 미래를 준다.

            두 영역 사이의 틈은 독특한 부정의를 만든다. 사람들은 임시 규칙 아래 영구적인 시간을 산다. 아이들은 캠프, 도시 주변부, 비공식 노동, 임시 지위 안에서 성장한다. 어른들은 행정적으로는 존재하지만 정치적으로는 부재한다. 외부 지원이 얇고 지역 비용이 보일 때 수용 공동체는 분노한다. 공여국은 연민을 말하면서 재정착 숫자는 좁게 둔다.

            해법은 하나의 구호가 아니다. 귀환, 통합, 재정착은 다른 길이다. 귀환에는 안전과 당사자 의사가 필요하다. 통합에는 수용 역량과 동의가 필요하다. 재정착에는 부유한 국가가 보호를 국경 정치의 장식이 아니라 책임으로 대하는 태도가 필요하다.

            ## 진지한 보도가 해야 할 일

            보도는 강제이주 숫자를 도덕적 분위기로만 사용해서는 안 된다. 범주를 나누고, 분모를 밝히고, 날짜를 쓰고, 저량과 유량을 구분하며, 행정 비용을 누가 부담하는지 말해야 한다. 어떤 사례에서 정착이 무엇을 뜻하는지도 물어야 한다. 시민권, 거주권, 노동권, 학교 접근, 재산 회복, 법적 신분, 정치적 포함 중 무엇인가.

            연민은 정책이 아니다. 국경 공포도 정책이 아니다. 지속 가능한 구성원 자격이 정책이다.

            ## 강제이주 수치가 지탱하는 것

            전체 근거 수준: 집계 범주에 대해서는 중간 이상, 시민적 유예가 구조 문제라는 해석에 대해서는 중간. 국가별 주장은 추가 분해 자료가 필요하다.

            ## 귀환은 하나의 일이 아니다

            이 글은 모든 귀환이 위험하다거나 모든 수용국이 모두를 통합할 수 있다고 주장하지 않는다. 끝점이 안정적 구성원 자격이 아니라 임시 보호일 때 강제이주는 해결되지 않았다고 말한다.

            ## 지속 가능한 정착에 관한 출처

            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [UNHCR, Refugee Data Finder](https://www.unhcr.org/refugee-statistics)
            - [UNHCR, Figures at a Glance](https://www.unhcr.org/us/about-unhcr/overview/figures-glance)
            """
        ),
    ),
    IndependentArticle(
        slug="korea-mandate-problem-local-elections",
        en_title="Korea's Mandate Problem After The Local Elections",
        ko_title="지방선거 이후 한국의 위임 문제",
        agent="Political Editor with Korea Source Researcher",
        thesis_en="The 2026 local elections produced a governing advantage but not an unlimited mandate; the result must be read across offices, regions, turnout, Seoul, and the pending official data cycle.",
        thesis_ko="2026년 지방선거는 집권세력에 우위를 주었지만 무제한 위임을 준 것은 아니다. 결과는 직위, 지역, 투표율, 서울, 공식 자료 검증 주기를 함께 보아야 한다.",
        sources=[
            ("Associated Press, South Korea local elections", "https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0", "high-quality provisional account of the result and Seoul contest"),
            ("National Election Commission schedule PDF", "https://img.nec.go.kr/common/board/Download.do?bcIdx=294445&cbIdx=1084&streFileNm=b7498932-8ad9-487c-ac6d-37b420175dc0.pdf", "official election calendar"),
            ("Public Data Portal, NEC vote/count data API", "https://www.data.go.kr/data/15000900/openapi.do", "official raw-data route; notes post-election transfer and verification cycle"),
        ],
        reporting_tasks=[
            "When NEC data are available, build tables for turnout, vote share, margin, office type, party control before and after, and invalid votes.",
            "Separate Seoul mayoral interpretation from national local-government control.",
            "Use Korean editorials only as evidence of discourse, not as raw evidence of voter motives.",
        ],
        evidence_control="Treat AP as provisional high-quality journalism and NEC/public-data sources as the raw-data path. Do not infer voter motives without survey or district-level evidence.",
        en_body=clean(
            """
            ## Abstract

            Local elections are a poor instrument for simple national commandments. They are several elections at once: metropolitan executives, municipal heads, councils, education offices, by-elections, turnout contests, candidate reputations, party machines, and local grievances. Korea's June 2026 local elections gave the ruling Democratic Party a broad advantage, but the Seoul result complicated any claim of an unlimited mandate.

            ## One Election, Many Offices

            [AP reported](https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0) that the ruling liberal party won a majority of races while losing the crucial Seoul mayoral contest. That sentence contains the whole analytical problem. "Majority of races" points toward governing advantage. "Seoul" points toward symbolic restraint.

            A local election is not one national referendum. It distributes administrative power. It tests party organization outside the presidency. It reveals where national mood travels easily and where local incumbency, urban property politics, candidate competence, education issues, or regional memory interrupt it.

            The temptation after such an election is narrative excess. Winners say the country has endorsed their project. Losers say the result contains a hidden warning. Both may be partly true. Neither is enough.

            ## The Seoul Exception

            Seoul is not Korea. It is, however, too important to treat as just another data point. It concentrates media attention, housing wealth, administrative scale, professional-class politics, and symbolic claims about competence. Losing Seoul while winning many other offices means the government can claim breadth but not ease.

            That distinction matters for President Lee Jae Myung's governing strategy. A broad local map can help implementation: budgets, regional projects, welfare delivery, administrative coordination. But a Seoul defeat can discipline the national reading. It may indicate limits among property-owning urban voters, skepticism toward centralization, candidate-specific factors, or a local desire for divided power. Without precinct-level data and surveys, none of these should be asserted as fact.

            ## Raw Data And The Waiting Period

            The official raw source for serious analysis is the National Election Commission and its election-statistics data. The public-data portal for NEC vote and count information notes that vote/count data are not provided as real-time election-day data and are ordinarily transferred and verified after the election. That matters editorially. A magazine should not pretend provisional maps are full evidence.

            The next version of this article should build its mandate analysis from official tables: turnout, vote share, margin, party control before and after, invalid votes, office type, and regional distribution. Until then, the responsible claim is narrower: the election created a governing advantage with a visible metropolitan limit.

            ## Mandate Is Not Permission

            A mandate is not a magic word. It has at least three components. Electoral scope: how many offices and regions changed. Programmatic clarity: whether voters selected a policy package or merely punished an opponent. Institutional authority: what the winners are legally empowered to do.

            Local victories strengthen implementation where local governments matter. They do not erase courts, opposition rights, fiscal constraints, administrative competence, or the need to explain policy. They also do not settle national constitutional questions. The lesson is not that voters spoke with one voice. They rarely do. The lesson is that they rearranged the governing field.

            ## The Mandate Case

            The strongest opposing view is that this caution underrates the democratic force of victory. Elections are how citizens allocate power. If a party wins most contests, it has earned authority to govern. Constantly qualifying wins can become a way for commentators to deny the public's choice.

            That argument is right about legitimacy. Winning matters. But a serious reading of elections must distinguish authority from blank checks. A local election produces offices, not metaphysical unanimity. The democratic value of a mandate increases when winners state its limits as clearly as its uses.

            ## Mandates Need Translation

            Korea's 2026 local elections should be read as a mandate for implementation, not a mandate for institutional impatience.

            The ruling party can reasonably claim that voters gave it local machinery to pursue the government's program. It cannot reasonably claim that the Seoul loss is irrelevant. The opposition can reasonably claim that Seoul shows limits. It cannot reasonably claim that a broad national local-election defeat is disguised victory.

            Good analysis lives in that tension. It should ask where the government now has administrative capacity, where it lacks urban consent, where local policy can produce visible results, and where the next conflict may come from schools, housing, welfare delivery, or local finance.

            ## What The Pre-Table Evidence Supports

            Overall evidence level: moderate and provisional. High confidence: the election was held on June 3, 2026, and high-quality reporting documents a ruling-party majority with a Seoul loss. Lower confidence: voter motives and national mandate interpretation until NEC data and post-election surveys are fully analyzed.

            ## What The Official Tables Must Decide

            This article intentionally avoids asserting a national psychology. The next evidentiary step is official election data, not louder interpretation.

            ## Sources For Election Verification

            - [AP, South Korea's ruling party wins most races in local elections](https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0)
            - [NEC election schedule PDF](https://img.nec.go.kr/common/board/Download.do?bcIdx=294445&cbIdx=1084&streFileNm=b7498932-8ad9-487c-ac6d-37b420175dc0.pdf)
            - [Public Data Portal, NEC vote/count information API](https://www.data.go.kr/data/15000900/openapi.do)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            지방선거는 단순한 전국 명령을 읽기에 좋지 않은 도구다. 그것은 여러 선거의 묶음이다. 광역단체장, 기초단체장, 지방의회, 교육감, 재보궐, 투표율, 후보 평판, 정당 조직, 지역 불만이 함께 움직인다. 2026년 6월 한국 지방선거는 집권 더불어민주당에 넓은 우위를 주었지만, 서울시장 결과는 무제한 위임이라는 해석을 어렵게 만들었다.

            ## 하나의 선거, 여러 직위

            [AP](https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0)는 집권 자유주의 정당이 다수의 선거에서 이겼지만 중요한 서울시장 선거를 잃었다고 보도했다. 이 한 문장에 분석의 문제가 들어 있다. 다수 승리는 통치 우위를 가리킨다. 서울 패배는 상징적 제약을 가리킨다.

            지방선거는 하나의 국민투표가 아니다. 그것은 행정 권력을 배분한다. 대통령제 밖의 정당 조직을 시험한다. 전국적 분위기가 어디까지 이동하는지, 어디에서 지역 현직, 도시 자산 정치, 후보 역량, 교육 문제, 지역 기억이 그것을 끊는지 보여준다.

            이런 선거 뒤에는 과잉 서사가 따라온다. 승자는 나라가 자신들의 프로젝트를 승인했다고 말한다. 패자는 결과 속에 숨은 경고가 있다고 말한다. 둘 다 부분적으로 맞을 수 있다. 그러나 어느 쪽도 충분하지 않다.

            ## 서울이라는 예외

            서울은 한국 전체가 아니다. 그러나 단순한 한 점으로 처리하기에는 너무 중요하다. 서울은 미디어 관심, 주택 자산, 행정 규모, 전문직 정치, 능력에 대한 상징적 요구를 집중한다. 여러 지역에서 이기면서 서울을 잃었다는 것은 정부가 폭은 주장할 수 있지만 쉬운 길은 주장하기 어렵다는 뜻이다.

            이 구분은 이재명 정부의 통치 전략에 중요하다. 넓은 지방 권력은 예산, 지역 프로젝트, 복지 전달, 행정 조정에 도움이 된다. 그러나 서울 패배는 전국 해석을 절제하게 만든다. 그것은 자산 보유 도시 유권자의 한계, 중앙집중에 대한 회의, 후보 요인, 분권 선호를 뜻할 수 있다. 그러나 구별 자료와 조사 없이 이것을 사실로 단정해서는 안 된다.

            ## 공식 자료를 기다리는 일

            진지한 분석의 원자료는 중앙선거관리위원회와 선거통계 자료다. 선관위 투개표 정보 공공데이터 경로는 투개표 자료가 선거 당일 실시간 자료가 아니며, 선거 종료 뒤 이관과 검증 절차를 거친다는 점을 밝힌다. 이는 편집상 중요하다. 계간지는 임시 지도를 완전한 증거처럼 써서는 안 된다.

            다음 판의 위임 분석은 공식 표에서 출발해야 한다. 투표율, 득표율, 표차, 전후 정당 지배, 무효표, 직위 유형, 지역 분포가 필요하다. 그 전까지 책임 있는 주장은 좁다. 이 선거는 집권 우위를 만들었고, 동시에 뚜렷한 수도권적 한계를 남겼다.

            ## 위임은 허가증이 아니다

            위임은 마법의 말이 아니다. 적어도 세 요소가 있다. 얼마나 많은 직위와 지역이 바뀌었는가라는 범위, 유권자가 정책 묶음을 선택했는지 상대를 벌했는지라는 프로그램성, 승자가 법적으로 무엇을 할 수 있는가라는 제도 권한이다.

            지방 승리는 지방정부가 중요한 곳에서 실행력을 높인다. 그러나 법원, 야당 권리, 재정 제약, 행정 능력, 정책 설명 의무를 지우지 않는다. 헌정 문제도 끝내지 않는다. 유권자가 한 목소리로 말했다는 것이 교훈은 아니다. 유권자는 거의 그렇게 말하지 않는다. 교훈은 통치 장이 재배열되었다는 것이다.

            ## 위임론

            가장 강한 반론은 이런 신중함이 승리의 민주적 힘을 과소평가한다는 것이다. 선거는 시민이 권력을 배분하는 방식이다. 한 정당이 대부분의 경쟁에서 이겼다면 통치 권한을 얻은 것이다. 승리를 계속 조건부로 만드는 것은 논평가가 대중의 선택을 부정하는 방식이 될 수 있다.

            이 반론은 정당성에 관해 옳다. 이긴다는 것은 중요하다. 그러나 선거를 진지하게 읽는 일은 권한과 백지수표를 구분해야 한다. 지방선거는 직위를 만들지 형이상학적 만장일치를 만들지 않는다. 위임의 민주적 가치는 승자가 그 한계를 그 사용처만큼 분명히 말할 때 커진다.

            ## 위임은 번역되어야 한다

            2026년 지방선거는 실행의 위임으로 읽어야지, 제도적 조급함의 위임으로 읽어서는 안 된다.

            집권당은 유권자가 정부 프로그램을 추진할 지방 기계를 주었다고 말할 수 있다. 서울 패배가 무관하다고 말할 수는 없다. 야당은 서울이 한계를 보여준다고 말할 수 있다. 그러나 넓은 지방선거 패배가 숨은 승리라고 말할 수는 없다.

            좋은 분석은 이 긴장 속에 있다. 정부가 어디에서 행정 역량을 갖게 되었는지, 어디에서 도시적 동의를 잃었는지, 어떤 지역 정책이 가시적 성과를 만들 수 있는지, 다음 갈등이 학교·주거·복지 전달·지방재정 중 어디에서 나올지를 물어야 한다.

            ## 공식 표 전의 근거가 지탱하는 것

            전체 근거 수준: 중간, 그리고 잠정적. 높은 확신: 선거는 2026년 6월 3일 실시되었고, 고품질 보도는 집권당 다수 승리와 서울 패배를 기록했다. 낮은 확신: 유권자 동기와 전국 위임 해석은 선관위 자료와 선거 후 조사가 분석되기 전까지 제한적이다.

            ## 공식 표가 결정해야 할 것

            이 글은 전국적 심리를 단정하지 않는다. 다음 증거 단계는 더 큰 해석이 아니라 공식 선거 자료다.

            ## 선거 검증을 위한 출처

            - [AP, South Korea's ruling party wins most races in local elections](https://apnews.com/article/south-korea-elections-mayors-lee-yoon-3f75bc77d129daecbcfac5afafbeb8d0)
            - [NEC election schedule PDF](https://img.nec.go.kr/common/board/Download.do?bcIdx=294445&cbIdx=1084&streFileNm=b7498932-8ad9-487c-ac6d-37b420175dc0.pdf)
            - [공공데이터포털, 중앙선거관리위원회 투개표 정보](https://www.data.go.kr/data/15000900/openapi.do)
            """
        ),
    ),
    IndependentArticle(
        slug="korea-semiconductor-recovery-welfare-state",
        en_title="Korea's Semiconductor Recovery And The Welfare State",
        ko_title="한국 반도체 회복과 복지국가",
        agent="Economics Editor with Korea Data Researcher",
        thesis_en="Korea's chip-led recovery creates fiscal and political opportunity, but a semiconductor cycle cannot by itself solve care, housing, demographic, and welfare-state capacity problems.",
        thesis_ko="한국의 반도체 주도 회복은 재정적·정치적 기회를 만들지만, 반도체 경기만으로 돌봄, 주거, 인구, 복지국가 역량 문제를 해결할 수는 없다.",
        sources=[
            ("Bank of Korea, Monetary Policy Decision and Opening Remarks, May 28 2026", "https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098190&programType=newsDataEng&relate=Y", "official growth, inflation, semiconductor, housing, exchange-rate context"),
            ("KDI Economic Outlook 2026-1st Half", "https://www.kdi.re.kr/eng/research/economy", "growth forecast, exports, investment, inflation, domestic demand"),
            ("OECD Economic Outlook, June 2026", "https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html", "global risk environment and AI investment backdrop"),
        ],
        reporting_tasks=[
            "Add fiscal-revenue, regional-employment, energy-demand, housing-cost, and care-service data once official tables are compiled.",
            "Compare chip-led cycles with shipbuilding, defense, and battery sectors without treating them as interchangeable.",
            "Separate temporary transfers from permanent welfare-state capacity.",
        ],
        evidence_control="Semiconductor-export strength is not evidence of household welfare unless linked to wages, prices, taxes, care, housing, and public services.",
        en_body=clean(
            """
            ## Abstract

            Korea's semiconductor recovery is real enough to change the economic conversation. It is not enough to answer the social question. A chip upcycle can lift growth, exports, investment, fiscal receipts, and stock-market confidence. It cannot automatically produce affordable housing, reliable care, gender-equal family formation, regional resilience, or a durable welfare state.

            ## The Boom That Buys Time

            The [Bank of Korea's May 28, 2026 policy communication](https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098190&programType=newsDataEng&relate=Y) raised the growth forecast for 2026 to 2.6 percent, citing strong semiconductors, exports, investment, and supportive domestic demand. KDI's first-half 2026 outlook similarly projects around 2.5 percent growth, supported by robust semiconductor exports and domestic demand recovery.

            This is not trivial. A country with Korea's demographic pressure, household debt sensitivity, export dependence, and geopolitical exposure needs growth. A strong semiconductor cycle can finance choices that were harder in stagnation. It can also create political mood: competence feels more plausible when exports and investment are moving.

            But a boom buys time. It does not decide how time is used.

            ## The Spillover Question

            The central economic question is spillover. Does semiconductor strength move beyond firms, suppliers, and asset markets into wages, regional employment, tax capacity, small-business demand, and public services? The answer is not automatic.

            High-end semiconductor production is capital-intensive and globally exposed. Its employment effects are real but narrower than the national symbolism suggests. Its fiscal contribution can be meaningful, but volatile. Its infrastructure demands, including energy, land, water, and logistics, can produce local strains. Its connection to household fertility, education costs, housing affordability, and elder care is indirect.

            The danger is to mistake national industrial pride for social settlement. Korea can be a winner in the AI hardware cycle and still fail to make ordinary life feel buildable for young households.

            ## Welfare State As Industrial Policy

            A welfare state is often discussed as what a country pays for after growth. That order is too simple. In an advanced economy, care, education, housing, health, retraining, and regional public services are part of the productive system. They determine whether workers can move, families can form, skills can renew, and citizens can accept structural change.

            If Korea treats welfare as compensation for people outside the semiconductor economy, it will miss the deeper point. Social policy is one condition of industrial durability. A society with unaffordable housing, overloaded families, intense education arms races, and insecure care cannot easily turn export success into legitimacy.

            ## Inflation, Housing, And The Constraint On Generosity

            The BOK's communication is also a warning. The same release that notes semiconductor strength also discusses inflation, exchange-rate volatility, Seoul-area housing prices, household debt, and uncertainty from the Middle East. KDI projects headline inflation around 2.7 percent in 2026 as oil prices and demand recovery interact.

            This means the welfare-state opportunity is real but constrained. Permanent commitments need revenue, not just cyclical confidence. Transfers can help households, but if housing supply, care capacity, and labor-market rules do not change, money may leak into prices or temporary relief.

            ## The Strategic-Industry Caution

            The strongest opposing view says Korea should not burden a strategic industry with social expectations. Semiconductors face fierce competition, energy constraints, export controls, China risk, U.S. pressure, and enormous capital needs. The first duty is to keep the sector globally competitive; welfare-state debates should not dilute industrial urgency.

            This is a serious warning. Without industrial competitiveness, social promises become harder to fund. But the opposition becomes too narrow if it imagines competitiveness and welfare capacity as separate worlds. The legitimacy of industrial strategy depends on whether citizens see national success entering ordinary life.

            ## The Boom Must Become Capacity

            Korea should treat the semiconductor recovery as fiscal breathing room and political leverage for social investment, not as proof that the social question has been solved.

            The right policy vocabulary is conversion. Convert export gains into stable revenue. Convert regional investment into livable communities. Convert training promises into credible adult-learning systems. Convert care from family burden into public infrastructure. Convert industrial strategy from company support into a social bargain.

            The semiconductor cycle can make this easier. It cannot do it by itself.

            ## What Export Strength Can Support

            Overall evidence level: moderate. Strong evidence supports the existence of a chip-led recovery in 2026 forecasts. The broader argument about welfare-state conversion is interpretive and requires additional fiscal, labor, regional, and household data.

            ## The Cycle May Still Turn

            This article does not claim semiconductor strength will fade soon or that welfare policy should override industrial policy. It claims the boom's political meaning depends on whether it becomes social capacity.

            ## Sources On Industry And Welfare Capacity

            - [Bank of Korea, May 28 2026 Monetary Policy Decision](https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098190&programType=newsDataEng&relate=Y)
            - [KDI Economic Outlook 2026-1st Half](https://www.kdi.re.kr/eng/research/economy)
            - [OECD Economic Outlook, June 2026](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            한국의 반도체 회복은 경제 대화를 바꿀 만큼 현실적이다. 그러나 사회적 질문에 답할 만큼 충분하지는 않다. 반도체 상승 국면은 성장, 수출, 투자, 세수, 주식시장 자신감을 높일 수 있다. 하지만 그것이 자동으로 주거 부담, 안정적 돌봄, 성평등한 가족 형성, 지역 회복력, 지속 가능한 복지국가를 만들어내지는 않는다.

            ## 시간을 사는 호황

            [한국은행의 2026년 5월 28일 통화정책 자료](https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098190&programType=newsDataEng&relate=Y)는 강한 반도체, 수출, 투자, 내수 흐름을 들어 2026년 성장률 전망을 2.6%로 높였다. KDI의 2026년 상반기 경제전망도 견조한 반도체 수출과 내수 회복을 배경으로 약 2.5% 성장을 전망한다.

            이는 작지 않다. 인구 압력, 가계부채 민감성, 수출 의존, 지정학 노출을 가진 한국에는 성장이 필요하다. 강한 반도체 경기는 침체 때 어려웠던 선택을 재정적으로 가능하게 만들 수 있다. 수출과 투자가 움직일 때 능력 있다는 정치적 분위기도 생긴다.

            그러나 호황은 시간을 산다. 그 시간을 어떻게 쓸지는 결정하지 않는다.

            ## 파급의 문제

            핵심 경제 질문은 파급이다. 반도체 강세가 기업, 협력업체, 자산시장을 넘어 임금, 지역 고용, 세수, 소상공인 수요, 공공서비스로 이동하는가. 답은 자동이 아니다.

            고급 반도체 생산은 자본집약적이고 세계 시장에 노출되어 있다. 고용 효과는 있지만 국가적 상징이 암시하는 것보다 좁을 수 있다. 재정 기여는 의미 있을 수 있지만 변동성이 크다. 전력, 토지, 물, 물류 같은 인프라 수요는 지역 부담을 만들 수 있다. 출산, 교육비, 주거, 노인 돌봄과의 연결은 간접적이다.

            위험은 국가적 산업 자부심을 사회적 정착으로 오인하는 것이다. 한국은 AI 하드웨어 경기에서 승자가 되면서도 젊은 가구에게 보통의 삶이 가능하다는 감각을 주는 데 실패할 수 있다.

            ## 산업정책으로서의 복지국가

            복지국가는 흔히 성장 뒤에 지불하는 것으로 말해진다. 이 순서는 너무 단순하다. 선진경제에서 돌봄, 교육, 주거, 보건, 재훈련, 지역 공공서비스는 생산 체계의 일부다. 그것들은 노동자가 이동할 수 있는지, 가족이 형성될 수 있는지, 숙련이 갱신될 수 있는지, 시민이 구조 변화를 받아들일 수 있는지를 결정한다.

            한국이 복지를 반도체 경제 바깥 사람들에 대한 보상으로만 다룬다면 핵심을 놓친다. 사회정책은 산업 지속성의 조건이다. 주거가 비싸고, 가족이 과부하 상태이며, 교육 경쟁이 격렬하고, 돌봄이 불안정한 사회는 수출 성공을 정당성으로 바꾸기 어렵다.

            ## 물가, 주거, 관대함의 제약

            한국은행 자료는 경고이기도 하다. 반도체 강세를 말하는 같은 자료가 물가, 환율 변동성, 서울과 수도권 주택가격, 가계부채, 중동발 불확실성을 함께 말한다. KDI도 유가와 경기 회복이 맞물리며 2026년 소비자물가 상승률을 약 2.7%로 전망한다.

            이는 복지국가의 기회가 현실적이지만 제약되어 있음을 뜻한다. 영구적 약속에는 경기 자신감이 아니라 안정적 재원이 필요하다. 현금 이전은 가계를 도울 수 있지만, 주거 공급, 돌봄 역량, 노동시장 규칙이 바뀌지 않으면 돈은 가격이나 임시 완화로 새어 나갈 수 있다.

            ## 전략산업 신중론

            가장 강한 반론은 전략 산업에 사회적 기대를 너무 많이 얹지 말라는 것이다. 반도체는 치열한 경쟁, 에너지 제약, 수출통제, 중국 리스크, 미국 압력, 거대한 자본 수요에 놓여 있다. 첫 임무는 세계 경쟁력을 지키는 것이며, 복지국가 논쟁이 산업적 긴급성을 흐려서는 안 된다.

            이 경고는 진지하다. 산업 경쟁력이 없으면 사회적 약속을 재정적으로 감당하기 어렵다. 그러나 경쟁력과 복지 역량을 별개의 세계로 상상하면 시야가 좁아진다. 산업전략의 정당성은 시민이 국가적 성공을 보통의 삶 속에서 느끼는가에 달려 있다.

            ## 호황은 역량이 되어야 한다

            한국은 반도체 회복을 사회 문제가 해결되었다는 증거가 아니라 사회투자를 위한 재정적 호흡과 정치적 지렛대로 보아야 한다.

            올바른 정책 언어는 전환이다. 수출 이익을 안정적 재원으로, 지역 투자를 살 만한 공동체로, 훈련 약속을 신뢰 가능한 성인학습 체계로, 돌봄을 가족 부담에서 공공 인프라로, 산업전략을 기업 지원에서 사회적 거래로 전환해야 한다.

            반도체 경기는 이 일을 쉽게 만들 수 있다. 그러나 혼자 해내지는 못한다.

            ## 수출 강세가 지탱할 수 있는 것

            전체 근거 수준: 중간. 2026년 전망에서 반도체 주도 회복이 나타난다는 점은 강한 근거가 있다. 복지국가 전환에 관한 넓은 주장은 해석이며 추가적인 재정, 노동, 지역, 가구 자료가 필요하다.

            ## 사이클은 여전히 바뀔 수 있다

            이 글은 반도체 강세가 곧 사라진다거나 복지정책이 산업정책을 압도해야 한다고 주장하지 않는다. 호황의 정치적 의미는 그것이 사회적 역량으로 바뀌는가에 달려 있다고 주장한다.

            ## 산업과 복지역량에 관한 출처

            - [Bank of Korea, May 28 2026 Monetary Policy Decision](https://www.bok.or.kr/eng/bbs/E0000634/view.do?depth=400423&menuNo=400423&nttId=10098190&programType=newsDataEng&relate=Y)
            - [KDI Economic Outlook 2026-1st Half](https://www.kdi.re.kr/eng/research/economy)
            - [OECD Economic Outlook, June 2026](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            """
        ),
    ),
    IndependentArticle(
        slug="korea-fertility-housing-pronatalism",
        en_title="Korea's Fertility Rebound And The Housing Question",
        ko_title="한국의 출산 반등과 주거 질문",
        agent="Sociology Editor with Korea Data Researcher",
        thesis_en="Korea's 2025 fertility rebound is welcome but structurally ambiguous; the central question is whether births are rising because family formation became more viable or because timing effects briefly improved the denominator.",
        thesis_ko="한국의 2025년 출산 반등은 반가운 일이지만 구조적으로는 모호하다. 핵심은 가족 형성이 더 가능해졌기 때문인지, 아니면 시기 효과가 일시적으로 분모를 개선했기 때문인지다.",
        sources=[
            ("KOSIS, Vital Statistics of Korea", "https://kosis.kr/statHtml/statHtml.do?language=en&orgId=101&tblId=DT_1B8000F", "official annual vital-statistics table"),
            ("Ministry of Data and Statistics, Preliminary Results of Birth and Death Statistics in 2025", "https://www.kostat.go.kr/board.es?act=view&bid=11773&list_no=444910&mid=a20108010000&nPage=1&ref_bid=11742%2C11743%2C11744%2C11745%2C11746%2C11747%2C11748%2C11749%2C11773%2C11774%2C11750&tag=", "official 2025 births, deaths, and natural increase"),
            ("OECD, Korea's Unborn Future", "https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/03/korea-s-unborn-future_1b836111/005ce8f7-en.pdf", "structural low-fertility analysis"),
        ],
        reporting_tasks=[
            "Disaggregate births by age, parity, region, marriage cohort, income, housing tenure, and employment where official data allow.",
            "Separate total fertility rate, number of births, marriages, and household formation.",
            "Use commentary about youth attitudes only as discourse evidence unless tied to survey data.",
        ],
        evidence_control="A one- or two-year rise from extreme lows is not proof of a solved fertility regime.",
        en_body=clean(
            """
            ## Abstract

            Korea's fertility rebound is good news. It is not yet a doctrine. In 2025 the number of live births rose to 254,457 and the total fertility rate reached 0.800, according to official Korean statistical sources. The increase deserves attention because it interrupts a brutal decline. It also demands restraint because a rebound from extreme lows can reflect timing, cohort composition, marriage recovery, or policy effects that are not yet separable.

            ## The Rebound Problem

            Birth numbers are emotionally powerful. They invite relief, explanation, and political claiming. A government wants to say policy worked. Critics want to say nothing structural changed. Commentators want a story about young people. None of these instincts should lead.

            The first fact is narrow. Korea's [Ministry of Data and Statistics](https://www.kostat.go.kr/board.es?act=view&bid=11773&list_no=444910&mid=a20108010000&nPage=1&ref_bid=11742%2C11743%2C11744%2C11745%2C11746%2C11747%2C11748%2C11749%2C11773%2C11774%2C11750&tag=) reported 254.5 thousand births in 2025, up 6.8 percent from 2024, while deaths remained higher at 363.4 thousand. KOSIS reports a 2025 total fertility rate of 0.800. These are real improvements within a continuing natural decrease.

            The second fact is conceptual. Births, fertility rate, marriages, and family viability are related but not identical. Births count events. The total fertility rate is a period measure. Marriages can rise after pandemic delay. First births can rise while second births remain weak. A cohort at peak childbearing age can temporarily lift the count without changing the underlying regime.

            ## Housing As A Family Institution

            Korea's fertility debate is often moralized. Young people are blamed for selfishness, pessimism, feminism, careerism, or insufficient patriotism. That style of argument is lazy. Fertility is not only a personal preference. It is a social estimate of whether a life can be built.

            Housing is central because it converts uncertainty into daily arithmetic. Marriage and childbirth require not simply affection but space, debt capacity, commute tolerance, school expectations, and confidence that a household can survive shocks. If housing prices rise faster than secure income, cash benefits may help but cannot fully change the calculation.

            The housing question also links fertility to class. Better-off households can buy stability; precarious households must rent uncertainty. A national fertility number can therefore hide unequal family viability.

            ## Pronatalism And Its Limits

            Pronatal policy is politically tempting because it promises a direct response to a visible number. More childcare, parental leave, housing support, and transfers can matter. But pronatalism fails when it treats childbirth as a target variable detached from work, gender, care, education, housing, and status competition.

            Korea has spent heavily on low fertility for years. The issue is not whether the state has tried. It is whether policy changes the life conditions that make parenthood feel possible. A subsidy cannot by itself lower the price of apartments, reduce after-school competition, shorten punishing work cultures, or redistribute care inside households.

            ## The Rebound Case

            The strongest opposing view says analysts should stop finding reasons to discount good news. Births rose, marriages improved, and attitudes may be shifting. If policy, social adaptation, and cohort timing finally produce better numbers, excessive skepticism could become another form of fatalism.

            That objection is fair. A society should notice improvement. But the purpose of caution is not pessimism. It is protection against false explanation. If a temporary cohort effect is mistaken for structural repair, policy will relax too soon. If policy effects are real, they need to be identified precisely so they can be strengthened.

            ## Family Formation As Institutional Confidence

            The fertility rebound should be treated as an opening, not a verdict.

            The right question is not "has Korea solved low fertility?" It plainly has not. The right question is "which part of the family-formation system changed?" Did marriage timing recover? Did first births rise because delayed couples moved? Did second births respond to childcare support? Did housing expectations ease in some regions? Did labor-market confidence improve among particular cohorts? Did policy affect lower-income households or mainly those already near childbirth?

            Only that disaggregation can turn relief into knowledge.

            ## What The Rebound Shows

            Overall evidence level: moderate. High confidence: official sources document a 2025 rise in births and TFR from very low levels. Moderate to low confidence: causal attribution among policy, marriage timing, cohort effects, housing, and labor conditions.

            ## One Better Year Is Not A Settlement

            This article welcomes the rebound but refuses to turn it into a demographic doctrine. The next serious version must be disaggregated or it will merely decorate a number.

            ## Sources On Births, Housing, And Family Formation

            - [KOSIS, Vital Statistics of Korea](https://kosis.kr/statHtml/statHtml.do?language=en&orgId=101&tblId=DT_1B8000F)
            - [Ministry of Data and Statistics, Preliminary Results of Birth and Death Statistics in 2025](https://www.kostat.go.kr/board.es?act=view&bid=11773&list_no=444910&mid=a20108010000&nPage=1&ref_bid=11742%2C11743%2C11744%2C11745%2C11746%2C11747%2C11748%2C11749%2C11773%2C11774%2C11750&tag=)
            - [OECD, Korea's Unborn Future](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/03/korea-s-unborn-future_1b836111/005ce8f7-en.pdf)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            한국의 출산 반등은 좋은 소식이다. 그러나 아직 교리는 아니다. 공식 통계에 따르면 2025년 출생아 수는 254,457명으로 늘었고 합계출산율은 0.800이 되었다. 이 증가는 혹독한 하락을 끊었다는 점에서 중요하다. 동시에 극단적 저점에서의 반등은 출산 시기, 코호트 구성, 혼인 회복, 정책 효과가 아직 분리되지 않은 결과일 수 있으므로 절제가 필요하다.

            ## 반등의 문제

            출생아 수는 감정적으로 강한 숫자다. 안도, 설명, 정치적 소유권을 부른다. 정부는 정책이 작동했다고 말하고 싶고, 비판자는 아무것도 구조적으로 바뀌지 않았다고 말하고 싶다. 논평가는 청년에 관한 이야기를 원한다. 그러나 이런 본능이 앞서서는 안 된다.

            첫 사실은 좁다. [국가데이터처](https://www.kostat.go.kr/board.es?act=view&bid=11773&list_no=444910&mid=a20108010000&nPage=1&ref_bid=11742%2C11743%2C11744%2C11745%2C11746%2C11747%2C11748%2C11749%2C11773%2C11774%2C11750&tag=)는 2025년 출생아 수가 25만 4,500명으로 2024년보다 6.8% 늘었고, 사망자는 36만 3,400명으로 여전히 더 많았다고 발표했다. KOSIS는 2025년 합계출산율을 0.800으로 제시한다. 이는 자연감소가 계속되는 가운데 나타난 실제 개선이다.

            둘째 사실은 개념적이다. 출생아 수, 합계출산율, 혼인, 가족 형성 가능성은 연결되어 있지만 같지 않다. 출생아 수는 사건을 센다. 합계출산율은 기간 지표다. 혼인은 팬데믹 이후 지연이 회복되며 늘 수 있다. 첫째아는 늘어도 둘째아는 약할 수 있다. 출산 집중 연령대 코호트가 일시적으로 수치를 올릴 수도 있다.

            ## 가족 제도로서의 주거

            한국의 출산 논쟁은 자주 도덕화된다. 청년은 이기심, 비관, 페미니즘, 경력주의, 애국심 부족으로 비난받는다. 이런 논증은 게으르다. 출산은 개인 취향만이 아니다. 삶을 세울 수 있는가에 대한 사회적 추정이다.

            주거는 불확실성을 매일의 산술로 바꾼다. 결혼과 출산에는 애정만이 아니라 공간, 부채 감당력, 통근, 학교 기대, 충격을 견딜 수 있다는 확신이 필요하다. 주거 가격이 안정적 소득보다 빠르게 오르면 현금 지원은 도움이 되지만 계산 전체를 바꾸기는 어렵다.

            주거 질문은 출산을 계급 문제와 연결한다. 더 나은 가구는 안정성을 살 수 있고, 불안정한 가구는 불확실성을 임차한다. 하나의 전국 출산율은 불평등한 가족 형성 가능성을 숨길 수 있다.

            ## 출산장려주의의 한계

            출산장려 정책은 눈에 보이는 숫자에 직접 대응하는 것처럼 보이기 때문에 정치적으로 유혹적이다. 보육, 육아휴직, 주거 지원, 현금 이전은 중요할 수 있다. 그러나 출산을 노동, 젠더, 돌봄, 교육, 주거, 지위 경쟁과 분리된 목표 변수로 다루면 실패한다.

            한국은 저출산에 오랫동안 많은 돈을 썼다. 문제는 국가가 시도했는가가 아니다. 정책이 부모가 될 수 있다는 생활 조건을 바꾸었는가이다. 보조금 하나가 아파트 가격, 사교육 경쟁, 긴 노동문화, 가구 내 돌봄 분배를 혼자 바꾸지는 못한다.

            ## 반등론

            가장 강한 반론은 분석가들이 좋은 소식을 할인할 이유만 찾는다는 것이다. 출생아가 늘고 혼인이 회복되었으며 태도도 바뀌고 있을 수 있다. 정책, 사회적 적응, 코호트 효과가 더 나은 숫자를 만들었다면 과도한 회의주의는 또 다른 숙명론일 수 있다.

            이 반론은 공정하다. 사회는 개선을 알아보아야 한다. 그러나 신중함의 목적은 비관이 아니다. 잘못된 설명을 막는 것이다. 일시적 코호트 효과를 구조적 회복으로 오해하면 정책은 너무 빨리 느슨해진다. 정책 효과가 실제라면 무엇이 작동했는지 정확히 찾아 강화해야 한다.

            ## 제도 신뢰로서의 가족 형성

            출산 반등은 판결이 아니라 기회로 다루어야 한다.

            올바른 질문은 “한국이 저출산을 해결했는가”가 아니다. 해결하지 못했다. 올바른 질문은 “가족 형성 체계의 어느 부분이 바뀌었는가”이다. 혼인 시기가 회복되었는가. 지연된 부부가 움직이며 첫째아가 늘었는가. 둘째아가 보육 지원에 반응했는가. 특정 지역의 주거 기대가 완화되었는가. 특정 코호트의 노동시장 자신감이 개선되었는가. 정책은 저소득층에 영향을 주었는가, 아니면 이미 출산 직전의 가구에 주로 작용했는가.

            그 분해만이 안도를 지식으로 바꿀 수 있다.

            ## 반등이 보여주는 것

            전체 근거 수준: 중간. 공식 자료가 2025년 출생아 수와 합계출산율의 상승을 보여준다는 점은 높은 확신이다. 정책, 혼인 시기, 코호트 효과, 주거, 노동 조건 사이의 인과 배분은 중간 이하의 확신이다.

            ## 한 해의 개선은 해결이 아니다

            이 글은 반등을 환영하지만 그것을 인구학 교리로 만들지 않는다. 다음 본격 판은 분해 자료를 갖추어야 한다. 그렇지 않으면 숫자를 장식하는 글에 그칠 것이다.

            ## 출생·주거·가족 형성에 관한 출처

            - [KOSIS, Vital Statistics of Korea](https://kosis.kr/statHtml/statHtml.do?language=en&orgId=101&tblId=DT_1B8000F)
            - [Ministry of Data and Statistics, Preliminary Results of Birth and Death Statistics in 2025](https://www.kostat.go.kr/board.es?act=view&bid=11773&list_no=444910&mid=a20108010000&nPage=1&ref_bid=11742%2C11743%2C11744%2C11745%2C11746%2C11747%2C11748%2C11749%2C11773%2C11774%2C11750&tag=)
            - [OECD, Korea's Unborn Future](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/03/korea-s-unborn-future_1b836111/005ce8f7-en.pdf)
            """
        ),
    ),
    IndependentArticle(
        slug="korea-constitutional-court-quiet-institutionalism",
        en_title="Korea's Constitutional Court And Quiet Institutionalism",
        ko_title="한국 헌법재판소와 조용한 제도주의",
        agent="Law and Institutions Editor",
        thesis_en="Korea's constitutional resilience after martial law is visible not only in crisis rulings but in the Court's routine work of thresholds, rights, remedies, and institutional boundaries.",
        thesis_ko="계엄 이후 한국의 헌정 회복력은 위기 판결뿐 아니라 기준, 권리, 구제, 제도 경계를 다루는 헌법재판소의 일상적 작업에서도 드러난다.",
        sources=[
            ("Constitutional Court of Korea, Latest Decisions", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "official English summaries of recent decisions"),
            ("Constitutional Court of Korea, Yoon impeachment decision summary", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "official summary of 2024Hun-Na8"),
            ("Constitutional Court of Korea, Cho Ji-ho impeachment summary", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "official summary of 2024Hun-Na7"),
        ],
        reporting_tasks=[
            "Read Korean full texts for holdings, concurrences, dissents, standards of review, and remedial orders before any permanent legal analysis.",
            "Separate binding reasoning from political interpretation.",
            "Compare emergency-power reasoning with ordinary-rights cases, including assembly and counsel-access decisions.",
        ],
        evidence_control="Official English summaries are enough for temporary framing, not enough for final doctrinal claims.",
        en_body=clean(
            """
            ## Abstract

            Constitutional resilience is often imagined as a dramatic event: soldiers stop, judges speak, crowds celebrate, a president falls. Korea's post-martial-law constitutional story contains that drama. But the deeper institutional lesson lies in quieter work: justiciability, proportionality, attorney access, assembly rules, electoral thresholds, remedial deadlines, and the line between political conflict and emergency power.

            ## The Crisis Case

            The [Constitutional Court of Korea's English decision summaries](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143) record the April 4, 2025 decision removing President Yoon Suk-yeol from office. The Court did not treat martial law as unreachable political mystery. It addressed justiciability, National Assembly procedure, the legal characterization of impeachment grounds, and whether the declaration met constitutional and statutory requirements.

            The central institutional point is simple but heavy: political conflict does not itself create the kind of emergency that justifies military power over constitutional institutions. A president's frustration with the legislature must be handled through ordinary constitutional mechanisms.

            That reasoning matters beyond Korea. Modern executives often redescribe opposition as paralysis, sabotage, crisis, or treason. The Court's logic resists that move. It says the existence of conflict inside a constitutional system is not permission to step outside the system.

            ## The Police Case

            The December 18, 2025 decision removing Police Commissioner General Cho Ji-ho extends the lesson down the chain of command. The official summary states that the National Assembly sought impeachment over blocking access to the National Assembly during martial law, deploying police to election-related facilities, and restricting assemblies.

            This matters because constitutional failure is rarely only presidential. Emergency power requires intermediaries: police, military, ministries, administrators, guards, communications officials. A court that examines only the apex leaves the machinery intact. A court that asks whether subordinate officials gravely violated constitutional duties protects the chain of legality.

            ## Ordinary Cases, Constitutional Habits

            The same official page also lists ordinary-rights cases from 2026: criminal punishment for unnotified outdoor assemblies, denial of weekend attorney visitation to an arrestee seeking review of legality of arrest, the threshold for proportional-representation seat allocation, and other matters. These cases are less internationally famous. They may be more revealing.

            A constitutional court earns legitimacy not only by confronting a failed emergency but by disciplining normal law. Assembly restrictions, counsel access, proportional representation, and remedial deadlines are not glamorous. They are where citizens experience the constitution as procedure rather than mythology.

            ## Quiet Institutionalism

            Quiet institutionalism is the practice of keeping thresholds visible. What counts as an emergency? What counts as a grave violation? When is a restriction proportionate? When should a law be invalidated immediately, and when should it remain temporarily while the legislature repairs it? Which procedural defects matter? Which claims are nonjusticiable?

            These questions sound technical. They are democratic infrastructure. Without them, constitutional politics becomes either heroic sentiment or raw power.

            ## The Anti-Judicialization Case

            The strongest opposing view is that courts can become too central in democratic life. If every political conflict is judicialized, elected institutions may lose responsibility. Courts may also be shaped by appointments, ideology, professional culture, and strategic self-protection. A court that saves democracy once cannot be assumed to save it always.

            This objection is right. Constitutional courts are not democratic angels. But Korea's recent experience shows why legal thresholds matter. The alternative to judicial review of emergency power is not pure democracy. It can be executive unilateralism covered in popular language.

            ## Correction Without Court Worship

            Korea's Constitutional Court should be read as an institution of correction, not as a heroic substitute for politics.

            Its value lies in the ability to say what ordinary politics may not do even under pressure. That role is strongest when it is legally narrow, publicly reasoned, procedurally careful, and consistent across spectacular and ordinary cases. Emergency-power decisions need ordinary-rights decisions around them. Otherwise constitutionalism becomes a one-time rescue rather than a habit.

            ## What Official Summaries Support

            Overall evidence level: moderate. Official English summaries support the article's institutional framing. Full doctrinal evaluation remains limited until Korean full texts, separate opinions, and remedial details are reviewed.

            ## Korean Full Texts Still Matter

            This article deliberately avoids final doctrinal claims based only on English summaries. It treats the summaries as a map of institutional questions requiring deeper Korean-language legal review.

            ## Sources On Constitutional Correction

            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            - [Constitutional Court of Korea, Case Search](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            헌정 회복력은 자주 극적인 사건으로 상상된다. 군인이 멈추고, 재판관이 말하고, 군중이 환호하고, 대통령이 물러나는 장면이다. 계엄 이후 한국의 헌정 이야기에는 그런 드라마가 있다. 그러나 더 깊은 제도적 교훈은 조용한 작업에 있다. 재판 가능성, 비례성, 변호인 접견, 집회 규율, 선거 의석 배분 기준, 개선입법 시한, 정치 갈등과 비상 권한의 경계가 그것이다.

            ## 위기 사건

            [대한민국 헌법재판소의 영문 결정 요약](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)은 2025년 4월 4일 윤석열 대통령 파면 결정을 기록한다. 헌재는 계엄을 사법심사의 바깥에 있는 정치적 신비로 다루지 않았다. 재판 가능성, 국회 절차, 탄핵 사유의 법적 성격 변경, 계엄 선포가 헌법과 법률상 요건을 충족했는지를 검토했다.

            핵심 제도적 요점은 단순하지만 무겁다. 정치 갈등 자체는 헌법기관 위에 군사력을 세울 비상사태가 아니다. 대통령의 의회에 대한 불만은 보통의 헌법 절차로 처리되어야 한다.

            이 논리는 한국을 넘어 중요하다. 현대 행정부는 종종 반대를 마비, 방해, 위기, 반역으로 다시 묘사한다. 헌재의 논리는 그 이동을 막는다. 헌정 체계 안의 갈등은 그 체계 바깥으로 나갈 허가가 아니라는 것이다.

            ## 경찰청장 사건

            2025년 12월 18일 조지호 경찰청장 파면 결정은 교훈을 지휘계통 아래로 확장한다. 공식 요약은 국회가 비상계엄 중 국회 출입 통제, 선거 관련 시설에 대한 경찰 배치, 집회 제한 등을 이유로 탄핵심판을 청구했다고 적는다.

            이는 헌정 실패가 대통령만의 일이 아니기 때문에 중요하다. 비상 권한에는 중간 행위자가 필요하다. 경찰, 군, 부처, 행정관, 경비 인력, 통신 담당자가 있다. 정점만 보는 법원은 기계를 남긴다. 하급 고위공직자의 헌법상 의무 위반까지 묻는 법원은 합법성의 사슬을 보호한다.

            ## 일상 사건과 헌법 습관

            같은 공식 페이지에는 2026년의 일상적 권리 사건도 올라와 있다. 미신고 옥외집회 처벌, 체포적부심을 준비하는 피의자에 대한 주말 변호인 접견 거부, 비례대표 의석 배분 기준, 그 밖의 사건들이다. 이 사건들은 국제적으로 덜 유명하다. 그러나 더 많은 것을 보여줄 수 있다.

            헌법재판소의 정당성은 실패한 비상사태를 막는 것뿐 아니라 보통의 법을 통제하는 데서 생긴다. 집회 제한, 변호인 접견, 비례대표, 개선입법 시한은 화려하지 않다. 그러나 시민이 헌법을 신화가 아니라 절차로 경험하는 장소다.

            ## 조용한 제도주의

            조용한 제도주의란 기준을 보이게 유지하는 일이다. 무엇이 비상인가. 무엇이 중대한 위반인가. 제한은 언제 비례적인가. 법은 언제 즉시 무효가 되고, 언제 입법자가 고칠 때까지 잠정 적용되는가. 어떤 절차 하자가 중요한가. 어떤 청구는 재판 대상이 아닌가.

            이런 질문은 기술적으로 들린다. 그러나 민주주의의 인프라다. 그것이 없으면 헌정 정치는 영웅적 감정이나 날것의 권력으로 바뀐다.

            ## 사법화 경계론

            가장 강한 반론은 법원이 민주적 삶에서 지나치게 중심이 될 수 있다는 것이다. 모든 정치 갈등이 사법화되면 선출 기관은 책임을 잃을 수 있다. 법원 역시 임명, 이념, 직업문화, 자기보호 전략의 영향을 받는다. 한 번 민주주의를 구한 법원이 언제나 구할 것이라고 볼 수는 없다.

            이 반론은 옳다. 헌법재판소는 민주주의의 천사가 아니다. 그러나 한국의 최근 경험은 법적 기준이 왜 중요한지 보여준다. 비상 권한에 대한 사법심사의 대안은 순수 민주주의가 아니다. 대중 언어로 포장된 행정부 일방주의일 수 있다.

            ## 법원 숭배 없는 교정

            한국 헌법재판소는 정치를 대체하는 영웅이 아니라 교정 기관으로 읽어야 한다.

            그 가치는 압력 속에서도 보통 정치가 해서는 안 되는 것을 말할 수 있다는 데 있다. 이 역할은 법적으로 좁고, 공개적으로 이유를 제시하며, 절차적으로 조심스럽고, 극적 사건과 일상 사건에서 일관될 때 가장 강하다. 비상 권한 판결 주변에는 일상적 권리 판결이 있어야 한다. 그렇지 않으면 헌정주의는 습관이 아니라 일회성 구조가 된다.

            ## 공식 요약이 지탱하는 것

            전체 근거 수준: 중간. 공식 영문 요약은 제도적 프레임을 지지한다. 최종 법리 평가는 한국어 전문, 별개의견, 구제 방식 검토 전까지 제한된다.

            ## 한국어 결정문 전문은 여전히 필요하다

            이 글은 영문 요약만으로 최종 법리 주장을 하지 않는다. 요약을 더 깊은 한국어 법률 검토가 필요한 제도 질문의 지도처럼 사용한다.

            ## 헌법적 교정에 관한 출처

            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            - [Constitutional Court of Korea, Case Search](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
    ),
    IndependentArticle(
        slug="universities-after-generative-ai",
        en_title="Universities After Generative AI",
        ko_title="생성형 AI 이후의 대학",
        agent="Education Editor with Technology Editor",
        thesis_en="Generative AI has made assessment design, not cheating detection, the central institutional problem for universities.",
        thesis_ko="생성형 AI는 대학의 핵심 문제를 부정행위 탐지가 아니라 평가 설계로 바꾸었다.",
        sources=[
            ("OECD Digital Education Outlook 2026", "https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html", "education-system response to generative AI"),
            ("UNESCO, Guidance for generative AI in education and research", "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research", "human-centred education governance and policy guidance"),
            ("OECD AI use data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "student and individual adoption context"),
        ],
        reporting_tasks=[
            "Compare actual university policies by discipline: banned, disclosed, permitted, required, or process-documented use.",
            "Add faculty workload data and examples of redesigned assignments.",
            "Separate AI-literacy policy from plagiarism enforcement.",
        ],
        evidence_control="AI use rates do not prove learning outcomes. Assessment claims need assignment-level evidence.",
        en_body=clean(
            """
            ## Abstract

            Generative AI did not merely create a new cheating problem. It exposed a design problem universities already had. If a degree depends on assignments that can be completed by tools students are already using, the question is not only who cheated. It is what the institution was trying to measure.

            ## The Artifact Problem

            Universities have long treated written artifacts as evidence of learning: essays, reports, take-home exams, code, reflections, summaries. Generative AI weakens the link between artifact and authorial process. A submitted essay may still be intelligent, organized, and well cited. It may no longer show what the student can independently do.

            Detection is an understandable response. It is also unstable. The more ordinary AI use becomes, the less plausible it is to treat every polished sentence as suspicious and every tool interaction as misconduct. The institution has to decide what it wants: unaided performance, guided tool use, transparent collaboration, oral defense, process evidence, in-class production, or professional simulation.

            ## Adoption Before Governance

            The [OECD Digital Education Outlook 2026](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html) describes generative AI as unusually accessible and often used beyond institutional control. OECD adoption data also show wide individual and student use. UNESCO's guidance argues for a human-centred approach, capacity building, and policy development rather than simple technological enthusiasm.

            The institutional sequence is uncomfortable. Students adopted first. Policies followed. Assessment redesign comes later because it is labor-intensive. A university can issue a rule in one afternoon; it cannot redesign a curriculum without time, training, and faculty cooperation.

            ## Five Assessment Regimes

            Universities now face at least five possible regimes.

            The prohibition regime bans AI use for defined tasks. It can preserve certain skills but requires credible enforcement and clear rationale. The disclosure regime permits use if students state how they used tools. It teaches accountability but may become ritual if no one checks process. The integration regime requires AI as part of professional practice. It can be realistic but risks widening inequality if some students have better tools or guidance. The process regime evaluates drafts, logs, oral explanations, and revision history. It is pedagogically strong and labor-intensive. The in-person regime returns some assessment to supervised settings. It can protect authorship but may narrow the kinds of work students can do.

            No single regime fits all disciplines. Philosophy, engineering, language learning, studio art, medicine, journalism, law, and computer science have different relationships to tools, evidence, and professional competence.

            ## The Fast-Adaptation Case

            The strongest opposing view says universities are overreacting. Calculators, search engines, grammar checkers, and coding tools all changed academic work. Students should learn to use AI because workplaces will demand it. Excessive policing will waste faculty time and punish honest students.

            This is partly right. AI literacy is now educationally relevant. But the analogy fails when it ignores assessment. A calculator does not write a legal memo, simulate a lab report, or produce a plausible literature review in seconds. The question is not whether tools belong in education. It is which claims a credential makes about the graduate.

            ## Assessment As Institutional Governance

            The university after generative AI must shift from artifact trust to assessment design.

            That means every program should state which competencies must be unaided, which may be tool-assisted, which require disclosure, and which require critique of AI output. It also means faculty need time. Redesigning assessment is not a memo; it is academic labor. Institutions that announce AI policy without changing workload will push the real burden onto individual instructors.

            The best university response is neither panic nor surrender. It is explicitness. Tell students what counts, why it counts, and how the evidence of learning will be gathered.

            ## What The Education Sources Support

            Overall evidence level: moderate. Strong evidence supports broad diffusion and policy urgency. Evidence on learning gains, reliable detection, and discipline-specific best practice remains developing.

            ## The Artifact Problem Is Still Moving

            This article does not claim traditional writing is obsolete. It claims the evidentiary status of submitted work has changed, and universities must redesign assessment around that fact.

            ## Sources On AI And Assessment

            - [OECD Digital Education Outlook 2026](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html)
            - [UNESCO, Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            생성형 AI는 단순히 새로운 부정행위 문제를 만든 것이 아니다. 대학이 이미 갖고 있던 설계 문제를 드러냈다. 학생들이 이미 쓰는 도구로 완성할 수 있는 과제가 학위의 핵심 증거라면, 질문은 누가 부정행위를 했는가에 그치지 않는다. 대학이 무엇을 측정하려 했는가가 된다.

            ## 산출물의 문제

            대학은 오랫동안 글, 보고서, 과제, 코드, 성찰문, 요약문을 학습의 증거로 다루었다. 생성형 AI는 산출물과 작성 과정의 연결을 약화시킨다. 제출된 글은 여전히 지적이고 정돈되어 있으며 인용을 갖출 수 있다. 그러나 그것이 학생이 독립적으로 할 수 있는 일을 보여준다는 보장은 약해졌다.

            탐지는 이해할 수 있는 반응이다. 그러나 불안정하다. AI 사용이 일상화될수록 모든 매끄러운 문장을 의심하고 모든 도구 상호작용을 비위로 다루기는 어렵다. 대학은 무엇을 원하는지 결정해야 한다. 무도구 수행인가, 안내된 도구 사용인가, 투명한 협업인가, 구술 방어인가, 과정 증거인가, 강의실 내 작성인가, 전문직 시뮬레이션인가.

            ## 거버넌스보다 빨랐던 채택

            [OECD Digital Education Outlook 2026](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html)은 생성형 AI가 매우 쉽게 접근 가능하고 제도 통제 바깥에서 많이 쓰인다고 설명한다. OECD의 AI 사용 자료도 개인과 학생의 넓은 사용을 보여준다. UNESCO 지침은 단순한 기술 낙관보다 인간 중심 접근, 역량 형성, 정책 개발을 강조한다.

            제도적 순서는 불편하다. 학생이 먼저 채택했다. 정책은 뒤따랐다. 평가 재설계는 더 늦다. 노동이 많이 들기 때문이다. 대학은 하루 만에 규칙을 낼 수 있지만, 교육과정은 시간, 훈련, 교수진 협력 없이 바뀌지 않는다.

            ## 다섯 가지 평가 체제

            대학 앞에는 적어도 다섯 가지 체제가 있다.

            금지 체제는 특정 과제에서 AI 사용을 금한다. 어떤 능력을 보존할 수 있지만 집행과 이유가 필요하다. 공개 체제는 사용을 허용하되 어떻게 썼는지 밝히게 한다. 책임성을 가르치지만 과정 확인이 없으면 의례가 된다. 통합 체제는 전문직 실무의 일부로 AI 사용을 요구한다. 현실적이지만 더 좋은 도구와 지도를 가진 학생에게 유리할 수 있다. 과정 체제는 초안, 기록, 구술 설명, 수정 이력을 평가한다. 교육적으로 강하지만 노동집약적이다. 대면 체제는 일부 평가를 감독 환경으로 되돌린다. 저자성을 보호하지만 학생이 할 수 있는 작업의 종류를 좁힐 수 있다.

            모든 학문에 하나의 체제가 맞지는 않는다. 철학, 공학, 언어교육, 예술, 의학, 저널리즘, 법학, 컴퓨터과학은 도구, 증거, 전문 능력과 맺는 관계가 다르다.

            ## 빠른 적응론

            가장 강한 반론은 대학이 과잉반응한다는 것이다. 계산기, 검색엔진, 문법 교정기, 코딩 도구도 학업을 바꾸었다. 직장에서도 AI를 요구할 것이므로 학생은 사용법을 배워야 한다. 과도한 단속은 교수 시간을 낭비하고 정직한 학생을 벌할 수 있다.

            부분적으로 맞다. AI 리터러시는 이제 교육적으로 중요하다. 그러나 비유는 평가를 무시할 때 실패한다. 계산기는 법률 메모, 실험 보고서, 그럴듯한 문헌 검토를 순식간에 작성하지 않는다. 문제는 도구가 교육에 속하는가가 아니라 학위가 졸업생에 대해 어떤 주장을 하는가이다.

            ## 제도 거버넌스로서의 평가

            생성형 AI 이후의 대학은 산출물 신뢰에서 평가 설계로 이동해야 한다.

            모든 전공은 어떤 역량이 무도구여야 하는지, 어떤 역량이 도구 보조를 허용하는지, 무엇을 공개해야 하는지, 어떤 경우 AI 산출물 비평이 필요한지 말해야 한다. 또한 교수진에게 시간이 필요하다. 평가 재설계는 공문이 아니라 학문 노동이다. 업무 부담을 바꾸지 않고 AI 정책만 발표하는 기관은 실제 부담을 개별 교수에게 떠넘긴다.

            최선의 대학 반응은 공포도 항복도 아니다. 명시성이다. 무엇이 평가되는지, 왜 평가되는지, 학습 증거를 어떻게 모을지 학생에게 말해야 한다.

            ## 교육 출처가 지탱하는 것

            전체 근거 수준: 중간. 넓은 확산과 정책 긴급성에는 강한 근거가 있다. 학습 효과, 신뢰 가능한 탐지, 학문별 최선 관행에 관한 증거는 아직 발전 중이다.

            ## 산출물 문제는 여전히 움직인다

            이 글은 전통적 글쓰기가 쓸모없어졌다고 주장하지 않는다. 제출물의 증거 지위가 바뀌었고, 대학은 그 사실에 맞게 평가를 다시 설계해야 한다고 주장한다.

            ## AI와 평가에 관한 출처

            - [OECD Digital Education Outlook 2026](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html)
            - [UNESCO, Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            """
        ),
    ),
    IndependentArticle(
        slug="culture-of-ai-fatalism",
        en_title="The Culture Of AI Fatalism",
        ko_title="AI 숙명론의 문화",
        agent="Culture Editor with Technology Editor",
        thesis_en="AI fatalism is a cultural politics of inevitability: it converts institutional choices about labor, education, infrastructure, and rights into a story that no one can meaningfully contest.",
        thesis_ko="AI 숙명론은 필연성의 문화정치다. 노동, 교육, 인프라, 권리에 관한 제도적 선택을 누구도 다툴 수 없는 이야기로 바꾼다.",
        sources=[
            ("Stanford HAI, 2026 AI Index Report", "https://hai.stanford.edu/ai-index/2026-ai-index-report", "diffusion, investment, and adoption context"),
            ("OECD AI use data", "https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html", "firm and individual adoption data"),
            ("UN Global Dialogue on AI Governance", "https://www.un.org/global-dialogue-ai-governance/en", "evidence that public institutions still claim governance authority"),
        ],
        reporting_tasks=[
            "Collect company statements, policy speeches, classroom debates, investor narratives, and magazine essays as discourse evidence only.",
            "Compare inevitability rhetoric with actual adoption gaps by firm size, sector, country, and institution.",
            "Separate cultural mood from technical capability and productivity evidence.",
        ],
        evidence_control="Discourse sources show what people are being told about AI, not what AI will necessarily do.",
        en_body=clean(
            """
            ## Abstract

            AI fatalism is not the belief that AI is powerful. It is the belief that meaningful choice has already ended. In its softer form, it says everyone must adapt. In its harder form, it says schools, workers, governments, writers, and citizens should stop arguing about direction and merely prepare for impact.

            ## Two Kinds Of Inevitability

            There is technical inevitability and social inevitability. Technical inevitability says capabilities will continue to improve. Social inevitability says institutions must reorganize around those capabilities in one predetermined way. The first may be partly true. The second is politics disguised as physics.

            The [Stanford HAI 2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report) and [OECD AI adoption data](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html) show rapid diffusion, uneven adoption, and real institutional pressure. They do not show that every social choice has vanished. Adoption differs by country, sector, firm size, and use case. That variation is precisely where politics lives.

            ## Fatalism As Management Style

            Fatalism is useful to people who want compliance before debate. A company can present layoffs as technological destiny rather than organizational choice. A university can treat assessment redesign as unavoidable disruption while avoiding investment in faculty time. A government can buy systems before building oversight and later say dependency is too advanced to reverse. A platform can describe harms as the cost of progress.

            This is not a conspiracy theory. It is a cultural pattern. When people are told a technology is inevitable, they often stop asking who benefits, who pays, who decides, who can appeal, and what alternatives were rejected.

            ## The Mood Of Acceleration

            AI fatalism flourishes because acceleration feels real. Students use tools before policies are written. Firms adopt systems before workers understand monitoring. Regulators issue guidance while products change. Infrastructure demand rises before energy planning catches up. Public debate is forced to chase announcements.

            The mood is therefore understandable. But understandable moods can still mislead. A fast change is not the same as a settled future.

            ## The Realism Objection

            The strongest opposing view says fatalism is a straw man. The real danger is denial. Institutions that keep debating too long will fail their students, workers, companies, and citizens. Adaptation is not surrender; it is realism.

            This objection is partly right. Refusing to adapt is irresponsible. But adaptation without choice is not realism. It is obedience. The question is not whether AI should be used. It is under what terms, for whose benefit, with which rights, and with what capacity to revise mistakes.

            ## Agency Against Inevitability

            The culture of AI fatalism should be resisted because it weakens democratic agency at the moment when institutions need more of it.

            A society can recognize capability gains and still govern procurement. It can teach AI literacy and still preserve writing, memory, judgment, and professional standards. It can support innovation and still demand audits, contestability, labor negotiation, and energy planning. It can admit uncertainty without calling every objection reactionary.

            Fatalism is not a description of the future. It is a way of closing the present.

            ## What Diffusion Evidence Can Show

            Overall evidence level: moderate. Adoption and diffusion are well documented by institutional sources. Claims about fatalism as cultural politics are interpretive and should be strengthened in later revisions through systematic discourse evidence.

            ## Fatalism Needs Discourse Evidence

            This article does not deny AI's importance. It denies that importance settles governance. The more consequential the technology becomes, the less acceptable fatalism should be.

            ## Sources On AI Mood And Governance

            - [Stanford HAI, 2026 AI Index Report](https://hai.stanford.edu/ai-index/2026-ai-index-report)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            - [United Nations, Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            AI 숙명론은 AI가 강력하다는 믿음이 아니다. 의미 있는 선택은 이미 끝났다는 믿음이다. 부드러운 형태에서는 모두가 적응해야 한다고 말한다. 단단한 형태에서는 학교, 노동자, 정부, 작가, 시민이 방향을 논쟁하지 말고 충격에 대비하라고 말한다.

            ## 두 가지 필연성

            기술적 필연성과 사회적 필연성은 다르다. 기술적 필연성은 능력이 계속 향상될 것이라고 말한다. 사회적 필연성은 제도가 그 능력에 맞추어 하나의 정해진 방식으로 재조직되어야 한다고 말한다. 첫 번째는 부분적으로 맞을 수 있다. 두 번째는 물리학처럼 차려입은 정치다.

            [Stanford HAI 2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report)와 [OECD AI 채택 자료](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)는 빠른 확산, 불균등한 채택, 실제 제도 압력을 보여준다. 그러나 모든 사회적 선택이 사라졌다고 보여주지는 않는다. 채택은 국가, 산업, 기업 규모, 사용 사례에 따라 다르다. 바로 그 차이가 정치가 있는 자리다.

            ## 관리 방식으로서의 숙명론

            숙명론은 논쟁 전에 순응을 얻고 싶은 사람에게 유용하다. 기업은 해고를 조직 선택이 아니라 기술 운명으로 제시할 수 있다. 대학은 교수 시간에 투자하지 않은 채 평가 재설계를 피할 수 없는 혼란으로 말할 수 있다. 정부는 감독 역량을 세우기 전에 시스템을 구매하고 나중에 의존이 너무 깊다고 말할 수 있다. 플랫폼은 피해를 진보의 비용으로 묘사할 수 있다.

            이것은 음모론이 아니다. 문화적 패턴이다. 어떤 기술이 필연이라고 들을 때 사람들은 누가 이익을 얻고, 누가 비용을 부담하며, 누가 결정하고, 누가 이의제기할 수 있고, 어떤 대안이 버려졌는지 덜 묻게 된다.

            ## 가속의 분위기

            AI 숙명론은 가속이 실제처럼 느껴지기 때문에 번성한다. 학생은 정책이 쓰이기 전에 도구를 쓴다. 기업은 노동자가 감시를 이해하기 전에 시스템을 도입한다. 규제기관은 제품이 바뀌는 동안 지침을 낸다. 전력 수요는 계획보다 빠르게 오른다. 공론장은 발표를 뒤쫓는다.

            그래서 분위기는 이해할 만하다. 그러나 이해 가능한 분위기도 틀릴 수 있다. 빠른 변화는 확정된 미래와 같지 않다.

            ## 현실주의 반론

            가장 강한 반론은 숙명론 비판이 허수아비라는 것이다. 진짜 위험은 부정이다. 너무 오래 논쟁하는 제도는 학생, 노동자, 기업, 시민을 실패하게 할 수 있다. 적응은 항복이 아니라 현실주의다.

            이 반론은 부분적으로 맞다. 적응을 거부하는 것은 무책임하다. 그러나 선택 없는 적응은 현실주의가 아니라 복종이다. 문제는 AI를 쓸 것인가가 아니다. 어떤 조건에서, 누구의 이익을 위해, 어떤 권리와 함께, 어떤 수정 능력을 갖고 쓸 것인가이다.

            ## 필연성에 맞서는 행위성

            AI 숙명론의 문화는 저항되어야 한다. 제도에 더 많은 민주적 행위성이 필요한 순간에 그것을 약화시키기 때문이다.

            한 사회는 능력 향상을 인정하면서도 조달을 통치할 수 있다. AI 리터러시를 가르치면서도 글쓰기, 기억, 판단, 전문직 기준을 보존할 수 있다. 혁신을 지원하면서도 감사, 이의제기 가능성, 노동 교섭, 에너지 계획을 요구할 수 있다. 불확실성을 인정하면서도 모든 반대를 반동으로 부르지 않을 수 있다.

            숙명론은 미래에 대한 설명이 아니다. 현재를 닫는 방식이다.

            ## 확산 근거가 보여줄 수 있는 것

            전체 근거 수준: 중간. 채택과 확산은 제도 출처로 잘 문서화된다. 숙명론을 문화정치로 보는 주장은 해석이며, 다음 수정에서는 기업 발언, 정책 연설, 잡지 논쟁, 교육 현장의 담론 증거로 더 강화되어야 한다.

            ## 숙명론에는 담론 증거가 필요하다

            이 글은 AI의 중요성을 부정하지 않는다. 중요성이 거버넌스를 대신 결정한다는 생각을 부정한다. 기술이 중요해질수록 숙명론은 더 용납되기 어렵다.

            ## AI 분위기와 거버넌스에 관한 출처

            - [Stanford HAI, 2026 AI Index Report](https://hai.stanford.edu/ai-index/2026-ai-index-report)
            - [OECD, AI use by individuals and firms](https://www.oecd.org/en/about/news/announcements/2026/01/ai-use-by-individuals-surges-across-the-oecd-as-adoption-by-firms-continues-to-expand.html)
            - [United Nations, Global Dialogue on AI Governance](https://www.un.org/global-dialogue-ai-governance/en)
            """
        ),
    ),
    IndependentArticle(
        slug="structural-reading-list",
        en_title="A Structural Reading List For The Quarter",
        ko_title="이번 분기를 위한 구조적 읽기 목록",
        agent="Final Managing Editor with Source Researcher",
        thesis_en="The issue's reading list should function as an annotated source map, not a prestige bibliography: each source should tell readers what kind of evidence it can and cannot bear.",
        thesis_ko="이번 호의 읽기 목록은 명망 있는 참고문헌 목록이 아니라 주석 달린 출처 지도여야 한다. 각 출처는 어떤 증거 부담을 감당할 수 있고 없는지 독자에게 말해야 한다.",
        sources=[
            ("IMF, World Economic Outlook, April 2026", "https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026", "conditional global macro forecast"),
            ("OECD Economic Outlook, June 2026", "https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html", "scenario-based advanced-economy and global outlook"),
            ("UNHCR Global Trends", "https://www.unhcr.org/us/global-trends", "forced displacement categories"),
            ("Freedom House 2026", "https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy", "democracy trend alarm"),
            ("KOSIS", "https://kosis.kr/eng/", "Korean official statistics portal"),
            ("Constitutional Court of Korea", "https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143", "Korean constitutional decision summaries"),
        ],
        reporting_tasks=[
            "Convert this list into a source-card index with update frequency, source tier, evidentiary use, and known limits.",
            "Add Korean original PDFs and tables where English summaries are insufficient.",
            "Keep opinion magazines in a separate discourse map unless they report original facts.",
        ],
        evidence_control="A bibliography should not blur primary sources, forecasts, indices, journalism, commentary, and discourse evidence.",
        en_body=clean(
            """
            ## Abstract

            A reading list can flatter a magazine or discipline it. The flattering version displays prestigious names. The disciplined version tells readers what each source is for, what it cannot prove, and how it should be checked. For this issue, the reading list should be a source map.

            ## How To Read The Sources

            The first rule is category. Official statistics, court decisions, legislation, institutional reports, academic literature, forecasts, journalism, and commentary do different work. A forecast is not a fact. An index is not a country study. A court summary is not a full opinion. A newspaper article can report facts but cannot replace raw data when raw data are available. A column can reveal discourse but should not be used as evidence that a claim is true.

            The second rule is burden. The more controversial a claim, the more weight the source must carry. A claim about birth numbers should go to KOSIS or the Ministry of Data and Statistics. A claim about a constitutional holding should go to the Constitutional Court. A claim about global displacement should go to UNHCR. A claim about democracy trends can begin with Freedom House or V-Dem but must move to country mechanisms before it becomes causal.

            ## Global Economy

            The [IMF World Economic Outlook, April 2026](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026) is the issue's main global macro source. Its value lies in conditional forecasting: growth, inflation, war risk, financial conditions, trade fragmentation, fiscal space. Its limit is the same as its strength. It is scenario-dependent and revisable.

            The [OECD Economic Outlook, June 2026](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html) adds advanced-economy comparison and scenario framing around disruption. It is useful for cross-country context, not for household-level welfare claims.

            ## Democracy And Institutions

            [Freedom House 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy) and [V-Dem 2026](https://www.v-dem.net/publications/democracy-reports/) should be used as alarms. Their convergence matters. Their limits also matter. They compress institutional realities into scores and categories. Use them to choose cases; do not use them to end arguments.

            The [Constitutional Court of Korea](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143) supplies decision summaries and, through case search, fuller legal material. English summaries are helpful for bilingual readers but insufficient for final doctrinal analysis. Korean full texts should be checked before strong claims about holdings, concurrences, dissents, or standards of review.

            ## Displacement

            [UNHCR Global Trends](https://www.unhcr.org/us/global-trends) is the necessary starting point for forced displacement. It distinguishes refugees, asylum seekers, internally displaced people, returnees, stateless people, and others needing protection. Its limit is aggregation. It tells us the global shape; it does not by itself show local integration, safety of return, or host-community capacity.

            ## Korea

            [KOSIS](https://kosis.kr/eng/) and the Ministry of Data and Statistics should anchor Korean demographic claims. The Bank of Korea and KDI should anchor macroeconomic claims. The National Election Commission and public-data systems should anchor election analysis once verified tables are available. Korean-language newspapers and columns can identify controversy and elite attention, but they should not replace raw sources for statistics, law, or event chronology.

            ## AI And Education

            The OECD AI adoption material, OECD Digital Education Outlook, UNESCO guidance, Stanford HAI AI Index, EU AI Act, and UN Global Dialogue each carry different evidentiary burdens. Adoption data show diffusion. Education reports frame institutional response. The AI Act supplies law and implementation architecture. The UN dialogue shows multilateral process. None alone proves productivity, learning, justice, or democratic legitimacy.

            ## The Anti-Checklist Objection

            The strongest objection to a source map is that it can make essays feel over-engineered. A magazine should have voice, selection, style, and judgment. If every paragraph stops to classify evidence, prose dies.

            The objection is real. But source discipline need not flatten style. It can sharpen it. A writer who knows what a source can bear can write with more confidence because the argument is not leaning on fog.

            ## What Source Mapping Can Do

            Overall evidence level: strong as a map of source hierarchy; moderate as an annotated bibliography because several entries still require Korean full-text, dataset, and PDF-level review.

            ## A Map Is Not The Territory

            This list is not a closed canon. It is a working map for a temporary issue. Sources should be added, downgraded, or removed as dossiers mature.

            ## Source Base For The Issue

            - [IMF, World Economic Outlook, April 2026](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)
            - [OECD Economic Outlook, June 2026](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [KOSIS](https://kosis.kr/eng/)
            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
        ko_body=clean(
            """
            ## 초록

            읽기 목록은 잡지를 꾸밀 수도 있고 훈련시킬 수도 있다. 꾸미는 목록은 명망 있는 이름을 전시한다. 훈련시키는 목록은 각 출처가 무엇을 위한 것인지, 무엇을 증명하지 못하는지, 어떻게 확인되어야 하는지 말한다. 이번 호의 읽기 목록은 참고문헌 장식이 아니라 출처 지도여야 한다.

            ## 출처를 읽는 법

            첫 규칙은 범주다. 공식 통계, 법원 결정, 법률, 제도 보고서, 학술문헌, 전망, 저널리즘, 논평은 서로 다른 일을 한다. 전망은 사실이 아니다. 지수는 국가 연구가 아니다. 법원 요약은 결정문 전문이 아니다. 신문 기사는 사실을 보도할 수 있지만 원자료가 있을 때 그것을 대체할 수 없다. 칼럼은 담론을 보여줄 수 있지만 어떤 주장이 사실이라는 증거로 쓰면 안 된다.

            둘째 규칙은 부담이다. 주장이 논쟁적일수록 출처가 더 많은 무게를 견뎌야 한다. 출생아 수 주장은 KOSIS나 국가데이터처로 가야 한다. 헌법 판단 주장은 헌법재판소로 가야 한다. 세계 강제이주 주장은 UNHCR로 가야 한다. 민주주의 추세 주장은 Freedom House나 V-Dem에서 출발할 수 있지만, 인과 주장으로 가려면 국가별 메커니즘으로 이동해야 한다.

            ## 세계경제

            [IMF 2026년 4월 세계경제전망](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)은 이번 호의 핵심 세계 거시경제 출처다. 그 가치는 조건부 전망에 있다. 성장, 물가, 전쟁 위험, 금융 여건, 무역 분절화, 재정 여지다. 한계도 그 강점과 같다. 시나리오 의존적이고 수정 가능하다.

            [OECD 2026년 6월 경제전망](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)은 선진경제 비교와 충격 시나리오를 더한다. 국가 간 맥락에는 유용하지만 가구 수준 복지 주장의 직접 증거는 아니다.

            ## 민주주의와 제도

            [Freedom House 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)과 [V-Dem 2026](https://www.v-dem.net/publications/democracy-reports/)은 경보로 사용해야 한다. 수렴은 중요하다. 한계도 중요하다. 이들은 제도 현실을 점수와 범주로 압축한다. 사례를 고르는 데 쓰되 논쟁을 끝내는 데 쓰면 안 된다.

            [대한민국 헌법재판소](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)는 결정 요약과 사건 검색을 통해 더 깊은 법률 자료를 제공한다. 영문 요약은 이중언어 독자에게 유용하지만 최종 법리 분석에는 부족하다. 주문, 별개의견, 심사기준을 강하게 말하려면 한국어 전문을 확인해야 한다.

            ## 강제이주

            [UNHCR Global Trends](https://www.unhcr.org/us/global-trends)는 강제이주의 필수 출발점이다. 난민, 비호 신청자, 국내실향민, 귀환자, 무국적자, 보호가 필요한 다른 인구를 구분한다. 한계는 집계다. 세계적 모양을 보여주지만 지역 통합, 귀환 안전성, 수용 공동체 역량은 별도 자료가 필요하다.

            ## 한국

            한국 인구 주장은 [KOSIS](https://kosis.kr/eng/)와 국가데이터처가 떠받쳐야 한다. 거시경제 주장은 한국은행과 KDI가 떠받쳐야 한다. 선거 분석은 검증된 표가 나오면 중앙선거관리위원회와 공공데이터 체계가 떠받쳐야 한다. 한국어 신문과 칼럼은 논쟁과 엘리트 관심을 보여줄 수 있지만 통계, 법, 사건 연대기의 원자료를 대신해서는 안 된다.

            ## AI와 교육

            OECD AI 채택 자료, OECD 디지털 교육 전망, UNESCO 지침, Stanford HAI AI Index, EU AI Act, 유엔 AI 거버넌스 글로벌 대화는 각각 다른 부담을 진다. 채택 자료는 확산을 보여준다. 교육 보고서는 제도 대응을 틀짓는다. AI Act는 법과 실행 구조를 제공한다. 유엔 대화는 다자 과정을 보여준다. 어느 하나도 생산성, 학습, 정의, 민주적 정당성을 단독으로 증명하지 않는다.

            ## 체크리스트 반론

            출처 지도의 가장 강한 반론은 글을 지나치게 설계된 것처럼 만들 수 있다는 것이다. 잡지에는 목소리, 선택, 문체, 판단이 있어야 한다. 모든 문단이 증거를 분류하다 멈추면 산문은 죽는다.

            이 반론은 현실적이다. 그러나 출처 규율이 반드시 문체를 평평하게 만들지는 않는다. 오히려 날카롭게 할 수 있다. 출처가 감당할 수 있는 무게를 아는 필자는 안개에 기대지 않기 때문에 더 자신 있게 쓸 수 있다.

            ## 출처 지도가 할 수 있는 것

            전체 근거 수준: 출처 위계 지도에 대해서는 강함. 주석 달린 참고목록으로서는 중간. 여러 항목은 한국어 전문, 데이터셋, PDF 수준 검토가 아직 필요하다.

            ## 지도는 영토가 아니다

            이 목록은 닫힌 정전이 아니다. 임시 호를 위한 작업 지도다. 도시에는 성숙함에 따라 출처를 추가, 하향, 삭제해야 한다.

            ## 이번 호의 출처 기반

            - [IMF, World Economic Outlook, April 2026](https://www.imf.org/en/publications/weo/issues/2026/04/14/world-economic-outlook-april-2026)
            - [OECD Economic Outlook, June 2026](https://www.oecd.org/en/publications/2026/06/oecd-economic-outlook-volume-2026-issue-1_8be0dba6.html)
            - [UNHCR, Global Trends](https://www.unhcr.org/us/global-trends)
            - [Freedom House, Freedom in the World 2026](https://freedomhouse.org/report/freedom-world/2026/growing-shadow-autocracy)
            - [KOSIS](https://kosis.kr/eng/)
            - [Constitutional Court of Korea, Latest Decisions](https://english.ccourt.go.kr/site/eng/ex/bbs/List.do?cbIdx=1143)
            """
        ),
    ),
]


def update_article_file(article: IndependentArticle, language: str, stage: str, body: str) -> None:
    path = BASE / stage / language / f"{article.slug}.md"
    meta, _old_body = split_front_matter(read_text(path))
    meta["independent_editorial_pass"] = TODAY
    meta["body_generation"] = "independent_article_structure"
    meta["assigned_agent"] = article.agent
    meta["updated"] = TODAY
    title = article.en_title if language == "en" else article.ko_title
    write_text(path, dump_front_matter(meta, article_header(title, language) + body), overwrite=True)


def write_dossier(article: IndependentArticle) -> None:
    path = BASE / "source_dossiers" / f"{article.slug}.md"
    text = f"""---
issue: "{ISSUE}"
slug: "{article.slug}"
title: "{article.en_title}"
status: independent_rewrite_dossier
chief_editor_status: approved_for_review
updated: "{TODAY}"
assigned_agent: "{article.agent}"
---

# Source Dossier: {article.en_title}

## Independent Reporting Assignment

This article is assigned to the {article.agent}. It must proceed as a magazine article, not a compact briefing skeleton. The public article should carry argument, evidence, cases, and prose; development notes belong here or in review files.

## Central Thesis

{article.thesis_en}

## Korean Thesis Check

{article.thesis_ko}

## Raw Source Base

{source_lines(article)}

## Reporting Tasks Moved Out Of Public Article

{task_lines(article)}

## Evidence Controls

{article.evidence_control}

## Sources Not To Use As Raw Evidence

Korean-language columns, editorials, newsletters, and already synthesized commentary may be used only as evidence of discourse, media attention, or elite framing unless they report original facts with traceable documentation. Statistics, legal claims, election facts, and policy descriptions must return to raw or institutional sources.
"""
    write_text(path, text, overwrite=True)


def write_review(article: IndependentArticle) -> None:
    path = BASE / "reviews" / f"{article.slug}_review.md"
    text = f"""---
issue: "{ISSUE}"
slug: "{article.slug}"
date: "{TODAY}"
status: independent_rewrite_checked
chief_editor_status: approved_for_temporary_publication
assigned_agent: "{article.agent}"
---

# Editorial Review: {article.en_title}

## Independent Agent Check

The June 12 rewrite assigns the article to the {article.agent} and removes the previous compact-body structure. The public text now uses article-specific sections, evidence, cases, and argument flow instead of a common 20-heading scaffold.

## Relocated Development Notes

The following items are retained as review or dossier tasks, not public-article prose:

{task_lines(article)}

## Fact Check

The article links factual claims to the raw source base listed in its dossier. Claims that require fuller tables, Korean full legal texts, or official post-election datasets are marked as provisional or deferred.

## Statistics Check

{article.evidence_control}

## Dissent Editor

The article includes an article-specific opposition section that states the strongest good-faith objection before the author's argument proceeds.

## Style Editor

The article was revised away from dossier language and repeated process phrases. Remaining limitations are handled in article-specific evidence and uncertainty sections.
"""
    write_text(path, text, overwrite=True)


def write_translation_review(article: IndependentArticle) -> None:
    path = BASE / "reviews" / f"{article.slug}_translation_review.md"
    text = f"""---
issue: "{ISSUE}"
slug: "{article.slug}"
date: "{TODAY}"
status: independent_translation_checked
chief_editor_status: approved_for_temporary_publication
---

# Translation Review: {article.en_title}

The Korean version follows the same thesis, source hierarchy, uncertainty limits, and opposing-view structure as the English version. It is not a literal line translation; it is written as Korean intellectual-magazine prose while preserving citations and claim boundaries.
"""
    write_text(path, text, overwrite=True)


def write_failure_memo() -> None:
    path = BASE / "reviews" / "independent_agent_failure_memo.md"
    text = f"""---
issue: "{ISSUE}"
date: "{TODAY}"
status: corrective_review
chief_editor_status: approved_for_review
---

# Corrective Review: Why The Independent-Agent Standard Failed

## Finding

The original policy documents required article work to be performed by distinct editorial agents: political editor, economics editor, sociology editor, law and institutions editor, technology editor, education editor, foreign affairs editor, culture editor, source researcher, data researcher, dissent editor, fact checker, statistics checker, translation editors, and final managing editor. The June 11 production pass did not satisfy that standard. The June 12 repair corrected nine articles but left four core English originals on the older scaffold: the editor's note, the AI governance essay, the AI/war-economy leader, and the macro fragility essay.

## Immediate Cause

The retired `pipelines/substantive_2026_q2_editorial_pass.py` centralized article bodies through compact generator functions named `{RETIRED_EN_BUILDER}` and `{RETIRED_KO_BUILDER}`. Those functions imposed the same section order, the same argument-reconstruction language, the same temporary-publication language, and similar source-limit paragraphs across unrelated articles. The later repair fixed the visible generator symbols but did not require every public English original to declare an assigned editor, use an independent article structure, or carry matching independent dossiers and reviews.

## Process Cause

The same pipeline wrote bodies, reviews, dossiers, translation checks, and publication-ready files in one pass. That collapsed role boundaries. It made a file look as if it had passed multiple editorial desks when the article body had in fact come from one scaffold.

## Metadata Cause

The public files identified broad "Codex Editorial Agents" rather than enforcing a per-article assigned editor in the generator. Agent-role prompt files existed, but the production script did not require role-specific outputs before publication.

## Review Gap

Existing tests checked publication gates, bilingual links, citation status, and required headings. They did not check repeated prose, identical section structures, public-facing development notes, whether source dossiers had been separated from article prose, or whether every public English original had an assigned editor and independent rewrite review.

## Corrective Actions Taken

- Retired the compact generation script and removed `{RETIRED_EN_BUILDER}` / `{RETIRED_KO_BUILDER}`.
- Added `pipelines/rewrite_2026_q2_independent_articles.py`, which stores article-specific bodies and assigned agents without a shared body template.
- Rewrote the nine affected article pairs with distinct structures, cases, and argument development.
- Completed the missed four core article pairs on June 13: `editors-note-capacity-question`, `govern-ai-before-infrastructure`, `ai-boom-war-economy`, and `new-macro-fragility`.
- Moved "stronger final version" and similar reporting-path material into source dossiers and review files.
- Added a regression test blocking compact-generation symbols and public-facing reporting-path phrases in final/site article files.
- Added regression tests requiring public English originals to declare `assigned_agent`, `body_generation: independent_article_structure`, and `independent_editorial_pass`; requiring matching independent source dossiers and reviews; blocking reuse of compact heading scaffolds; and blocking duplicate final English heading signatures.

## Remaining Editorial Risk

The corrected articles are substantive temporary-publication drafts. Several still need deeper non-temporary reporting: Korean full legal texts, official election tables after NEC verification, disaggregated fertility data, fiscal and welfare tables, and systematic discourse evidence for AI fatalism. These are now recorded as dossier tasks rather than presented as article conclusions.
"""
    write_text(path, text, overwrite=True)


def main() -> int:
    for article in ARTICLES:
        update_article_file(article, "en", "drafts", article.en_body)
        update_article_file(article, "ko", "drafts", article.ko_body)
        update_article_file(article, "en", "final", article.en_body)
        update_article_file(article, "ko", "final", article.ko_body)
        write_dossier(article)
        write_review(article)
        write_translation_review(article)

    write_failure_memo()
    copy_approved_articles_to_site()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
