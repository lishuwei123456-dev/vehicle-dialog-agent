const form = document.querySelector("#commandForm");
const input = document.querySelector("#queryInput");
const quickCommands = document.querySelector("#quickCommands");
const resetButton = document.querySelector("#resetButton");
const jsonOutput = document.querySelector("#jsonOutput");
const moduleList = document.querySelector("#moduleList");
const replyText = document.querySelector("#replyText");
const intentBadge = document.querySelector("#intentBadge");
const confidenceText = document.querySelector("#confidenceText");
const sessionText = document.querySelector("#sessionText");
const navText = document.querySelector("#navText");
const mediaText = document.querySelector("#mediaText");
const climateText = document.querySelector("#climateText");
const windowText = document.querySelector("#windowText");
const volumeText = document.querySelector("#volumeText");
const seatText = document.querySelector("#seatText");
const weatherBadge = document.querySelector("#weatherBadge");
const clockText = document.querySelector("#clockText");

const examples = [
  "导航去北京南站",
  "打开空调",
  "关闭车窗",
  "播放周杰伦的歌",
  "查询北京天气",
  "调高音量",
  "哈哈哈",
  "去上海虹桥站",
];

const sessionId = `web-${Math.random().toString(36).slice(2, 10)}`;
sessionText.textContent = sessionId;

function tickClock() {
  const now = new Date();
  const hour = String(now.getHours()).padStart(2, "0");
  const minute = String(now.getMinutes()).padStart(2, "0");
  clockText.textContent = `${hour}:${minute}`;
}

function buildQuickCommands() {
  examples.forEach((command) => {
    const button = document.createElement("button");
    button.className = "quick-command";
    button.type = "button";
    button.textContent = command;
    button.title = command;
    button.addEventListener("click", () => {
      input.value = command;
      submitCommand(command);
    });
    quickCommands.appendChild(button);
  });
}

async function submitCommand(query) {
  const trimmed = query.trim();
  if (!trimmed) {
    input.focus();
    return;
  }

  document.body.classList.add("is-loading");
  replyText.textContent = "处理中";
  try {
    const response = await fetch("/v1/cockpit/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: trimmed, session_id: sessionId }),
    });
    const payload = await response.json();
    renderPayload(payload);
  } catch (error) {
    renderError(error);
  } finally {
    document.body.classList.remove("is-loading");
  }
}

function renderPayload(payload) {
  const dialogue = payload.dialogue;
  const state = payload.state;

  intentBadge.textContent = dialogue.intent;
  intentBadge.classList.toggle("reject", !dialogue.accepted);
  confidenceText.textContent = dialogue.confidence.toFixed(2);
  replyText.textContent = dialogue.reply;
  jsonOutput.textContent = JSON.stringify(payload, null, 2);

  navText.textContent = state.navigation_destination;
  mediaText.textContent = state.media_title;
  climateText.textContent = state.climate_on ? `${state.cabin_temperature}度` : "关闭";
  windowText.textContent = `${state.window_position}%`;
  volumeText.textContent = String(state.volume);
  seatText.textContent = state.seat_heat ? "加热" : "常规";
  weatherBadge.textContent = state.weather_summary;

  renderModules(payload.modules);
}

function renderModules(modules) {
  moduleList.replaceChildren();
  modules.forEach((item, index) => {
    const row = document.createElement("li");
    row.className = "module-step";

    const badge = document.createElement("span");
    badge.className = "module-index";
    badge.textContent = String(index + 1);

    const body = document.createElement("div");
    const name = document.createElement("p");
    name.className = "module-name";
    name.textContent = `${item.name} · ${item.status}`;

    const detail = document.createElement("p");
    detail.className = "module-detail";
    detail.textContent = item.detail;

    body.append(name, detail);
    row.append(badge, body);
    moduleList.appendChild(row);
  });
}

function renderError(error) {
  const message = error instanceof Error ? error.message : "unknown error";
  intentBadge.textContent = "ERROR";
  intentBadge.classList.add("reject");
  replyText.textContent = "接口请求失败";
  jsonOutput.textContent = JSON.stringify({ error: message }, null, 2);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  submitCommand(input.value);
});

resetButton.addEventListener("click", () => {
  window.location.reload();
});

tickClock();
setInterval(tickClock, 30000);
buildQuickCommands();
submitCommand("导航去北京南站");
