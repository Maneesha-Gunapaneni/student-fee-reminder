import { useEffect, useState } from "react";

export default function App() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/pending-fees")
      .then((res) => res.json())
      .then((data) => setStudents(data))
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  const sendMessages = () => {
    fetch("http://127.0.0.1:5000/send-messages")
      .then((res) => res.json())
      .then((data) => alert("Messages sent to all pending students!"))
      .catch((err) => console.error("Error sending messages:", err));
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>📚 Student Fee Reminder - Pending List</h1>
      <button onClick={sendMessages} style={{ marginBottom: 15 }}>
        Send Messages
      </button>

      {students.length === 0 ? (
        <p>No pending fees found!</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>Name</th>
              <th>Parent Contact</th>
              <th>Pending Term 1</th>
              <th>Pending Term 2</th>
              <th>Total Pending</th>
              <th>Due Date</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.StudentID}>
                <td>{s.Name}</td>
                <td>{s.ParentContact}</td>
                <td>{s.PendingTerm1}</td>
                <td>{s.PendingTerm2}</td>
                <td>{s.TotalPending}</td>
                <td>{s.DueDate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
