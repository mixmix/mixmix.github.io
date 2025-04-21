---
title: Uncapturable Distribution
description: I've hosted two workshops this year where the highest named goal was humanity joining the Galactic Council. 
# slug: power-and-learning
date: 2015-10-25 00:00:00+0000
image: galaxy.jpg
categories:
    # - peer-2-peer
tags:
    - peer-2-peer
    - systems
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---


So I hang out with a bunch of big dreaming nerds with a bunch of different
interests, but when we explore what it is we want in our future, it's a happy
thriving civilisation. You'll know we're there because we'll be looking after
each other, curiously exploring, sharing our successes, and making
intergalactic friends.

The workshops were about developing a Theory of Change for each group. 

> **Theory of Change**
>
> _The process of forming a [Theory of
> Change](http://www.theoryofchange.org/what-is-theory-of-change/) is about
> coming up with a map of how change will come about in the world. It starts by
> a group building a shared vision of it's particular desired end-state is.You
> then proceed to build a graph of dependent states back from that end point to
> the current state of the world. This is called 'back-casting'._
>
> _The process has several steps including things like surfacing and testing
> assumptions, detailing how you would measure successful change at each step,
> and assessing the cost and nature of intervention to prgress between states._


In each of the workshops, 2 hours of conversation made barely a dent in
completing a fully detailed map, but we'd revealed a lot of territory. Both
workshops explored similar veins, but here I'll explore the second, because
it's fresher in memory and highly relevant to my current work.

## Why build a decentralised database?

This is a workshop I ran with the Secure Scuttlebutt team who all happened to
be in San Francisco recently. Here's what the top of our theory of change
diagram looked like :

![](TOS_2.jpg)

Some important things we agreed we need to achieve were :

- specialisation without inequity
- rich ecosystem (supports diverse approaches)

I'd like to explore one particular chain of states back. This format makes it
hard to simultaneously discuss the branching and interconnected dependencies,
so please forgive me if the analysis seems to narrow. I'm interested in this
particular chain because it raised questions which provided a useful frame or
lens for projects I'm working on or with. From the top it reads :

1. Galactic council
2. Large scale social harmony
3. Post scarcity
4. Distribution primarily in service of society
5. Distribution is distributed and un-ownable
6. We build our distribution on un-capturable technologies

As distribution surfaced as a theme, we tested our assumptions against real-world examples :

- distribution of food and goods: supermarkets, walmart
- distribution of information: email, google, facebook

We observed that **ownership** of distribution by **actors mainly interested in
profit** has lead to problematic dynamics which block us from joining the
Galactic Council. See massive food waste, destruction of diversity through
monopoly, development of tools which optimise addiction and consumption,
development of tools which define value for us.


## Some examples

Here's a breakdown of a couple of interesting cases in the context of
information distribution.

**[Email]** : a super successful open protocol. Anyone can send emails to
anyone. The failing of email is that it has no mechanism for dealing with
un-wanted noise (see spam). This has generated a niche for organisations to
offer value (spam filtering), and capture users. For example Gmail is popular
because it does fairly reliable spam filtering. This makes email less open,
because small private servers have a harder time generating a good 'not-spam'
reputation.

> Distribution systems must have a solution to noise.

**[Facebook]** : built on an open protocol - http - but has centralised closed
databases, and a closed (proprietary) interface. Facebook's primary motivation
is profit, which inclines it to leverage it's closed-ness (right of refusal of
access) to extract value from it's user-base.

> All parts of a distribution system need to be uncapturable - open protocols
> are not sufficient

_[facebook ToS](https://www.facebook.com/terms.php)_

**[Google]** : the growth of the internet beyond easily navigable scales led to
the birth of search engines. The current winning solution to this problem is an
algorithm which determines site value based on linkages and references. Again,
this is a niche which has been captured by a primarily profit motivated
organisation. This capture looks something like a monopoly through dependence,
and is [defended by a suite of related free and powerful
tools](http://techcrunch.com/2011/03/25/search-googles-castle-moat/).

> Distribution systems need to address capturable searchability


## Things you should consider

I've named a bunch of assumptions and principles that we think need to be
integrated in order to get us on the road to The Galactic Council.

What is your interaction with distribution systems, are you investing in
systems that build the future you want to see?

- How do you network online, is it via an actor interested mostly in profit?
- Who holds power over the definition of value of what you're interacting with?
- Where do you publish your content?

I think it's overly idealistic to transition immediately to decentralised
uncapturable solutions, but there are small choices that we can and should
start making if we want to live in a thriving society.


## Possible solutions

### Open-sourcing

![Loomio logo](loomio.jpg)

With [Loomio](http://www.loomio.org/) (a collaborative decision-making
platform), we've addressed some of these same problems by a steadfast
commitment to being [open-source](https://github.com/loomio/loomio). While
individual instances of the platform may have closed databases, the
open-sourcing of the platform code means that anyone can own and control their
own instance. It also makes advertising and data-mining significantly less
likely, because anyone in the community can fork the code-base and rip anything
extractive out. For Loomio this is actually a selling point - it's a clear
signal that our primary value is in serving society.

With Loomio, capturing ownership has also been very seriously addressed in how
we've written our constitution, and our approach to investment. In short, you
can't buy Loomio, and no one person can control it.

### Publish carefully

![Hypermarkdown logo](hypermarkdown.png)

You might notice this isn't published on medium. Honestly, this is an
experiment in document splicing using a tool I made currently called
[Hypermarkdown](https://github.com/mixmix/hypermarkdown). In retrospect this
approach does tick some boxes. This content is currently being hosted at
[github.com](https://github.com/mixmix/blogposts/blob/master/uncapturable_distribution.md)...
which sounds like my content might be captured buuuut, github is acutally built
on a distributed content system called [git](https://git-scm.com/). An exact
mirror of the data lives on my computer as well, and could easily be hosted by
any git based server, like a self-hosted [gitlab](https://about.gitlab.com/).

There's still the problem of how it is you've found your way to this blog.
99.9% liklihood is that in 2015 it was via facebook, or twitter (it probably
wasn't via google because the way I built this accidentally makes it harder to
index).

(**Edit (2025)** - I've since pulled this into another git repo which generates
this static site using Hugo)


### Build an open combined protocol-database

The solution I'm currently investing in is [**Secure Scuttlebutt**
](https://github.com/ssbc/docs). It's an open and secure decentralised database
where distribution flows along trust lines, as determined by following
(positive value) and flagging (negative value).

![Hermes the hermit-crab](hermes_logo.png)

Anyone is free to build an app to interface (read/ write) with this database.
The first app is a proof of concept messaging app called
[**Patchwork**](https://github.com/ssbc/patchwork). 

Check out a brief introduction +[](https://www.youtube.com/watch?v=vmQUfZMCVJ0)

The Scuttlebutt team is planning to open beta Patchwork in November 2015.

An overview of scuttlebutt's solution to some know problems with distribution
systems:

- [x] All open uncapturable system: the protocol is open and the database is
  open and distributed. People can only edit their own data and reference
  others.
- [x] Has an uncapturable solution to noise: distribution only flows along
  trust lines in the network.
- [x] Searchable: relevance is similarly determined by trust relationships in
  the network.

**(Which pitfalls have we missed?)**

