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

export async function  startSession(msg){
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

export function openHtml(msg) {
    return apiClient.send({
        action: 'open-html',
        data: msg
    })
}

export function addParadigmFromLocal(msg) {
    return apiClient.send({
        action: 'add-paradigm',
        data: msg
    })
}

export function postConfig(msg) {
    return apiClient.send({
        action: 'get-config',
        data: msg
    })
}

export function getApplications(msg) {
    return apiClient.send({
        action:'get-applications',
        data: msg
    })
}


export function homePage(msg) {
    return apiClient.send({
        action:'go-to-home-page',
        data: msg
    })
}


export function openTimeSeriseWindow(msg) {
    return apiClient.send({
        action:'open-time-serise-window',
        data: msg
    })
}

export function closeTimeSeriseWindow(msg) {
    return apiClient.send({
        action:'close-time-serise-window',
        data: msg
    })
}


export function openFFTWindow(msg) {
    return apiClient.send({
        action:'open-fft-window',
        data: msg
    })
}

export function closeFFTWindow(msg) {
    return apiClient.send({
        action:'close-fft-window',
        data: msg
    })
}

export function openPSDWindow(msg) {
    return apiClient.send({
        action:'open-psd-window',
        data: msg
    })
}

export function closePSDWindow(msg) {
    return apiClient.send({
        action:'close-psd-window',
        data: msg
    })
}

export function openHeadPlotWindow(msg) {
    return apiClient.send({
        action:'open-head-plot-window',
        data: msg
    })
}

export function closeHeadPlotindow(msg) {
    return apiClient.send({
        action:'close-head-plot-window',
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

export function endTrialTask(msg) {
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

export function getChannelImageByFiles(msg) {
    return apiClient.send({
        action: 'get-result-image-by-filename',
        data: msg
    })
}

export function postSelectChannel(msg) {
    return apiClient.send({
        action: 'post-time-serise-channel-show',
        data: msg
    })
}

export function initTestBoard(msg){
    return apiClient.send({
        action: 'init-board',
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

export function initDevTools(msg) {
    return apiClient.send({
        action: 'init-dev-tools',
        data: msg
    })
}

export function getCurrentBoardData(msg) {
    return apiClient.send({
        action: 'get-current-board-data',
        data: msg
    })
}

export function openFileDialog(msg){
    return apiClient.send({
        action: 'open-file-dialog',
        data: msg
    })
}

export function openRealTimeFFT(msg) {
    return apiClient.send({
        action: 'open-real-time-fft',
        data: msg
    })
}

export function filterBoardData(msg) {
    return apiClient.send({
        action: 'filter-board-dta',
        data: msg
    })
}

export function getBatteryProportion(msg) {
    return apiClient.send({
        action: 'get-battery-proportion',
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


export function getEEGElectronPosition(msg) {
    return apiClient.send({
        action: "get-eeg-electron-position",
        data: msg
    })
}