---
# An update within a project. Shown inline on the project's page and as its own
# item on the homepage (project name + this title as the subtitle).
title: "{{ replace .Name `-` ` ` | title }}"
date: {{ .Date }}
# image:   # optional; otherwise the first image below, then the project's image
---
