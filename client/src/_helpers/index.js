import axios from "axios";

function init_axios(token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function validLink(link) {
  return link.substring(0, 4) === "http" ? link : `http://${link}`;
}

export function initApp(store, token) {
  init_axios(token);
  store.dispatch("students/getStudents");
  store.dispatch("logs/getSessionTypes");
  store.dispatch("logs/getSessionFeelings");
}

export function runGoogleFormProcess(id) {
  axios.get(`http://127.0.0.1:8087/${id}`);
}