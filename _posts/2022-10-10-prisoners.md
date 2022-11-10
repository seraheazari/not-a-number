---
layout: post
title: "زندانیان"
date: 2022-10-10 00:00:00
permalink: prisoners/
---

<div class='prisoners'>
  {% for person in site.data.prisoners %}
  <div class='profile'>
    <div class='fa lang-fa'>
      <p class='name'>{{ person.name_fa }}</p>
      <div class='meta'>
        <span class='date'>
          تاریخ بازداشت: 
          {{ person.arrest_date }}
          </span>
      </div>
      <img src='{{ person.image | prepend: site.baseurl }}' />
    </div>
    
    <div class='en hidden'>
      <p class='name'>{{ person.name_en }}</p>
      <div class='meta'>
        <span class='date'>
          Detainment date:
          {{ person.arrest_date }}
        </span>
      </div>
      <img src='{{ person.image | prepend: site.baseurl }}' />
    </div>
  </div>
  {% endfor %}
</div>

<script src="/js/prisoners.js"></script>
