---
layout: default
---

<div class="index">
  <ul class="post-list">
    {% for post in site.posts %}
      <li class='lang-{% if post.lang %}{{ post.lang }}{% else %}en{% endif %}'>
        <h2>
          <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title | markdownify }}</a>

          <p class="post-meta">
            <!--<span>{{ post.date | date: "%b %-d, %Y" }}</span>-->
          </p>
        </h2>
        <article class='post-content'>
          {{ post.excerpt }}
        </article>
      </li>
    {% endfor %}
  </ul>
</div>
