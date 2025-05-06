---
title: Pōneke Mesh
description: A primer and opinionated guide to getting Wellington set up with LoRa comms
date: 2025-05-05
slug: poneke-mesh
image: cover.png
categories:
  - projects
tags:
  - meshtastic
  - LoRA
weight: 1

links:
  - title: SensecCAP T1000e
    website: https://www.seeedstudio.com/SenseCAP-Card-Tracker-T1000-E-for-Meshtastic-p-5913.html
draft: true
---



## Why?

In an earthquake, one of your primary needs is to be able to coordinate with 
those you love. _Are you ok? Where are you? Do you have the kids?_

The cellular network is great, but relies on a functional electrical grid, fibre
network. Any remaining towers may be overwhelmed (everyone panics and calls)...
ideally they are serving people buried under buildings. So we need something
else


## Mesh Networks

A low-cost, accessible solution is we run our own mesh network. A mesh network
is made up of many devices, each of which can talk to it's neighbour. This means
that someone in Miramar can write a message, which is thrown to peer in
Kilbernie, then Mount Vic, ... and on to it's destination in Upper Hutt.

![An mesh network made up of devices talking to their neighbours. Bold red line
showing the path a message took from Miramar → Upper Hutt](mesh_map.png)

The more devices there are in a mesh network, the more resilient it becomes.kk

Cell phones alone can't do this, but there are consumer-grade Bluetooth devices
which effectively let us do this for $67 NZD.

![Picture of a SenseCAP T1000e - a mesh networking device](senscap_t1000e.png)


A mesh network is one made up of many devices, and messages are passed from
one to another, traversing the mesh.

![](meshtastic.svg)

There are now consumer-grade devices which let us turn our cell-phones
into devices which can communicate over longer distances, using an ad-hoc
(pop-up) mesh network.



This solution is each own a small device, which connects to your phone, and can
throw messages many kilometers using low-powered, long-range radio
([LoRa](https://en.wikipedia.org/wiki/LoRa)).



In a swarm, these devi 


A mesh network is made up of a bunch of peers talking who can talk to each
other, passing messages to their neigbours to get messages to travel further.



is one which is made up of a bunch of peers/ nodes which talk to each other, and
pass messages to one another.




