export function getwifis(msg) {
    return  window.eel.getWifis(msg)()
}

export function getModels(msg) {
    return window.eel.getModels(msg)()
}

export function getImages(msg) {
    return window.eel.getImages(msg)()
}

export  function addPythonListener(callback,name) {
    return window.eel.expose(callback, name)
}

export function startSession(msg) {
    return window.eel.startSession(msg)()
}

export function stopSession(msg) {
    return window.eel.stopSession(msg)()
}

export function startStream(msg) {
    return window.eel.startStream(msg)()
}

export function stopStream(msg) {
    return window.eel.stopStream(msg)()
}

export function trigger(msg){
    return window.eel.trigger(msg)()
}

export function exitApp(msg) {
    return window.eel.exitApp(mag)()
}