import ApiClient from '../plugins/webBridge';
const apiClient = new ApiClient("context", "requestFromClient", "responseSignal");
apiClient.addResponseListener();

export function sendMsg(msg) {
    return apiClient.send({
        action: 'send-msg',
        data: msg
    });
}

export function sendSyncMsg(msg) {
    return apiClient.send({
        action: 'send-msg-sync',
        data: msg
    });
}

function _addMsgListener(callback) {
    apiClient.on("getFromServer", callback);
}

function _removeMsgListener(callback) {
    apiClient.off("getFromServer", callback);
} 

export const msgListener = {
    add: _addMsgListener,
    remove: _removeMsgListener
};
export function startSession(msg){
    return apiClient.send({
        action: 'start-session',
        data: msg
    })
}

export function stopSession(msg) {
    return apiClient.send({
        action: 'stop-session',
        data: msg
    })
}

export function startStream(msg) {
    return apiClient.send({
        action: 'start-stream',
        data: msg
    })
}

export function stopStream(msg) {
    return apiClient.send({
        action: 'stop-stream',
        data: msg
    })
}


export function trigger(msg) {
    return apiClient.send({
        action: 'trigger',
        data: msg
    })
}

export function p300_check(msg) {
    return apiClient.send({
        action: 'p300-check',
        data: msg
    })
}

export function getConfigFromServe(msg) {
    return apiClient.send({
        action: 'get-config',
        data: msg
    })
}

export function initDevTools(msg) {
    return apiClient.send({
        action: 'init-dev-tools',
        data: msg
    })
}

export function endTotalTask(msg) {
    return apiClient.send({
        action: 'end-total-task',
        data: msg
    })
}

export function getP300DectectionResult(msg){
    return apiClient.send({
        action: 'get-p300-dectation'
    })
}

export function homePage(msg) {
    return apiClient.send({
        action:'go-to-home-page',
        data: msg
    })
}

export function addPatientInfo(msg) {
    return apiClient.send({
        action: 'add-patient-info',
        data: msg
    })
}

export function openFilesDialog(msg) {
    return apiClient.send({
        action: 'open-files-dialog',
        data: msg
    })
}

export function openFileDialog(msg) {
    return apiClient.send({
        action: 'open-files-dialog',
        data: msg
    })
}

export function openDirDialog(msg) {
    return apiClient.send({
        action: 'open-dir-dialog',
        data: msg
    })
}

export function createMechainLearnP300(msg) {
    return apiClient.send({
        action: 'create-mechain-learn-p300',
        data: msg
    })
}