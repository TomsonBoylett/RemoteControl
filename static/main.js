let ws = new WebSocket(
    (location.protocol == "http:" ? "ws:" : "wss:") + "//" + location.hostname +
    (location.port ? ":" + location.port : "") + "/ws"
);

window.addEventListener("load", () => {
    let items = document.getElementsByClassName("item");
    let event_type = "ontouchend" in window ? "touchend" : "click";
    for (item of items) {
        item.addEventListener(event_type, (event) => {
            let command = event.target.dataset.command;
            if (command) {
                ws.send(command);
            }
        });
    }

    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
});