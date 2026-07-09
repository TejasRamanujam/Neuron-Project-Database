import type { Project } from './types'

const API = '/api'

export async function fetchProjects(params: {
  query?: string
  tags?: string
  difficulty?: string
}): Promise<Project[]> {
  const search = new URLSearchParams()
  if (params.query) search.set('query', params.query)
  if (params.tags) search.set('tags', params.tags)
  if (params.difficulty) search.set('difficulty', params.difficulty)
  const qs = search.toString()
  const res = await fetch(`${API}/projects${qs ? `?${qs}` : ''}`)
  return res.json()
}

export async function fetchProject(id: number): Promise<Project> {
  const res = await fetch(`${API}/projects/${id}`)
  return res.json()
}

export async function fetchTags(): Promise<string[]> {
  const res = await fetch(`${API}/tags`)
  return res.json()
}

export async function fetchDifficulties(): Promise<string[]> {
  const res = await fetch(`${API}/difficulties`)
  return res.json()
}
