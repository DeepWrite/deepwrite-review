---
layout: home
title: "DeepWrite Review"
permalink: /
---

<section class="home-hero">
  <div class="home-hero-copy">
    <p class="issue-label">2026-Q2 temporary publication</p>
    <h1>DeepWrite Review</h1>
    <p class="hero-subtitle">A bilingual quarterly review of politics, economy, society, technology, law, education, and culture.</p>
    <div class="hero-actions">
      <a class="button primary" href="{{ '/current/' | relative_url }}">Current Issue</a>
      <a class="button secondary" href="{{ '/editorial-policy/' | relative_url }}">Editorial Policy</a>
    </div>
  </div>
  <aside class="issue-mockup" aria-label="Current issue editorial model">
    <div class="mockup-masthead">
      <span>DeepWrite Review</span>
      <span>English / 한국어</span>
    </div>
    <div class="mockup-feature">
      <p>Current issue</p>
      <h2>The AI Boom Meets The War Economy</h2>
      <p class="mockup-ko">AI 붐은 전쟁경제와 만난다</p>
    </div>
    <div class="mockup-byline">
      <strong>DeepWrite Review Editorial Desk</strong>
      <span>Prepared with Codex editorial agents</span>
      <span>책임편집: 손제연</span>
    </div>
    <ol class="mockup-list">
      <li><span>01</span><strong>Leader Essay</strong><em>temporarily published</em></li>
      <li><span>02</span><strong>Macro Essay</strong><em>temporarily published</em></li>
      <li><span>03</span><strong>Korea Essays</strong><em>temporarily published</em></li>
      <li><span>04</span><strong>Annotated Bibliography</strong><em>temporarily published</em></li>
    </ol>
  </aside>
</section>

<section class="editorial-frame">
  <div>
    <h2>Continuous editorial radar, quarterly publication judgment.</h2>
    <p>The magazine gathers, classifies, and prepares between issues. Publication waits for human editorial approval.</p>
  </div>
  <ol class="process-list">
    <li><strong>Weekly</strong><span>editor brief</span></li>
    <li><strong>Monthly</strong><span>topic map</span></li>
    <li><strong>Quarterly</strong><span>issue production</span></li>
    <li><strong>Always</strong><span>evidence gates</span></li>
  </ol>
</section>

<section class="issue-preview">
  <div class="section-heading">
    <h2>Current Issue</h2>
    <a href="{{ '/archive/' | relative_url }}">Archive</a>
  </div>
  {% assign temporary_articles = site.articles | where: "status", "temporary_publication" | where: "chief_editor_status", "approved_for_temporary_publication" %}
  {% assign final_articles = site.articles | where: "status", "published" | where: "chief_editor_status", "approved_for_publication" %}
  {% assign published_articles = temporary_articles | concat: final_articles %}
  {% if published_articles.size > 0 %}
    <div class="article-grid">
      {% for article in published_articles limit: 6 %}
        <article class="article-card">
          <a href="{{ article.url | relative_url }}">
            <span>{{ article.language | upcase }}</span>
            <h3>{{ article.title }}</h3>
            <p>{{ article.subtitle }}</p>
          </a>
        </article>
      {% endfor %}
    </div>
  {% else %}
    <div class="empty-publication">
      <h3>No approved public articles yet.</h3>
      <p>2026-Q2 production has begun. No article will appear here until it passes citation, evidence, translation, and Chief Editor approval gates.</p>
    </div>
  {% endif %}
</section>

<section class="policy-strip">
  <a href="{{ '/source-policy/' | relative_url }}">
    <strong>Explicit sourcing</strong>
    <span>Tiered source hierarchy and traceable claims.</span>
  </a>
  <a href="{{ '/evidence-policy/' | relative_url }}">
    <strong>Evidence grading</strong>
    <span>Statistical claims require metadata and limitations.</span>
  </a>
  <a href="{{ '/editorial-policy/' | relative_url }}">
    <strong>Argument balance</strong>
    <span>Strong opposing views before judgment.</span>
  </a>
  <a href="{{ '/authorship-policy/' | relative_url }}">
    <strong>Transparent bylines</strong>
    <span>Editorial desk authorship with disclosed Codex assistance.</span>
  </a>
</section>
