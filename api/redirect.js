import { readFileSync } from "fs";
import { join } from "path";

export default function handler(req, res) {
    try {
        const filePath = join(process.cwd(), "public", "data", "data.json");
        const jsonData = readFileSync(filePath, "utf8");
        const projects = JSON.parse(jsonData);

        const path = req.url.replace(/^\/api\/redirect\//, "");

        const project = projects.find(p => p.slug === path);

        if (project && project.url) {
            res.writeHead(302, { Location: project.url });
            res.end();
        } else {
            res.status(404).json({ error: "Project not found" });
        }
    } catch (error) {
        console.error("Error processing request:", error);
        res.status(500).json({ error: "Internal server error" });
    }
}
