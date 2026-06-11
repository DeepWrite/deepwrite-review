---
title: "Current Issue"
subtitle: "2026-Q2 temporary publication"
permalink: /current/
---

The 2026-Q2 issue has entered temporary publication. Two bilingual article pairs are public while the rest of the issue remains in draft, review, or commissioning.

The editorial mix remains roughly 70 percent global or transnational coverage and 30 percent Republic of Korea coverage.

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
No article is public yet. Drafts remain under `/issues/2026-Q2/` until the Chief Editor approves publication.
{% endif %}
