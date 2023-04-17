import ApiClient from '../plugins/webBridge';
const apiClient = new ApiClient("context", "requestFromClient", "responseFromServer");
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
    apiClient.on("receiveMsgFromServer", callback);
}

function _removeMsgListener(callback) {
    apiClient.off("receiveMsgFromServer", callback);
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

export function openDataAnalysis(msg) {
    return apiClient.send({
        action: 'open-analysis',
        data: msg
    })
}

export function openSSVEP(msg) {
    return apiClient.send({
        action: 'open-ssvep',
        data: msg
    })
}


export function openP300(msg) {
    return apiClient.send({
        action: 'open-p300',
        data: msg
    })
}

export function openMI(msg) {
    return apiClient.send({
        action: 'open-mi',
        data: msg
    })
}
