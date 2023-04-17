import axios from "axios";
const instance = axios.create({
    baseURL: url,
    timeout: 100,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
});


export default instance