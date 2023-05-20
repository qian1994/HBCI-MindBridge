import axios from 'axios'
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

export function openFileDialog(msg){
    return apiClient.send({
        action: 'open-file-dialog',
        data: msg
    })
}

export function openDirDialog(msg){
    return apiClient.send({
        action: 'open-dir-dialog',
        data: msg
    })
}

export function initDevTools(msg) {
    return apiClient.send({
        action: 'init-dev-tools',
        data: msg
    })
}

export function getConfigFromServe(msg) {
    return apiClient.send({
        action: 'get-config',
        data: msg
    })
}

export function getEEGElectronPosition(msg) {
    return apiClient.send({
        action: "get-eeg-electron-position",
        data: msg
    })
}

export function getLabelByFileName(msg) {
    return apiClient.send({
        action: 'get-file-labels-by-file-name',
        data: msg
    })
}

export function processingOriginData(msg) {
    return apiClient.send({
        action: 'processing-origin-data',
        data: msg
    })
}

export function plotOriginEEGDataByFile(msg) {
    return apiClient.send({
        action: 'processing-origin-data',
        data: msg
    })
}