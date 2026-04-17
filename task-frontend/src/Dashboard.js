import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios.get("http://127.0.0.1:8000/analytics/tasks", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(res => setData(res.data))
    .catch(err => console.log(err));
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Total Tasks: {data.total_tasks}</p>
      <p>Completed: {data.completed}</p>
      <p>Pending: {data.pending}</p>
      <p>In Progress: {data.in_progress}</p>
    </div>
  );
}

export default Dashboard;