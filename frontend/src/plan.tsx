import type { ReactNode } from 'react'

/* ---------------------------------------------------------------- *
 *  Tiny renderer for the build_plan markdown dialect used by the
 *  API: "## Phase N: …" headings, paragraphs, "**bold**" leads and
 *  `inline code`. Some records are terse ("## Phase 1\none line"),
 *  some are long-form with "**Step N: title.** body" paragraphs.
 * ---------------------------------------------------------------- */

export interface PlanStep {
  lead: string | null
  body: string
}

export interface PlanPhase {
  heading: string
  steps: PlanStep[]
}

export function parsePlan(md: string): PlanPhase[] {
  const chunks = md
    .split(/^##\s+/m)
    .map((c) => c.trim())
    .filter(Boolean)

  return chunks.map((chunk) => {
    const nl = chunk.indexOf('\n')
    const heading = (nl === -1 ? chunk : chunk.slice(0, nl)).trim()
    const body = nl === -1 ? '' : chunk.slice(nl + 1).trim()

    const paragraphs = body
      .split(/\n{2,}/)
      .map((p) => p.replace(/\s*\n\s*/g, ' ').trim())
      .filter(Boolean)

    const steps: PlanStep[] = paragraphs.map((p) => {
      const m = p.match(/^\*\*(.+?)\*\*\s*(.*)$/s)
      if (m) return { lead: m[1].trim(), body: m[2].trim() }
      return { lead: null, body: p }
    })

    return { heading, steps }
  })
}

/** Render **bold** and `code` spans inside a line of text. */
export function Inline({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  const nodes: ReactNode[] = parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      return <code key={i}>{part.slice(1, -1)}</code>
    }
    return part
  })
  return <>{nodes}</>
}

const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

/** "Phase 3: Frontend — Dashboard" → { numeral: "III", label: "Frontend — Dashboard" } */
export function phaseLabel(heading: string, index: number) {
  const m = heading.match(/^Phase\s+(\d+)\s*:?\s*(.*)$/i)
  const n = m ? parseInt(m[1], 10) : index + 1
  const label = m && m[2] ? m[2].trim() : m ? '' : heading
  return { numeral: ROMAN[n - 1] ?? String(n), label }
}

/** Strip a leading "Step N:" from a bold lead, returning [n, rest]. */
export function stepLabel(lead: string): { n: string | null; text: string } {
  const m = lead.match(/^Step\s+(\d+)\s*:?\s*(.*)$/i)
  if (m) return { n: m[1], text: m[2].trim() }
  return { n: null, text: lead }
}

/** "https://github.com/owner/repo" → "owner/repo" */
export function repoName(url: string): string {
  const m = url.match(/github\.com\/([^/]+\/[^/#?]+)/)
  return m ? m[1] : url.replace(/^https?:\/\//, '')
}
