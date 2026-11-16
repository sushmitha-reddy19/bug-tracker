import React, { useEffect, useState } from 'react';

type Bug = { id: number; title: string; severity: string; status: string };
export default function App() {
  const [bugs, setBugs] = useState<Bug[]>([]), [filter, setFilter] = useState(''), [page, setPage] = useState(1);
  const [title, setTitle] = useState(''), [severity, setSeverity] = useState('medium');
  const load = () => fetch(`/bugs?page=${page}&size=5${filter ? `&status=${filter}` : ''}`).then(r => r.json()).then(d => setBugs(d.items || []));
  useEffect(load, [page, filter]);
  const create = () => fetch('/bugs', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({title, severity}) }).then(() => { setTitle(''); load(); });
  return <main><h1>Bug Tracker</h1><input placeholder="Bug title" value={title} onChange={e => setTitle(e.target.value)} /><select value={severity} onChange={e => setSeverity(e.target.value)}><option>low</option><option>medium</option><option>high</option><option>critical</option></select><button onClick={create}>Create</button><select value={filter} onChange={e => {setFilter(e.target.value); setPage(1)}}><option value="">All</option><option value="open">Open</option><option value="in_progress">In progress</option><option value="closed">Closed</option></select><ul>{bugs.map(b => <li key={b.id}>{b.title} — {b.severity} — {b.status}</li>)}</ul><button disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button><button onClick={() => setPage(page + 1)}>Next</button></main>;
}
