---
title: Dark Crystal
description: Secret recovery through social backups
date: 2018-07-01
slug: dark-crystal
image: logo.jpeg
categories:
  - projects
tags:
  - cryptography
  - scuttlebutt
  - accessibility
weight: 1

links:
  - title: Dark Crystal
    description: Website
    website: https://darkcrystal.pw/
  - title: Dark Crystal (Java, Briar)
    website: https://dark-crystal-java.gitlab.io/
---

## About

Some friends and I were exploring blockers to cryptocurrency being accessible
and identified that "recovery" (of secrets) was perhaps the number 1 challenge.

In 2017 I'd messed around with [Shamir's secret sharing](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing), and we noticed that we could use this concept in concert with a social network in order to safely store backups. Here's some art I made describing the process:

![1. sharding and distributing](shard_1.jpeg)
![2. recovering shards](shard_2.jpeg)
![3. recombining shards](shard_3.jpeg)
![4. secret recovered](shard_4.jpeg)

We designed a protocol, wrote a specification, and implemented a prototype in Scuttlebutt (a social p2p/ local-first social network).

![Dark Crystal in Patchbay](screenshot.jpeg)

We presented our work at [DevCon 4](https://www.youtube.com/watch?v=pOloj658DtQ)
and this led to grants from the Ethereum Foundation, further iterations on
protocol, user-research, partnership with Briar, a java implementation and more.




## Technical


| Library | Description |
|---|---|
| [scuttle-dark-crystal](https://github.com/blockades/scuttle-dark-crystal) | Raw function for running Dark Crystal over Scuttlebutt |
| [patchbay-dard-crystal](https://github.com/blockades/patchbay-dark-crystal) | plugin for [Patchbay](/p/patchbay) (a Scuttlebutt client) |


