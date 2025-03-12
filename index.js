document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("./data/data.json");
        const projects = await response.json();

        const container = document.getElementById("portfolio");
        const projectContainer = document.getElementById("project-detail");

        const path = window.location.pathname.replace(/^\//, "");

        projects.forEach(element => {
            if (element.slug === path && element.type === "app") {
                redirectApp(element)
            } else {
                renderHome()
            }
        })

        renderArticle(projects)
    } catch (error) {
        console.error("Error loading projects:", error);
    }
});

function redirectApp(element){
    location.replace(element.url)
}

function renderHome() {

}

async function renderArticle(projects){
    const data = await fetch("./template/article.html")
    const text = await data.text()
    let dom = new DOMParser().parseFromString(text, "text/html")
    projects.forEach(element => {
        let article = dom.querySelector("article").cloneNode(true)
        article.querySelector("a").href = element.url
        article.querySelector("img").src = `./data/img/${element.slug}.png`
        article.querySelector("h2").innerText = element.name
        article.querySelector("h3").innerText = element.date
        article.querySelector("p").innerText = element.description

        document.querySelector("main").appendChild(article)
    })
}