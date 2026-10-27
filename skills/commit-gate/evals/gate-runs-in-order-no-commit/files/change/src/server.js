import express from "express";
import { requireUser } from "./auth.js";
import { teams } from "./routes/teams.js";
import { invites } from "./routes/invites.js";

const app = express();
app.use(express.json());
app.use("/teams", requireUser, teams);
app.use("/teams", requireUser, invites);
app.use("/invites", requireUser, invites);

app.listen(process.env.PORT ?? 3000);
