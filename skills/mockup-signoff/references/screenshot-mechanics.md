# Screenshot mechanics

How the browser tooling fails while capturing screens, and what each failure
actually means. None of this is project-specific, the width to shoot at, the
sign-in details and the screens that look broken on local data are all in the
project's own `.claude/mockup-notes.md`.

Every failure below looks like something else, which is why they are worth
knowing before spending an hour on the wrong diagnosis.

---

## The tab reports a 0 × 0 viewport

Every measurement comes back zero, so any width checked reads as broken layout
and the screenshot is unusable or empty.

The tell is that `window.innerWidth` is itself `0`.

The fix is to bring the tab to the front and *then* resize it. Resizing a
background tab silently does nothing and reports no error, so a resize that
appears to have worked may not have.

---

## Screenshots are unavailable entirely

The tool reports that the browser pane is not being displayed, and no image comes
back at all.

Reading the page's text and computed styles still works, so content can be
verified, what cannot be produced is a picture.

What to do about it depends on which skill is running, and the difference matters:

- **`mockup-prebuild`**, rebuild the current screen as HTML from its component
  source instead, and tell the person who invoked the skill that it is a
  reconstruction so they know the comparison is approximate. That caveat is for
  them, not for the client; it would only confuse the client.
- **`mockup-signoff`**, say plainly that the screenshot could not be taken. Do
  not substitute a drawing. That skill's entire value is that the picture is real,
  and a mock presented as the built thing invites sign-off on something nobody has
  verified.

---

## A click and a check for what it changed cannot share one call

Clicking a row and then checking for the dialog it opened, in the same call,
returns the state from *before* the click. The page has not re-rendered yet.

It reads as "the click did nothing" and sends you looking for a bug that is not
there. Split them across two calls.

---

## Before and after must differ in exactly one way

Not a tooling failure, but it wastes runs the same way. Same sign-in, same
filters, same tab, same window size, same scroll position, with only the change
itself varying.

A before and after that differ in two ways at once teaches the client nothing
about either, and usually costs a full round trip to discover.
