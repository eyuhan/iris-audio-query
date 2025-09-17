import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [query, setQuery] = useState('')
  const [uploadStatus, setUploadStatus] = useState('')
  const [queryResult, setQueryResult] = useState('')
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setUploadStatus('')
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first')
      return
    }

    setLoading(true)
    setUploadStatus('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8001/audio/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        await response.json()
        setUploadStatus('Upload successful!')
      } else {
        setUploadStatus(`Upload failed: ${response.statusText}`)
      }
    } catch (error) {
      setUploadStatus(`Upload error: ${error}`)
    } finally {
      setLoading(false)
    }
  }

  const handleQuery = async () => {
    if (!query.trim()) {
      setQueryResult('Please enter a query')
      return
    }

    setLoading(true)
    setQueryResult('')

    try {
      const response = await fetch(`http://localhost:8001/audio/query?query=${encodeURIComponent(query)}`)

      if (response.ok) {
        const result = await response.json()
          setQueryResult(result)
      } else {
        setQueryResult(`Query failed: ${response.statusText}`)
      }
    } catch (error) {
      setQueryResult(`Query error: ${error}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>IRIS Audio Query</h1>

      <div style={{ marginBottom: '2rem' }}>
        <h2>Upload Audio File</h2>
        <input
          type="file"
          accept="audio/*"
          onChange={handleFileChange}
          style={{ marginBottom: '1rem', display: 'block' }}
        />
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          style={{ padding: '0.5rem 1rem' }}
        >
          Upload
        </button>
        {uploadStatus && <p style={{ marginTop: '0.5rem' }}>{uploadStatus}</p>}
      </div>

      <div>
        <h2>Query</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
          style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
        />
        <button
          onClick={handleQuery}
          disabled={loading || !query.trim()}
          style={{ padding: '0.5rem 1rem' }}
        >
          Submit Query
        </button>
        {queryResult && (
          <pre style={{
            marginTop: '1rem',
            padding: '1rem',
            background: '#f5f5f5',
            borderRadius: '4px',
            overflow: 'auto'
          }}>
            {queryResult}
          </pre>
        )}
      </div>
    </div>
  )
}

export default App
