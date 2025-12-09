const API_BASE = "http://localhost:8000/api";

// Decide what to do with a URL using the backend
async function inspectUrl(url) {
  try {
    const res = await fetch(`${API_BASE}/inspect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    if (!res.ok) {
      console.warn("Inspect API returned non-OK:", res.status);
      return { decision: "allow", reason: "api_error" };
    }

    const data = await res.json();
    return {
      decision: data.decision || "allow",
      reason: data.reason || "unknown"
    };
  } catch (err) {
    console.error("Error calling inspect API", err);
    return { decision: "allow", reason: "exception" };
  }
}

// Trigger on main-frame navigations (new page loads)
chrome.webNavigation.onCommitted.addListener(async (details) => {
  // Only main frame
  if (details.frameId !== 0) return;

  const url = details.url;
  // Skip chrome://, about:blank, extension pages, etc.
  if (!url.startsWith("http://") && !url.startsWith("https://")) return;

  const { tabId } = details;
  const { decision, reason } = await inspectUrl(url);

  if (decision === "block") {
    // Redirect to local blocked page
    const blockedUrl = chrome.runtime.getURL(
      `blocked.html?reason=${encodeURIComponent(reason)}&url=${encodeURIComponent(url)}`
    );

    await chrome.tabs.update(tabId, { url: blockedUrl });

    // Optional notification
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon128.png",
      title: "WebDefender-X blocked a page",
      message: `Reason: ${reason}`
    });
  }
});
