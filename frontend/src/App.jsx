import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>React + FastAPI</h1>
      <p>{data ? JSON.stringify(data) : "Loading…"}</p>
    </div>
  );
}

export default App;
