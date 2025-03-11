document.addEventListener("DOMContentLoaded", () => {
    fetch("data.json")
        .then(response => response.json())
        .then(projects => {
            const container = document.getElementById("portfolio");
            const projectContainer = document.getElementById("project-detail");

            const path = window.location.pathname.replace(/^\//, "");
            console.log(path)

        })
        .catch(error => console.error("Error loading projects:", error));
});
