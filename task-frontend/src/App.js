import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [data, setData] = useState(null);
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [taskTitle, setTaskTitle] = useState("");

  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiZXhwIjoxNzc2NDE2NTY0fQ.MC2bRDh2tlkhchk5T9TmjSC22QQwj84htX7EV-L0avY";

  // 🔹 Fetch analytics
  useEffect(() => {
    fetch("http://127.0.0.1:8000/analytics/tasks", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("API DATA:", data);
        setData(data);
      })
      .catch((err) => console.error(err));
  }, []);

  // 🔹 Fetch projects
  useEffect(() => {
    fetch("http://127.0.0.1:8000/projects", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("PROJECTS:", data);
        setProjects(data);
      })
      .catch((err) => console.error(err));
  }, []);

  // 🔹 Fetch tasks when project selected
  useEffect(() => {
    if (!selectedProject) return;

    fetch(`http://127.0.0.1:8000/tasks/${selectedProject.id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("TASKS:", data);
        setTasks(data);
      })
      .catch((err) => console.error(err));
  }, [selectedProject]);

  // ➕ Add task
  const addTask = () => {
    if (!selectedProject) {
      alert("Select a project first");
      return;
    }

    fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: taskTitle,
        project_id: selectedProject.id,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Task added:", data);
        setTaskTitle("");
        setTasks((prev) => [...prev, data]);
      })
      .catch((err) => console.error(err));
  };

  if (!data) return <div>Loading...</div>;

  // 📊 Chart data
  const chartData = {
    labels: ["Completed", "Pending"],
    datasets: [
      {
        data: [data.completed, data.pending],
        backgroundColor: ["green", "orange"],
      },
    ],
  };

  return (
    <div style={{ display: "flex", padding: "20px" }}>
      
      {/* LEFT SIDE - PROJECTS */}
      <div style={{ width: "30%", borderRight: "1px solid gray", padding: "10px" }}>
        <h2>Projects</h2>

        <ul>
          {projects.map((project, index) => (
            <li
              key={index}
              onClick={() => setSelectedProject(project)}
              style={{ cursor: "pointer", padding: "5px" }}
            >
              {project.project_name}
            </li>
          ))}
        </ul>
      </div>

      {/* RIGHT SIDE */}
      <div style={{ width: "70%", padding: "20px" }}>
        
        {/* TASK INPUT */}
        <h2>Tasks</h2>
        <input
          placeholder="Task title"
          value={taskTitle}
          onChange={(e) => setTaskTitle(e.target.value)}
        />
        <button onClick={addTask}>Add</button>

        {/* TASK LIST */}
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>{task.title}</li>
          ))}
        </ul>

        {/* ANALYTICS */}
        <h2>Analytics</h2>
        <p>Total Tasks: {data.total_tasks}</p>
        <p>Completed: {data.completed}</p>
        <p>Pending: {data.pending}</p>

        <div style={{ width: "300px", marginTop: "20px" }}>
          <Pie data={chartData} />
        </div>

      </div>
    </div>
  );
}

export default App;