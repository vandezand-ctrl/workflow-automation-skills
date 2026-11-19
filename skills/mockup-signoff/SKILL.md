---
name: mockup-signoff
description: Photograph the screens a finished branch actually changed, put them next to how they look today, and publish it as a shareable link so a non-technical stakeholder can confirm the work before it is merged. Use this once UI work is built and working but not yet merged, triggered by "sign-off", "signoff", "show the client what we built", "confirm before we merge/ship", "is this ready to merge", "get the client to approve this", or when a branch with visible changes is about to become a pull request. Also offer it unprompted whenever UI work finishes and a PR is about to be opened, since this is the last point before the change reaches real users. For work that does not exist yet, use mockup-prebuild instead.
---

# Get sign-off on what was actually built

Produce one shareable web page showing each changed screen **as it looks today**
next to **how it looks on this branch**, using real screenshots of the running
app on both sides, and publish it as a link for the client to confirm.

**This is a gate.** The purpose is a decision: the client looks, and says yes or
asks for a change, before the work reaches real users. Say so when you hand the
link over, and do not treat the work as finished until they have answered.

The difference from `mockup-prebuild` is the whole point: that skill shows a
drawing of an intention, this one shows a photograph of reality. Nothing on this
page may be hand-drawn. If a screenshot is impossible, say so rather than
substituting a mock, a mock presented as the built thing is worse than no page
at all, because it invites sign-off on something nobody has verified.

This skill knows nothing about any particular app. Everything project-specific , 
the screens, how to run it, the test data that makes working screens look broken
,  lives in that project's own notes file, which step 0 finds.

---

## Step 0, Find the project's notes file

Glob for `.claude/mockup-notes.md` from the project root.

**Missing** → copy `references/notes-template.md` to `.claude/mockup-notes.md`
in the project, then **stop**. Tell the user in one message that the file has
been created, name the sections they need to fill in, and say to re-run this
skill afterwards. Do not start photographing, and do not infer the app's screens
or sign-in from the code.

**Present** → read the sections you need as you reach them. Each step names the
section it wants.

**A section you need still says `FILL IN`** → stop and name that section.

**`Last checked` more than about three months old** → carry on, but mention once
in the handover that the notes may have drifted from the app.

Generic screenshot failure modes are in `references/screenshot-mechanics.md`,
which applies to every project. Read it when a capture misbehaves, several of
them look like a bug in the feature you are photographing.

## Step 1, Work out which screens changed, then ask

List **every screen this branch changes**, naming each the way the client would,
not the way a file is named. The screen inventory is in the notes file, section
1. Note which are new.

Then ask which to include. **Default to all**, but ask, some screens change so
slightly that including them buries the ones that matter. With four or fewer
screens, ask as a multiple-choice question; beyond that, list them and ask
which to drop.

If a `mockup-prebuild` page was produced for this work, list the same screens it
covered, so the client is looking at the same set they already approved.

## Step 2, Capture "before"

In order of preference:

1. **Reuse the before screenshots from the prebuild run** if they are still in
   scratch space. Same images, guaranteed consistency with what the client saw
   before.
2. **Otherwise, run the app from a checkout of the project's main branch**, a
   separate worktree on an alternate port is the least disruptive way, and
   screenshot there. Section 2 of the notes has the start commands, and what to
   change when the usual port is taken.

**Never screenshot production.** This page becomes a link that can be forwarded,
and production holds real people's names, contact details and whatever else the
app stores about them. Local test data has invented people in it, which is what
makes it safe to publish. This is the one rule in this skill with a consequence
outside the project.

For a screen that is genuinely new, use the template's "does not exist today"
panel rather than inventing a predecessor.

## Step 3, Capture "after"

Run the branch, sign in as the role that actually does this job, and screenshot
each screen at the size the notes file gives in section 3. Sign-in details are
in section 2.

Take the same view on both sides, same role, same filters, same tab, same
size. A before and after that differ in two ways at once teaches the client
nothing about either.

While you are in the browser, this is also the moment to confirm the thing
works: click it, watch it respond, and check nothing rendered at a useless size.
Automated tests frequently apply no styling at all, so a screen can pass every
test and still be visibly broken. Two tooling mechanics reliably produce false
alarms here, both in `references/screenshot-mechanics.md`.

**If a screenshot shows something wrong, that is a finding, not a caption.** Fix
it and re-shoot. The client should be confirming a decision, not discovering a
defect you already saw.

## Step 4, Say where it differs from what was agreed

If a prebuild page exists, compare what shipped against what was drawn. Where
they differ, say so on the page in one plain sentence, with the reason.

Do this even when the difference is an improvement. A client who spots an
unannounced change stops trusting the page; a client who reads *"the new column
ended up beside Status rather than at the end, because the row would otherwise
have run off the edge of the screen"* learns something and trusts it more.

Where nothing drifted, say that too, it is a short sentence and it is exactly
what they want to know.

## Step 5, Assemble the page and publish it

Copy `assets/page-template.html` into scratch space, replace every `REPLACE`
marker, and duplicate the screen block once per screen. Set `--canvas-w`,
`--canvas-h`, `--app-bg`, `--app-ink` and the typeface from sections 3 and 4 of
the notes. Set the status line to something like *"Built and ready, please
confirm before it goes live."*

Write it to **scratch space, never the repo.** These pages go stale in weeks,
and one committed next to the code becomes a second, wrong description of how
the app works.

Publish it as an artifact for the link. If a prebuild page exists for the same
work, publish this one to its **own** file path, the two pages answer different
questions and both are worth keeping reachable while the decision is open.

## Step 6, Hand it over, and hold the gate

Return three things:

1. **The link.**
2. **A short message to paste to the client**, naming what changed and asking
   plainly for confirmation to go live.
3. **A line for the pull request description** with the same link, so whoever
   reviews the code can see what it was meant to look like.

Then say clearly that the branch is waiting on the client's answer. The value of
this skill is entirely in that pause; a page produced and then merged past is
just decoration.

---

## Writing the page for the client

Section 0 of the notes file names who this reader is and what words they use.
They have never seen the code and never will.

**Never name** a file, component, database table, column, function, branch or
pull request, and never write that something was refactored, migrated or
extracted. Each one costs the reader a moment of feeling this page is not for
them.

**Describe changes as things a person does differently.** Not *"the delivery
field is now conditional"* but *"when the order is being collected in person,
the tool stops asking for an address."*

**Keep captions to one or two sentences.** Lead with the change, then why it
helps.

**Use the reader's own vocabulary**, the words listed in section 0.
Translating their words helps nobody.

**Say what does not change.** The template has a section for it. Someone about
to approve a change to a tool their team depends on is quietly wondering what
else moved, and naming the things that stayed put is often the difference
between a fast yes and a nervous meeting.

Avoid *simply*, *just* and *obviously*.

---

## Traps worth knowing

**Screenshotting production.** Covered above and worth repeating, because it is
the easy path: production is already running and already has interesting data in
it. It also has real people's personal details, and this page is a link that can
be forwarded. Use local test data.

**Photographing a screen that looks broken but is not.** Most apps have a few
screens that render empty, zero or sparse on local test data. Notes file,
section 6, lists them. Sending the client a page where a working screen appears
empty will cost you a meeting.

**A before and after that differ in more than the change.** Different sign-in,
different filter, different tab, different window size. The comparison only
carries meaning if one thing varies.

**Quietly redrawing a screenshot to look better.** If the built thing is uglier
than the mock, that is information the client is entitled to. Show it and
explain it. The moment this page contains anything hand-drawn, it stops being
evidence and becomes another drawing.

---

## Keeping this in step with mockup-prebuild

Three files are **byte-for-byte copies** of the same files in the
`mockup-prebuild` skill:

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

A drifted pair shows up as two pages about the same app that do not look alike , 
which, on a page whose whole job is to be trusted evidence, costs more than the
duplication does.
