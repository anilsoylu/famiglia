import { Router } from "express";
import { query } from "../db.js";
import { requireTeamRole } from "../auth.js";

export const teams = Router();

teams.get("/:id", async (req, res) => {
  if (!(await requireTeamRole(query, req.params.id, req.user.id, ["owner", "admin", "member"]))) {
    return res.status(404).json({ error: "not found" });
  }
  const { rows } = await query("select id, name from teams where id = $1", [req.params.id]);
  res.json(rows[0]);
});
