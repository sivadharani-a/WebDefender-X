import React, { useEffect, useState, useMemo } from "react";
import { getLogs } from "./api";
import {
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
  AreaChart,
  Area,
} from "recharts";


export default function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLogs();
    const interval = setInterval(loadLogs, 4000); // auto-refresh
    return () => clearInterval(interval);
  }, []);

  async function loadLogs() {
    try {
      const res = await getLogs();
      setLogs(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching logs", err);
    } finally {
      setLoading(false);
    }
  }

  const {
    total,
    successCount,
    errorCount,
    successRate,
    categoryData,
    timelineData,
    compositionData,
    topSourceData,
  } = useMemo(() => computeAnalytics(logs), [logs]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-100">
        <div className="text-lg">Initialising real-time analytics…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-5">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div>
          <div className="text-xs tracking-[0.25em] uppercase text-slate-400 mb-1">
            Real-Time Analytics
          </div>
          <h1 className="text-2xl md:text-3xl font-semibold">
            Event Analytics Dashboard
          </h1>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Live view of incoming events, status distribution and categories
            across your system.
          </p>
        </div>
        <div className="flex flex-col items-end gap-2 text-xs md:text-sm">
          <span className="inline-flex items-center gap-2 bg-emerald-900/30 border border-emerald-400/60 rounded-full px-3 py-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Stream status: <span className="font-medium">Live</span>
          </span>
          <span className="text-slate-400">
            Total events in view:{" "}
            <span className="text-slate-100 font-semibold">{total}</span>
          </span>
        </div>
      </header>

      {/* KPI cards */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <KpiCard
          title="Total Events"
          value={total}
          color="#38bdf8"
          subtitle="Current window"
        />
        <KpiCard
          title="Successful"
          value={successCount}
          color="#22c55e"
          subtitle="Status: allowed / ok"
        />
        <KpiCard
          title="Errors / Rejected"
          value={errorCount}
          color="#f97316"
          subtitle="Status: blocked / error"
        />
        <KpiCard
          title="Success Rate"
          value={`${successRate.toFixed(1)}%`}
          color="#a855f7"
          subtitle="Successful events share"
        />
      </section>

      {/* Row: timeline + composition */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
        {/* Line: event count over time */}
        <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
          <SectionHeader
            title="Event Throughput"
            subtitle="Number of events over the latest decisions"
          />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData}>
                <XAxis
                  dataKey="index"
                  stroke="#94a3b8"
                  tick={false}
                  label={{
                    value: "Event index (latest at right)",
                    position: "insideBottom",
                    offset: -5,
                    fill: "#64748b",
                    fontSize: 10,
                  }}
                />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#020617",
                    border: "1px solid #334155",
                    fontSize: 12,
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="total"
                  stroke="#38bdf8"
                  strokeWidth={1.8}
                  dot={false}
                  name="Events"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Area: composition over time */}
        <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
          <SectionHeader
            title="Status Composition"
            subtitle="Success vs error share over the recent stream"
          />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={compositionData} stackOffset="expand">
                <XAxis dataKey="index" stroke="#94a3b8" tick={false} />
                <YAxis
                  stroke="#94a3b8"
                  tickFormatter={(v) => `${Math.round(v * 100)}%`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#020617",
                    border: "1px solid #334155",
                    fontSize: 12,
                  }}
                  formatter={(val) => `${Math.round(val * 100)}%`}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="success"
                  stackId="1"
                  stroke="#22c55e"
                  fill="#22c55e60"
                  name="Successful"
                />
                <Area
                  type="monotone"
                  dataKey="error"
                  stackId="1"
                  stroke="#f97316"
                  fill="#f9731660"
                  name="Errors / Rejected"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Row: category bar + top sources */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
        {/* Category breakdown */}
        <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
          <SectionHeader
            title="Category Breakdown"
            subtitle="Distribution by category / label"
          />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryData}>
                <XAxis dataKey="category" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#020617",
                    border: "1px solid #334155",
                    fontSize: 12,
                  }}
                />
                <Bar dataKey="count" fill="#38bdf8" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top sources */}
        <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
          <SectionHeader
            title="Top Sources"
            subtitle="Most active sources in the current window"
          />
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topSourceData} layout="vertical">
                <XAxis type="number" stroke="#94a3b8" />
                <YAxis
                  type="category"
                  dataKey="ip"
                  stroke="#94a3b8"
                  width={110}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#020617",
                    border: "1px solid #334155",
                    fontSize: 12,
                  }}
                />
                <Legend />
                <Bar
                  dataKey="total"
                  fill="#38bdf8"
                  name="Events"
                  radius={[0, 6, 6, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* Live table */}
      <section className="bg-slate-900/80 border border-slate-700/80 rounded-2xl p-4 shadow-xl">
        <SectionHeader
          title="Live Event Stream"
          subtitle="Newest events at the top"
        />
        <div className="overflow-x-auto max-h-80">
          <table className="w-full text-xs md:text-sm">
            <thead>
              <tr className="text-slate-400 border-b border-slate-700 text-left">
                <th className="py-2 pr-3">Source</th>
                <th className="py-2 pr-3">Target / URL</th>
                <th className="py-2 pr-3">Status</th>
                <th className="py-2 pr-3">Category</th>
              </tr>
            </thead>
            <tbody>
              {logs
                .slice()
                .reverse()
                .slice(0, 50)
                .map((log, i) => (
                  <tr
                    key={i}
                    className="border-b border-slate-800/80 hover:bg-slate-900/40"
                  >
                    <td className="py-2 pr-3 whitespace-nowrap">{log.ip}</td>
                    <td className="py-2 pr-3 truncate max-w-[260px]">
                      {log.url}
                    </td>
                    <td
                      className={`py-2 pr-3 font-medium ${
                        log.action === "blocked"
                          ? "text-amber-400"
                          : "text-emerald-400"
                      }`}
                    >
                      {log.action === "blocked" ? "error / rejected" : "ok"}
                    </td>
                    <td className="py-2 pr-3 whitespace-nowrap">
                      {log.reason || "uncategorised"}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

/* ---------- helper components ---------- */

function KpiCard({ title, value, color, subtitle }) {
  return (
    <div className="bg-slate-900/80 border border-slate-700/80 rounded-2xl px-4 py-3 flex flex-col justify-between shadow-xl">
      <div className="text-[0.7rem] text-slate-400 uppercase tracking-[0.16em] mb-1">
        {title}
      </div>
      <div className="flex items-baseline justify-between">
        <div className="text-2xl md:text-3xl font-semibold">{value}</div>
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold"
          style={{
            background: `radial-gradient(circle at 30% 30%, ${color}, transparent)`,
            boxShadow: `0 0 16px ${color}70`,
          }}
        >
          •
        </div>
      </div>
      <div className="text-[0.7rem] text-slate-500 mt-1">{subtitle}</div>
    </div>
  );
}

function SectionHeader({ title, subtitle }) {
  return (
    <div className="flex items-baseline justify-between mb-3">
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-sky-400 shadow-[0_0_10px_rgba(56,189,248,0.9)]" />
        <h2 className="text-sm md:text-base font-semibold tracking-[0.16em] uppercase text-slate-300">
          {title}
        </h2>
      </div>
      <span className="text-[0.7rem] text-slate-500">{subtitle}</span>
    </div>
  );
}

/* ---------- analytics core ---------- */

function computeAnalytics(logs) {
  const total = logs.length;

  // Treat "allowed" as success, "blocked" as error/rejected
  const successCount = logs.filter((l) => l.action === "allowed").length;
  const errorCount = total - successCount;
  const successRate = total ? (successCount / total) * 100 : 0;

  // Category breakdown (using "reason" as category label)
  const categories = {};
  logs.forEach((l) => {
    const key = l.reason || "uncategorised";
    categories[key] = (categories[key] || 0) + 1;
  });
  const categoryData = Object.entries(categories).map(([category, count]) => ({
    category,
    count,
  }));

  // Timeline: simple index-based series (no timestamps in logger)
  const timelineData = logs.map((_, index) => ({
    index,
    total: 1,
  }));

  // Status composition over time (expand to ratio)
  const compositionData = logs.map((l, index) => ({
    index,
    success: l.action === "allowed" ? 1 : 0,
    error: l.action === "blocked" ? 1 : 0,
  }));

  // Top sources by total event volume
  const sourceCounts = {};
  logs.forEach((l) => {
    if (!sourceCounts[l.ip]) {
      sourceCounts[l.ip] = { ip: l.ip, total: 0 };
    }
    sourceCounts[l.ip].total += 1;
  });
  const topSourceData = Object.values(sourceCounts)
    .sort((a, b) => b.total - a.total)
    .slice(0, 7);

  return {
    total,
    successCount,
    errorCount,
    successRate,
    categoryData,
    timelineData,
    compositionData,
    topSourceData,
  };
}
