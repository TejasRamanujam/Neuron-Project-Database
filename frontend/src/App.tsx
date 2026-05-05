import { useEffect, useState, useCallback } from 'react'
import type { Project } from './types'
import { fetchProjects, fetchTags, fetchDifficulties } from './api'
import './App.css'

const DIFFICULTY_COLORS: Record<string, string> = {
  Beginner: '#4caf50',
  Intermediate: '#ff9800',
  Advanced: '#f44336',
}

function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [difficulties, setDifficulties] = useState<string[]>([])
  const [query, setQuery] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [selectedDiffs, setSelectedDiffs] = useState<string[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchProjects({
        query,
        tags: selectedTags.join(','),
        difficulty: selectedDiffs.join(','),
      })
      setProjects(data)
    } finally {
      setLoading(false)
    }
  }, [query, selectedTags, selectedDiffs])

  useEffect(() => {
    fetchTags().then(setTags)
    fetchDifficulties().then(setDifficulties)
  }, [])

  useEffect(() => {
    load()
  }, [load])

  return (
    <div className="app">
      <header className="header">
        <h1>CS Project Database</h1>
        <p className="subtitle">
          Searchable project ideas to elevate your resume — inspired by career-ops, maigret &amp; Archon
        </p>
      </header>

      <div className="toolbar">
        <input
          className="search-input"
          type="text"
          placeholder="Search projects by title, tech, library, or tag..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="filters">
          <div className="filter-group">
            <span className="filter-label">Difficulty</span>
            <div className="filter-chips">
              {difficulties.map((d) => (
                <button
                  key={d}
                  className={`chip ${selectedDiffs.includes(d) ? 'active' : ''}`}
                  style={selectedDiffs.includes(d) ? { borderColor: DIFFICULTY_COLORS[d] || '#888' } : {}}
                  onClick={() =>
                    setSelectedDiffs((prev) =>
                      prev.includes(d) ? prev.filter((x) => x !== d) : [...prev, d]
                    )
                  }
                >
                  {d}
                </button>
              ))}
            </div>
          </div>
          <div className="filter-group">
            <span className="filter-label">Tags</span>
            <div className="filter-chips">
              {tags.map((t) => (
                <button
                  key={t}
                  className={`chip ${selectedTags.includes(t) ? 'active-tag' : ''}`}
                  onClick={() =>
                    setSelectedTags((prev) =>
                      prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]
                    )
                  }
                >
                  {t}
                </button>
              ))}
            </div>
          </div>
        </div>
        <div className="result-count">{projects.length} project{projects.length !== 1 ? 's' : ''}</div>
      </div>

      <div className="main">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : projects.length === 0 ? (
          <div className="empty">No projects match your filters. Try broadening your search.</div>
        ) : (
          <div className="grid">
            {projects.map((p) => (
              <ProjectCard key={p.id} project={p} onClick={setSelectedProject} />
            ))}
          </div>
        )}
      </div>

      {selectedProject && (
        <ProjectModal project={selectedProject} onClose={() => setSelectedProject(null)} />
      )}
    </div>
  )
}

function ProjectCard({ project, onClick }: { project: Project; onClick: (p: Project) => void }) {
  return (
    <div className="card" onClick={() => onClick(project)}>
      <div className="card-header">
        <h2>{project.title}</h2>
        <span
          className="difficulty-badge"
          style={{ backgroundColor: DIFFICULTY_COLORS[project.difficulty] || '#888' }}
        >
          {project.difficulty}
        </span>
      </div>
      <p className="card-subtitle">{project.subtitle}</p>
      <div className="card-tech">
        {project.tech_stack.slice(0, 5).map((t) => (
          <span key={t} className="tech-pill">{t}</span>
        ))}
        {project.tech_stack.length > 5 && <span className="tech-pill more">+{project.tech_stack.length - 5}</span>}
      </div>
      <div className="card-tags">
        {project.tags.map((t) => (
          <span key={t} className="tag-pill">{t}</span>
        ))}
      </div>
      <div className="card-footer">
        <span className="card-time">{project.estimated_time}</span>
        <span className="card-link">View details →</span>
      </div>
    </div>
  )
}

function ProjectModal({ project, onClose }: { project: Project; onClose: () => void }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>

        <div className="modal-header">
          <h2>{project.title}</h2>
          <span
            className="difficulty-badge"
            style={{ backgroundColor: DIFFICULTY_COLORS[project.difficulty] || '#888' }}
          >
            {project.difficulty}
          </span>
          <span className="modal-time">{project.estimated_time}</span>
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
