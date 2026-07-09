import { useEffect, useState } from 'react'
import type { Project } from './types'
import { fetchProject } from './api'
import { Inline, parsePlan, phaseLabel, repoName, stepLabel } from './plan'

const pad = (n: number) => String(n).padStart(2, '0')
const slug = (d: string) => d.toLowerCase()

interface Props {
  id: number
  project: Project | null
  listLoading: boolean
  prev: Project | null
  next: Project | null
}

function RailSection({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <section className="rail-sec">
      <h3 className="sec-label">{label}</h3>
      {children}
    </section>
  )
}

export function Detail({ id, project, listLoading, prev, next }: Props) {
  const [fetched, setFetched] = useState<Project | null>(null)
  const [missing, setMissing] = useState(false)

  // Deep-link fallback: if the current list doesn't contain the id, fetch it.
  useEffect(() => {
    setFetched(null)
    setMissing(false)
  }, [id])

  useEffect(() => {
    if (project || listLoading || fetched?.id === id) return
    let live = true
    fetchProject(id)
      .then((p) => {
        if (!live) return
        if (p && typeof p.id === 'number') setFetched(p)
        else setMissing(true)
      })
      .catch(() => live && setMissing(true))
    return () => {
      live = false
    }
  }, [id, project, listLoading, fetched])

  const p = project ?? fetched

  if (!p) {
    return (
      <main className="dossier">
        <div className="dossier-bar">
          <a className="crumb" href="#/">
            ← Index
          </a>
        </div>
        {missing ? (
          <div className="notice">
            <p className="notice-big">No specimen filed under № {pad(id)}.</p>
            <a className="clear" href="#/">
              Return to the index →
            </a>
          </div>
        ) : (
          <p className="consulting">Retrieving specimen…</p>
        )}
      </main>
    )
  }

  const phases = parsePlan(p.build_plan)
  const d = slug(p.difficulty)

  return (
    <main className="dossier" data-diff={d}>
      <div className="dossier-bar">
        <a className="crumb" href="#/">
          ← Index
        </a>
        <span className="topbar-rule" aria-hidden="true" />
        <span className="dossier-no">Specimen № {pad(p.id)}</span>
      </div>

      <header className="dossier-head">
        <div className="dossier-marks">
          <span className="stamp big" data-diff={d}>
            {p.difficulty}
          </span>
          <span className="dossier-tags">{p.tags.join(' · ')}</span>
        </div>
        <h1 className="dossier-title">{p.title}</h1>
        <p className="dossier-sub">{p.subtitle}</p>
      </header>

      <blockquote className="problem">
        <span className="sec-label">The problem</span>
        <p>{p.problem_statement}</p>
      </blockquote>

      <p className="dossier-desc">{p.description}</p>

      <div className="dossier-grid">
        <div className="dossier-main">
          <h2 className="sec-label plan-label">Build plan</h2>
          {phases.map((phase, i) => {
            const { numeral, label } = phaseLabel(phase.heading, i)
            return (
              <section className="phase" key={i}>
                <header className="phase-head">
                  <span className="phase-numeral" aria-hidden="true">
                    {numeral}
                  </span>
                  <h3 className="phase-title">
                    <span className="phase-kicker">Phase {i + 1}</span>
                    {label || `Phase ${i + 1}`}
                  </h3>
                </header>
                <ol className="steps">
                  {phase.steps.map((step, j) => {
                    const lead = step.lead ? stepLabel(step.lead) : null
                    return (
                      <li className="step" key={j}>
                        {lead && (
                          <p className="step-lead">
                            {lead.n && <span className="step-n">Step {lead.n}</span>}
                            <Inline text={lead.text} />
                          </p>
                        )}
                        {step.body && (
                          <p className="step-body">
                            <Inline text={step.body} />
                          </p>
                        )}
                      </li>
                    )
                  })}
                </ol>
              </section>
            )
          })}

          <div className="twin-lists">
            <section>
              <h2 className="sec-label">Key features</h2>
              <ul className="flat-list">
                {p.key_features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
            </section>
            <section>
              <h2 className="sec-label">You will learn</h2>
              <ul className="flat-list">
                {p.learning_outcomes.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
            </section>
          </div>
        </div>

        <aside className="dossier-rail">
          <RailSection label="Tech stack">
            <ul className="chip-list">
              {p.tech_stack.map((t) => (
                <li className="chip static" key={t}>
                  {t}
                </li>
              ))}
            </ul>
          </RailSection>
          <RailSection label="Architectures">
            <ul className="rail-list">
              {p.architectures_used.map((a) => (
                <li key={a}>{a}</li>
              ))}
            </ul>
          </RailSection>
          <RailSection label="Libraries">
            <ul className="rail-list">
              {p.libraries_used.map((l) => (
                <li key={l}>{l}</li>
              ))}
            </ul>
          </RailSection>
          <RailSection label="UI components">
            <ul className="rail-list">
              {p.ui_components.map((u) => (
                <li key={u}>{u}</li>
              ))}
            </ul>
          </RailSection>
          {p.repo_inspiration.length > 0 && (
            <RailSection label="Inspiration">
              <ul className="rail-list">
                {p.repo_inspiration.map((r) => (
                  <li key={r}>
                    <a className="repo-link" href={r} target="_blank" rel="noreferrer">
                      {repoName(r)} ↗
                    </a>
                  </li>
                ))}
              </ul>
            </RailSection>
          )}
          <RailSection label="Résumé gap filled">
            <p className="rail-note">{p.resume_gap_filled}</p>
          </RailSection>
        </aside>
      </div>

      <nav className="dossier-nav" aria-label="Adjacent specimens">
        {prev ? (
          <a className="adj" href={`#/p/${prev.id}`}>
            <span className="adj-dir">← № {pad(prev.id)}</span>
            <span className="adj-title">{prev.title}</span>
          </a>
        ) : (
          <span />
        )}
        {next ? (
          <a className="adj adj-next" href={`#/p/${next.id}`}>
            <span className="adj-dir">№ {pad(next.id)} →</span>
            <span className="adj-title">{next.title}</span>
          </a>
        ) : (
          <span />
        )}
      </nav>
    </main>
  )
}
