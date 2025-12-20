const API_BASE = "http://localhost:8000/api";

async function loadLogs() {
  const tbody = document.getElementById("logs-body");
  try {
    const res = await fetch(`${API_BASE}/logs`);
    if (!res.ok) throw new Error("Non-OK: " + res.status);
    const logs = await res.json();

    tbody.innerHTML = "";

    // Show last 8 events, newest last
    logs.slice(-8).forEach((log) => {
      const tr = document.createElement("tr");

      const actionTd = document.createElement("td");
      actionTd.textContent = log.action;
      actionTd.className =
        log.action === "blocked" ? "tag-blocked" : "tag-allowed";

      const ipTd = document.createElement("td");
      ipTd.textContent = log.ip;

      const reasonTd = document.createElement("td");
      reasonTd.textContent = log.reason;

      tr.appendChild(actionTd);
      tr.appendChild(ipTd);
      tr.appendChild(reasonTd);
      tbody.appendChild(tr);
    });

    if (!logs.length) {
      tbody.innerHTML = "<tr><td colspan='3'>No events yet</td></tr>";
    }
  } catch (err) {
    console.error(err);
    tbody.innerHTML = "<tr><td colspan='3'>Error loading logs</td></tr>";
  }
}

loadLogs();
