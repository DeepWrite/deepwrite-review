---
title: "Historical Issues"
subtitle: "Retrospective legal philosophy and legal theory reviews reconstructed at five-year intervals"
permalink: /historical/
---

The historical back-issue program is separate from the contemporary quarterly review. Each issue is labeled by target year and keeps time-situated analysis, retrospective editor's notes, and archival uncertainty apart.

{% assign historical_issues = site.historical_issues | sort: "target_year" | reverse %}

<div class="historical-list">
{% for issue in historical_issues %}
  <article class="historical-list-item">
    <a href="{{ issue.url | relative_url }}">
      <span>{{ issue.historical_status }}</span>
      <h2>Historical Issue: {{ issue.target_year }}</h2>
      <p>{{ issue.coverage_note }}</p>
    </a>
  </article>
{% endfor %}
</div>

## Production Order

Default: 2025, 2020, 2015, 2010, 2005, 2000, 1995, 1990, 1985, 1980, 1975.

The Chief Editor may choose chronological, theme-first, or opportunistic reconstruction based on available sources.
