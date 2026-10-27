import express from "express";
import { requireUser } from "./auth.js";
import { teams } from "./routes/teams.js";

const app = express();
app.use(express.json());
app.use("/teams", requireUser, teams);

app.listen(process.env.PORT ?? 3000);
