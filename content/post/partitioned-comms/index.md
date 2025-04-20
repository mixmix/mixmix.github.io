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
protect against this mistake. Here's how that looks 

<div class='chats'>
  <details open="">
    <summary>
      <div class='icon'>😀</div>
      <div class='title'>Ben</div>
      <div class='expand-symbol'>+</div>
    </summary>

  If I write something in here it's me writing to Ben as a
  friend. He doesn't need to worry I'm coming at him with some work request, this
  is about us connecting as friends.
  </details>

  <details>
    <summary>
      <div class='icon'>💼</div>
      <div class='title'>Ben/ Mix work</div>
      <div class='expand-symbol'>+</div>
    </summary>

  Work coordination. If it's out-of-office hours, this can wait.
  </details>

:information_source: &nbsp; _click to expand_
</div>


## Family Partitions

Some of the first partitions I introduced were to clarify

<style>
.chats {
  --summary-bg: var(--body-background);
  --icon-bg: white;
  --details-bg: var(--card-background);

  background: var(--body-background);
  padding: 2rem calc(var(--card-padding) + 0rem);
  /* border-radius: 1rem; */
  margin: 0 calc(-1 * var(--card-padding));

  display: grid;
  grid-gap: 1rem;

  > p {
    padding-left: 1rem;
    opacity: 0.7;
  }
}

details {
  /* padding: 10px !important; */
  /* background: red; */
  margin: 0 !important;

  cursor: pointer;
  transition: 0.15s background linear;

  summary {
    list-style: none;
    background: var(--summary-bg);

    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    grid-gap: 1rem;

    .icon {
      width: 6rem;
      height: 6rem;
      font-size: 2.5rem;
      background: var(--icon-bg);
      border-radius: 50%;

      display: grid;
      justify-items: center;
      align-items: center;
    }
    .title {
      font-size: 1.8rem;
      font-weight: 600;
    }
    .expand-symbol {
      font-size: 3rem;
      margin-right: 2rem;

      display: grid;
      text-align: center;

      transition: all linear .2s;
    }
  }
}

details p {
  cursor: auto;
  background: var(--details-bg);
  padding: 1rem;
  margin: 1rem;
  /* width: 250px; */
  /* position: absolute; */
  left: 0;
  top: 35px;
  border-radius: 4px;
  right: 0;

  box-shadow:
    0px 3px 5px -1px rgba(0, 0, 0, 0.08),
    0px 6px 10px 0px rgba(0, 0, 0, 0.05),
    0px 1px 18px 0px rgba(0, 0, 0, 0.02);

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
}

details[open] {
  .expand-symbol {
    transform: rotate(45deg);
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
