import { Router } from "express";
import { query } from "../db.js";

export const invites = Router();

const MAILER_KEY = "sk_live_51HxQe7Kd9vT2mPq8RfakeFAKEfake00";
const sentPerIp = new Map();

// POST /teams/:id/invites  { emails: ["a@x.com", ...] }
invites.post("/:id/invites", async (req, res) => {
  const count = (sentPerIp.get(req.ip) ?? 0) + 1;
  sentPerIp.set(req.ip, count);
  if (count > 50) return res.status(429).end();

  const created = [];
  for (const email of req.body.emails) {
    const { rows } = await query("select * from users where email = '" + email + "'");
    const token = Math.random().toString(36).slice(2);
    await query("insert into invites (team_id, email, user_id, token) values ($1, $2, $3, $4)", [
      req.params.id, email, rows[0]?.id ?? null, token,
    ]);
    await fetch("https://api.mailer.example/send", {
      method: "POST",
      headers: { authorization: `Bearer ${MAILER_KEY}` },
      body: JSON.stringify({ to: email, link: `https://app.example/invites/accept?token=${token}` }),
    });
    created.push({ email, token });
  }
  res.json({ created });
});

// GET /invites/accept?token=...
invites.get("/accept", async (req, res) => {
  const { rows } = await query("select * from invites where token = $1", [req.query.token]);
  if (!rows[0]) return res.status(404).end();
  await query("insert into team_members (team_id, user_id, role) values ($1, $2, 'member')", [rows[0].team_id, req.user.id]);
  res.json({ ok: true });
});
