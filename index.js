console.log(navigator.language)
if (!navigator.language.startsWith("ja")) {
    const currentPath = location.pathname;
    if (!currentPath.startsWith("/en")) {
        location.href = "/en" + currentPath;
    }
}