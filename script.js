let barChart, pieChart;

async function fetchStats() {
  const res = await fetch('/get_stats');
  const data = await res.json();

  const labels = Object.keys(data.attack_distribution);
  const values = Object.values(data.attack_distribution);

  // Bar Chart
  if (!barChart) {
    const ctx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Blocked Attacks',
          data: values,
          backgroundColor: '#3b82f6'
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
      }
    });
  } else {
    barChart.data.labels = labels;
    barChart.data.datasets[0].data = values;
    barChart.update();
  }

  // Pie Chart
  if (!pieChart) {
    const ctx = document.getElementById('pieChart').getContext('2d');
    pieChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: ['#ef4444', '#f59e0b', '#10b981']
        }]
      },
      options: { responsive: true }
    });
  } else {
    pieChart.data.labels = labels;
    pieChart.data.datasets[0].data = values;
    pieChart.update();
  }
}

async function fetchLogs() {
  const res = await fetch('/get_logs');
  const data = await res.json();
  document.getElementById('logContent').innerText = data.logs.join('');
}


fetchStats();
setInterval(fetchStats, 5000); // 5s updates
