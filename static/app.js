const state = {
  bootstrap: null,
  teamMap: new Map(),
  activeView: "dashboard",
  rendered: new Set(),
  simCount: 0,
};

const TITLES = {
  dashboard: "Dashboard",
  comparison: "Team Comparison",
  predictions: "Match Prediction",
  simulator: "World Cup Simulator",
  rankings: "FIFA Rankings",
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[char]);
}

function fmt(value, suffix = "") {
  const number = Number(value);
  if (!Number.isFinite(number)) return `--${suffix}`;
  const clean = Number.isInteger(number) ? String(number) : number.toFixed(1);
  return `${clean}${suffix}`;
}

function pct(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return 0;
  return Math.max(0, Math.min(100, number));
}

function api(path, params = {}) {
  const url = new URL(path, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, value);
  });
  return fetch(url).then(async (response) => {
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Richiesta non riuscita.");
    return payload;
  });
}

function showToast(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("is-visible");
  window.setTimeout(() => toast.classList.remove("is-visible"), 3200);
}

function flagHTML(flag, team, className = "flag") {
  if (!flag) return `<span class="${className} flag-empty" aria-hidden="true"></span>`;
  return `<img class="${className}" src="${escapeHTML(flag)}" alt="Bandiera ${escapeHTML(team)}" loading="lazy">`;
}

function findGroup(team) {
  for (const [group, teams] of Object.entries(state.bootstrap.groups)) {
    if (teams.includes(team)) return group;
  }
  return "A";
}

function groupOptions(selected) {
  return Object.keys(state.bootstrap.groups)
    .map((group) => `<option value="${group}" ${group === selected ? "selected" : ""}>Girone ${group}</option>`)
    .join("");
}

function teamOptions(group, selected) {
  return (state.bootstrap.groups[group] || [])
    .map((team) => `<option value="${escapeHTML(team)}" ${team === selected ? "selected" : ""}>${escapeHTML(team)}</option>`)
    .join("");
}

function selectorPanel(prefix, title, selectedTeam) {
  const group = findGroup(selectedTeam);
  return `
    <div class="control-panel">
      <p class="control-label">${escapeHTML(title)}</p>
      <div class="control-row">
        <div class="field">
          <label for="${prefix}-group">Girone</label>
          <select id="${prefix}-group">${groupOptions(group)}</select>
        </div>
        <div class="field">
          <label for="${prefix}-team">Squadra</label>
          <select id="${prefix}-team">${teamOptions(group, selectedTeam)}</select>
        </div>
      </div>
    </div>
  `;
}

function attachTeamSelector(prefix) {
  const groupEl = $(`#${prefix}-group`);
  const teamEl = $(`#${prefix}-team`);
  groupEl.addEventListener("change", () => {
    const teams = state.bootstrap.groups[groupEl.value] || [];
    teamEl.innerHTML = teamOptions(groupEl.value, teams[0]);
  });
}

function selectedTeam(prefix) {
  return $(`#${prefix}-team`).value;
}

function miniStat(label, value, suffix = "") {
  return `
    <div class="mini-stat">
      <span class="mini-label">${escapeHTML(label)}</span>
      <strong>${fmt(value, suffix)}</strong>
    </div>
  `;
}

function teamCard(team, variant = "home") {
  return `
    <article class="team-card ${variant === "away" ? "away" : ""}">
      <div class="team-head">
        ${flagHTML(team.flag, team.Squadra, "flag flag-lg")}
        <div>
          <h3 class="team-name">${escapeHTML(team.Squadra)}</h3>
          <div class="team-meta">Girone ${escapeHTML(team.Girone)} · Overall ${fmt(team.OverallRating)}</div>
        </div>
      </div>
      <div class="team-stats">
        ${miniStat("Gol", team.Gol)}
        ${miniStat("xG", team.xG)}
        ${miniStat("Possesso", team.Possesso, "%")}
      </div>
    </article>
  `;
}

function radarSVG(radar) {
  const labels = radar.labels || [];
  const series = radar.series || [];
  const cx = 180;
  const cy = 164;
  const radius = 112;
  const count = labels.length || 1;
  const maxByAxis = labels.map((_, index) => Math.max(1, ...series.map((item) => Number(item.values[index]) || 0)) * 1.12);

  const point = (index, ratio) => {
    const angle = (-90 + (360 / count) * index) * Math.PI / 180;
    return [cx + Math.cos(angle) * radius * ratio, cy + Math.sin(angle) * radius * ratio];
  };

  const rings = [0.25, 0.5, 0.75, 1].map((ratio) => {
    const points = labels.map((_, index) => point(index, ratio).join(",")).join(" ");
    return `<polygon points="${points}" fill="none" stroke="#dbe3dd" stroke-width="1"></polygon>`;
  }).join("");

  const axes = labels.map((label, index) => {
    const [x, y] = point(index, 1);
    const [tx, ty] = point(index, 1.18);
    return `
      <line x1="${cx}" y1="${cy}" x2="${x}" y2="${y}" stroke="#dbe3dd" stroke-width="1"></line>
      <text x="${tx}" y="${ty}" text-anchor="middle" dominant-baseline="middle" fill="#69746f" font-size="11" font-weight="800">${escapeHTML(label)}</text>
    `;
  }).join("");

  const polygons = series.map((item, index) => {
    const points = labels.map((_, axis) => {
      const ratio = Math.min(1, (Number(item.values[axis]) || 0) / maxByAxis[axis]);
      return point(axis, ratio).join(",");
    }).join(" ");
    const color = item.color || (index === 0 ? "#007f5f" : "#c43f4b");
    return `
      <polygon points="${points}" fill="${color}" fill-opacity="0.16" stroke="${color}" stroke-width="3"></polygon>
      ${labels.map((_, axis) => {
        const ratio = Math.min(1, (Number(item.values[axis]) || 0) / maxByAxis[axis]);
        const [x, y] = point(axis, ratio);
        return `<circle cx="${x}" cy="${y}" r="3.5" fill="${color}"></circle>`;
      }).join("")}
    `;
  }).join("");

  const legend = series.map((item) => `
    <span class="legend-item"><i style="background:${escapeHTML(item.color)}"></i>${escapeHTML(item.name)}</span>
  `).join("");

  return `
    <div class="radar-chart">
      <svg viewBox="0 0 360 330" role="img" aria-label="Radar confronto">
        ${rings}
        ${axes}
        ${polygons}
      </svg>
      <div class="radar-legend">${legend}</div>
    </div>
  `;
}

function metricCard(item) {
  return `
    <article class="metric-card">
      <div class="metric-top">
        ${flagHTML(item.flag, item.value)}
        <span class="metric-label">${escapeHTML(item.label)}</span>
      </div>
      <div>
        <strong class="metric-value">${escapeHTML(item.value)}</strong>
        <span class="metric-note">${escapeHTML(item.detail)}</span>
      </div>
    </article>
  `;
}

function listRow(row, mode = "team") {
  const title = mode === "team" ? row.team : row.name;
  const subtitle = mode === "team"
    ? `Overall ${fmt(row.overall)} · ATT ${fmt(row.attack)} · DEF ${fmt(row.defense)}`
    : `${row.team} · ${fmt(row.assists)} assist · xG ${fmt(row.xG)}`;
  const value = mode === "team" ? fmt(row.overall) : `${fmt(row.goals)} gol`;
  return `
    <div class="list-row">
      <span class="rank">${row.rank}</span>
      <div class="list-main">
        <span class="list-title">${escapeHTML(title)}</span>
        <span class="list-subtitle">${escapeHTML(subtitle)}</span>
      </div>
      <div class="list-value">${escapeHTML(value)}</div>
    </div>
  `;
}

function renderDashboard() {
  const home = state.bootstrap.home;
  $("#dashboard-view").innerHTML = `
    <div class="metrics-grid">
      ${home.topStats.map(metricCard).join("")}
    </div>

    <div class="dashboard-grid">
      <div>
        <section class="panel">
          <div class="panel-head">
            <div>
              <p class="section-kicker">Featured match</p>
              <h2 class="panel-title">${escapeHTML(home.featuredMatch.team1.Squadra)} vs ${escapeHTML(home.featuredMatch.team2.Squadra)}</h2>
            </div>
          </div>
          <div class="matchup">
            ${teamCard(home.featuredMatch.team1)}
            <div class="vs-block">VS</div>
            ${teamCard(home.featuredMatch.team2, "away")}
          </div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <p class="section-kicker">Leaderboard</p>
              <h2 class="panel-title">Top nazionali e marcatori</h2>
            </div>
          </div>
          <div class="leaderboard-grid">
            <div class="list-stack">
              ${home.leaderboards.teams.map((row) => listRow(row, "team")).join("")}
            </div>
            <div class="list-stack">
              ${home.leaderboards.scorers.map((row) => listRow(row, "player")).join("")}
            </div>
          </div>
        </section>
      </div>

      <div>
        <section class="panel">
          <div class="panel-head">
            <div>
              <p class="section-kicker">Radar</p>
              <h2 class="panel-title">Profilo squadre</h2>
            </div>
          </div>
          <div class="radar-wrap">${radarSVG(home.featuredMatch.radar)}</div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <p class="section-kicker">Sezioni</p>
              <h2 class="panel-title">Analisi disponibili</h2>
            </div>
          </div>
          <div class="sections-grid">
            <button class="section-button" type="button" data-shortcut="comparison">Team Comparison<span>Radar, barre e rosa</span></button>
            <button class="section-button" type="button" data-shortcut="predictions">Match Prediction<span>Probabilita e verdetto</span></button>
            <button class="section-button" type="button" data-shortcut="simulator">WC Simulator<span>Gironi e knockout</span></button>
            <button class="section-button" type="button" data-shortcut="rankings">FIFA Rankings<span>Classifica e gruppi</span></button>
          </div>
        </section>
      </div>
    </div>
  `;

  $$("[data-shortcut]").forEach((button) => {
    button.addEventListener("click", () => activateView(button.dataset.shortcut));
  });
}

function comparisonBars(rows) {
  return rows.map((row) => `
    <div class="dual-bar-row">
      <div class="bar-values">
        <span>${fmt(row.left, row.suffix)}</span>
        <span class="bar-label">${escapeHTML(row.label)}</span>
        <span>${fmt(row.right, row.suffix)}</span>
      </div>
      <div class="dual-bars">
        <div class="bar-track left"><span class="bar-fill" style="width:${pct(row.leftWidth)}%"></span></div>
        <div class="bar-track"><span class="bar-fill away" style="width:${pct(row.rightWidth)}%"></span></div>
      </div>
    </div>
  `).join("");
}

function renderRoster(team, groups) {
  if (!groups || groups.length === 0) {
    return `<section class="panel"><h2 class="panel-title">${escapeHTML(team)}</h2><div class="empty-state">Rosa non disponibile</div></section>`;
  }
  return `
    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Rosa</p>
          <h2 class="panel-title">${escapeHTML(team)}</h2>
        </div>
      </div>
      ${groups.map((group) => `
        <div class="role-group">
          <h3 class="role-title">${escapeHTML(group.label)}</h3>
          ${group.players.map((player) => `
            <article class="player-card">
              <div class="player-head">
                <span class="player-name">${escapeHTML(player.name)}</span>
                <span class="badge">${escapeHTML(player.role)} · ${escapeHTML(player.age ?? "--")} anni</span>
              </div>
              <div class="stat-pills">
                ${player.stats.map((stat) => `<span class="stat-pill">${escapeHTML(stat.label)} <strong>${fmt(stat.value, stat.suffix)}</strong></span>`).join("")}
              </div>
            </article>
          `).join("")}
        </div>
      `).join("")}
    </section>
  `;
}

function renderComparisonResult(data) {
  $("#comparison-result").innerHTML = `
    <section class="panel">
      <div class="matchup">
        ${teamCard(data.team1)}
        <div class="vs-block">VS</div>
        ${teamCard(data.team2, "away")}
      </div>
    </section>

    <div class="two-column">
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Statistiche</p>
            <h2 class="panel-title">Confronto diretto</h2>
          </div>
        </div>
        ${comparisonBars(data.stats)}
      </section>
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Radar</p>
            <h2 class="panel-title">Profilo avanzato</h2>
          </div>
        </div>
        ${radarSVG(data.radar)}
      </section>
    </div>

    <div class="roster-grid">
      ${renderRoster(data.team1.Squadra, data.rosters[data.team1.Squadra])}
      ${renderRoster(data.team2.Squadra, data.rosters[data.team2.Squadra])}
    </div>
  `;
}

async function loadComparison() {
  const target = $("#comparison-result");
  const team1 = selectedTeam("compare-a");
  const team2 = selectedTeam("compare-b");
  if (team1 === team2) {
    target.innerHTML = `<div class="empty-state">Seleziona due squadre diverse</div>`;
    return;
  }
  target.innerHTML = `<div class="loading">Caricamento confronto</div>`;
  try {
    renderComparisonResult(await api("/api/compare", { team1, team2 }));
  } catch (error) {
    target.innerHTML = `<div class="empty-state">${escapeHTML(error.message)}</div>`;
  }
}

function renderComparisonView() {
  $("#comparison-view").innerHTML = `
    <div class="control-grid">
      ${selectorPanel("compare-a", "Squadra 1", "Spagna")}
      ${selectorPanel("compare-b", "Squadra 2", "Francia")}
    </div>
    <div class="panel-actions">
      <button class="primary-button" type="button" id="compare-run">Aggiorna confronto</button>
    </div>
    <div id="comparison-result" class="simulator-stage"></div>
  `;
  attachTeamSelector("compare-a");
  attachTeamSelector("compare-b");
  $("#compare-run").addEventListener("click", loadComparison);
  loadComparison();
}

function renderPredictionResult(data) {
  const probability = data.probability;
  $("#prediction-result").innerHTML = `
    <section class="panel">
      <div class="matchup">
        ${teamCard(data.team1)}
        <div class="vs-block">VS</div>
        ${teamCard(data.team2, "away")}
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Win probability</p>
          <h2 class="panel-title">${escapeHTML(data.team1.Squadra)} · Pareggio · ${escapeHTML(data.team2.Squadra)}</h2>
        </div>
      </div>
      <div class="probability-bar" style="--home-pct:${pct(probability.team1)}fr;--draw-pct:${pct(probability.draw)}fr;--away-pct:${pct(probability.team2)}fr">
        <div class="prob-home">${fmt(probability.team1, "%")}</div>
        <div class="prob-draw">${fmt(probability.draw, "%")}</div>
        <div class="prob-away">${fmt(probability.team2, "%")}</div>
      </div>
    </section>

    <div class="two-column">
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Risultato previsto</p>
            <h2 class="panel-title">Scoreline</h2>
          </div>
        </div>
        <div class="scoreline">
          <div class="team-card">${miniStat("xG previsto", data.score.xg1)}<h3 class="team-name">${escapeHTML(data.team1.Squadra)}</h3></div>
          <div class="score-number">${data.score.team1} - ${data.score.team2}</div>
          <div class="team-card away">${miniStat("xG previsto", data.score.xg2)}<h3 class="team-name">${escapeHTML(data.team2.Squadra)}</h3></div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Reparti</p>
            <h2 class="panel-title">Analisi rating</h2>
          </div>
        </div>
        ${comparisonBars(data.departments)}
      </section>
    </div>

    <div class="two-column">
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Radar</p>
            <h2 class="panel-title">Confronto tecnico</h2>
          </div>
        </div>
        ${radarSVG(data.radar)}
      </section>
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Match insights</p>
            <h2 class="panel-title">Verdetto</h2>
          </div>
        </div>
        <div class="insight-list">
          ${data.insights.map((item) => `<div class="insight ${escapeHTML(item.tone)}"><strong>${escapeHTML(item.label)}:</strong> ${escapeHTML(item.text)}</div>`).join("")}
          <div class="insight ${data.verdict.type === "balanced" ? "neutral" : "home"}"><strong>${escapeHTML(data.verdict.favorite)}:</strong> ${escapeHTML(data.verdict.text)}</div>
        </div>
      </section>
    </div>
  `;
}

async function loadPrediction() {
  const target = $("#prediction-result");
  const team1 = selectedTeam("predict-a");
  const team2 = selectedTeam("predict-b");
  if (team1 === team2) {
    target.innerHTML = `<div class="empty-state">Seleziona due squadre diverse</div>`;
    return;
  }
  target.innerHTML = `<div class="loading">Calcolo predizione</div>`;
  try {
    renderPredictionResult(await api("/api/predict", { team1, team2 }));
  } catch (error) {
    target.innerHTML = `<div class="empty-state">${escapeHTML(error.message)}</div>`;
  }
}

function renderPredictionsView() {
  $("#predictions-view").innerHTML = `
    <div class="control-grid">
      ${selectorPanel("predict-a", "Squadra casa", "Spagna")}
      ${selectorPanel("predict-b", "Squadra ospite", "Francia")}
    </div>
    <div class="panel-actions">
      <button class="primary-button" type="button" id="predict-run">Calcola predizione</button>
    </div>
    <div id="prediction-result" class="simulator-stage"></div>
  `;
  attachTeamSelector("predict-a");
  attachTeamSelector("predict-b");
  $("#predict-run").addEventListener("click", loadPrediction);
  loadPrediction();
}

function renderOfficialGroups() {
  return Object.entries(state.bootstrap.groups).map(([group, teams]) => `
    <article class="group-card">
      <h3 class="group-title">Girone ${group}</h3>
      ${teams.map((team) => {
        const meta = state.teamMap.get(team) || {};
        return `
          <div class="group-team">
            ${flagHTML(meta.flag, team)}
            <span>${escapeHTML(team)}</span>
            <strong>${fmt(meta.OverallRating)}</strong>
          </div>
        `;
      }).join("")}
    </article>
  `).join("");
}

function matchCard(match) {
  const footer = match.penalties
    ? `Rigori · ${match.winner}`
    : (match.draw ? "Pareggio" : `Vince ${match.winner}`);
  return `
    <article class="match-card">
      <div class="match-teams">
        <span>${flagHTML(match.team1Flag, match.team1)}${escapeHTML(match.team1)}</span>
        <strong class="match-score">${match.goals1}-${match.goals2}</strong>
        <span>${flagHTML(match.team2Flag, match.team2)}${escapeHTML(match.team2)}</span>
      </div>
      <div class="match-footer">${escapeHTML(footer)}</div>
    </article>
  `;
}

function renderGroupDetail(group) {
  return `
    <div class="standing-grid">
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Classifica</p>
            <h2 class="panel-title">Girone ${escapeHTML(group.group)}</h2>
          </div>
        </div>
        ${group.standing.map((row) => `
          <div class="standing-row ${row.qualified ? "is-qualified" : ""}">
            <strong>${row.rank}</strong>
            ${flagHTML(row.flag, row.team)}
            <span>${escapeHTML(row.team)}</span>
            <span>${row.points} pt · ${row.goalsFor}:${row.goalsAgainst} · ${row.goalDiff > 0 ? "+" : ""}${row.goalDiff}</span>
          </div>
        `).join("")}
      </section>
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Risultati</p>
            <h2 class="panel-title">Partite girone</h2>
          </div>
        </div>
        <div class="matches-grid">${group.matches.map(matchCard).join("")}</div>
      </section>
    </div>
  `;
}

function chartRows(rows, valueKey, options = {}) {
  const max = Math.max(1, ...rows.map((row) => Number(row[valueKey]) || 0));
  return `
    <div class="chart-bars">
      ${rows.map((row) => {
        const value = Number(row[valueKey]) || 0;
        const width = Math.max(2, value / max * 100);
        const label = row.team || row.Squadra;
        const flag = row.flag;
        const formatted = options.suffix ? `${fmt(value)}${options.suffix}` : fmt(value);
        return `
          <div class="chart-row">
            <div class="chart-label">${flagHTML(flag, label)}<span>${escapeHTML(label)}</span></div>
            <div class="single-bar"><span style="width:${width}%"></span></div>
            <strong>${escapeHTML(formatted)}</strong>
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function renderSimulationResult(data) {
  const target = $("#sim-result");
  const firstGroup = data.groups[0];
  target.innerHTML = `
    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Campione del mondo</p>
          <h2 class="panel-title">${escapeHTML(data.champion.Squadra)}</h2>
        </div>
        ${flagHTML(data.champion.flag, data.champion.Squadra, "flag flag-lg")}
      </div>
      <div class="team-stats">
        ${miniStat("Overall", data.champion.OverallRating)}
        ${miniStat("Attacco", data.champion.AttackRating)}
        ${miniStat("Difesa", data.champion.DefenseRating)}
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Fase a gironi</p>
          <h2 class="panel-title">Risultati simulati</h2>
        </div>
        <div class="field">
          <label for="sim-group">Girone</label>
          <select id="sim-group">${data.groups.map((group) => `<option value="${group.group}">Girone ${group.group}</option>`).join("")}</select>
        </div>
      </div>
      <div id="sim-group-detail">${renderGroupDetail(firstGroup)}</div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Qualificate</p>
          <h2 class="panel-title">${data.qualified.length} squadre alla fase knockout</h2>
        </div>
      </div>
      <div class="qualified-grid">
        ${data.qualified.map((row) => `
          <div class="qualified-item">
            ${flagHTML(row.flag, row.team)}
            <span>${escapeHTML(row.team)}</span>
          </div>
        `).join("")}
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Knockout</p>
          <h2 class="panel-title">Tabellone</h2>
        </div>
      </div>
      <div class="rounds">
        ${data.rounds.map((round) => `
          <div>
            <h3 class="role-title">${escapeHTML(round.name)}</h3>
            <div class="round-scroll"><div class="round-grid">${round.matches.map(matchCard).join("")}</div></div>
          </div>
        `).join("")}
      </div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Monte Carlo</p>
          <h2 class="panel-title">Probabilita vittoria torneo</h2>
        </div>
      </div>
      ${chartRows(data.monteCarlo, "probability", { suffix: "%" })}
    </section>
  `;

  $("#sim-group").addEventListener("change", (event) => {
    const selected = data.groups.find((group) => group.group === event.target.value) || data.groups[0];
    $("#sim-group-detail").innerHTML = renderGroupDetail(selected);
  });
}

async function runSimulation() {
  const button = $("#sim-run");
  const target = $("#sim-result");
  button.disabled = true;
  button.textContent = "Simulazione in corso";
  target.innerHTML = `<div class="loading">Calcolo torneo e Monte Carlo</div>`;
  state.simCount += 1;
  try {
    const seed = 2026 + state.simCount * 17;
    renderSimulationResult(await api("/api/simulate", { seed }));
  } catch (error) {
    target.innerHTML = `<div class="empty-state">${escapeHTML(error.message)}</div>`;
  } finally {
    button.disabled = false;
    button.textContent = "Simula Mondiale 2026";
  }
}

function renderSimulatorView() {
  $("#simulator-view").innerHTML = `
    <section class="panel">
      <div class="panel-head">
        <div>
          <p class="section-kicker">Gironi ufficiali</p>
          <h2 class="panel-title">FIFA World Cup 2026</h2>
        </div>
        <button class="primary-button" type="button" id="sim-run">Simula Mondiale 2026</button>
      </div>
      <div class="groups-grid">${renderOfficialGroups()}</div>
    </section>
    <div id="sim-result" class="simulator-stage"></div>
  `;
  $("#sim-run").addEventListener("click", runSimulation);
}

function rankingRow(row) {
  const bars = [
    ["Attacco", row.AttackRating, "var(--scarlet)"],
    ["Centro", row.MidfieldRating, "var(--aqua)"],
    ["Difesa", row.DefenseRating, "var(--pitch)"],
  ].map(([label, value, color]) => {
    const width = Math.max(0, Math.min(100, ((Number(value) - 50) / 45) * 100));
    return `
      <div class="rating-row">
        <span>${label}</span>
        <div class="single-bar"><span style="width:${width}%;background:${color}"></span></div>
        <strong>${fmt(value)}</strong>
      </div>
    `;
  }).join("");

  return `
    <div class="ranking-row">
      ${flagHTML(row.flag, row.Squadra, "flag flag-lg")}
      <div class="list-main">
        <span class="list-title">#${row.RankingFIFA} · ${escapeHTML(row.Squadra)}</span>
        <span class="list-subtitle">Girone ${escapeHTML(row.Girone)} · ${fmt(row.Punti)} punti FIFA</span>
      </div>
      <div class="rating-bars">${bars}</div>
      <div class="list-value">${fmt(row.OverallRating)}</div>
    </div>
  `;
}

function renderRankingsResult(data) {
  $("#rankings-result").innerHTML = `
    ${data.top3.length ? `
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Top 3 FIFA</p>
            <h2 class="panel-title">Podio ranking</h2>
          </div>
        </div>
        <div class="podium-grid">
          ${data.top3.map((row) => `
            <article class="podium-card">
              ${flagHTML(row.flag, row.Squadra, "flag flag-lg")}
              <strong>#${row.RankingFIFA} · ${escapeHTML(row.Squadra)}</strong>
              <span class="list-subtitle">${fmt(row.Punti)} punti · Girone ${escapeHTML(row.Girone)}</span>
            </article>
          `).join("")}
        </div>
      </section>
    ` : ""}

    <div class="two-column">
      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">${data.count} nazionali</p>
            <h2 class="panel-title">Ranking completo</h2>
          </div>
        </div>
        ${data.items.length ? data.items.map(rankingRow).join("") : `<div class="empty-state">Nessun risultato</div>`}
      </section>

      <section class="panel">
        <div class="panel-head">
          <div>
            <p class="section-kicker">Girone ${escapeHTML(data.chartGroup)}</p>
            <h2 class="panel-title">Punti FIFA</h2>
          </div>
        </div>
        ${chartRows(data.chart, "Punti")}
      </section>
    </div>
  `;
}

async function loadRankings() {
  const search = $("#ranking-search").value.trim();
  const group = $("#ranking-group").value;
  const chartGroup = $("#ranking-chart-group").value;
  $("#rankings-result").innerHTML = `<div class="loading">Caricamento ranking</div>`;
  try {
    renderRankingsResult(await api("/api/rankings", { search, group, chart_group: chartGroup }));
  } catch (error) {
    $("#rankings-result").innerHTML = `<div class="empty-state">${escapeHTML(error.message)}</div>`;
  }
}

function renderRankingsView() {
  $("#rankings-view").innerHTML = `
    <section class="panel">
      <div class="rankings-tools">
        <div class="field">
          <label for="ranking-search">Cerca nazionale</label>
          <input id="ranking-search" type="search" placeholder="Es. Brasile" autocomplete="off">
        </div>
        <div class="field">
          <label for="ranking-group">Filtro girone</label>
          <select id="ranking-group">
            <option value="Tutti">Tutti</option>
            ${Object.keys(state.bootstrap.groups).map((group) => `<option value="${group}">Girone ${group}</option>`).join("")}
          </select>
        </div>
        <div class="field">
          <label for="ranking-chart-group">Grafico</label>
          <select id="ranking-chart-group">
            ${Object.keys(state.bootstrap.groups).map((group) => `<option value="${group}">Girone ${group}</option>`).join("")}
          </select>
        </div>
      </div>
    </section>
    <div id="rankings-result"></div>
  `;

  let timer = null;
  $("#ranking-search").addEventListener("input", () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(loadRankings, 180);
  });
  $("#ranking-group").addEventListener("change", loadRankings);
  $("#ranking-chart-group").addEventListener("change", loadRankings);
  loadRankings();
}

function activateView(view) {
  state.activeView = view;
  $(".view.is-active")?.classList.remove("is-active");
  $(`#${view}-view`).classList.add("is-active");
  $$(".nav-item").forEach((button) => button.classList.toggle("is-active", button.dataset.view === view));
  $("#page-title").textContent = TITLES[view];

  if (!state.rendered.has(view)) {
    const renderers = {
      dashboard: renderDashboard,
      comparison: renderComparisonView,
      predictions: renderPredictionsView,
      simulator: renderSimulatorView,
      rankings: renderRankingsView,
    };
    renderers[view]();
    state.rendered.add(view);
  }
}

async function init() {
  try {
    state.bootstrap = await api("/api/bootstrap");
    state.bootstrap.teams.forEach((team) => state.teamMap.set(team.Squadra, team));
    $("#team-count").textContent = `${state.bootstrap.home.summary.teams} squadre`;
    $("#player-count").textContent = `${state.bootstrap.home.summary.players} giocatori`;
    $("#sidebar-count").textContent = `${state.bootstrap.home.summary.teams} nazionali`;
    $$(".nav-item").forEach((button) => button.addEventListener("click", () => activateView(button.dataset.view)));
    activateView("dashboard");
  } catch (error) {
    showToast(error.message);
    $("#dashboard-view").innerHTML = `<div class="empty-state">${escapeHTML(error.message)}</div>`;
  }
}

document.addEventListener("DOMContentLoaded", init);
