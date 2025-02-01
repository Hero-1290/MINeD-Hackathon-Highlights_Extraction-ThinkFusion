const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const port = 3000;

// Serve static files (e.g., HTML, CSS, JS)
app.use(express.static("public"));

// Serve videos from the "highlights" folder
app.use("/highlights", express.static(path.join(__dirname, "highlights")));

// Endpoint to fetch videos
app.get("/highlights", (req, res) => {
  const highlightsPath = path.join(__dirname, "highlights");
  fs.readdir(highlightsPath, (err, files) => {
    if (err) {
      return res.status(500).json({ error: "Unable to fetch videos" });
    }
    res.json(files.map((file) => ({ name: file })));
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
