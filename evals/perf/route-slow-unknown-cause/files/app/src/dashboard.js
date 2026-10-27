export function buildDashboard(events) {
  return { summary: summarize(events), activityPanel: activityPanel(events) };
}

function summarize(events) {
  let errors = 0;
  for (const e of events) if (e.type === "error") errors++;
  return { total: events.length, errors };
}

function activityPanel(events) {
  const users = [];
  for (const e of events) if (!users.includes(e.user)) users.push(e.user);
  return users.map((user) => {
    const mine = events.filter((e) => e.user === user);
    mine.sort((a, b) => b.at - a.at);
    return { user, count: mine.length, latest: mine.slice(0, 5) };
  });
}
