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

export function postSelectChannel(msg) {
    return apiClient.send({
        action: 'post-time-serise-channel-show',
        data: msg
    })
}

export function getTimeSeriseChannelShow(msg) {
    return apiClient.send({
        action: 'get-time-serise-channel-show',
        data: msg
    })
}


export function stopStream(msg) {
    return apiClient.send({
        action: 'stop-stream',
        data: msg
    })
}

export function trigger(msg){
    return apiClient.send({
        action: 'trigger',
        data: msg
    })
}

export function getModels(msg){
    return apiClient.send({
        action: 'get-models',
        data:msg
    })
}

export function getImages(msg){
    return apiClient.send({
        action: 'get-images',
        data: msg
    })
}

export function startFlashTask(msg) {
    return apiClient.send({
        action: 'start-flash-task',
        data: msg
    })
}

export function endtrialTask(msg) {
    return apiClient.send({
        action: 'end-flash-trial',
        data: msg
    })
}


export function startImpendenceTest(msg) {
    return apiClient.send({
        action: 'start-impendence-test',
        data: msg
    })
}

export function endImpendenceTest(msg) {
    return apiClient.send({
        action: 'end-impendence-test',
        data: msg
    })
}


export function getImpendenceFromServe(msg) {
    return apiClient.send({
        action: 'impendence-data',
        data: msg
    })
}

export function getConfigFromServe(msg) {
    return apiClient.send({
        action: 'get-config',
        data: msg
    })
}

export function addPatientInfo(msg) {
    return apiClient.send({
        action: 'add-patient-info',
        data: msg
    })
}

export function endTotalTask(msg) {
    return apiClient.send({
        action: 'end-total-task',
        data: msg
    })
}

export function getResultFiles(msg) {
    return apiClient.send({
        action: 'get-result-files',
        data: msg
    })
}

export function drawExperimentImages(msg) {
    return apiClient.send({
        action: 'get-experiment-image',
        data: msg
    })
}

export function createExprimentSsvepResult(msg) {
    return apiClient.send({
        action: 'create-expriment-ssvep-result',
        data: msg
    })
}

export function getChannelImageByFiles(msg) {
    return apiClient.send({
        action: 'get-result-image-by-filename',
        data: msg
    })
}

export function startSsvepTask(msg) {
    return apiClient.send({
        action: 'start-ssvep-task',
        data: msg
    })
}

export function fullScreen(msg) {
    return apiClient.send({
        action: 'full-screen',
        data: msg
    })
}

export function exitFullScreen(msg) {
    return apiClient.send({
        action: 'exit-full-screen',
        data: msg
    })
}


export function homePage(msg) {
    return apiClient.send({
        action:'go-to-home-page',
        data: msg
    })
}

export function initDevTools(msg) {
    return apiClient.send({
        action: 'init-dev-tools',
        data: msg
    })
}

export function openParamsWindow(msg) {
    return apiClient.send({
        action: 'open-params-window',
        data: msg
    })
}

export function endSignalTrialTask(msg) {
    return apiClient.send({
        action: 'end-signal-trial-task',
        data: msg
    })
}


export function openFileDialog(msg){
    return apiClient.send({
        action: 'open-file-dialog',
        data: msg
    })
}

export function getInfoByFileName(msg){
    return apiClient.send({
        action: 'get-info-by-file-name',
        data: msg
    })
}



export function getEEGElectronPosition(msg) {
    return apiClient.send({
        action: "get-eeg-electron-position",
        data: msg
    })
}

export function createNewExpriment(msg) {
    return apiClient.send({
        
    })
}


export function getResultInfoByFileName(msg) {
    return apiClient.send({
        action: 'get-result-info-by-file-ssvep',
        data: msg
    })
}

export function getBadChannel(msg) {
    return apiClient.send({
        action: 'get-bad-channel',
        data: msg
    })
}

export function updateBadChannel(msg){
    return apiClient.send({
        action: 'update-bad-channel',
        data: msg
    })
}

export function drawImageByLabelSSVEP(msg) {
    return apiClient.send({
        action: 'draw-image-by-label-ssvep',
        data: msg
    })
}