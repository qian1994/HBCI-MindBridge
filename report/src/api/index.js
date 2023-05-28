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









export function getImages(msg){
    return apiClient.send({
        action: 'get-images',
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

export function drawImageByLabelSSVEP(msg) {
    return apiClient.send({
        action: 'draw-image-by-label-ssvep',
        data: msg
    })
}


