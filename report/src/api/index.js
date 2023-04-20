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

export function getReportFileListSSVEP(msg) {
    return apiClient.send({
        action: 'get-report-file-list-ssvep',
        data: msg
    })
}


export function createFileReportSSVEP(msg) {
    return apiClient.send({
        action: 'create-file-reaport-ssvep',
        data: msg
    })
}


export function initDevTools(msg) {
    return apiClient.send({
        action: 'init-dev-tools',
        data: msg
    })
}