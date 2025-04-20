---
title: Comms Gardening
description: How I use Signal groups for memory, dreaming, sense-making, coherance.
# slug:
date: 2025-04-19 00:00:00+0000
# image: cover.jpeg
categories:
    - patterns
tags:
    - learning
weight: 1
draft: true
---

## The death of a friendship :skull: :seedling:

This pattern was born of the death of a relationship. I helped grow an really
successful open-source project with this person - we grew a community,
distributed grant funds, started a coop, and took on contracts to build products
based on the tech. 

The problem that snuck up on us was that our personal communications were
interleavened with our technical (and work) conversations. This was not so
uncommon in my experience from social-enterprise -- we bring our "whole selves"
to the grand project right? Ultimately my friend raised that he was having trouble
distinguising whether my messages were us connecting as friends or me filing
support tickets. Seeing unread messages from me had started to generate
confusion and I guess anxiety.

We managed to name the problem, but too late. Too much damage had been done and
we were unable to recover. I was gutted -- I was complicit, naive, and deeply
mourned the loss of our friendship. I never wanted to make this mistake again...
and so I started partitioning my comms. As this pattern evolved I noticed new
generative dynamitcs which I'd not foreseen :seedling:


## Work Chats

These were the first. In Signal I started creating dedicated 1:1 chats to
protect against this mistake. Here's how that looks:

<div class='chats'>
  <details open="">
    <summary>
      <div class='icon'>😀</div>
      <div class='title'>Ben</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>

  If I write something in here it's me writing to Ben as a
  friend. He doesn't need to worry I'm coming at him with some work request, this
  is about us connecting as friends.
    </div>
  </details>

  <details>
    <summary>
      <div class='icon'>💼</div>
      <div class='title'>Ben/ Mix work</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>

  Work coordination. If it's out-of-office hours, this can wait.
    </div>
  </details>

:information_source: &nbsp; _click to expand_
</div>


## Family Chats

Some of the first partitions I introduced were to clarify...

<div class='chats'>
  <details>
    <summary>
      <div class='icon'>🏡</div>
      <div class='title'>Family Admin</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>

  I've got a couple young kids. Family administration is a whole category, it's kinda 
  a grind and I got scared that this would dominate all my communication with my wife.
  This channel is mundane, but like the "work" chat above it allows us to protect our
  relationship (to a degree) from the onslaught of logistics.

   </div>
  </details>

  <details open=true>
    <summary>
      <div class='icon'>🚑</div>
      <div class='title'>Family Health Stuff</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>

  This channel started when I noticed that there are some health symptoms which
  are not a threat ... unless they've been running longer than a few
  weeks. This is a dumping ground for misc observations on the wellbeing
  on anyone in the family:
  - <Daughter> ears / ear - seemed to clear yesterday "everything is so loud"
  - son, dry cough still
  - daughter: 5mL Parecetamol
  - Mix: 81KG, blood pressure 126/80

  Things
   </div>
  </details>

  <details>
    <summary>
      <div class='icon'>🌈</div>
      <div class='title'>Read/ Watch/ Do</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>

  <details>
    <summary>
      <div class='icon'>🎉</div>
      <div class='title'>Family Dreams</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>

  <details>
    <summary>
      <div class='icon icon-double'>💬 😅</div>
      <div class='title'>Family Quotes</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>

  <details>
    <summary>
      <div class='icon'>🥵</div>
      <div class='title'>Only Fans</div>
      <div class='note'>(not lewd)</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>

  <details>
    <summary>
      <div class='icon'>T_T</div>
      <div class='title'>Emotional Damage</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>

  <details>
    <summary>
      <div class='icon'>❤️</div>
      <div class='title'>Relationship Retro</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
  </details>
</div>


## Community Chats

<div class='chats'>
  <details >
    <summary>
      <div class='icon'>☀️</div>
      <div class='title'>Pōneke Toddler Wranglers</div>
      <div class='expand-symbol'>+</div>
    </summary>
    <div class='body'>
    </div>
</div>


<style>
.chats {
  --summary-bg: var(--card-background);
  --icon-bg: rgb(255, 245, 255);
  --details-bg: var(--card-background);

  background: var(--summary-bg);
  padding: 2rem calc(var(--card-padding) + 0rem);
  /* border-radius: 1rem; */
  border: 1px solid var(--body-text-color);
  /* box-shadow:  */
  /*   0px 3px 5px -1px rgba(0, 0, 0, 0.10) inset, */
  /*   0px 6px 10px 0px rgba(0, 0, 0, 0.05) inset, */
  /*   0px 1px 18px 0px rgba(0, 0, 0, 0.02) inset; */
  margin: 0 calc(-1 * var(--card-padding));

  display: grid;
  grid-gap: 1.5rem;

  > p {
    /* color: white; */
    padding-left: 1rem;
    opacity: 0.8;
  }

  --lum: 95%;
  details:nth-last-child(-2n) { --icon-bg: hsl(180deg, 100%, var(--lum)); }
  details:nth-last-child(2n+1) { --icon-bg: hsl(270deg, 100%, var(--lum)); }
  details:nth-last-child(4n+1) { --icon-bg: hsl(0deg, 100%, var(--lum)); }
  details:nth-last-child(3n+2) { --icon-bg:  hsl(80deg, 100%, var(--lum)); }
}

details {
  /* padding: 10px !important; */
  /* background: red; */
  margin: 0 !important;

  cursor: pointer;
  transition: 0.15s background linear;

  summary {
    list-style: none;
    /* color: white; */
    background: var(--summary-bg);

    display: grid;
    grid-template-columns: auto 1fr auto auto;
    align-items: center;
    grid-gap: 1.5rem;

    .icon {
      width: 6rem;
      height: 6rem;
      font-size: 3.2rem;
      background: var(--icon-bg);
      color: #333;

      border-radius: 50%;
      box-shadow: 0px 3px 5px -1px rgba(0, 0, 0, 0.10);

      display: grid;
      justify-items: center;
      align-items: center;

      &.icon-double {
        font-size: 2.4rem;
      }
    }
    .title {
      font-size: 1.8rem;
      font-weight: 500;
    }
    .note {
      opacity: 0.6;
      margin-right: 2rem;
    }
    .expand-symbol {
      grid-column: 4;
      font-size: 3rem;
      margin-right: 2rem;

      display: grid;
      text-align: center;

      transition: all linear .2s;
    }
  }

  .body {
    min-height: 6rem;
    cursor: auto;
    background: var(--details-bg);
    padding: 4px 0;
    border-radius: 4px;
    margin: 1rem;

    /* carat thing */
    &:before {
      content: "";
      width: 0;
      height: 0;
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      border-bottom: 12px solid var(--details-bg);
      top: -10px;
      position: absolute;
      left: 10px;
    }

    filter:
      drop-shadow(0px 3px 5px  rgba(0, 0, 0, 0.12))
      drop-shadow(0px 6px 10px rgba(0, 0, 0, 0.05))
      drop-shadow(0px 1px 18px rgba(0, 0, 0, 0.03));
  }
}


details[open] {
  .expand-symbol {
    transform: rotate(-45deg);
    opacity: 0.4;
  }

  p {
   animation: animateDown 0.2s linear forwards;
 }
}

@keyframes animateDown {
  0% {
    opacity: 0;
    transform: translatey(-15px);
  }
  100% {
    opacity: 1;
    transform: translatey(0);
  }
}

</style>
