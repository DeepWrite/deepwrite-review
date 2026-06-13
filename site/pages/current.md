---
title: "Current Issue"
subtitle: "2026-Q2 temporary full-issue publication"
permalink: /current/
---

The 2026-Q2 issue is temporarily published in full: 13 English-Korean article pairs are public under Chief Editor approval.

The issue remains open to later source strengthening, Korean style editing, and complete quarterly packaging.

{% assign temporary_articles = site.articles | where: "status", "temporary_publication" | where: "chief_editor_status", "approved_for_temporary_publication" %}
{% assign final_articles = site.articles | where: "status", "published" | where: "chief_editor_status", "approved_for_publication" %}
{% assign published_articles = temporary_articles | concat: final_articles %}

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
