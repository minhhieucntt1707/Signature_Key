
setInterval(() => {
    fetch("/logs")
        .then(res => res.json())
        .then(data => {
            const logDiv = document.getElementById("log");
            logDiv.textContent = data.join("\n");
            logDiv.scrollTop = logDiv.scrollHeight;
        });
}, 2000);
