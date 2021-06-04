let ws = new WebSocket(
    (location.protocol == "http:" ? "ws:" : "wss:") + "//" + location.hostname +
    (location.port ? ":" + location.port : "") + "/ws"
);

window.addEventListener("load", () => {
    let items = document.getElementsByClassName("item");
    let event_type = "ontouchend" in window ? "touchend" : "click";
    for (item of items) {
        let command = item.dataset.command;
        if (command) {
            item.addEventListener(event_type, () => {
                window.navigator.vibrate(10);
                ws.send(command); 
            });
        }
    }

    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);

    if (document.getElementsByClassName('simple-keyboard').length > 0) {
        setupKeyboard();
    }
});

function setupKeyboard() {
    const Keyboard = window.SimpleKeyboard.default;

    const keyboard = new Keyboard({
        theme: "hg-theme-default fit-container",
        onKeyPress: button => onKeyPress(button),
        layout: {
            'default': [
            '1 2 3 4 5 6 7 8 9 0',
            'q w e r t y u i o p',
            'a s d f g h j k l',
            '{shift} z x c v b n m {backspace}',
            '{symbols} , {space} . {enter}'
            ],
            'shift': [
                '1 2 3 4 5 6 7 8 9 0',
                'Q W E R T Y U I O P',
                'A S D F G H J K L',
                '{shift} Z X C V B N M {backspace}',
                '{symbols} , {space} . {enter}'
            ],
            'symbols1': [
                '1 2 3 4 5 6 7 8 9 0',
                '+ x ÷ = / _ € £ ¥ ₩',
                '! @ # $ % ^ & * ( )',
                '{1of2} - \' " : ; ? {backspace}',
                '{ABC} , {space} . {enter}'
            ],
            'symbols2': [
                '1 2 3 4 5 6 7 8 9 0',
                '` ~ \\ | < > { } [ ]',
                '° • ○ ● □ ■ ♤ ♡ ◇ ♧',
                '{2of2} ☆ ▪︎ ¤ 《 》 ¡ ¿ {backspace}',
                '{ABC} , {space} . {enter}'
            ]
        },
        mergeDisplay: true,
        display: {
            '{backspace}': '⌫',
            '{enter}': '⏎',
            '{shift}': '⇧',
            '{symbols}': '!#1',
            '{1of2}': '1/2',
            '{2of2}': '2/2',
            '{ABC}': 'ABC'
        },
        buttonTheme: [
            {
                class: "max-width",
                buttons: ", . {enter} {symbols} {ABC} "
            },
            {
                class: "no-max-width",
                buttons: "@"
            }
        ]
    });

    const layout_buttons = {
        "{shift}": (currentLayout) => {
            return currentLayout === "default" ? "shift" : "default"
        },
        "{symbols}": (currentLayout) => {
            return "symbols1"
        },
        "{1of2}": (currentLayout) => {
            return "symbols2"
        },
        "{2of2}": (currentLayout) => {
            return "symbols1"
        },
        "{ABC}": (currentLayout) => {
            return "default"
        }
    }

    function onKeyPress(button) {
        window.navigator.vibrate(10);
        if (button in layout_buttons) {
            let currentLayout = keyboard.options.layoutName;
            keyboard.setOptions({
                layoutName: layout_buttons[button](currentLayout)
            });
        } else {
            let command = keyboard.keyboardDOM.dataset.command;
            ws.send(command + ',' + button)
        }
    }
}