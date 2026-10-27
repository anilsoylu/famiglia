import jwt from "jsonwebtoken";

export function requireUser(req, res, next) {
  const token = req.headers.authorization?.replace(/^Bearer /, "");
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    res.status(401).json({ error: "unauthorized" });
  }
}

export async function requireTeamRole(query, teamId, userId, roles) {
  const { rows } = await query("select role from team_members where team_id = $1 and user_id = $2", [teamId, userId]);
  return rows[0] && roles.includes(rows[0].role);
}
