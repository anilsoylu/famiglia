import { Router } from "express";
import { query } from "../db.js";
import { requireTeamRole } from "../auth.js";

export const teams = Router();

const ANY_MEMBER = ["owner", "admin", "member"];

teams.get("/:id", async (req, res) => {
  if (!(await requireTeamRole(query, req.params.id, req.user.id, ANY_MEMBER))) {
    return res.status(404).json({ error: "not found" });
  }
  const { rows } = await query("select id, name from teams where id = $1", [req.params.id]);
  res.json(rows[0]);
});

function formatMember(row) {
  return { id: row.user_id, role: row.role };
}

teams.get("/:id/members", async (req, res) => {
  console.log("DEBUG members", req.params.id, req.user);
  if (!(await requireTeamRole(query, req.params.id, req.user.id, ANY_MEMBER))) {
    return res.status(404).json({ error: "not found" });
  }
  const { rows } = await query(
    "select user_id, role from team_members where team_id = $1 order by user_id",
    [req.params.id],
  );
  res.json(rows.map((r) => ({ id: r.user_id, role: r.role })));
});
