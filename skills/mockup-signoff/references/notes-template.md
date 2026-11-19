# <App name>, notes for building mock-ups and screenshots

This file lives at `.claude/mockup-notes.md` inside the project it describes. The
`mockup-prebuild` and `mockup-signoff` skills read it; they know nothing about
this app except what is written here.

Fill in every `FILL IN`. A skill stops rather than guess at a section it needs,
so a half-filled file blocks the run that needs it, but it can be filled in over
time, since each section is only read when a run actually requires it.

**Do not renumber the sections.** Both skills cite them by number.

`Last checked: FILL IN, YYYY-MM-DD`
_The date someone last confirmed this file still matches the app. Once it goes
stale the skills carry on but say so._

---

- [0. Who the page is for](#0-who-the-page-is-for)
- [1. Screen inventory](#1-screen-inventory)
- [2. Running the app and signing in](#2-running-the-app-and-signing-in)
- [3. Taking screenshots](#3-taking-screenshots)
- [4. Making a mock look like the real app](#4-making-a-mock-look-like-the-real-app)
- [5. Layout limits a mock must respect](#5-layout-limits-a-mock-must-respect)
- [6. Test-data traps](#6-test-data-traps)

---

## 0. Who the page is for

Every sentence on the client-facing page is written for this person. Naming them
is what stops the page drifting into developer language.

| | |
|---|---|
| **App name** | FILL IN, appears as the label at the top of the page |
| **Who reads the page** | FILL IN, their job, not their name, e.g. "the person who runs the warehouse". Assume they have never seen the code and never will. |
| **What they use the app for** | FILL IN, one sentence |
| **Their vocabulary** | FILL IN, the words they use for the things in the app, and any word they would *not* recognise. The page uses their words, never the code's. |

---

## 1. Screen inventory

Every screen, named the way a user says it, not the way a file is named. The
skills use these names on the client-facing page and when asking which screens to
include.

| Area | Screens | Who can see it |
|---|---|---|
| FILL IN | FILL IN | FILL IN |

**Names people get wrong.** FILL IN, screens that sound like they exist but do
not, settings that live inside a dialog rather than on their own page, or two
screens people habitually confuse. Delete this line if there are none.

**Which screens are mobile.** FILL IN, if some screens are phone-sized and the
rest desktop-only, say which. A mock drawn at the wrong device size shows a
layout the real app will never render.

---

## 2. Running the app and signing in

Enough for someone who has never started this app to get it running and reach any
screen in section 1.

**Start it:**

```
FILL IN, the commands, one per line, with the port each serves on
```

**First run on a fresh checkout.** FILL IN, dependency install, database reset or
seed, anything not tracked in version control. Chain steps with `&&`, never `;` , 
with `;` a failed step still reports success and the breakage surfaces later
looking like a code problem.

**Signing in.** FILL IN, how to sign in locally, and whether it needs a real
account. List the test users worth knowing:

| User | Role | Use it for |
|---|---|---|
| FILL IN | FILL IN | FILL IN |

Confirm the sign-in worked by looking for that person's name on screen, not by
assuming the write landed.

**When the port is already taken.** FILL IN, how to run on an alternate port,
including any origin or CORS setting that must change with it. Getting that half
right typically means reads work and saves fail, which looks exactly like a bug in
the feature being photographed. Delete this if it never happens.

**The URL to open.** FILL IN, including any path suffix.

---

## 3. Taking screenshots

**Shoot at:** FILL IN, width × height, e.g. `1440 × 900`. Choose the width where
this app's layout problems become *visible* rather than hidden, which is usually
the narrowest width a real user would have.

**Device:** FILL IN, desktop-only, responsive, mobile-first, or a mix. If mixed,
say which screens are which; section 1 should already list them.

**Second size worth capturing:** FILL IN, or "none". Only worth it if the app is
genuinely used at two sizes.

Generic screenshot failure modes, a viewport reporting zero width, the pane
being unavailable, a click and a check colliding in one call, live in the skill's
own `references/screenshot-mechanics.md`. They are not project-specific and do not
belong here.

---

## 4. Making a mock look like the real app

A mock built from the app's real values is close to pixel-accurate for almost no
extra effort. A generic-looking one trains the client to review the drawing rather
than the decision.

**Where the real styling lives:** FILL IN, a CSS framework and its config, a
design-tokens file, a theme module, or inline styles in the components. Give the
path. The skills read values out of the code rather than out of this file, so they
cannot drift as the app changes.

**Read before drawing anything:** FILL IN, the one or two files worth opening
every time, such as the shared palette or token file.

These few are structural enough to state here, and are what a mock gets wrong most
visibly:

| | Value |
|---|---|
| Typeface | FILL IN, and whether it is on Google Fonts, the only font host a published page may load from |
| Page background | FILL IN |
| Panels / cards | FILL IN |
| Borders | FILL IN |
| Primary / active colour | FILL IN |
| Fixed structural widths | FILL IN, a sidebar that never shrinks, a fixed header height |
| Light or dark | FILL IN, which the app renders in. If it is light-only a dark mock is a lie, and the reverse. |
| Date format on screen | FILL IN, e.g. `DD-MM-YYYY`. Getting this wrong reads as a change nobody asked for. |

**Framework note.** The mock is a standalone page and may use a `<style>` block
regardless of how the app itself is authored. What it must not do is pull a CSS
framework from a CDN, those are blocked when the page is published, so every
class silently resolves to nothing and the mock renders as bare HTML. If this app
uses a framework, the mock reproduces the *result* by hand.

---

## 5. Layout limits a mock must respect

A mock that gets approved and then cannot be built as drawn is worse than no mock
,  a promise has been made on the developer's behalf. List what would break.

Worth checking for and recording here:

- **Tables already at or past their width.** FILL IN, name the table, its column
  count, and the width it needs. Where a table already overflows, adding a column
  is a decision about which existing column stops being visible, and a mock showing
  a new column fitting comfortably is lying.
- **Anything that clips instead of scrolling.** FILL IN, content cut off at an edge
  with no way to reach it.
- **Fixed minimum widths** that hold a component wider than its contents, so editing
  column widths will not narrow it. FILL IN.
- **Props or attributes the app silently ignores.** FILL IN, for instance a shared
  cell component that drops column spans. A mock relying on one needs a different
  approach in the real build.

Delete any bullet that does not apply. An empty section 5 is a legitimate answer
for a simple app, write "none known" rather than leaving `FILL IN`.

---

## 6. Test-data traps

Screens that render empty, zero or sparse on local data and look broken when they
are fine. Photographing one and captioning it as the current state would be badly
wrong.

- FILL IN, the screen, what it looks like, and the one action that makes it show
  real content: switching a filter, seeding a record, signing in as someone else.

Also record states that are **unreachable** on local data, an over-budget warning,
an error, a full inbox. If a mock needs to show one it has to be inserted by hand,
or flagged as unverifiable.

Write "none known" rather than leaving `FILL IN` if local data is clean.
