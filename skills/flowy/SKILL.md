---
name: flowy
description: Create, read, and update Flowy diagram HTML files for flowcharts, system diagrams, and UI wireframes/mockups. Use this skill whenever the user asks to diagram a flow, visualize architecture, sketch a UI, plan a feature visually, create a wireframe, map out a process, create an HTML diagram, or mentions "flowy". Also use when the user references existing .html diagram files in the docs/diagrams/ directory, or asks to update/modify a diagram.
---

# Flowy, AI-Native Diagram Skill

Flowy generates **self-contained HTML files** that render interactive SVG diagrams. Each file includes embedded CSS, JavaScript, and diagram data, zero dependencies, just double-click to open in any browser.

## File Locations

- **Diagrams**: `docs/diagrams/*.html` (e.g. `docs/diagrams/upload-flow.html`).
  Create the folder on first use; it may not exist yet. If a project already keeps
  diagrams somewhere else, follow that project's convention instead.
- **HTML template**: `${CLAUDE_SKILL_DIR}/references/html-template.html`, the
  canonical renderer, and the only reference file this skill ships. The path resolves
  to this skill's own folder wherever it is installed (plugin, personal or project),
  so it does not depend on the current project.

There is deliberately no schema file, no examples folder and no visual editor. Earlier
versions of this skill pointed at `flowy/schema.ts`, `flowy/examples/`,
`flowy/editor.html` and a `Flowy` source repo on disk. **None of those exist**, the
paths were stale, and following them wasted time. The HTML template above is the
source of truth for the structure; read it before writing a diagram.

## Preflight

Before creating or editing a Flowy diagram:
1. Read `${CLAUDE_SKILL_DIR}/references/html-template.html` to have the current renderer code
2. List existing diagrams in `docs/diagrams/` to avoid naming conflicts
3. If updating an existing diagram, read it first and extract the `DIAGRAM` object

## Schema

Every diagram is a JavaScript object with three fields:

```
{
  meta: { title, description, type, tags[], created, updated },
  nodes: [...],
  edges: [...]
}
```

### meta

| Field       | Type     | Required | Notes |
|-------------|----------|----------|-------|
| title       | string   | yes      | Human-readable title |
| description | string   | no       | What the diagram shows |
| type        | string   | yes      | `"flowchart"` or `"ui-mockup"` |
| tags        | string[] | no       | For organization |
| created     | string   | no       | ISO date (YYYY-MM-DD) |
| updated     | string   | no       | ISO date, set to today when creating/updating |

### nodes

| Field    | Type              | Required | Notes |
|----------|-------------------|----------|-------|
| id       | string            | yes      | unique, snake_case (e.g. `"step1_upload"`) |
| type     | string            | yes      | `"box"`, `"circle"`, `"diamond"`, `"note"`, `"group"` |
| label    | string            | yes      | Primary text displayed in the shape |
| sublabel | string            | no       | Secondary text shown in hover tooltip |
| position | `{ x, y }`        | yes      | Top-left corner in pixels |
| size     | `{ width, height }` | yes   | Dimensions in pixels |
| style    | object            | no       | See node style fields below |
| group    | string            | no       | id of parent group node (visual grouping only) |

**Node style fields**: `fill`, `stroke`, `strokeWidth`, `color` (text), `fontSize`, `borderRadius`, `opacity`

### edges

| Field        | Type   | Required | Notes |
|--------------|--------|----------|-------|
| id           | string | yes      | unique (e.g. `"e_upload_to_extract"`) |
| source       | string | yes      | source node id |
| target       | string | yes      | target node id |
| label        | string | no       | text on the arrow (e.g. `"yes"`, `"error"`) |
| sourceHandle | string | no       | `"top"`, `"right"`, `"bottom"` (default), `"left"` |
| targetHandle | string | no       | `"top"` (default), `"right"`, `"bottom"`, `"left"` |
| style        | object | no       | See edge style fields below |

**Edge style fields**: `stroke`, `strokeWidth`, `strokeDasharray`, `markerEnd`

## Node Rendering Rules

| Type    | SVG Element  | Details |
|---------|-------------|---------|
| box     | `<rect>`    | Rounded corners via `rx`/`ry` from `borderRadius`. Default: 8px |
| circle  | `<ellipse>` | `cx = x + width/2`, `cy = y + height/2`, `rx = width/2`, `ry = height/2` |
| diamond | `<polygon>` | 4 points: top-center, right-center, bottom-center, left-center |
| note    | `<path>`    | Rectangle with folded corner (top-right). Fold size: 12px |
| group   | `<rect>`    | Dashed border (`stroke-dasharray: 6,3`). Rendered BEHIND all other nodes. Label at top-left. Low opacity |

## Edge Rendering Rules

1. Compute **source point**: center of the specified handle side of the source node (default: bottom)
2. Compute **target point**: center of the specified handle side of the target node (default: top)
3. Draw a **cubic bezier** (`C` command) with control points offset **50px** in the handle direction
4. Add an **arrowhead** using an SVG `<marker>` definition
5. If `strokeDasharray` is set, render as **dashed line**
6. If `label` exists, render at the **midpoint of the bezier** with a small white background rect behind it

## Layout Rules

### Flow Direction
- **Flowcharts**: Top-to-bottom (default)
- **UI mockups**: Top-to-bottom within a group container, annotations to the right

### Spacing
- Minimum **70px vertical** between node centers
- Minimum **60px horizontal** between parallel nodes
- Group padding: **40px** inside group boundaries

### Decision Diamonds
- **Left** branch = primary / yes path
- **Right** branch = secondary / no / error path

### Error/Warning Notes
- Place to the **RIGHT** of the main flow
- Connect with **dashed red edges** (`strokeDasharray: "6,3"`, stroke: `#991b1b`)

### Standard Sizes

| Type    | Width | Height |
|---------|-------|--------|
| box     | 200   | 50     |
| circle  | 90    | 40     |
| diamond | 120   | 60     |
| note    | 180   | 44     |

### Color Palette

| Purpose          | Fill    | Stroke  | Text    |
|------------------|---------|---------|---------|
| Actions          | #ffffff | #2d6a4f | #1f2937 |
| Primary actions  | #d1fae5 | #065f46 | #065f46 |
| Decisions        | #fef3c7 | #92400e | #1f2937 |
| Errors           | #fee2e2 | #991b1b | #991b1b |
| Terminals        | #40916c | #2d6a4f | #ffffff |
| Groups           | #f5f5f2 | #e6e4df | #374151 |
| Info/secondary   | #dbeafe | #1e40af | #1e40af |
| Default edges    |,       | #6b7280 |,       |

## HTML File Structure

Every Flowy HTML file follows this structure. Read the HTML template reference for the complete working code.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{diagram title}</title>
  <style>
    /* All CSS inline, toolbar, canvas, tooltips, selection highlights */
  </style>
</head>
<body>
  <div id="toolbar">
    <!-- [Fit] [-] 100% [+]   Title  badge   [Download JSON] -->
  </div>
  <div id="canvas-wrap">
    <svg id="canvas">
      <defs><!-- arrowhead markers --></defs>
      <g id="diagram-root"></g>
    </svg>
  </div>
  <div id="tooltip"></div>
  <script>
    const DIAGRAM = { meta: {...}, nodes: [...], edges: [...] };
    // Rendering + interactivity code
  </script>
</body>
</html>
```

### Toolbar
- Fixed at top, 48px tall, white background, bottom border
- **Left**: Zoom to Fit button, zoom out, zoom %, zoom in
- **Center**: Diagram title (bold) + type badge (gray pill)
- **Right**: Download JSON button (blue)

### Interactivity (all vanilla JS)
1. **Zoom**: Mouse wheel scales SVG viewBox. Range: 0.2x to 5x. Zoom toward cursor position.
2. **Pan**: Click-drag on empty canvas translates the viewBox.
3. **Hover**: Hovering a node shows its `sublabel` in a tooltip near the cursor.
4. **Click**: Clicking a node highlights it (blue border) and all connected edges. Click empty space to deselect.
5. **Zoom to Fit**: Button calculates bounding box of all nodes and sets viewBox with 60px padding.
6. **Download JSON**: Serializes the `DIAGRAM` object as formatted JSON and triggers a file download.

## Creating a New Diagram

When the user asks for a new flowchart or UI mockup:

1. **Read the template**: Read the HTML template reference file to get the current renderer code
2. **Analyze the request**: Identify nodes (steps, decisions, errors) and edges (connections)
3. **Assign positions** using the layout rules (top-to-bottom grid, standard spacing)
4. **Apply colors** using the color palette (terminals = green, decisions = amber, errors = red, etc.)
5. **Generate the complete HTML file**: Copy the template structure, replace the `DIAGRAM` object with the new data
6. **Save** to `docs/diagrams/{kebab-case-name}.html`
7. **Tell the user**: "Open `docs/diagrams/{name}.html` in your browser to view the diagram."

### File Naming
- Location: `docs/diagrams/{name}.html`
- Format: `kebab-case.html` (e.g. `docs/diagrams/upload-flow.html`, `docs/diagrams/checkout-screen.html`)
- Set `meta.updated` to today's ISO date

## Updating an Existing Diagram

When the user asks to modify a diagram:

1. **Read** the existing HTML file
2. **Extract** the `DIAGRAM` object from the `<script>` block
3. **Modify** the nodes/edges as requested
4. **Update** `meta.updated` to today's date
5. **Regenerate** the complete HTML file with the updated data (re-read the template for the latest renderer)
6. **Save** back to the same path

## Reading a Diagram

When asked to analyze or describe a diagram:

1. Read the HTML file
2. Find the `const DIAGRAM = { ... };` block
3. List nodes by type and label
4. Trace edges to describe the flow in natural language
5. Highlight decision points and their branches

## Examples

### "Create a flowchart for the login flow"

**Action**: Create `docs/diagrams/login-flow.html` with:
- `start` (circle, green) → `enter_credentials` (box) → `validate` (diamond, amber)
- `validate` → yes/left → `dashboard` (circle, green)
- `validate` → no/right → `show_error` (note, red) → dashed arrow back to `enter_credentials`

### "Update the settings mockup to add a dark mode toggle"

**Action**: Read `docs/diagrams/settings-screen.html`, extract DIAGRAM, add a new box node `"section_dark_mode"` with label "Dark Mode" positioned after the Theme section, update `meta.updated`, regenerate the HTML.

### "Add error handling to step 3 of the upload flow"

**Action**: Read the HTML, find step 3 in the nodes array, add an error note node to the right, add a dashed red edge from step 3 to the error note, regenerate.

## Important Constraints

- **Zero dependencies**: No npm, no CDN links, no external scripts/styles
- **Works offline**: Must render without internet access
- **Single file**: Each diagram is ONE `.html` file
- **Browser-native**: Standard HTML5, CSS3, SVG, and vanilla ES6+ JavaScript only
- **LLM-friendly**: The DIAGRAM JSON must be clean-formatted, not minified

## Self-Maintenance

If you discover a useful pattern while creating diagrams, a new layout trick, a color that works well for a specific purpose, a rendering improvement, update this skill file to include it. Keep the skill accurate and actionable.
