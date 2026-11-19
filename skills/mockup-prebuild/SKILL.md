---
name: mockup-prebuild
description: Build a clickable before/after prototype of the screens a planned change will affect, and publish it as a shareable link a non-technical stakeholder can approve BEFORE any code is written. Use this whenever a plan touches a user-facing screen and someone wants to see or show it first, triggered by "mock this up", "mockup", "prototype", "show me what it will look like", "let me show the client first", "before we build", "can I see the screens", or a request for design sign-off. Also offer it unprompted once an implementation plan involving new or changed screens has been agreed, since that is the last moment when changing the design is cheap. Not for finished work, use mockup-signoff once the code exists.
---

# Mock up a change before building it

Produce one shareable web page showing each affected screen **as it is today**
next to **what it would become**, written for someone who has never seen the
code, and publish it as a link.

The point is timing. Once the plan is agreed, changing the design costs a plan
edit. Once it is built, it costs a rewrite. This page exists to get an
objection out of the client's head during the cheap window.

Two ways this goes wrong, and both are avoidable:

- **A mock that cannot actually be built.** It gets approved, then the real
  thing comes out different and you have broken a promise you made on the
  developer's behalf. Step 4 exists entirely to prevent this.
- **A mock too rough to judge.** If it does not look like the app, the client
  reviews the drawing rather than the decision, and you have spent a round trip
  learning nothing.

**Do not use this for** backend-only work, bug fixes with no visible change, or
anything already built. It costs the client's attention, so spend it only where
there is a real design decision to make.

This skill knows nothing about any particular app. Everything project-specific
,  the screens, how to run it, its colours, its layout limits, lives in that
project's own notes file, which step 0 finds.

---

## Step 0, Find the project's notes file

Glob for `.claude/mockup-notes.md` from the project root.

**Missing** → copy `references/notes-template.md` to `.claude/mockup-notes.md`
in the project, then **stop**. Tell the user in one message that the file has
been created, name the sections they need to fill in, and say to re-run this
skill afterwards. Do not start the mockup, and do not infer the app's screens
or styling from the code, a guessed screen inventory is worse than none,
because it looks authoritative.

**Present** → read the sections you need as you reach them, not all at once.
Each step below names the section it wants.

**A section you need still says `FILL IN`** → stop and name that section. Same
reason: do not guess.

**`Last checked` more than about three months old** → carry on, but mention
once in the handover that the notes may have drifted from the app.

Generic screenshot failure modes are in `references/screenshot-mechanics.md`,
which applies to every project. Read it when a capture misbehaves.

## Step 1, Work out which screens change, then ask

Read the agreed plan or feature description and list **every screen it
touches**, naming each one the way the client would, not the way a file is
named. The screen inventory is in the notes file, section 1.

For each, write one line on what changes there. Mark any screen that does not
exist yet as new, because it will have no "before".

Then ask which to include. **Default to all**, but ask, because some screens
change so trivially that showing them dilutes the ones that matter, and the
person requesting knows which those are. With four or fewer screens ask as a
multiple-choice question; beyond that, list them and ask which to drop.

Getting this list right in front of a human first also catches the case where
the plan touches a screen nobody had thought about, which is worth knowing
before you spend an hour drawing.

## Step 2, Capture "before"

Run the app, sign in, and screenshot each screen at the size the notes file
gives in section 3. Sign-in details and start commands are in section 2.

Sign in as the role that actually does this job. Roles usually see different
screens, and a "before" captured as the wrong person is a misleading
comparison rather than a helpful one. Section 1 says who sees what.

For a screen that does not exist yet, do not invent a before. The template has
a panel that says so plainly; an honest blank is more informative than a
mocked-up predecessor that never existed.

If screenshots are impossible, rebuild the current screen as HTML from its
component source, and tell the person who invoked the skill that it is a
reconstruction, so they know the comparison is approximate. That caveat is for
them, not for the client.

## Step 3, Build "after"

This is the substance. Notes file, section 4.

**Copy, do not invent.** Read the component being changed and lift its real
colours, spacing and font sizes from wherever section 4 says the styling
lives. A mock built from the app's own values is close to pixel-accurate for
almost no extra effort. A generic-looking one trains the client to review your
drawing rather than the decision.

**Change only what the plan changes.** Keep the surrounding screen intact , 
sidebar, header, neighbouring columns, the other fields on the form. People
judge a change by what it sits next to. A cropped mock hides exactly the
problems this exercise is for, such as a new column pushing an old one off the
edge.

**Make it clickable wherever the change is behavioural.** If choosing an option
makes two fields disappear, the client should be able to choose it and watch
them go. That interaction *is* the feature; a still image cannot show it and
the client will imagine something else. Plain JavaScript in the page is enough.

**Do not build a working feature.** No real data, no saving, no validation.
Enough to demonstrate, not to use. If you find yourself wiring up state
management, you have gone past the point where a mock is the cheap option.

## Step 4, Check it can actually be built

Before anyone sees it, check the mock against what the app can really do.
Notes file, section 5, lists the limits that bite here, tables already at
their width, components that clip instead of scrolling, attributes the app
silently ignores.

Ask directly: *if a developer built exactly this, would it come out looking
like this?*

If the answer is no, you have found something valuable early. Either redraw the
mock to something buildable, or tell the person who invoked the skill that the
plan has a problem, before the client sees a design that cannot be delivered.

## Step 5, Assemble the page and publish it

Copy `assets/page-template.html` into the scratch directory, replace every
`REPLACE` marker, and duplicate the screen block once per screen. Set
`--canvas-w`, `--canvas-h`, `--app-bg`, `--app-ink` and the typeface from
sections 3 and 4 of the notes.

Write the page to **scratch space, never the repo.** These pages go stale
within weeks, and a stale mock committed alongside the code becomes a second,
wrong description of how the app works. A dated link that is obviously a
snapshot is safer than a file that looks current.

Publish it as an artifact to get the link. Give it a plain title in the
client's words. On a later revision, publish the **same file path** so the link
the client already has keeps working rather than becoming a second version to
confuse them.

## Step 6, Hand it over

Return two things:

1. **The link.**
2. **A short message they can paste to the client**, two or three sentences
   naming what to look at and what decision is being asked for. Sign-off is
   much faster when the client knows what question they are answering.

Also mention anything you had to assume, and anything from step 4 that
constrained the design. That belongs in the chat, not on the page.

---

## Writing the page for the client

Section 0 of the notes file names who this reader is and what words they use.
They have never seen the code and never will. Every sentence on the page is
for them.

**Never name** a file, component, database table, column, function, branch or
pull request. Never write that something was refactored, migrated, re-keyed or
extracted. These are true and they are noise, and each one costs the reader a
moment of feeling that this page is not for them.

**Describe changes as things a person does differently.** Not *"the delivery
field becomes conditional"* but *"when the order is being collected in person,
the tool stops asking for an address."*

**Keep captions to one or two sentences,** leading with the change and then why
it helps. If a caption needs a third sentence, the screen is probably doing two
things and wants splitting.

**Use the reader's own vocabulary**, the words listed in section 0. They are
their words, and translating them helps nobody.

**Say what does not change.** The template has a section for it. A client
reading about changes will silently wonder what else moved; naming the things
that stayed put is often the difference between a quick yes and a nervous
meeting.

Avoid *simply*, *just* and *obviously*. Nothing is simple to someone seeing it
for the first time, and those words quietly tell the reader they are slow.

---

## Traps worth knowing

**Screenshotting a screen that looks broken but is not.** Most apps have a few
screens that render empty, zero or sparse on local test data. Notes file,
section 6, lists them. Photographing one of those and captioning it as the
current state would be badly wrong.

**Mocking at a narrower width because it is easier.** Use the width in section
3. A mock built narrower than the app is ever used at shows a layout the real
thing will never render, and hides the crowding that is often the actual design
problem.

**Letting a mock become documentation.** The moment it is approved it starts
going out of date. It answers one question at one moment. If someone wants to
keep a record of what was agreed, keep the link somewhere outside the repo.

**Drawing the happy path only.** If the change has an empty state, an error, or
a "nobody has set this up yet" state, that is frequently where the real design
question is. Ask whether it is worth a second screen rather than assuming not.

---

## Keeping this in step with mockup-signoff

Three files are **byte-for-byte copies** of the same files in the
`mockup-signoff` skill:

```
assets/page-template.html
references/notes-template.md
references/screenshot-mechanics.md
```

The two skills are deliberately independent, neither reaches into the other's
folder, because a cross-skill path breaks quietly the moment either is moved or
renamed.

The cost of that independence is that a fix applied to one copy leaves the other
wrong, and nothing will tell you. After changing any of the three, copy it across
and run this from `~/.claude/skills` in Git Bash. It prints `all good` or the one
thing that is wrong:

```bash
for f in assets/page-template.html references/notes-template.md references/screenshot-mechanics.md; do diff -q "mockup-prebuild/$f" "mockup-signoff/$f" >/dev/null 2>&1 || { echo "OUT OF SYNC: $f"; exit 1; }; done; echo "all good"
```

A drifted pair shows up as two mock-ups of the same app that do not look alike,
which reads as sloppiness to the client rather than as the maintenance slip it is.
