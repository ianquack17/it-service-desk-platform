import './App.css'
import { useState, useEffect } from 'react'


function App() {

  const [tickets, setTickets] = useState<any[]>([
    { id: 1, title: "Zoom issue" },
    { id: 2, title: "Blackboard issue"},
    { id: 3, title: "Projector Issue"}
  ])

  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  useEffect(() => {

    loadTickets()

  }, [])

  async function createTicket(title, description) {

    const response = await fetch("http://127.0.0.1:8000/tickets", {
      method: "POST",
      headers: {
        "Content-Type": "application.json"
      },
      body: JSON.stringify({
        title: title,
        description: description
      })
    })
  }

  async function loadTickets() {

      const response = await fetch("http://127.0.0.1:8000/tickets")
      const data = await response.json()
      setTickets(data)
    }

  function changeTickets() {
    setTickets([
      "New issue",
      "Also new issue",
      "Checking one more thing"
    ])
  }

  return (
    <div>

      <h1>IT Service Desk</h1>

      {tickets.map((ticket) => (
        <p key={ticket.id}>{ticket.title}</p>
      ))}

      <button onClick={changeTickets}>
        Change Tickets
      </button>

      <input 
        value={title} 
        onChange={(event) => setTitle(event.target.value)}
      />

      <input
        value={description}
        onChange={(event) => setTitle(event.target.value)}
      />

    </div>
  )
}


export default App
