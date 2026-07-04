import { useEffect, useState, useCallback, useRef } from 'react'
import type { Project } from './types'
import { fetchProjects, fetchTags, fetchDifficulties } from './api'
import './App.css'

const DIFFICULTY_CLASS: Record<string, string> = {
  Beginner: 'diff-beginner',
  Intermediate: 'diff-intermediate',
  Advanced: 'diff-advanced',
}

function difficultyClass(d: string) {
  return DIFFICULTY_CLASS[d] || 'diff-default'
}

function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [difficulties, setDifficulties] = useState<string[]>([])
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [selectedDiffs, setSelectedDiffs] = useState<string[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const searchRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query), 220)
    return () => clearTimeout(t)
  }, [query])

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchProjects({
        query: debouncedQuery,
        tags: selectedTags.join(','),
        difficulty: selectedDiffs.join(','),
      })
      setProjects(data)
    } finally {
      setLoading(false)
    }
  }, [debouncedQuery, selectedTags, selectedDiffs])

  useEffect(() => {
    fetchTags().then(setTags)
    fetchDifficulties().then(setDifficulties)
  }, [])

  useEffect(() => {
    load()
  }, [load])

  // "/" focuses search
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === '/' && document.activeElement?.tagName !== 'INPUT') {
        e.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const hasFilters = query !== '' || selectedTags.length > 0 || selectedDiffs.length > 0
  const clearFilters = () => {
    setQuery('')
    setSelectedTags([])
    setSelectedDiffs([])
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark" aria-hidden="true">
              <svg viewBox="0 0 32 32" width="18" height="18">
                <path d="M9 10h14M9 16h10M9 22h6" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
                <circle cx="24" cy="22" r="3.2" fill="#4cc9f0" stroke="none" />
              </svg>
            </span>
            <span className="brand-name">Project Database</span>
            <span className="brand-tag">CS ideas</span>
          </div>
          <a className="back-pill" href="https://tejas-live-demos.vercel.app">
            <span aria-hidden="true">&larr;</span> Back to demos
          </a>
        </div>
      </header>

      <section className="hero">
        <h1>Find your next build.</h1>
        <p className="hero-sub">
          Searchable CS project ideas with full build plans, tech stacks, and resume impact —
          inspired by career-ops, maigret &amp; Archon.
        </p>
        <div className="search-wrap">
          <svg className="search-icon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
            <path d="m20 20-3.8-3.8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <input
            ref={searchRef}
            className="search-input"
            type="text"
            placeholder="Search by title, tech, library, or tag..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Search projects"
          />
          <kbd className="search-kbd" aria-hidden="true">/</kbd>
        </div>
      </section>

      <div className="layout">
        <aside className="sidebar" aria-label="Filters">
          <div className="sidebar-head">
            <h2 className="sidebar-title">Filters</h2>
            {hasFilters && (
              <button className="clear-btn" onClick={clearFilters}>
                Clear all
              </button>
            )}
          </div>

          <div className="filter-group">
            <span className="filter-label">Difficulty</span>
            <div className="filter-chips">
              {difficulties.map((d) => {
                const active = selectedDiffs.includes(d)
                return (
                  <button
                    key={d}
                    className={`chip ${difficultyClass(d)} ${active ? 'active' : ''}`}
                    aria-pressed={active}
                    onClick={() =>
                      setSelectedDiffs((prev) =>
                        prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]
                      )
                    }
                  >
                    <span className="chip-dot" aria-hidden="true" />
                    {d}
                  </button>
                )
              })}
            </div>
          </div>

          <div className="filter-group">
            <span className="filter-label">Tags</span>
            <div className="filter-chips">
              {tags.map((t) => {
                const active = selectedTags.includes(t)
                return (
                  <button
                    key={t}
                    className={`chip tag ${active ? 'active' : ''}`}
                    aria-pressed={active}
                    onClick={() =>
                      setSelectedTags((prev) =>
                        prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]
                      )
                    }
                  >
                    {t}
                  </button>
                )
              })}
            </div>
          </div>
        </aside>

        <main className="main">
          <div className="results-bar">
            <span className="result-count" role="status">
              {loading ? 'Searching…' : `${projects.length} project${projects.length !== 1 ? 's' : ''}`}
            </span>
          </div>

          {loading ? (
            <div className="grid" aria-hidden="true">
              {Array.from({ length: 6 }).map((_, i) => (
                <SkeletonCard key={i} />
              ))}
            </div>
          ) : projects.length === 0 ? (
            <div className="empty">
              <div className="empty-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="28" height="28">
                  <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="1.6" />
                  <path d="m20 20-3.8-3.8" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
                  <path d="M8.5 11h5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
                </svg>
              </div>
              <p className="empty-title">No projects match your filters</p>
              <p className="empty-sub">Try broadening your search or removing a filter.</p>
              {hasFilters && (
                <button className="empty-clear" onClick={clearFilters}>
                  Clear all filters
                </button>
              )}
            </div>
          ) : (
            <div className="grid">
              {projects.map((p) => (
                <ProjectCard key={p.id} project={p} onClick={setSelectedProject} />
              ))}
            </div>
          )}
        </main>
      </div>

      {selectedProject && (
        <ProjectModal project={selectedProject} onClose={() => setSelectedProject(null)} />
      )}
    </div>
  )
}

function SkeletonCard() {
  return (
    <div className="card skeleton-card">
      <div className="sk sk-title" />
      <div className="sk sk-line" />
      <div className="sk sk-line short" />
      <div className="sk-pills">
        <div className="sk sk-pill" />
        <div className="sk sk-pill" />
        <div className="sk sk-pill" />
      </div>
    </div>
  )
}

function ProjectCard({ project, onClick }: { project: Project; onClick: (p: Project) => void }) {
  return (
    <article
      className="card"
      role="button"
      tabIndex={0}
      onClick={() => onClick(project)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onClick(project)
        }
      }}
      aria-label={`View details for ${project.title}`}
    >
      <div className="card-header">
        <h2>{project.title}</h2>
        <span className={`difficulty-badge ${difficultyClass(project.difficulty)}`}>
          {project.difficulty}
        </span>
      </div>
      <p className="card-subtitle">{project.subtitle}</p>
      <div className="card-tech">
        {project.tech_stack.slice(0, 5).map((t) => (
          <span key={t} className="tech-pill">{t}</span>
        ))}
        {project.tech_stack.length > 5 && (
          <span className="tech-pill more">+{project.tech_stack.length - 5}</span>
        )}
      </div>
      <div className="card-footer">
        <div className="card-tags">
          {project.tags.slice(0, 3).map((t) => (
            <span key={t} className="tag-pill">{t}</span>
          ))}
        </div>
        <span className="card-link">
          View details <span aria-hidden="true">&rarr;</span>
        </span>
      </div>
    </article>
  )
}

function ProjectModal({ project, onClose }: { project: Project; onClose: () => void }) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = ''
    }
  }, [onClose])

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={project.title}
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close" onClick={onClose} aria-label="Close details">
          &times;
        </button>

        <div className="modal-header">
          <h2>{project.title}</h2>
          <span className={`difficulty-badge ${difficultyClass(project.difficulty)}`}>
            {project.difficulty}
          </span>
        </div>
        <p className="modal-subtitle">{project.subtitle}</p>

        <section>
          <h3>Problem</h3>
          <p>{project.problem_statement}</p>
        </section>

        <section>
          <h3>Description</h3>
          <p>{project.description}</p>
        </section>

        <section className="build-plan">
          <h3>Build Plan</h3>
          <div className="plan-content">
            {project.build_plan.split('\n').map((line, i) => {
              const t = line.trim()
              if (t.startsWith('## ')) return <h4 key={i} className="plan-phase">{t.replace('## ', '')}</h4>
              if (t.startsWith('**Step') || t.match(/^Step \d+:/)) {
                const stepText = t.replace(/\*\*/g, '')
                return <p key={i} className="plan-step">{stepText}</p>
              }
              if (!t) return null
              return <p key={i} className="plan-line">{t.replace(/\*\*/g, '')}</p>
            })}
          </div>
        </section>

        <div className="modal-columns">
          <section>
            <h3>Tech Stack</h3>
            <div className="modal-list">
              {project.tech_stack.map((t) => (
                <span key={t} className="tech-pill">{t}</span>
              ))}
            </div>
          </section>
          <section>
            <h3>Libraries</h3>
            <div className="modal-list">
              {project.libraries_used.map((l) => (
                <span key={l} className="lib-pill">{l}</span>
              ))}
            </div>
          </section>
        </div>

        <section>
          <h3>Architectures</h3>
          <ul>
            {project.architectures_used.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </section>

        <section>
          <h3>Key Features</h3>
          <ul>
            {project.key_features.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
        </section>

        <section>
          <h3>UI Components</h3>
          <ul>
            {project.ui_components.map((u) => (
              <li key={u}>{u}</li>
            ))}
          </ul>
        </section>

        <section>
          <h3>Learning Outcomes</h3>
          <ul>
            {project.learning_outcomes.map((l) => (
              <li key={l}>{l}</li>
            ))}
          </ul>
        </section>

        <section className="resume-gap">
          <h3>Resume Impact</h3>
          <p>{project.resume_gap_filled}</p>
        </section>

        {project.repo_inspiration.length > 0 && (
          <section>
            <h3>Inspiration</h3>
            <div className="inspo-links">
              {project.repo_inspiration.map((url) => (
                <a key={url} href={url} target="_blank" rel="noopener noreferrer">{url}</a>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}

export default App
